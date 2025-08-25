from loguru import logger
from email_validator import validate_email, EmailNotValidError

def send_notification(user_email, message):
    # דמו: שליחת התראה בדוא"ל (אפשר להרחיב ל־SMTP אמיתי)
    try:
        valid = validate_email(user_email)
        logger.info(f"Sending notification to {user_email}: {message}")
        # כאן אפשר להטמיע שליחה אמיתית
        return True
    except EmailNotValidError:
        logger.error(f"Invalid email: {user_email}")
        return False