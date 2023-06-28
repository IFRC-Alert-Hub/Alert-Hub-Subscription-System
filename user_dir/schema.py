from datetime import timedelta

from uuid import uuid4

import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required
from graphene_django import DjangoObjectType

from django.contrib.auth import logout
from django.utils import timezone

from .models import CustomUser
from .tasks import send_email


class UserType(DjangoObjectType):
    """ User type object """

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'username',
            'phoneNumber',
            'avatar',
            'country',
            'city',
            'verified',
        ]


class Query(graphene.ObjectType):
    profile = graphene.Field(UserType)

    @login_required
    def resolve_profile(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None


class Register(graphene.Mutation):
    """ Mutation to register a user """

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        if CustomUser.objects.filter(email__iexact=email).exists():
            errors = ['emailAlreadyExists']
            return Register(success=False, errors=errors)

        # create user
        user = CustomUser.objects.create(email=email)
        user.set_password(password)

        # create email verification link
        user.email_verification_token = uuid4()
        user.email_verification_token_expires_at = timezone.now() + timedelta(days=30)

        user.save()

        context = {
            'verification_token': user.email_verification_token,
        }

        send_email.delay(user.id, 'Activate your account.', 'email_verification.html', context)

        return Register(success=True)


class VerifyEmail(graphene.Mutation):
    """ Mutation for verifying an email """

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        token = graphene.String(required=True)

    def mutate(self, info, token):
        try:
            user = CustomUser.objects.get(email_verification_token=token)
        except CustomUser.DoesNotExist:
            errors = ['wrongToken']
            return VerifyEmail(success=False, errors=errors)

        if timezone.now() > user.email_verification_token_expires_at:
            errors = ['Token has expired']
            return VerifyEmail(success=False, errors=errors)

        user.verified = True
        user.save()
        return VerifyEmail(success=True)


class ResendVerifyEmail(graphene.Mutation):
    """ Mutation for resending email verification """

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            errors = ['userDoesNotExists']
            return ResendVerifyEmail(success=False, errors=errors)

        if user.verified:
            errors = ['emailAlreadyVerified']
            return ResendVerifyEmail(success=False, errors=errors)

        # create email verification link
        user.email_verification_token = uuid4()
        user.email_verification_token_expires_at = timezone.now() + timedelta(days=30)

        user.save()

        context = {
            'verification_token': user.email_verification_token,
        }

        send_email.delay(user.id, 'Activate your account.', 'email_verification.html', context)

        return ResendVerifyEmail(success=True)


class ResetEmail(graphene.Mutation):
    """ Mutation to reset an email """

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        email = graphene.String(required=True)

    @login_required
    def mutate(self, info, email):
        try:
            user = CustomUser.objects.get(email=email)
            if user.verified is False:
                errors = ['emailNotVerified']
                return ResetPassword(success=False, errors=errors)
        except CustomUser.DoesNotExist:
            errors = ['emailDoesNotExists']
            return ResetPassword(success=False, errors=errors)

        # create email verification link
        user.email_reset_token = uuid4()
        user.email_reset_token_expires_at = timezone.now() + timedelta(days=1)

        user.save()

        context = {
            'reset_token': user.email_reset_token,
        }

        send_email.delay(user.id, 'Confirmation for resetting email.', 'email_reset.html', context)

        return ResetEmail(success=True)


class ResetEmailConfirm(graphene.Mutation):
    """ Mutation for requesting a password reset email """

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        token = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, token, email):
        # Check if the token is empty
        if not token:
            errors = ['emptyToken']
            return ResetPasswordConfirm(success=False, errors=errors)

        try:
            user = CustomUser.objects.get(email_reset_token=token)
        except CustomUser.DoesNotExist:
            errors = ['wrongToken']
            return ResetEmailConfirm(success=False, errors=errors)

        if CustomUser.objects.filter(email__iexact=email).exists():
            errors = ['emailAlreadyExists']
            return Register(success=False, errors=errors)

        user.email = email
        user.email_reset_token = uuid4()
        user.verified = False

        # create email verification link
        user.email_verification_token = uuid4()
        user.email_verification_token_expires_at = timezone.now() + timedelta(days=30)

        user.email_reset_token = uuid4()

        user.save()

        context = {
            'verification_token': user.email_verification_token,
        }

        send_email.delay(user.id, 'Verify your new email.', 'email_verification.html', context)

        return ResetEmailConfirm(success=True)


class UpdateProfile(graphene.Mutation):
    """ Mutation to update a user's profile information """

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        username = graphene.String(default_value=None)
        country = graphene.String(default_value=None)
        city = graphene.String(default_value=None)
        avatar = graphene.String(default_value=None)

    @login_required
    def mutate(self, info, username, country, city, avatar):
        user = info.context.user

        if CustomUser.objects.filter(username__iexact=username).exclude(
                pk=user.pk).exists() and username:
            errors = ['usernameAlreadyExists']
            return UpdateProfile(success=False, errors=errors)

        user.username = username
        user.country = country
        user.city = city
        user.avatar = avatar
        user.save()
        return UpdateProfile(success=True)


class Logout(graphene.Mutation):
    """ Mutation to log out a user """

    success = graphene.Boolean()

    @login_required
    def mutate(self, info):
        logout(info.context)
        return Logout(success=True)


class ResetPassword(graphene.Mutation):
    """ Mutation for requesting a password reset email """

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        try:
            user = CustomUser.objects.get(email=email)
            if user.verified is False:
                errors = ['emailNotVerified']
                return ResetPassword(success=False, errors=errors)
        except CustomUser.DoesNotExist:
            errors = ['emailDoesNotExists']
            return ResetPassword(success=False, errors=errors)

        # create email verification link
        user.password_reset_token = uuid4()
        user.password_reset_token_expires_at = timezone.now() + timedelta(days=1)

        user.save()

        context = {
            'reset_token': user.password_reset_token,
        }

        send_email.delay(user.id, 'Reset your password.', 'password_reset.html', context)

        return ResetPassword(success=True)


class ResetPasswordConfirm(graphene.Mutation):
    """ Mutation for requesting a password reset email """

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        token = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, token, password):
        # Check if the token is empty
        if not token:
            errors = ['emptyToken']
            return ResetPasswordConfirm(success=False, errors=errors)

        try:
            user = CustomUser.objects.get(password_reset_token=token)
        except CustomUser.DoesNotExist:
            errors = ['wrongToken']
            return ResetPasswordConfirm(success=False, errors=errors)

        user.set_password(password)
        user.password_reset_token = uuid4()
        user.save()
        return ResetPasswordConfirm(success=True)


class Mutation(graphene.ObjectType):
    register = Register.Field()
    verify = VerifyEmail.Field()
    resend_verify_email = ResendVerifyEmail.Field()

    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    update_profile = UpdateProfile.Field()

    logout = Logout.Field()
    reset_password = ResetPassword.Field()
    reset_password_confirm = ResetPasswordConfirm.Field()
    reset_email = ResetEmail.Field()
    reset_email_confirm = ResetEmailConfirm.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
