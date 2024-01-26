from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class AccountStatuses(TextChoices):
    ACTIVE = "Active", _("Active")
    INACTIVE = "Inactive", _("Inactive")


class AccountTypes(TextChoices):
    USER = "User", _("User")
    ARTISAN = "Artisan", _("Artisan")


class APIMessages:
    SUCCESS = "Operation completed successfully"
    FORM_ERROR = "One or more validation(s) failed"
    ACCOUNT_CREATED = "Account created successfully"
    ACCOUNT_UPDATED = "Account updated successfully"
    ACCOUNT_SETUP_NOT_COMPLETED = "Account setup not completed"
    ACCOUNT_SETUP_COMPLETED = "Account setup completed"
    ACCOUNT_SETUP_COMPLETED_ALREADY = "Account setup completed already"

    FEEDBACK_MESSAGE = "Your message has been received"

    OTP_SENT = "OTP sent successfully"
    OTP_VERIFIED = "OTP verified successfully"

    PASSWORD_CHANGED = "Password changed successfully"
    PASSWORD_RESET = "Password reset successfully"
    PASSWORD_RESET_LOGGED_IN_ERROR = "You cannot reset password while logged in."
    PASSWORD_RESET_CODE_SENT = "Password reset code sent successfully."
    PASSWORD_RESET_CODE_VERIFIED = "Code verified successfully."
    PASSWORD_CREATE_SUCCESS = "Password created successfully."

    LOGIN_SUCCESS = "Login successful"
    LOGIN_FAILURE = "Invalid login credentials"
    ACCOUNT_LOCKED = (
        "Your account has been locked, please reset your password to unlock your account."
    )

    INVITE_SUCCESS = "User invited successfully"

    TOKEN_REFRESH_FAILURE = "Invalid or expired token"

    PROFILE_UPDATED_SUCCESSFULLY = "Profile Updated"

    FORBIDDEN = "Access denied"
    NOT_FOUND = "Page not found."

    CHAT_CREATED = "Chat created"

    THREAD_NOT_FOUND = "Chat not found"
    THREAD_DELETED = "Chat deleted"
    THREAD_PINNED = "Chat pinned"
    THREAD_UNPINNED = "Chat unpinned"
