import pytest
import os
from src.grade_system.storage import GradeStorage
from src.grade_system.models import Student, Course


def test_save_and_load():
    storage = GradeStorage("test_grades.csv")
    student = Student("Alice", [90, 85])
    storage.save(student)
    entities = storage.load_all()
    assert any(e.name == "Alice" for e in entities)
    os.remove("test_grades.csv")


def test_update_student():
    storage = GradeStorage("test_grades.csv")
    student = Student("Alice", [90, 85])
    storage.save(student)
    storage.update_student("Alice", [95, 90])
    entities = storage.load_all()
    updated_student = next(e for e in entities if e.name == "Alice")
    assert updated_student.grades == [95, 90]
    os.remove("test_grades.csv")


def test_delete_course():
    storage = GradeStorage("test_grades.csv")
    course = Course("Math", {"Alice": 90})
    storage.save(course)
    storage.delete_course("Math")
    entities = storage.load_all()
    assert not any(
        isinstance(e, Course) and e.name == "Math"
        for e in entities
    )
    os.remove("test_grades.csv")


def test_export_summary():
    storage = GradeStorage("test_grades.csv")
    student = Student("Alice", [90, 85])
    storage.save(student)
    storage.export_summary("summary.txt")

    with open("summary.txt", "r") as f:
        content = f.read()

    assert "Student: Alice, Average Grade: 87.67" in content
    os.remove("test_grades.csv")
    os.remove("summary.txt")