from django import template

register = template.Library()

@register.filter
def is_doctor(user):
    try:
        return hasattr(user, 'doctor') and user.doctor is not None
    except Exception:
        return False
