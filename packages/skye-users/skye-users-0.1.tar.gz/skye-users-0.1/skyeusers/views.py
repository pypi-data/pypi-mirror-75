from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.decorators import action

from skyeusers.models import UserAccount, Role
from skyeusers.serializers import UserSerializer, RoleSerializer
from skyeusers.utils import generate_random_password, initiate_roles


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserAccount.objects.all()
    random_password = generate_random_password()

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        user.set_password(self.random_password)
        user.save()

    @action(detail=True, methods=['post'])
    def send_registration_email(self, request, pk=None):
        user = self.get_object()
        subject = 'Skye Account Activation'
        message = f"Hello {user.first_name}, \n" \
                  f"Your Skye account has been created. \n" \
                  f"You can login to your account by visiting skye.com \n" \
                  f"Your default password is: {self.random_password} \n" \
                  f"Regards, \n" \
                  f'Skye Group.'
        from_address = settings.DEFAULT_FROM_EMAIL
        recipients = [user.email]
        send_mail(subject, message, from_address, recipients)

    @action(detail=True, methods=['post'])
    def set_user_role_group(self, request, pk=None):
        user = self.get_object()
        user_group = Group.objects.get(name=Role.objects.get(name=user.data['role']).name)
        user_group.user_set.add(user)


class RoleViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            role = Role(name=serializer.data['name'])
            role.save()
            initiate_roles(serializer=serializer)
