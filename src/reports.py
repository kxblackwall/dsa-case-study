import csv
import os
from typing import List, Dict, Any

# Type Aliases for clarity
StudentRow = Dict[str, Any]
StudentData = List[StudentRow]

def export_at_risk_csv(
    at_risk_data: StudentData, 
    output_dir: str
) -> bool:
    """
    Exports the list of at-risk students to a CSV file.
    """
    if not at_risk_data:
        print("Report: No at-risk students to export.")
        return True # Not an error, just nothing to do
        
    # Define file path
    file_path = os.path.join(output_dir, "at_risk_report.csv")
    
    # Define the headers (keys from the first student)
    # We'll select a few key fields to make the report useful
    headers = [
        'student_id', 'last_name', 'first_name', 'section',
        'final_grade', 'letter_grade', 'attendance_percent'
    ]
    
    print(f"Report: Exporting {len(at_risk_data)} at-risk students to {file_path}...")
    
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            # DictWriter maps our dictionaries to CSV rows
            writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
            
            writer.writeheader()
            for row in at_risk_data:
                writer.writerow(row)
        return True
    except IOError as e:
        print(f"Error writing at-risk CSV: {e}")
        return False

def export_section_reports(
    student_data: StudentData, 
    output_dir: str
) -> bool:
    """
    Splits the data by 'section' and exports one CSV for each.
    This is a classic "array operation" (grouping/partitioning).
    """
    
    # 1. Group data by section
    sections: Dict[str, StudentData] = {}
    for row in student_data:
        section = row.get('section', 'UNKNOWN')
        if section not in sections:
            sections[section] = [] # Create a new empty list for this section
        sections[section].append(row)
        
    if not sections:
        print("Report: No student data to export by section.")
        return True

    # 2. Define headers (all keys from the first student)
    if not student_data:
        return True # Nothing to export
    
    headers = list(student_data[0].keys())

    # 3. Write one file per section
    try:
        for section_name, section_data in sections.items():
            file_path = os.path.join(output_dir, f"section_{section_name}_report.csv")
            print(f"Report: Exporting {len(section_data)} students for {section_name} to {file_path}...")
            
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(section_data)
                
        return True
    except IOError as e:
        print(f"Error writing section CSVs: {e}")
        return False
    