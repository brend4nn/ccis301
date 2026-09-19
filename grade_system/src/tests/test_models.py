import pytest
from src.grade_system.models import Student, Course


def test_student_calculate_grade():
    student = Student("Alice", [90, 85, 88])
    assert abs(student.calculate_grade() - 87.67) < 0.01


def test_course_calculate_grade():
    course = Course("Math", {"Alice": 90, "Bob": 85})
    assert abs(course.calculate_grade() - 87.5) < 0.01