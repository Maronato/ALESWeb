from schools.models import Student
from teachers.models import Teacher


def get_obj_from_key(key):
    if key is None:
        return key
    obj1 = Student.objects.filter(facebook_create_url=key).first()
    obj2 = Teacher.objects.filter(facebook_create_url=key).first()

    return obj1 or obj2 or None


def get_user_from_key(key):
    obj = get_obj_from_key(key)
    return obj.user if obj is not None else obj


def remove_key_from_user(key):
    obj = get_obj_from_key(key)

    if obj is not None:
        obj.facebook_create_url = "KEY USED"
        obj.save()
    return obj
