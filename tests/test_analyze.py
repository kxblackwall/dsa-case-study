import pytest
from src.analyze import calculate_statistics, find_at_risk_students

# --- Test 1: Test Statistics Calculation ---
def test_calculate_statistics():
    # 1. Arrange
    sample_data = [
        {'final_grade': 10},
        {'final_grade': 20},
        {'final_grade': 30},
        {'final_grade': None}, # Should be ignored
    ]
    
    # 2. Act
    stats = calculate_statistics(sample_data, 'final_grade')
    
    # 3. Assert
    assert stats['mean'] == 20.0  # (10 + 20 + 30) / 3
    assert stats['median'] == 20.0
    assert stats['min'] == 10.0
    assert stats['max'] == 30.0

def test_calculate_statistics_even():
    # 1. Arrange: Test median with an even number
    sample_data = [
        {'final_grade': 10},
        {'final_grade': 20},
        {'final_grade': 30},
        {'final_grade': 40},
    ]
    
    # 2. Act
    stats = calculate_statistics(sample_data, 'final_grade')
    
    # 3. Assert
    assert stats['median'] == 25.0 # (20 + 30) / 2

def test_calculate_statistics_empty():
    # 1. Arrange: Test with no data
    sample_data = []
    
    # 2. Act
    stats = calculate_statistics(sample_data, 'final_grade')
    
    # 3. Assert
    assert stats['mean'] is None
    assert stats['median'] is None

# --- Test 2: Test At-Risk Student Finder ---
def test_find_at_risk_students():
    # 1. Arrange
    sample_data = [
        # Student 1: Safe
        {'id': 1, 'final_grade': 90, 'attendance_percent': 95},
        # Student 2: At-risk (grade)
        {'id': 2, 'final_grade': 60, 'attendance_percent': 90},
        # Student 3: At-risk (attendance)
        {'id': 3, 'final_grade': 80, 'attendance_percent': 70},
        # Student 4: At-risk (both)
        {'id': 4, 'final_grade': 50, 'attendance_percent': 60},
    ]
    grade_thresh = 65
    att_thresh = 80
    
    # 2. Act
    at_risk, safe = find_at_risk_students(sample_data, grade_thresh, att_thresh)
    
    # 3. Assert
    assert len(at_risk) == 3
    assert len(safe) == 1
    assert at_risk[0]['id'] == 2
    assert at_risk[1]['id'] == 3
    assert at_risk[2]['id'] == 4
    assert safe[0]['id'] == 1
    