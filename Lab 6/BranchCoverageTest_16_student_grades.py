
import pytest
from student_grades import letter_grade, final_marks, exam_eligibility


# Letter grade branches and boundaries
@pytest.mark.parametrize("marks, expected", [
    (0, "z"),
    (39, "F"),
    (40, "E"),
    (49, "E"),
    (50, "D"),
    (59, "D"),
    (60, "C"),
    (69, "C"),
    (70, "B"),
    (79, "B"),
    (80, "A"),
    (89, "A"),
    (90, "S"),
    (100, "S"),
])
def test_grade_branches(marks, expected):
    assert letter_grade(marks) == expected


@pytest.mark.parametrize("marks", [-1, 101])
def test_invalid_grade_branches(marks):
    with pytest.raises(ValueError):
        letter_grade(marks)


# Final marks branches
def test_internal_marks_out_of_range():
    with pytest.raises(ValueError):
        final_marks(41, 30, False)


def test_external_marks_out_of_range():
    with pytest.raises(ValueError):
        final_marks(30, 61, False)


def test_valid_marks_no_project():
    assert final_marks(30, 50, False) == 80


def test_project_added_without_cap():
    assert final_marks(30, 50, True) == 85


def test_project_added_with_cap():
    assert final_marks(40, 60, True) == 100


# Exam eligibility branches
def test_fees_unpaid():
    assert exam_eligibility(90, False, False) == "blocked"


def test_attendance_at_75():
    assert exam_eligibility(75, True, False) == "eligible"


def test_attendance_above_75():
    assert exam_eligibility(80, True, False) == "eligible"


def test_medical_exception_at_65():
    assert exam_eligibility(65, True, True) == "eligible"


def test_medical_exception_with_low_attendance():
    assert exam_eligibility(70, True, True) == "eligible"


def test_medical_condition_false():
    assert exam_eligibility(70, True, False) == "detained"


def test_attendance_below_65():
    assert exam_eligibility(60, True, True) == "detained"
