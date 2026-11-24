import phonenumbers
from email_validator import validate_email, EmailNotValidError

def normalize_email(raw: str) -> str | None:
    try: return validate_email(raw.strip(),check_deliverability=False).normalized.lower()
    except EmailNotValidError: return None

def normalize_phone(raw: str, region: str) -> str | None:
    try:
        phone=phonenumbers.parse(raw,region)
        if phonenumbers.is_valid_number(phone) and not phone.extension:
            return phonenumbers.format_number(phone,phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException: pass
    return None
