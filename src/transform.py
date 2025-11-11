from typing import List, Dict, Any

# Type Aliases for clarity
StudentRow = Dict[str, Any]
StudentData = List[StudentRow]

def _calculate_quiz_average(row: StudentRow, quiz_count: int) -> float:
    """
    Calculates the average quiz score, handling missing quizzes (None).
    Missing quizzes are treated as 0.
    """
    quiz_score_total = 0.0
    
    for i in range(1, quiz_count + 1):
        quiz_name = f'quiz{i}'
        score = row.get(quiz_name) # score is either a float or None
        
        if score is not None:
            quiz_score_total += score
            
    if quiz_count == 0:
        return 0.0
        
    # Averages over all quizzes, treating missing as 0
    return quiz_score_total / quiz_count

def compute_weighted_grade(
    student_data: StudentData, 
    weights: Dict[str, float], 
    quiz_count: int
) -> StudentData:
    """
    Computes the final weighted grade for each student and adds it to their row.
    Handles missing data (None) by treating it as 0.
    """
    
    # This is an "array operation" - we are iterating over the list
    for row in student_data:
        # 1. Calculate average quiz score
        avg_quiz = _calculate_quiz_average(row, quiz_count)
        
        # 2. Get other scores, defaulting 'None' to 0.0
        midterm_score = row.get('midterm') or 0.0
        final_score = row.get('final') or 0.0
        attendance_score = row.get('attendance_percent') or 0.0
        
        # 3. Apply weights
        weighted_grade = (
            (avg_quiz * weights['quizzes']) +
            (midterm_score * weights['midterm']) +
            (final_score * weights['final']) +
            (attendance_score * weights['attendance'])
        )
        
        # 4. Add the new 'final_grade' field to the row
        row['final_grade'] = round(weighted_grade, 2)

    return student_data

def apply_grade_curve(
    student_data: StudentData, 
    curve_settings: Dict[str, Any]
) -> StudentData:
    """
    Applies a "scale-to-max" grade curve to all students.
    """
    print("Applying grade curve...")
    
    # 1. Find the max grade
    grades = [
        row['final_grade'] for row in student_data 
        if row.get('final_grade') is not None
    ]
    if not grades:
        print("  No grades found to curve.")
        return student_data

    max_grade = max(grades)
    target_max = curve_settings["target_max_grade"]
    cap = curve_settings["curve_cap"]

    # 2. Calculate curve amount
    curve_amount = target_max - max_grade
    
    if curve_amount <= 0:
        print(f"  No curve applied (max grade is already {max_grade}).")
        return student_data
        
    print(f"  Applying a {curve_amount:.2f} point curve to all students.")

    # 3. Apply the curve
    for row in student_data:
        if row.get('final_grade') is not None:
            new_grade = row['final_grade'] + curve_amount
            # Apply the cap
            capped_grade = min(new_grade, cap)
            row['final_grade'] = round(capped_grade, 2)
            
    return student_data

def assign_letter_grade(
    student_data: StudentData, 
    cutoffs: Dict[str, float]
) -> StudentData:
    """
    Assigns a letter grade to each student based on their final_grade.
    """
    # Sort cutoffs from highest to lowest score
    sorted_cutoffs = sorted(cutoffs.items(), key=lambda item: item[1], reverse=True)
    
    for row in student_data:
        # Default to 'F'
        row['letter_grade'] = 'F'
        
        if 'final_grade' not in row:
            continue
            
        # Check against each cutoff
        for grade, min_score in sorted_cutoffs:
            if row['final_grade'] >= min_score:
                row['letter_grade'] = grade
                break 
                
    # --- THIS WAS THE FIX ---
    # This line is essential for the pipeline to continue
    return student_data
