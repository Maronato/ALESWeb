# Decorators used to allow or deny access to certain views


def is_teacher(user):
    # Checks whether the user is a teacher
    if not user.is_authenticated:
        return False
    return user.is_teacher or user.is_superuser


def is_student(user):
    # Checks whether the user is a student
    if not user.is_authenticated:
        return False
    return user.is_student


def is_admin(user):
    # Checks whether the user is an admin
    if not user.is_authenticated:
        return False
    return user.is_superuser


def is_admin_or_student(user):
    # Checks whether the user is an admin or a studetn
    return is_admin(user) or is_student(user)
