import os
import re


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
            current_question = {'question': question_text, 'options': [], 'selected': None}

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


def main():
    # ASCII box-drawing characters for tables
    h_line = "─"
    v_line = "│"
    tl_corner = "┌"
    tr_corner = "┐"
    bl_corner = "└"
    br_corner = "┘"
    t_down = "┬"
    t_up = "┴"
    t_right = "├"
    t_left = "┤"
    cross = "┼"

    quiz_files = find_quiz_files()

    # Summary table for all files
    print("QUIZ VALIDATION SUMMARY")
    print("======================")

    # Generate the header row of the summary table
    header = ["File", "Total Qs", "Answered", "Missing"]
    col_widths = [20, 10, 10, 10]

    # Top border
    print(
        f"{tl_corner}{h_line * col_widths[0]}{t_down}{h_line * col_widths[1]}{t_down}{h_line * col_widths[2]}{t_down}{h_line * col_widths[3]}{tr_corner}")

    # Header row
    print(
        f"{v_line}{header[0].ljust(col_widths[0])}{v_line}{header[1].ljust(col_widths[1])}{v_line}{header[2].ljust(col_widths[2])}{v_line}{header[3].ljust(col_widths[3])}{v_line}")

    # Separator
    print(
        f"{t_right}{h_line * col_widths[0]}{cross}{h_line * col_widths[1]}{cross}{h_line * col_widths[2]}{cross}{h_line * col_widths[3]}{t_left}")

    # Process each file and show details
    for file_path in quiz_files:
        file_name = os.path.basename(file_path)
        questions = extract_answers(file_path)

        total = len(questions)
        answered = sum(1 for q in questions if q['selected'] is not None)
        missing = total - answered

        # Print row for this file in summary table
        print(
            f"{v_line}{file_name.ljust(col_widths[0])}{v_line}{str(total).ljust(col_widths[1])}{v_line}{str(answered).ljust(col_widths[2])}{v_line}{str(missing).ljust(col_widths[3])}{v_line}")

    # Bottom border of summary table
    print(
        f"{bl_corner}{h_line * col_widths[0]}{t_up}{h_line * col_widths[1]}{t_up}{h_line * col_widths[2]}{t_up}{h_line * col_widths[3]}{br_corner}")

    print("\nDETAILED RESULTS")
    print("===============")

    # For each quiz file, show detailed results
    for file_path in quiz_files:
        file_name = os.path.basename(file_path)
        questions = extract_answers(file_path)

        print(f"\n{file_name}")
        print("-" * len(file_name))

        # Table for individual questions
        q_col_width = 5
        status_col_width = 10

        # Top border
        print(f"{tl_corner}{h_line * q_col_width}{t_down}{h_line * status_col_width}{tr_corner}")

        # Header row
        print(f"{v_line}{'Q#'.ljust(q_col_width)}{v_line}{'Status'.ljust(status_col_width)}{v_line}")

        # Separator
        print(f"{t_right}{h_line * q_col_width}{cross}{h_line * status_col_width}{t_left}")

        # Questions
        for i, q in enumerate(questions):
            status = "✓" if q['selected'] else "✗"
            print(f"{v_line}{str(i + 1).ljust(q_col_width)}{v_line}{status.ljust(status_col_width)}{v_line}")

        # Bottom border
        print(f"{bl_corner}{h_line * q_col_width}{t_up}{h_line * status_col_width}{br_corner}")


if __name__ == "__main__":
    main()