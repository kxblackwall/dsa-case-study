# PUPQC cademic Analytics 
------- This is made on Linux but instructions are given for both  macOS and windows  on how to run the program----------
Course: Data Structures and Algorithms
Author: DSA group 7

## 1. Project Overview

This project is a modular Python-based data pipeline designed to ingest, clean, transform, and analyze records from a csv file. It demonstrates a analytic tool for instructors to gain knowdlege into course outcome without them needing a full data base.

The entire system is built using standard Python libraries, focusing on array-based operations (using Python lists of dictionaries) and a modular design that separates concerns for ingestion, transformation, analysis, and reporting.

## 2. Features

* Clean Ingest: Reads raw CSV data, validates fields (e.g., score ranges 0-100), cleans whitespace, and handles missing or bad data.
* Data Transformation:
* Calculates a final weighted grade based on configurable weights (quizzes, midterm, final, attendance).
* Applies a "scale-to-max" grade curve, configurable in `config.json`.
* Assigns a final letter grade (A/B/C/D/F) based on customizable cutoffs.
* Analytics: Computes class-wide statistics (mean, median, min, max) and identifies at-risk students based on grade and attendance thresholds.
* Reporting: Generates  csv  reports for all students in each section and a separate CSV for all at-risk students.
* Interactive Menu: Features a command-line interface to run the pipeline, view statistics, or search for a student by ID.
* Unit Tested: Includes `pytest` unit tests to validate the core business logic in the `transform` and `analyze` modules.

## 3. How to Run  (Linux/macOS)

### Prerequisites
* Python 3.10+
* `pip` and `venv`
* Git

### Setup and Installation (Linux/macOS)

1.  **Clone Repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[YourUsername]/[Your-Repo-Name].git
    ```
2.  **Navigate to Project:**
    ```bash
    cd python_projects
    ```
3.  **Create Virtual Environment:**
    ```bash
    python3 -m venv .venv
    ```
4.  **Activate Environment:**
    ```bash
    source .venv/bin/activate
    ```
5.  **Install Dependencies:**
    ```bash
    # Install pytest for testing
    pip install pytest
    ```

### Running the Program (Linux/macOS)

To launch the interactive menu, run the `main` module from the root folder:

```bash
python3 -m src.main

-------------------------------------------- SETUP FOR WINDOWS ----------------------------------------------


Clone  Repository: 

# PowerShell 
git clone [https://github.com/](https://github.com/)[YourUsername]/[Your-Repo-Name].git

# Navigate  to  project (in CMD  or Powershell)
cd python_projects

# 3. Create a Virtual environment
# 'python' is typically used instead of 'python3' on Windows
python -m venv .venv

# 4. Activate  Environment (in powershell):
 .\.venv\Scripts\Activate.ps1
 (If using old Command Prompt, the command is .\.venv\Scripts\activate.bat)

# 5. Install dependencies
 pip install pytest

# 6. Run the  program  
pythom -m  src.main


# 7. Running the test 
- To verify all logic is working correctly, run pytest from the root folder (this command is the same on all platforms):
pytest 

------------------------------------------  END --------------------------------------------




# CONFIGURATION
  -  the  whole pipeline is controlled by config.json
  -  paths: Specifies the csv  input and output directories
  -  weights:  Defines the percentage  weight for each grade components
  -  quiz_count: tells the  ingestor how many quiz column to look for.
  -  threshold:  Sets the cut-off  for the  at-risk student report.
  -  grade_cutoffs: Defines the minimum grade for each letter (A, B, C, etc.).
  -  curve_settings:
      - apply_curve: true or false to enable/disable the grade curve.
      - target_max_grade: The score the highest student will be curved to (e.g., 100).
      - curve_cap: The absolute maximum score any student can have after the curve (e.g., 100).





# PROGRAM STRUCTURE

python_projects/
├── config.json             # Main configuration file
├── README.md               # This file
├── .gitignore              # Tells Git what files to ignore
├── data/
│   ├── input.csv           # Sample raw data
│   ├── at_risk_report.csv  # Generated report
│   └── section_..._report.csv # Generated report
├── src/
│   ├── __init__.py
│   ├── ingest.py           # reading and validating data
│   ├── transform.py        # grade/curve calculation
│   ├── analyze.py          # stats and at-risk logic
│   ├── reports.py          # writing new CSV files
│   └── main.py             # Runs the main menu and pipeline
└── tests/
    ├── __init__.py
    ├── test_analyze.py     # analysis logic
    └── test_transform.py   # transform logic


# COMPLEXITY DISCUSSION

  Data structure : 
 The primary data structure for this project is an array of dictionaries (a Python list of dicts). This structure was chosen because it provides a highly intuitive and flexible way to manage student records. Each student is represented as a single dictionary, allowing for easy access to data by name, such as row['final_grade'] or row['student_id']. This is far more readable than managing multiple "parallel arrays" (e.g., one list for names, one for grades) where data could easily become unsynchronized. This structure also made transformations simple, as new computed values (like final_grade or letter_grade) could be added directly to each student's dictionary.

The data structure used for this project is an array  of dictionaries (  python  lists ). we chose this because it provided a flexible way to maange records. Each student is represented by  a single dictionary, allowing for easy access to data by  name, such row (Final grade) or row (student ID) this is very readable than managing multiple arrays where data can beome unsynchronized. This also made the transformations simple.

Algorithm side : the piple is primarily linear. where we let N be the number of student records. 
- Ingest, trasnform and Report: all main pipeline operations. reading the csv  computing grades,  curving,  assigning letters and exporting reports. 
Statistics - The most computing oriented operation we have is the analyze.py that calculates the median  grades. 
Search :  We had a command line menu so that the user can interact and this is one of its part. It performs a linear search  through the array. 




# LEARNING REFLECTION
So our group worked together to provide a simple yet but effective program for the case study assigned to us. 
we had to study coding python for a bit more before diving deep into making this case study even after taking our certifcations
the First challenging part was when we tried to work as one while using different operating system. but eventually we had our work around so that we can collaborate still as a group even if we are far from one another.
this project  was a very big for us and we had many challening parts and the most important thing we learn was to be resourceful and do our best into learning how to build a full projects instead of just writing code. at first we were confused as to why we need many folders and we ran into many issues. then we tried using other python ide like pycharm but after having an easy time we reflect back to the case study file that we had to provide a whole structure of the files so we went back to vscode  and did the best we can to make it work. as we  understood how the editor runs the code and the set up that we had to do.
we also learned how to run unit test and we learned it act as a safety nets even if we took some time on coding it as well. 
Finally, we debugged many errors that taught us a lot and we were able to learn how to traceback codes and  analyze things properly and sometimes we just forgot to put " or brackets.
but overall in general we learned something we can apply to our day to day studies that coding involves testing, debugging and amanaging the project structure so that it can look presentable. its more than just writing code but understanding logic itself.  