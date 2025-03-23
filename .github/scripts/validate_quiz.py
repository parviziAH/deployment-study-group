import os
import re
import sys


def find_quiz_files():
    quiz_files = []
    theory_dir = 'exercises/theory'
    if os.path.exists(theory_dir):
        for file in os.listdir(theory_dir):
            if file.endswith('.md'):
                quiz_files.append(os.path.join(theory_dir, file))
    return sorted(quiz_files)


def extract_answers(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all questions and their options
    questions = []
    current_question = None
    option_pattern = re.compile(r'\s*-\s+\[([ xX])\]\s+(.*)')

    for line in content.split('\n'):
        # Look for question headers (numbered questions with bold formatting)
        if re.match(r'\d+\.\s+\*\*', line):
            if current_question:
                questions.append(current_question)
            question_text = re.sub(r'\d+\.\s+\*\*|\*\*$', '', line).strip()
            current_question = {'question': question_text, 'options': [], 'selected': None, 'correct': None}

        # Look for options
        option_match = option_pattern.match(line)
        if option_match and current_question is not None:
            is_selected = option_match.group(1).lower() == 'x'
            option_text = option_match.group(2).strip()

            current_question['options'].append(option_text)
            if is_selected:
                current_question['selected'] = option_text

    # Add the last question
    if current_question:
        questions.append(current_question)

    return questions


def get_report(file_path):
    file_name = os.path.basename(file_path)
    questions = extract_answers(file_path)

    # Build the report
    report = f"# Quiz Report: {file_name}\n\n"

    # Summary statistics
    total_questions = len(questions)
    answered_questions = sum(1 for q in questions if q['selected'] is not None)

    report += f"- Total questions: {total_questions}\n"
    report += f"- Questions answered: {answered_questions}\n"
    report += f"- Questions missing answers: {total_questions - answered_questions}\n\n"

    # Detailed breakdown
    report += "## Question Details\n\n"
    for i, q in enumerate(questions):
        status = "✅ Answered" if q['selected'] else "❌ Missing answer"
        report += f"{i + 1}. **{q['question']}** - {status}\n"
        if q['selected']:
            report += f"   - Selected: {q['selected']}\n"
        report += "\n"

    return report


def main():
    print("# Quiz Validation Results\n")

    quiz_files = find_quiz_files()
    if not quiz_files:
        print("No quiz files found in exercises/theory directory")
        return

    print(f"Found {len(quiz_files)} quiz files\n")

    all_reports = []
    for file_path in quiz_files:
        report = get_report(file_path)
        all_reports.append(report)
        print(report)
        print("---\n")

    # Write the combined report to a file for reference
    with open('quiz_validation_report.md', 'w') as f:
        f.write("# Complete Quiz Validation Report\n\n")
        f.write("\n\n".join(all_reports))

    print("Full report written to quiz_validation_report.md")


if __name__ == "__main__":
    main()