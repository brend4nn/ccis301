import typer
from .models import Student, Course
from .storage import GradeStorage


app = typer.Typer()


@app.command()
def add_student(
    name: str,
    grades: str = typer.Argument(
        ...,
        help="Comma-separated grades (e.g., 90,85,88)"
    )
):
    """Add a student with grades."""
    grade_list = [float(g) for g in grades.split(",")]
    student = Student(name, grade_list)
    storage = GradeStorage()
    storage.save(student)
    typer.echo(f"Added student {name} with grades {grade_list}")


@app.command()
def add_course(
    name: str,
    student_grades: str = typer.Argument(
        ...,
        help="Student grades as name:grade pairs (e.g., Alice:90,Bob:85)"
    )
):
    """Add a course with student grades."""
    grades_dict = {
        pair.split(":")[0]: float(pair.split(":")[1])
        for pair in student_grades.split(",")
    }
    course = Course(name, grades_dict)
    storage = GradeStorage()
    storage.save(course)
    typer.echo(f"Added course {name} with student grades {grades_dict}")


@app.command()
def update_student(
    name: str,
    grades: str = typer.Argument(
        ...,
        help="Comma-separated new grades (e.g., 95,90,88)"
    )
):
    """Update grades for an existing student."""
    try:
        grade_list = [float(g) for g in grades.split(",")]
        storage = GradeStorage()
        storage.update_student(name, grade_list)
        typer.echo(f"Updated grades for student {name}: {grade_list}")
    except ValueError as e:
        typer.echo(str(e))
        raise typer.Exit(code=1)


@app.command()
def delete_course(name: str):
    """Delete a course by name."""
    try:
        storage = GradeStorage()
        storage.delete_course(name)
        typer.echo(f"Deleted course {name}")
    except ValueError as e:
        typer.echo(str(e))
        raise typer.Exit(code=1)


@app.command()
def view_all():
    """View all students and courses."""
    storage = GradeStorage()
    entities = storage.load_all()

    for entity in entities:
        avg = entity.calculate_grade()
        typer.echo(
            f"{entity.__class__.__name__}: "
            f"{entity.name}, Average Grade: {avg:.2f}"
        )


@app.command()
def average(entity_type: str, name: str):
    """Calculate average grade for a student or course."""
    storage = GradeStorage()
    entities = storage.load_all()

    for entity in entities:
        if (
            entity.__class__.__name__.lower() == entity_type.lower()
            and entity.name == name
        ):
            avg = entity.calculate_grade()
            typer.echo(
                f"Average grade for {entity_type} {name}: {avg:.2f}"
            )
            return

    typer.echo(f"No {entity_type} named {name} found")


@app.command()
def export_summary(
    output: str = typer.Argument(
        ...,
        help="Output file for summary"
    )
):
    """Export a summary of all students and courses to a file."""
    try:
        storage = GradeStorage()
        storage.export_summary(output)
        typer.echo(f"Summary exported to {output}")
    except Exception as e:
        typer.echo(f"Error exporting summary: {str(e)}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()