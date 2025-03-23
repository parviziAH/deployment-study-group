#!/usr/bin/env python3
"""
Quiz Checker - Evaluates quiz answers in markdown files against answer keys
"""

import os
import re
import json
from pathlib import Path

# Configuration
THEORY_DIR = 'exercises/theory'
ANSWERS_FILE = '.github/quiz_answers.json'
OUTPUT_FILE = 'quiz_results.md'


# Load answer keys
def load_answer_keys():
    with open(ANSWERS_FILE, 'r') as f:
        return json.load(f)


# Extract questions and selected answers from markdown
def parse_quiz_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Extract questions and answers
    questions = []
    current_question = None

    for line in content.split('\n'):
        # New question detection
        question_match = re.match(r'^\d+\.\s+\*\*(.+)\*\*$', line.strip())
        if question_match:
            if current_question:
                questions.append(current_question)
            current_question = {
                'text': question_match.group(1),
                'answers': [],
                'selected': None
            }
            continue

        # Answer detection
        answer_match = re.match(r'^\s*-\s+\[([\sx])\]\s+(.+)$', line.strip())
        if answer_match and current_question:
            is_selected = answer_match.group(1) == 'x'
            answer_text = answer_match.group(2)
            current_question['answers'].append(answer_text)
            if is_selected:
                current_question['selected'] = len(current_question['answers']) - 1

    # Add the last question
    if current_question:
        questions.append(current_question)

    return questions


# Check answers against the answer key
def check_answers(module_name, student_answers, answer_keys):
    if module_name not in answer_keys:
        return {"correct": 0, "wrong": 0, "missing": 0, "total": 0}

    key = answer_keys[module_name]
    results = {"correct": 0, "wrong": 0, "missing": 0, "total": len(key)}

    # Create a mapping of question text to student's selected answer
    student_selections = {}
    for q in student_answers:
        student_selections[q['text']] = q['selected']

    # Check each question in the answer key
    for question_text, correct_answer_index in key.items():
        if question_text not in student_selections:
            results["missing"] += 1
        elif student_selections[question_text] is None:
            results["missing"] += 1
        elif student_selections[question_text] == correct_answer_index:
            results["correct"] += 1
        else:
            results["wrong"] += 1

    return results


# Generate markdown results table
def generate_results_table(all_results):
    markdown = "# Quiz Results\n\n"
    markdown += "| Module | Correct | Wrong | Missing | Total |\n"
    markdown += "|--------|---------|-------|---------|-------|\n"

    for module, results in all_results.items():
        markdown += f"| {module} | {results['correct']} | {results['wrong']} | {results['missing']} | {results['total']} |\n"

    return markdown


# Main function
def main():
    # Load answer keys
    try:
        answer_keys = load_answer_keys()
    except Exception as e:
        print(f"Error loading answer keys: {e}")
        # Create empty answer keys for testing
        answer_keys = {}

    all_results = {}

    # Process each module file
    theory_dir = Path(THEORY_DIR)
    for module_file in theory_dir.glob("module*.md"):
        module_name = module_file.stem

        try:
            student_answers = parse_quiz_file(module_file)
            results = check_answers(module_name, student_answers, answer_keys)
            all_results[module_name] = results

            print(
                f"Processed {module_name}: {results['correct']} correct, {results['wrong']} wrong, {results['missing']} missing")
        except Exception as e:
            print(f"Error processing {module_name}: {e}")
            all_results[module_name] = {"correct": 0, "wrong": 0, "missing": len(answer_keys.get(module_name, {})),
                                        "total": len(answer_keys.get(module_name, {}))}

    # Generate and save results table
    results_table = generate_results_table(all_results)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(results_table)

    print(f"Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()