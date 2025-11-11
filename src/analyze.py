from typing import List, Dict, Any, Tuple

# Type Aliases for clarity
StudentRow = Dict[str, Any]
StudentData = List[StudentRow]

def calculate_statistics(student_data: StudentData, field: str) -> Dict[str, float | None]:
    """
    Calculates mean, median, min, and max for a given numeric field,
    ignoring 'None' values.
    """
    # 1. Project: Create a new array (list) of only the values we need
    # This is a core array operation.
    values = [row[field] for row in student_data if row.get(field) is not None]
    
    if not values:
        return {'mean': None, 'median': None, 'min': None, 'max': None}

    # 2. Sort: An essential array operation for median, min, and max
    values.sort()

    # 3. Calculate Mean
    mean = sum(values) / len(values)
    
    # 4. Calculate Median
    median = 0.0
    n = len(values)
    if n % 2 == 1:
        # Odd number of elements
        median = values[n // 2]
    else:
        # Even number of elements
        mid1 = values[n // 2 - 1]
        mid2 = values[n // 2]
        median = (mid1 + mid2) / 2
        
    # 5. Min and Max
    min_val = values[0]
    max_val = values[-1]

    return {
        'mean': round(mean, 2),
        'median': round(median, 2),
        'min': round(min_val, 2),
        'max': round(max_val, 2)
    }

def find_percentile(student_data: StudentData, field: str, percentile: int) -> float | None:
    """
    Finds the value at a given percentile (e.g., 90th percentile).
    Uses the "Nearest Rank" method.
    """
    values = [row[field] for row in student_data if row.get(field) is not None]
    if not values:
        return None

    values.sort()
    
    # Calculate index
    n = len(values)
    # We use (n - 1) for 0-based indexing
    index = (percentile / 100) * (n - 1)
    
    # Simple nearest rank: round to nearest whole number
    rank = int(round(index))
    
    return values[rank]

def find_at_risk_students(
    student_data: StudentData,
    grade_threshold: float,
    attendance_threshold: float
) -> Tuple[StudentData, StudentData]:
    """
    Selects students who are 'at-risk'.
    An 'at-risk' student is defined as EITHER:
    1. final_grade < grade_threshold
    2. attendance_percent < attendance_threshold
    
    Returns two lists: at_risk_students and the remaining (safe) students.
    """
    at_risk_list: StudentData = []
    safe_list: StudentData = []

    # This is a 'select' or 'filter' array operation
    for row in student_data:
        is_at_risk = False
        
        # Check grade
        if row.get('final_grade') is not None and row['final_grade'] < grade_threshold:
            is_at_risk = True
        
        # Check attendance
        if row.get('attendance_percent') is not None and row['attendance_percent'] < attendance_threshold:
            is_at_risk = True
            
        if is_at_risk:
            at_risk_list.append(row)
        else:
            safe_list.append(row)
            
    return at_risk_list, safe_list
