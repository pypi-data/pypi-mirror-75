import string
import random

from django.core.management import call_command

from skyeusers.models import UserAccount

ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits
STRING_LENGTH = 8

GROUPS_PERMISSIONS = {}


def generate_random_password(chars=ALPHANUMERIC_CHARS, length=STRING_LENGTH):
    return "".join(random.choice(chars) for _ in range(length))


def initiate_roles(serializer):
    skyeusers_permissions = []
    categories_permissions = []
    recipient_permissions = []

    if serializer.data['view_skyeusers'] is True:
        skyeusers_permissions.append('view')

    if serializer.data['add_skyeusers'] is True:
        skyeusers_permissions.append('add')

    if serializer.data['change_skyeusers'] is True:
        skyeusers_permissions.append('change')

    if serializer.data['delete_skyeusers'] is True:
        skyeusers_permissions.append('delete')

    permissions = {UserAccount: skyeusers_permissions}
    GROUPS_PERMISSIONS[serializer.data['name']] = permissions
    call_command('initgroups')
