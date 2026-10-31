
import pytest
from student_grades import letter_grade, final_marks, exam_eligibility


# Letter grade tests
def test_grade_s():
    assert letter_grade(95) == "S"

def test_grade_a():
    assert letter_grade(85) == "A"

def test_grade_b():
    assert letter_grade(75) == "B"

def test_grade_c():
    assert letter_grade(65) == "C"

def test_grade_d():
    assert letter_grade(55) == "D"

def test_grade_e():
    assert letter_grade(45) == "E"

def test_grade_f():
    assert letter_grade(30) == "F"

def test_invalid_marks():
    with pytest.raises(ValueError):
        letter_grade(-1)

    with pytest.raises(ValueError):
        letter_grade(101)


# Final marks tests
def test_final_marks_without_project():
    assert final_marks(30, 50, False) == 80

def test_final_marks_with_project():
    assert final_marks(30, 50, True) == 85

def test_final_marks_cap_at_100():
    assert final_marks(40, 60, True) == 100

def test_invalid_internal_marks():
    with pytest.raises(ValueError):
        final_marks(41, 50, False)

def test_invalid_external_marks():
    with pytest.raises(ValueError):
        final_marks(30, 61, False)


# Exam eligibility tests
def test_fees_not_paid():
    assert exam_eligibility(90, False, False) == "blocked"

def test_attendance_eligible():
    assert exam_eligibility(75, True, False) == "eligible"

def test_medical_eligibility():
    assert exam_eligibility(65, True, True) == "eligible"

def test_detained():
    assert exam_eligibility(60, True, False) == "detained"
    
def test_letter_grade_zero_marks():
    assert letter_grade(0) == "F"
