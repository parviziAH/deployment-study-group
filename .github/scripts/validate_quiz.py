#!/usr/bin/env python3
"""
Quiz validator script for GitHub Actions.
Checks if the student has marked the correct answers in the quiz markdown file.
"""

import os
import re
import requests
import glob
from pathlib import Path

# Define the correct answers for Module 1 quiz
CORRECT_ANSWERS = {
    "1": "Containerized deployments package the application with its dependencies, ensuring consistency across environments",
    "2": "Elimination of the need for operating systems",
    "3": "Containers use the host operating system's kernel rather than virtualizing an entire OS",
    "4": "It ensures the inventory algorithm will run consistently regardless of the deployment environment",
    "5": "docker ps",
    "6": "Mounts the current directory to /app in the container and runs algorithm.py",
    "7": "Read-only filesystem components that make up a Docker image",
    "8": "Efficient layer management can reduce image size and improve build performance"
}


def find_quiz_files():
    """Find all potential quiz files in the repository."""
    # Look for any markdown files that might contain the Module 1 quiz
    quiz_files = glob.glob("**/*[mM]odule*1*.md", recursive=True)
    quiz_files += glob.glob("**/*quiz*.md", recursive=True)

    if not quiz_files:
        # If no specific files are found, check all markdown files
        quiz_files = glob.glob("**/*.md", recursive=True)

    print(f"Potential quiz files found: {quiz_files}")
    return quiz_files


def is_quiz_file(file_path):
    """Check if the file contains the Module 1 quiz content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if the content looks like our quiz
        if "Module 1" in content and "Containerization & Docker Fundamentals" in content:
            return True

        # Count how many checkbox markdown elements are in the file
        checkbox_count = len(re.findall(r'- \[[ xX]\]', content))
        if checkbox_count > 10:  # If there are several checkboxes, it's likely a quiz
            return True

        return False
    except Exception as e:
        print(f"Error checking file {file_path}: {str(e)}")
        return False


def parse_quiz_file(file_path):
    """Parse the quiz markdown file and extract student answers."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"Processing file: {file_path}")
        print(f"File content preview: {content[:200]}...")

        # Extract questions and answers using regex
        student_answers = {}

        # Pattern to match question numbers and options with checkboxes
        # This pattern is more flexible to handle different markdown formatting
        pattern = r'(\d+)\.[\s\*]*.*?[\*\s]*((?:[\s\S]*?- \[[xX ]\].*?(?:\n|$))+)'
        questions = re.finditer(pattern, content)

        for match in questions:
            question_num = match.group(1)
            options_text = match.group(2)

            print(f"Found question {question_num}")
            print(f"Options text: {options_text[:100]}...")

            # Find which option is checked
            option_pattern = r'- \[([xX])\](.*?)(?:\n|$)'
            options = re.finditer(option_pattern, options_text)

            for option in options:
                if option.group(1).lower() == 'x':
                    student_answer = option.group(2).strip()
                    student_answers[question_num] = student_answer
                    print(f"Found selected answer for question {question_num}: {student_answer[:50]}...")

        print(f"Total answers found: {len(student_answers)}")
        return student_answers
    except Exception as e:
        print(f"Error parsing file {file_path}: {str(e)}")
        return {}


def validate_answers(student_answers):
    """Validate student answers against correct answers."""
    results = {
        'correct': [],
        'incorrect': [],
        'missing': []
    }

    for question_num, correct_answer in CORRECT_ANSWERS.items():
        if question_num in student_answers:
            # Normalize the answers for comparison
            student_ans_norm = ' '.join(student_answers[question_num].split())
            correct_ans_norm = ' '.join(correct_answer.split())

            # Compare normalized answers
            if student_ans_norm.lower() == correct_ans_norm.lower():
                results['correct'].append(question_num)
            else:
                results['incorrect'].append(question_num)
                print(f"Question {question_num} answer incorrect:")
                print(f"  Student: {student_ans_norm}")
                print(f"  Correct: {correct_ans_norm}")
        else:
            results['missing'].append(question_num)

    return results


def create_pr_comment(results, repo_owner, repo_name, pr_number, github_token):
    """Create a comment to post on the PR with validation results."""
    if not github_token or not pr_number:
        print("Missing GitHub token or PR number, skipping comment creation")
        return

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    score = len(results['correct'])
    total = len(CORRECT_ANSWERS)

    comment = f"## Quiz Validation Results\n\n"
    comment += f"### Score: {score}/{total}\n\n"

    if results['correct']:
        comment += "✅ **Correct Answers**\n"
        for question in results['correct']:
            comment += f"- Question {question}\n"
        comment += "\n"

    if results['incorrect']:
        comment += "❌ **Incorrect Answers**\n"
        for question in results['incorrect']:
            comment += f"- Question {question}\n"
        comment += "\n"

    if results['missing']:
        comment += "⚠️ **Missing Answers**\n"
        for question in results['missing']:
            comment += f"- Question {question}\n"
        comment += "\n"

    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments'
    data = {'body': comment}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Comment posted successfully to PR #{pr_number}")
    except Exception as e:
        print(f"Error posting comment: {str(e)}")


def main():
    # Print environment variables for debugging (excluding secrets)
    print("Environment variables:")
    for key, value in os.environ.items():
        if not key.lower().contains("token") and not key.lower().contains("secret"):
            print(f"  {key}: {value}")

    # Repository info
    github_repository = os.environ.get('GITHUB_REPOSITORY', '')
    repo_parts = github_repository.split('/')

    if len(repo_parts) >= 2:
        repo_owner, repo_name = repo_parts[0], repo_parts[1]
    else:
        repo_owner, repo_name = '', github_repository

    github_token = os.environ.get('GITHUB_TOKEN')
    pr_number = os.environ.get('PR_NUMBER')

    # Find quiz files
    print("Looking for quiz files...")
    quiz_files = find_quiz_files()

    if not quiz_files:
        print("No potential quiz files found in the repository")
        return

    # Filter for files that actually contain quiz content
    quiz_files = [file for file in quiz_files if is_quiz_file(file)]

    if not quiz_files:
        print("No quiz content found in the potential quiz files")
        return

    print(f"Found {len(quiz_files)} quiz files to process")

    for quiz_file in quiz_files:
        print(f"Processing quiz file: {quiz_file}")
        student_answers = parse_quiz_file(quiz_file)

        if not student_answers:
            print(f"No student answers found in {quiz_file}")
            continue

        results = validate_answers(student_answers)

        # Create PR comment if we have the necessary info
        if github_token and pr_number:
            create_pr_comment(results, repo_owner, repo_name, pr_number, github_token)

        # Print results
        print(f"Quiz validation results:")
        print(f"  Correct: {len(results['correct'])}/{len(CORRECT_ANSWERS)}")
        print(f"  Incorrect: {len(results['incorrect'])}")
        print(f"  Missing: {len(results['missing'])}")

        # Set exit code based on results
        if results['incorrect'] or results['missing']:
            print(
                f"❌ Quiz validation failed: {len(results['incorrect'])} incorrect and {len(results['missing'])} missing answers")
            exit(1)
        else:
            print(f"✅ All answers correct ({len(results['correct'])}/{len(CORRECT_ANSWERS)})")
            exit(0)


if __name__ == "__main__":
    main()