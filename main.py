import csv
from pathlib import Path

DATA_FILE = Path(__file__).with_name("student_scores.csv")
REPORT_FILE = Path(__file__).with_name("report.txt")


def load_students(file_path):
    """Load student records from a CSV file into a list of dictionaries."""
    students = []
    with file_path.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            students.append({
                "name": row["name"],
                "python": int(row["python"]),
                "statistics": int(row["statistics"]),
            })
    return students


def calculate_average(student):
    """Return the average of a student's subject scores."""
    return (student["python"] + student["statistics"]) / 2


def analyze_students(students):
    """Add individual averages and calculate class summary statistics."""
    for student in students:
        student["average"] = calculate_average(student)
        if student["average"] >= 80:
            student["result"] = "Strong"
        else:
            student["result"] = "Keep practicing"

    subject_averages = {
        "Python": sum(student["python"] for student in students) / len(students),
        "Statistics": sum(student["statistics"] for student in students) / len(students),
    }
    class_average = sum(student["average"] for student in students) / len(students)
    top_student = max(students, key=lambda student: student["average"])
    return class_average, subject_averages, top_student


def write_report(students, class_average, subject_averages, top_student, file_path):
    """Write the analysis results to a plain-text report file."""
    lines = [
        "STUDENT SCORE ANALYSIS",
        "=======================",
        f"Students analyzed: {len(students)}",
        f"Class average: {class_average:.1f}",
        f"Top student: {top_student['name']} ({top_student['average']:.1f})",
        "",
        "Subject averages:",
    ]
    for subject, average in subject_averages.items():
        lines.append(f"- {subject}: {average:.1f}")

    lines.extend(["", "Student results:"])
    for student in students:
        lines.append(
            f"- {student['name']}: average {student['average']:.1f} "
            f"({student['result']})"
        )

    report_text = "\n".join(lines)
    file_path.write_text(report_text + "\n", encoding="utf-8")
    return report_text


def main():
    students = load_students(DATA_FILE)
    if not students:
        print("No student data found. Add rows to student_scores.csv and try again.")
        return

    class_average, subject_averages, top_student = analyze_students(students)
    report = write_report(
        students, class_average, subject_averages, top_student, REPORT_FILE
    )
    print(report)
    print(f"\nSaved report to {REPORT_FILE.name}")


if __name__ == "__main__":
    main()
