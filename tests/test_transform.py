# We need to import the functions we want to test from the 'src' folder
from src.transform import compute_weighted_grade, assign_letter_grade

# --- Test 1: Test Letter Grade Assignment ---
# We use 'test_' at the start of the function name
def test_assign_letter_grade():
    # 1. Arrange: Create our sample data
    # We only need the 'final_grade' field for this function
    sample_data = [
        {'final_grade': 95},    # A
        {'final_grade': 82},    # B
        {'final_grade': 70},    # C
        {'final_grade': 69.9},  # D (testing the boundary)
        {'final_grade': 55},    # F
        {'final_grade': 89.9}   # B (testing the boundary)
    ]
    cutoffs = {"A": 90, "B": 80, "C": 70, "D": 60}
    
    # 2. Act: Run the function we are testing
    result_data = assign_letter_grade(sample_data, cutoffs)
    
    # 3. Assert: Check if the result is what we expect
    assert result_data[0]['letter_grade'] == 'A'
    assert result_data[1]['letter_grade'] == 'B'
    assert result_data[2]['letter_grade'] == 'C'
    assert result_data[3]['letter_grade'] == 'D'
    assert result_data[4]['letter_grade'] == 'F'
    assert result_data[5]['letter_grade'] == 'B'


# --- Test 2: Test Weighted Grade Calculation ---
def test_compute_weighted_grade():
    # 1. Arrange: Create sample data and weights
    sample_student = [
        {
            'quiz1': 100, 'quiz2': 100, 'quiz3': 100, 'quiz4': 100, 'quiz5': 100,
            'midterm': 100,
            'final': 100,
            'attendance_percent': 100
        },
        {
            'quiz1': 50, 'quiz2': 50, 'quiz3': None, 'quiz4': None, 'quiz5': None,
            'midterm': 70,
            'final': 80,
            'attendance_percent': 100
        }
    ]
    
    # Using the weights from config.json
    weights = {
        "quizzes": 0.30,
        "midterm": 0.30,
        "final": 0.30,
        "attendance": 0.10
    }
    quiz_count = 5
    
    # 2. Act: Run the function
    result_data = compute_weighted_grade(sample_student, weights, quiz_count)
    
    # 3. Assert: Check the calculation
    # Student 1: All 100s -> 100.0
    assert result_data[0]['final_grade'] == 100.0
    
    # Student 2:
    # Quiz Avg: (50 + 50 + 0 + 0 + 0) / 5 = 20
    # Grade: (20 * 0.3) + (70 * 0.3) + (80 * 0.3) + (100 * 0.1)
    # Grade: 6 + 21 + 24 + 10 = 61.0
    assert result_data[1]['final_grade'] == 61.0

    