import csv
from typing import List, Dict, Any, Tuple

StudentRow = Dict[str, Any]
CleanData = List[StudentRow]
BadData = List[Tuple[int, str, List[str]]] 

def validate_and_clean_row(
    row_num: int, 
    row: Dict[str, str], 
    quiz_count: int
) -> Tuple[StudentRow | None, str | None]:
    try:
        clean_row = {}
        clean_row['student_id'] = int(row['student_id'].strip())
        clean_row['last_name'] = row['last_name'].strip()
        clean_row['first_name'] = row['first_name'].strip()
        clean_row['section'] = row['section'].strip()

        numeric_fields = []
        for i in range(1, quiz_count + 1):
            numeric_fields.append(f'quiz{i}')
        numeric_fields.extend(['midterm', 'final', 'attendance_percent'])

        for field in numeric_fields:
            value = row.get(field, '').strip() 

            if not value:
                clean_row[field] = None
                continue

            score = float(value)

            if not (0 <= score <= 100):
                raise ValueError(f"Score {score} out of range (0-100)")

            clean_row[field] = score

        return clean_row, None 

    except Exception as e:
        return None, str(e)

def read_and_validate_csv(
    csv_path: str, 
    quiz_count: int
) -> Tuple[CleanData, BadData]:
    clean_records: CleanData = []
    bad_rows: BadData = []

    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for i, row in enumerate(reader):
                row_num = i + 2 
                raw_row_list = list(row.values())
                clean_row, error = validate_and_clean_row(row_num, row, quiz_count)

                if error:
                    bad_rows.append((row_num, error, raw_row_list))
                else:
                    clean_records.append(clean_row)

    except FileNotFoundError:
        print(f"Error: Input file not found at {csv_path}")
        return [], [] 
    except Exception as e:
        print(f"Error: General error reading CSV: {e}")
        return [], []

    return clean_records, bad_rows
