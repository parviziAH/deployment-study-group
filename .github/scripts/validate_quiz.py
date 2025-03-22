#!/usr/bin/env python3
"""
Quiz validator script for GitHub Actions.
Checks if the student has marked the correct answers in the quiz markdown file.
"""

import os
import re
import requests
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

def get_pr_files():
    """Get the files changed in the PR."""
    github_token = os.environ.get('GITHUB_TOKEN')
    pr_number = os.environ.get('PR_NUMBER')
    repo = os.environ.get('GITHUB_REPOSITORY')
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f'https://api.github.com/repos/{repo}/pulls/{pr_number}/files'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return [file['filename'] for file in response.json()]

def parse_quiz_file(file_path):
    """Parse the quiz markdown file and extract student answers."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract questions and answers using regex
    student_answers = {}
    
    # Pattern to match question numbers and options with checkboxes
    pattern = r'(\d+)\.\s+\*\*.*?\*\*\s+((?:[\s\S]*?- \[[xX ]\].*?\n)+)'
    questions = re.finditer(pattern, content)
    
    for match in questions:
        question_num = match.group(1)
        options_text = match.group(2)
        
        # Find which option is checked
        option_pattern = r'- \[([xX])\](.*?)$'
        options = re.finditer(option_pattern, options_text, re.MULTILINE)
        
        for option in options:
            if option.group(1).lower() == 'x':
                student_answers[question_num] = option.group(2).strip()
    
    return student_answers

def validate_answers(student_answers):
    """Validate student answers against correct answers."""
    results = {
        'correct': [],
        'incorrect': [],
        'missing': []
    }
    
    for question_num, correct_answer in CORRECT_ANSWERS.items():
        if question_num in student_answers:
            if student_answers[question_num] == correct_answer:
                results['correct'].append(question_num)
            else:
                results['incorrect'].append(question_num)
        else:
            results['missing'].append(question_num)
    
    return results

def create_pr_comment(results):
    """Create a comment to post on the PR with validation results."""
    github_token = os.environ.get('GITHUB_TOKEN')
    pr_number = os.environ.get('PR_NUMBER')
    repo = os.environ.get('GITHUB_REPOSITORY')
    
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
    
    url = f'https://api.github.com/repos/{repo}/issues/{pr_number}/comments'
    data = {'body': comment}
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

def main():
    # Get files changed in the PR
    pr_files = get_pr_files()
    
    # Look for quiz markdown files
    quiz_files = [file for file in pr_files if 'Module 1' in file and file.endswith('.md')]
    
    if not quiz_files:
        print("No quiz files found in the PR")
        return
    
    for quiz_file in quiz_files:
        student_answers = parse_quiz_file(quiz_file)
        results = validate_answers(student_answers)
        create_pr_comment(results)
        
        # Set exit code based on results
        if results['incorrect'] or results['missing']:
            print(f"❌ Quiz validation failed: {len(results['incorrect'])} incorrect and {len(results['missing'])} missing answers")
            exit(1)
        else:
            print(f"✅ All answers correct ({len(results['correct'])}/{len(CORRECT_ANSWERS)})")
            exit(0)

if __name__ == "__main__":
    main()
