import json
import os
from . import ingest
from . import transform
from . import analyze
from . import reports
from typing import List, Dict, Any

StudentData = List[Dict[str, Any]]

def load_config(config_path: str) -> Dict[str, Any]:
    """Loads the JSON configuration file."""
    print(f"Loading configuration from: {config_path}")
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def run_full_pipeline(config: Dict[str, Any]) -> StudentData:
    """
    Runs the complete ETL (Extract, Transform, Load) pipeline.
    This is the main function we've already built.
    """
    # 1. this is the start of the ingestion, reading and validating of data inside the (input.csv)
    print("--- 1. Ingestion ---")
    student_records, bad_rows = ingest.read_and_validate_csv(
        config["paths"]["input_csv"],
        config["quiz_count"]
    )
    
    print(f"\n ingested: {len(student_records)} records")
    print(f"Skipped: {len(bad_rows)}")
    if bad_rows:
        print(f"Bad row log (first 5): {bad_rows[:5]}")

    # If no records, return an empty list
    if not student_records:
        print("\nNo student record found. aborting pipeline.")
        return []

    # 2. transformation of the data provided
    print("\n--- 2. Transformation ---")
    student_records = transform.compute_weighted_grade(
        student_records,
        config["weights"],
        config["quiz_count"]
    )
    print("Weighted grades computed.")
    # grade curve
    if config.get("curve_settings", {}).get("apply_curve", False):
        student_records = transform.apply_grade_curve(
            student_records,
            config["curve_settings"]
        )
    else:
        print("Grade curve is disabled in config.")

    
    student_records = transform.assign_letter_grade(
        student_records,
        config["grade_cutoffs"]
    )
    print("Letter grades assigned.")

    # 3. calculation/analyzation of the data
    print("\n--- 3. Analysis ---")
    grade_stats = analyze.calculate_statistics(student_records, 'final_grade')
    print("\n final class grades (Final Grade):")
    
    at_risk_list, _ = analyze.find_at_risk_students(
        student_records,
        config["thresholds"]["at_risk_grade"],
        config["thresholds"]["at_risk_attendance"]
    )
    print(f"\nStudents at risk: {len(at_risk_list)}")

    # 4. reporting of data
    print("\n--- 4. Reporting ---")
    output_dir = config["paths"]["output_dir"]
    os.makedirs(output_dir, exist_ok=True)
    reports.export_at_risk_csv(at_risk_list, output_dir)
    reports.export_section_reports(student_records, output_dir)
    
    print("\n--- Pipeline Complete ---")
    
    # it returns processed data so that the menu will be able to hold it.
    return student_records
#  command  line menu 
def show_menu():
    """Prints the main menu options to the console."""
    print("\n" + "="*30)
    print("  PUPQC Academic Analytics  Menu")
    print("="*30)
    print("[1] Run Full Pipeline (Load, Transform, Report)")
    print("[2] Show Class Statistics")
    print("[3] Find Student by ID")
    print("[Q] Quit")
    print("="*30)

def find_student_by_id(student_data: StudentData):
    """
    Asks the user for an ID and prints that student's record.
    """
    if not student_data:
        print("Error: no data processed. run the pipeline [1] first.")
        return

    try:
        search_id = int(input("Enter student_id to find: "))
        
        # This is a 'select' or 'search' array operation
        for student in student_data:
            if student['student_id'] == search_id:
                print("\n--- Student Found ---")
                print(f"  Name:    {student['first_name']} {student['last_name']}")
                print(f"  Section: {student['section']}")
                print(f"  Grade:   {student['final_grade']} ({student['letter_grade']})")
                print(f"  Att.:    {student['attendance_percent']}%")
                return
                
        print(f"Error: Student with id {search_id} not found.")

    except ValueError:
        print("Error: Please enter a valid number for the ID.")

def show_statistics(student_data: StudentData):
    """
    A new function to just print stats on demand.
    """
    if not student_data:
        print("Error: No data loaded. Run the pipeline [1] first.")
        return
        
    print("\n--- Class Statistics (Final Grade) ---")
    grade_stats = analyze.calculate_statistics(student_data, 'final_grade')
    print(f"  Mean:   {grade_stats.get('mean')}")
    print(f"  Median: {grade_stats.get('median')}")
    print(f"  Min:    {grade_stats.get('min')}")
    print(f"  Max:    {grade_stats.get('max')}")

# --- This is our new main function ---
def main(config_path: str = "config.json"):
    """
    Runs the interactive command-line menu.
    """
    config = load_config(config_path)
    
    # This variable will 'hold' our data after the pipeline runs
    all_student_data: StudentData = [] 
    
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip().upper()
        
        if choice == '1':
            print("\nRunning full pipeline...")
            #runs the pipleine and store the results of our variables
            all_student_data = run_full_pipeline(config)
            
        elif choice == '2':
            show_statistics(all_student_data)
            
        elif choice == '3':
            find_student_by_id(all_student_data)

        elif choice == 'Q':
            print("Exiting...")
            break # ends the while loop
            
        else:
            print(f"Error: '{choice}' is not a valid option.")


if __name__ == "__main__":
    
    main()
    