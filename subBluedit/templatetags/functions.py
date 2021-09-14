from django import template
from subBluedit.models import Abo
register = template.Library()

# Checks the Level of a User in a specific Sub
@register.simple_tag
def isAuth(user, forum):
    if Abo.objects.filter(user=user, forum=forum).exists():
        auth = Abo.objects.get(user=user, forum=forum)
        if auth.type == 'B': # Banned
            return 0
        elif auth.type == 'N': # Normal
            return 1
        elif auth.type == 'S': # Supervisor
            return 2
        elif auth.type == 'A': # Admin
            return 3
        else:
            return 4 # Owner
    else:
        return -1 # Not Following the Sub