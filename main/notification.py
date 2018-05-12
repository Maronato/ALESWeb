from custom_auth.facebook_methods import get_graph as app_graph
from django.shortcuts import reverse
from facebook import GraphAPIError


def student_notification(email_list, student, course):
    """Student Notification

    render and send student notifications
    """

    if not student.has_facebook or student.facebookuser is None:
        return

    template = email_list.subject
    href = reverse('render_notification', kwargs={'instance': email_list.id, 'student': student.id, 'course': course.id if course is not None else 0})
    userid = student.facebookuser.social_id
    try:
        app_graph().put_object(parent_object=userid, connection_name="notifications", href=href, template=template)
    except:
        pass


def student_or_teacher_reminder(obj, events, days):
    """Student or Teacher Reminder Notification

    Remind student or teacher about their classes
    """
    if not obj.is_subscribed or not obj.has_facebook:
        return

    if days == 1:
        d = "amanhã"
        dd = ""
        days = ""
    else:
        d = " dias"
        dd = " daqui a"
    if events == 1:
        e = "aula"
    else:
        e = "aulas"

    template = "{}, não esqueça que você tem {} {} do ALES{} {}{}!".format(obj.facebookuser.first_name, events, e, dd, days, d)
    href = reverse('render_redirect')
    userid = obj.facebookuser.social_id

    try:
        app_graph().put_object(parent_object=userid, connection_name="notifications", href=href, template=template)
    except GraphAPIError:
        pass
