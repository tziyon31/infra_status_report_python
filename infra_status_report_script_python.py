#!/usr/bin/env python3
import subprocess, argparse, requests, webbrowser, os

# פונקציה שבודקת אם אפשר להגיע לכתובת IP באמצעות פקודת ping
# מחזירה True אם הצליח להגיע, False אם לא
def ping_host(address):
    result = subprocess.run(
        ["ping","-c","1", address],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

# פונקציה שבודקת אם אפשר לגשת לשרת HTTP
# מחזירה True אם קיבלנו תשובה תקינה (קוד 200-299), False אם לא
def check_http(address):
    try:
        res = requests.get("http://",address, timeout=5)
        return 199 < res.status_code < 300
    except requests.RequestException:
        return False 

# פונקציה שיוצרת את תחילת דוח ה-HTML עם הכותרת והטבלה
# יוצרת קובץ HTML חדש עם מבנה בסיסי של טבלה
def generate_report():
    with open("report.html", "w") as f:
        f.write("<html><head><title>Status Report</title></head><body>")
        f.write("<h1>Service Status Report</h1>")
        f.write("<table border='1' cellpadding='5'><tr><th>Address</th><th>Check Type</th><th>Status</th></tr>") 

# פונקציה שסוגרת את תגיות ה-HTML בסוף הדוח
# מוסיפה את תגיות הסגירה הנדרשות לקובץ ה-HTML
def finalize_report():
    with open("report.html", "a") as f:
        f.write("</table></body></html>")

# פונקציה שבודקת אם יש ממשק גרפי זמין במערכת
# מחזירה True אם יש, False אם לא
def has_gui():
    return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))

def main(): 
    outputs = []
    # הגדרת הפרמטרים שהסקריפט מקבל מהמשתמש
    #  אפשר להשתמש ב-t או --target כדי להגדיר כתובות לבדיקה
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', action='append', help="format: type:address (e.g., http:https://google.com or ping:8.8.8.8)")
    args = parser.parse_args()
    # בדיקה שיש לפחות כתובת אחת לבדיקה
    # אם אין כתובות, מציג הודעת שגיאה למשתמש
    if not args.target:
        parser.error("No targets specified. Use -t type:address.")
    # יצירת הדוח - מתחיל את קובץ ה-HTML עם הכותרת והטבלה
    generate_report()
    # לולאה שעוברת על כל הכתובות שצריך לבדוק
    # כל כתובת צריכה להיות בפורמט type:address (לדוגמה: ping:8.8.8.8)
    for target in args.target:
                # פיצול הכתובת לסוג הבדיקה ולכתובת עצמה
        check_type, address = target.split(':', 1)
        # בדיקת סוג הבדיקה וביצוע הבדיקה המתאימה
        # אם זה ping - משתמש בפונקציית ping_host
        # אם זה http/https - משתמש בפונקציית check_http
        if check_type == "ping":
            if ping_host(address):
                   status_symbol = "✅"
            else:
                 status_symbol = "❌"
        elif check_type in ("http://" , "https://"):
            if check_http(address):
                status_symbol = "✅"
            else:
                status_symbol = "❌"
        # הוספת התוצאה לרשימת הפלטים ולקובץ הדוח
        # שומר את התוצאה גם בזיכרון וגם בקובץ ה-HTML
        outputs.append([address, check_type, status_symbol])
        with open("report.html", "a") as f:
            f.write(f"<tr><td>{address}</td><td>{check_type}</td><td>{status_symbol}</td></tr>")
    # סיום הדוח והצגתו למשתמש
    # אם יש ממשק גרפי - פותח את הדוח בדפדפן
    # אם אין - מציג את התוצאות בטרמינל
    finalize_report()
    if has_gui():
        webbrowser.open("report.html")
    else:
        for output in outputs:
            print(output[0],output[1], ":", output[2])



if __name__ == "__main__":
    main()
