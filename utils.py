def validate_user_input(field, value, user_data):
    if field == "email" and "@" not in value:
        return False, "❌ Invalid email address."
    if field == "mobile" and not value.isdigit():
        return False, "❌ Mobile must be numeric."
    if field == "confirm_password" and value != user_data.get("password"):
        return False, "❌ Passwords do not match."
    if "date" in field.lower() and len(value.split("-")) != 3:
        return False, "❌ Date must be in YYYY-MM-DD format."
    return True, ""