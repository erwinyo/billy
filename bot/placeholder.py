# Built-in imports
import os

# Third-party imports


# Local imports


BILLY_ENDPOINT = os.getenv("BILLY_ENDPOINT")
BILLY_API_ENDPOINT = os.getenv("BILLY_API_ENDPOINT")
BILLY_API_LOGIN_ENDPOINT = os.getenv("BILLY_API_LOGIN_ENDPOINT")
BILLY_PAGE_SIGNUP_ENDPOINT = os.getenv("BILLY_PAGE_SIGNUP_ENDPOINT")


def placeholder_login_email(email: str, telegram_id: str):
    P_LOGIN_EMAIL = f"""
    Welcome to Billy Telegram!
    
    To complete the login process, please click the link below:
    
    Please login to your account using the following link: {BILLY_API_ENDPOINT}{BILLY_API_LOGIN_ENDPOINT}?email={email}&telegram_id={telegram_id}

    If you receive error message "account not found" after logging, you can register first by clicking the link below:
    {BILLY_API_ENDPOINT}{BILLY_PAGE_SIGNUP_ENDPOINT}

    If you receive this email by mistake, please ignore it. If you have any questions, feel free to contact our support team.
    
    """

    return P_LOGIN_EMAIL
