import gspread
from google.oauth2.service_account import Credentials
import uuid
from datetime import datetime

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "service_account.json",
    scopes=scope
)

client = gspread.authorize(creds)
sheet = client.open("SSC_Steno_Skill_Test_Portal_DB")

students_sheet  = sheet.worksheet("StudentMaster")
passages_sheet  = sheet.worksheet("Passages")
attempts_sheet  = sheet.worksheet("Attempts")
mistakes_sheet  = sheet.worksheet("MistakeDetails")


def get_student(student_id):
    data = students_sheet.get_all_records()
    for row in data:
        if str(row.get("StudentID", "")).strip() == str(student_id).strip():
            return row
    return None


def get_passage(code):
    data = passages_sheet.get_all_records()
    for row in data:
        sheet_code   = str(row.get("PassageCode", "")).strip().lower()
        input_code   = str(code).strip().lower()
        active_value = str(row.get("Active", "")).strip().lower()
        if sheet_code == input_code and active_value == "true":
            return {
                "code":       row.get("PassageCode"),
                "name":       row.get("PassageName"),
                "word_count": int(row.get("TotalWords", 0)),
                "text":       row.get("Passage"),
                "category":   row.get("Category",""),
                "speed":      row.get("Speed",""),
            }
    return None



def get_passage_any(code):
    """Get passage by code regardless of Active status (for admin corrections)."""
    data = passages_sheet.get_all_records()
    for row in data:
        if str(row.get("PassageCode","")).strip().lower() == str(code).strip().lower():
            return {
                "code":       row.get("PassageCode"),
                "name":       row.get("PassageName"),
                "word_count": int(row.get("TotalWords", 0) or 0),
                "text":       row.get("Passage")
            }
    return None

def save_attempt(data):
    attempts_sheet.append_row([
        data["AttemptID"],
        data["StudentID"],
        data["PassageCode"],
        data["TimeTaken"],
        data["TypedWords"],
        data["WPM"],
        data["FullMistakes"],
        data["HalfMistakes"],
        data["Omissions"],
        data["ExtraWords"],
        data["Capitalization"],
        data["FullStop"],
        data["TotalErrors"],
        data["ErrorPercent"],
        data["Mode"],
        data["DeviceID"],
        data["Date"],
        data["HighlightedPassage"]
    ])


def build_attempt_record(student_id, passage_code, result, time_taken, typed_words, highlighted):
    return {
        "AttemptID":         str(uuid.uuid4()),
        "StudentID":         student_id,
        "PassageCode":       passage_code,
        "TimeTaken":         time_taken,
        "TypedWords":        typed_words,
        "WPM":               result["wpm"],
        "FullMistakes":      result["full"],
        "HalfMistakes":      result["half"],
        "Omissions":         result["omission"],
        "ExtraWords":        result["extra"],
        "Capitalization":    result["capitalization"],
        "FullStop":          result["fullstop"],
        "TotalErrors":       result["total_errors"],
        "ErrorPercent":      result["error_percent"],
        "Mode":              "Online",
        "DeviceID":          "Web",
        "Date":              datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "HighlightedPassage": highlighted
    }


# ─────────────────────────────────────────────────────────────────────────────
# ADMIN — READ FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def get_all_students():
    return students_sheet.get_all_records()

def get_all_passages():
    return passages_sheet.get_all_records()

def get_all_attempts():
    return attempts_sheet.get_all_records()

def get_attempts_by_student(student_id):
    data = attempts_sheet.get_all_records()
    return [r for r in data if str(r.get("StudentID","")).strip() == str(student_id).strip()]

def get_attempt_by_id(attempt_id):
    data = attempts_sheet.get_all_records()
    for r in data:
        if str(r.get("AttemptID","")).strip() == str(attempt_id).strip():
            return r
    return None

def get_attempt_row_index(attempt_id):
    """Return 1-based row index in Attempts sheet for a given AttemptID."""
    data = attempts_sheet.get_all_values()
    for idx, row in enumerate(data):
        if row and str(row[0]).strip() == str(attempt_id).strip():
            return idx + 1  # gspread is 1-indexed
    return None

def update_attempt_errors(attempt_id, corrected):
    """
    Overwrite error fields for a given attempt.
    Column order in Attempts sheet (1-indexed for gspread):
    1 AttemptID, 2 StudentID, 3 PassageCode, 4 TimeTaken, 5 TypedWords,
    6 WPM, 7 FullMistakes, 8 HalfMistakes, 9 Omissions, 10 ExtraWords,
    11 Capitalization, 12 FullStop, 13 TotalErrors, 14 ErrorPercent,
    15 Mode, 16 DeviceID, 17 Date, 18 HighlightedPassage, 19 AdminNote
    """
    row_idx = get_attempt_row_index(attempt_id)
    if not row_idx:
        return False
    col_map = {
        "FullMistakes": 7, "HalfMistakes": 8, "Omissions": 9,
        "ExtraWords": 10, "Capitalization": 11, "FullStop": 12,
        "TotalErrors": 13, "ErrorPercent": 14,
        "AdminNote": 19,
    }
    for field, value in corrected.items():
        col = col_map.get(field)
        if col:
            attempts_sheet.update_cell(row_idx, col, value)
    return True

def add_student(student_id, name, batch="", email=""):
    students_sheet.append_row([student_id, name, batch, email,
                                datetime.now().strftime("%Y-%m-%d")])

def toggle_passage_active(passage_code, active: bool):
    """
    Sheet column order: A=PassageCode, B=PassageName, C=TotalWords, D=Passage, E=Active
    Active is column 5.
    """
    data = passages_sheet.get_all_values()
    for idx, row in enumerate(data):
        if idx == 0:
            continue  # skip header
        if row and str(row[0]).strip().lower() == str(passage_code).strip().lower():
            # Find the Active column from header
            header = data[0]
            try:
                active_col = header.index("Active") + 1  # 1-indexed
            except ValueError:
                active_col = 5  # fallback: column E
            passages_sheet.update_cell(idx + 1, active_col, "TRUE" if active else "FALSE")
            return True
    return False

def add_passage(code, name, text, total_words, active=True, category="", speed=""):
    """
    Sheet column order: A=PassageCode, B=PassageName, C=TotalWords, D=Passage, E=Active, F=Category, G=Speed
    """
    passages_sheet.append_row([
        code,
        name,
        total_words,
        text,
        "TRUE" if active else "FALSE",
        category,
        speed,
    ])
