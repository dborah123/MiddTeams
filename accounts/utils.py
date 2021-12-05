from datetime import datetime

def change_password(old_password, actual_old_password, new_password, new_password_check):
    """
    Verifies that old password is correct and that the new ones match

    returns:
        - 0 if valid
        - 1 if old password doesn't match
        - 2 if new passwords don't match
    """
    if (old_password != actual_old_password):
        return 1
    elif (new_password != new_password_check):
        return 2
    else:
        return 0
