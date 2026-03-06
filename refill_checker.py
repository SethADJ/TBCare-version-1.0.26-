import pandas as pd
from datetime import datetime, timedelta
import os

# REPLACE THIS WITH YOUR GOOGLE LINK
SHEET_URL = "PASTE_YOUR_COPIED_LINK_HERE"

def generate_id(name, facility, date_str, index):
    initials = "".join([n[0].upper() for n in str(name).split() if n])
    fac_initials = "".join([f[0].upper() for f in str(facility).split() if f])
    year = pd.to_datetime(date_str).year
    serial = str(index + 1).zfill(3)
    return f"{initials}-{fac_initials}-{year}-{serial}"

def get_report():
    try:
        df = pd.read_csv(SHEET_URL)
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        due_today, due_tomorrow = [], []

        for i, row in df.iterrows():
            p_id = generate_id(row['Patient Name'], row['Facility Name'], row['Treatment Start Date'], i)
            start_date = pd.to_datetime(row['Treatment Start Date']).date()
            
            for refill_num in range(1, 6):
                refill_date = start_date + timedelta(days=28 * refill_num)
                entry = f"• ID: {p_id} | Name: {row['Patient Name']} (Refill #{refill_num})"
                
                if refill_date == today:
                    due_today.append(entry)
                elif refill_date == tomorrow:
                    due_tomorrow.append(entry)

        report = "--- 🔔 DUE TODAY (URGENT) ---\n" + ("\n".join(due_today) if due_today else "None")
        report += "\n\n--- 📧 DUE TOMORROW (24H NOTICE) ---\n" + ("\n".join(due_tomorrow) if due_tomorrow else "None")
        return report
    except Exception as e:
        return f"Error: {str(e)}"

output_text = get_report()
with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
    print(f'report<<EOF\n{output_text}\nEOF', file=f)
