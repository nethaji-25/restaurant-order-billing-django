import gspread

from google.oauth2.service_account import Credentials
from datetime import datetime,timedelta,date
import calendar
from .models import ShiftAssignment


def update_google_sheet(employee_name=None):
    # Google credentials setup
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("service_account.json", scopes=scope)
    client = gspread.authorize(creds)

    today = date.today()
    month_name = today.strftime("%b")
    year = today.year

    sheet = client.open("Shift Schedule").worksheet(month_name)

    # Number of days in the current month
    num_days = calendar.monthrange(year, today.month)[1]
    date_headers = [(today.replace(day=d)).strftime("%d-%b") for d in range(1, num_days + 1)]

    # ✅ Step 1: Ensure header exists
    if not sheet.get_all_values():
        header = ["Employee Name"] + date_headers
        sheet.append_row(header)

    # ✅ Step 2: Find or create row for employee
    try:
        cell = sheet.find(employee_name)
        row_index = cell.row
    except gspread.exceptions.CellNotFound:
        sheet.append_row([employee_name] + [""] * num_days)
        cell = sheet.find(employee_name)
        row_index = cell.row

    # ✅ Step 3: Read existing row (to preserve old shifts)
    row_data = sheet.row_values(row_index)

    # If row has fewer columns than header, pad it
    while len(row_data) < len(date_headers) + 1:
        row_data.append("")

    # ✅ Step 4: Get all assignments for this employee
    assignments = ShiftAssignment.objects.filter(employee__name=employee_name)

    for a in assignments:
        shift = a.shift.shift_name
        start_date = a.from_date
        end_date = a.to_date

        current_day = start_date
        while current_day <= end_date:
            if current_day.month == today.month and current_day.year == year:
                day_num = current_day.day  # 1 → 31
                # Column offset +1 because column A is "Employee Name"
                row_data[day_num] = shift
            current_day += timedelta(days=1)

    # ✅ Step 5: Write merged row back to sheet
    sheet.update(f"A{row_index}:AF{row_index}", [row_data[:len(date_headers) + 1]])
