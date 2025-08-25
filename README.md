# Stock Screener – סורק מניות פוטנציאליות

מערכת זו סורקת בזמן אמת מניות ע"פ קריטריונים לבחירת מניות פוטנציאליות.
המערכת מתחברת ל־Yahoo Finance ומציגה ממשק Web פשוט.

## הרצה מהירה

1. התקן Python 3.8+
2. התקן ספריות:
   ```
   pip install -r requirements.txt
   ```
3. הרץ את התוכנה:
   ```
   python stock_screener_app.py
   ```
4. גש ל־[http://localhost:8000](http://localhost:8000)

## קבצים עיקריים

- `stock_screener_app.py` – כל הלוגיקה וה־UI.
- `requirements.txt` – ספריות נדרשות.
- `README.md` – תיעוד.
- `.gitignore` – התעלמות מקבצים זמניים.

## הרחבות אפשריות

- הוספת קריטריונים/אינדיקטורים מתקדמים
- הרשמת משתמשים, שמירת תוצאות
- גרפים מתקדמים
- התממשקות ל־API נוספים (Finnhub, Alpha Vantage ועוד)

---

לשאלות/שיפורים – פתח Issue בריפו.
