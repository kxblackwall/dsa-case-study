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
```

Setup and Running (Windows)
The project runs perfectly on Windows. The setup commands are just slightly different.

Clone Repository:

PowerShell

git clone [https://github.com/](https://github.com/)[YourUsername]/[Your-Repo-Name].git
Navigate to Project (in PowerShell or CMD):

PowerShell

cd python_projects
Create Virtual Environment:

PowerShell

# 'python' is typically used instead of 'python3' on Windows
python -m venv .venv
Activate Environment (in PowerShell):

PowerShell

.\.venv\Scripts\Activate.ps1
(If using old Command Prompt, the command is .\.venv\Scripts\activate.bat)

Install Dependencies:

PowerShell

pip install pytest
Run the Program:

PowerShell

python -m src.main
Running the Tests
To verify all logic is working correctly, run pytest from the root folder (this command is the same on all platforms):

Bash

pytest
4. Configuration (config.json)
The entire pipeline is controlled by config.json.

paths: Specifies the CSV input and output directories.

weights: Defines the percentage weight for each grade component.

quiz_count: Tells the ingestor how many quiz columns to look for.

thresholds: Sets the cutoffs for the at-risk student report.

grade_cutoffs: Defines the minimum grade for each letter (A, B, C, etc.).

curve_settings:

apply_curve: true or false to enable/disable the grade curve.

target_max_grade: The score the highest student will be curved to (e.g., 100).

curve_cap: The absolute maximum score any student can have after the curve (e.g., 100).
```
5. Program Structure
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
│   ├── ingest.py           # Handles reading and validating data
│   ├── transform.py        # Handles grade/curve calculation
│   ├── analyze.py          # Handles stats and at-risk logic
│   ├── reports.py          # Handles writing new CSV files
│   └── main.py             # Runs the main menu and pipeline
└── tests/
    ├── __init__.py
    ├── test_analyze.py     # Unit tests for analysis logic
    └── test_transform.py   # Unit tests for transform logic
   ``` 
6. Complexity Discussion
Data Structure
The primary data structure for this project is an array of dictionaries (a Python list of dicts). This structure was chosen because it provides a highly intuitive and flexible way to manage student records. Each student is represented as a single dictionary, allowing for easy access to data by name, such as row['final_grade'] or row['student_id']. This is far more readable than managing multiple "parallel arrays" (e.g., one list for names, one for grades) where data could easily become unsynchronized. This structure also made transformations simple, as new computed values (like final_grade or letter_grade) could be added directly to each student's dictionary.

Algorithmic Complexity
The pipeline's performance is primarily linear, where N is the number of student records.

Ingest, Transform, and Report: Most main pipeline operations iterate through the list of N students once, resulting in O(N) (Linear) complexity. This includes reading the CSV, computing grades, curving, and exporting reports.

Statistics: The most computationally expensive part is in the analyze.py module. To calculate the median, the list of N grades must be sorted, which has a time complexity of O(N log N).

Search: The "Find Student" feature in the menu performs a linear search, which has a worst-case complexity of O(N).

7. Learning Reflection
Our group worked together to provide a simple yet effective program for the case study assigned to us. Even after taking certifications, we realized we needed to study Python more before diving deep into this case study.

A key challenge was collaborating as a group while using different operating systems. We had to find a workaround to ensure we could all contribute effectively. This was a big project for us, and we learned from its challenges. The most important lesson was to be resourceful and learn how to build a full project instead of just writing isolated code.

At first, we were confused by the multi-folder structure and ran into many import issues. We even tried PyCharm, which was easier, but we returned to VS Code to meet the project's structural requirements. This forced us to truly understand how the editor runs code and how to configure a project properly. We also learned how to write unit tests, which act as a "safety net" for our code, even though it took extra time to write them.

Finally, debugging taught us how to read tracebacks, analyze problems properly, and catch simple syntax errors. Overall, we learned that coding isn't just writing logic; it's about testing, debugging, and managing a project's structure to make it presentable and functional. This is a lesson we can apply to all our studies.