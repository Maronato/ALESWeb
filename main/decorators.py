# Decorators used to allow or deny access to certain views


def is_teacher(user):
    # Checks whether the user is a teacher
    return user.is_teacher


def is_student(user):
    # Checks whether the user is a student
    return user.is_student


def is_admin(user):
    # Checks whether the user is an admin
    return user.is_superuser


def is_admin_or_student(user):
    # Checks whether the user is an admin or a studetn
    return is_admin(user) or is_student(user)
