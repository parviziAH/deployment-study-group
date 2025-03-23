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
        return {"correct": 0, "wrong": 0, "missing": 0, "total": 0, "details": []}

    key = answer_keys[module_name]
    results = {"correct": 0, "wrong": 0, "missing": 0, "total": len(key), "details": []}

    # Create a mapping of question text to student's selected answer
    student_selections = {}
    student_answers_map = {}
    for q in student_answers:
        student_selections[q['text']] = q['selected']
        student_answers_map[q['text']] = q

    # Check each question in the answer key
    for question_text, correct_answer_index in key.items():
        detail = {
            "question": question_text,
            "status": "missing",
            "correct_index": correct_answer_index,
            "selected_index": None,
            "correct_answer": "",
            "selected_answer": ""
        }

        if question_text not in student_selections:
            results["missing"] += 1
        elif student_selections[question_text] is None:
            results["missing"] += 1
        else:
            detail["selected_index"] = student_selections[question_text]
            if student_selections[question_text] == correct_answer_index:
                results["correct"] += 1
                detail["status"] = "correct"
            else:
                results["wrong"] += 1
                detail["status"] = "wrong"

            # Add the actual answer text if available
            if question_text in student_answers_map:
                q_data = student_answers_map[question_text]
                if 0 <= correct_answer_index < len(q_data['answers']):
                    detail["correct_answer"] = q_data['answers'][correct_answer_index]
                if 0 <= student_selections[question_text] < len(q_data['answers']):
                    detail["selected_answer"] = q_data['answers'][student_selections[question_text]]

        results["details"].append(detail)

    return results


# Generate markdown results table
def generate_results_table(all_results):
    markdown = "# Quiz Results\n\n"
    markdown += "## Summary\n\n"
    markdown += "| Module | Correct | Wrong | Missing | Total |\n"
    markdown += "|--------|---------|-------|---------|-------|\n"

    for module, results in all_results.items():
        markdown += f"| {module} | {results['correct']} | {results['wrong']} | {results['missing']} | {results['total']} |\n"

    # Add detailed results for each module
    markdown += "\n## Detailed Results\n\n"

    for module, results in all_results.items():
        if not results['details']:
            continue

        markdown += f"### {module}\n\n"
        markdown += "| Question | Status | Your Answer | Correct Answer |\n"
        markdown += "|----------|--------|------------|---------------|\n"

        for detail in results['details']:
            status = "❌ Wrong" if detail["status"] == "wrong" else "✅ Correct" if detail[
                                                                                      "status"] == "correct" else "❓ Missing"
            selected = detail["selected_answer"] if detail["selected_answer"] else "None selected"
            correct = detail["correct_answer"] if detail["correct_answer"] else "N/A"

            # Truncate long questions
            question = detail["question"]
            if len(question) > 50:
                question = question[:47] + "..."

            markdown += f"| {question} | {status} | {selected} | {correct} |\n"

        markdown += "\n"

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
                                        "total": len(answer_keys.get(module_name, {})), "details": []}

    # Generate and save results table
    results_table = generate_results_table(all_results)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(results_table)

    print(f"Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
