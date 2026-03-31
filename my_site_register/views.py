from django.shortcuts import render
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.views import View
from .models import UniqUser
from .permissions import (
    get_logged_in_user ,
    assign_role
)

def send_confirmation_email(request, user):
    token = user.generate_email_verification_token()
    confirmation_url = request.build_absolute_uri(
        reverse('confirm_email', args=[token])
    )

    message = (
        f'Hello {user.username},\n\n'
        'Thank you for registering.\n'
        'Open the link below to confirm your email:\n'
        f'{confirmation_url}\n\n'
        'This confirmation link works for 24 hours.'
    )

    send_mail(
        subject='Confirm your email',
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_reset_password_email(request, user):
    token = user.generate_reset_password_token()
    reset_url = request.build_absolute_uri(reverse('reset_password', args=[token]))


    message = (
        f'Hello {user.username},\n\n'
        'We received a request to reset your password.\n'
        'Open the link below to create a new password:\n'
        f'{reset_url}\n\n'
        'This reset link works for 1 hour.'
    )

    send_mail(
        subject='Reset your password',
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

class RegistrationView(View):
    def get(self, request):
        if get_logged_in_user(request):
            return redirect('home')
        return render(request, 'register.html')

    def post(self, request):
        if get_logged_in_user(request):
            return redirect('home')

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif UniqUser.objects.filter(username=username).exists():
            messages.error(request, 'This username already exists.')
        else:
            existing_email_user = UniqUser.objects.filter(email=email).first()

            if existing_email_user and existing_email_user.is_email_verified:
                messages.error(request, 'This email is already registered.')
            else:
                try:
                    validate_password(password, user=UniqUser(username=username, email=email))
                except ValidationError as error:
                    for message in error.messages:
                        messages.error(request, message)
                else:
                    if existing_email_user:
                        existing_email_user.username = username
                        existing_email_user.set_password(password)
                        existing_email_user.save(update_fields=['username', 'password'])
                        send_confirmation_email(request, existing_email_user)
                        if not existing_email_user.groups.exists():
                            assign_role(existing_email_user, 'Student')
                    else:
                        user = UniqUser.objects.create(username=username, email=email)
                        user.set_password(password)
                        user.save(update_fields=['password'])
                        assign_role(user, 'Student')
                        send_confirmation_email(request, user)

                    messages.success(request, 'Registration completed. Please confirm your email before login.')
                    return redirect('email_confirmation_sent')

        return render(request, 'register.html')


class EmailConfirmationSentView(View):
    def get(self, request):
        return render(request, 'email_confirmation_sent.html')


class ConfirmEmailView(View):
    def get(self, request, token):
        user = UniqUser.objects.filter(email_verification_token=token).first()

        if not user:
            messages.error(request, 'This confirmation link is invalid.')
            return redirect('login_view')

        if not user.email_verification_token_is_valid():
            send_confirmation_email(request, user)
            messages.info(request, 'The old confirmation link expired. A new confirmation email was sent.')
            return redirect('email_confirmation_sent')

        user.confirm_email()
        messages.success(request, 'Your email was confirmed. You can now log in.')
        return redirect('login_view')


class LoginView(View):
    def get(self, request):
        if get_logged_in_user(request):
            return redirect('home')
        return render(request, 'login.html')

    def post(self, request):
        if get_logged_in_user(request):
            return redirect('home')

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_email_verified:
                send_confirmation_email(request, user)
                messages.error(request, 'Please confirm your email first. We sent a new confirmation email.')
            else:
                login(request, user)
                messages.success(request, 'Login successful.')
                request.session.set_expiry(1209600 if remember_me else 0)
                return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect.')

        return render(request, 'login.html')


class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'forgot_password.html')

    def post(self, request):
        email = request.POST.get('email', '').strip().lower()
        user = UniqUser.objects.filter(email=email, is_email_verified=True).first()

        if user:
            send_reset_password_email(request, user)

        messages.success(request, 'If the email exists, a password reset link has been sent.')
        return redirect('forgot_password')


class ResetPasswordView(View):
    def get(self, request, token):
        user = UniqUser.objects.filter(reset_password_token=token).first()

        if not user or not user.reset_password_token_is_valid():
            if user:
                user.clear_reset_password_token()
            messages.error(request, 'This reset link is invalid or expired.')
            return redirect('forgot_password')

        return render(request, 'reset_password.html', {'token': token})

    def post(self, request, token):
        user = UniqUser.objects.filter(reset_password_token=token).first()

        if not user or not user.reset_password_token_is_valid():
            if user:
                user.clear_reset_password_token()
            messages.error(request, 'This reset link is invalid or expired.')
            return redirect('forgot_password')

        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            try:
                validate_password(password, user=user)
            except ValidationError as error:
                for message in error.messages:
                    messages.error(request, message)
            else:
                user.set_password(password)
                user.save(update_fields=['password'])
                user.clear_reset_password_token()
                messages.success(request, 'Your password has been reset. Please log in.')
                return redirect('login_view')

        return render(request, 'reset_password.html', {'token': token})


class ChangePasswordView(View):
    def get(self, request):
        if not get_logged_in_user(request):
            messages.error(request, 'Please log in first.')
            return redirect('login_view')
        return render(request, 'change_password.html')

    def post(self, request):
        current_user = get_logged_in_user(request)

        if not current_user:
            messages.error(request, 'Please log in first.')
            return redirect('login_view')

        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not current_user.check_password(old_password):
            messages.error(request, 'Your current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        else:
            try:
                validate_password(new_password, user=current_user)
            except ValidationError as error:
                for message in error.messages:
                    messages.error(request, message)
            else:
                current_user.set_password(new_password)
                current_user.save(update_fields=['password'])
                messages.success(request, 'Your password was changed successfully.')
                return redirect('home')

        return render(request, 'change_password.html')


class ProfileView(View):
    def get(self, request):
        current_user = get_logged_in_user(request)

        if not current_user:
            messages.error(request, 'Please log in first.')
            return redirect('login_view')

        return render(request, 'profile.html', {'profile_user': current_user})


class EditProfileView(View):
    def get(self, request):
        current_user = get_logged_in_user(request)

        if not current_user:
            messages.error(request, 'Please log in first.')
            return redirect('login_view')

        return render(request, 'edit_profile.html', {'profile_user': current_user})

    def post(self, request):
        current_user = get_logged_in_user(request)

        if not current_user:
            messages.error(request, 'Please log in first.')
            return redirect('login_view')

        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        bio = request.POST.get('bio', '').strip()

        if not username:
            messages.error(request, 'Username cannot be empty.')
            return render(request, 'edit_profile.html', {'profile_user': current_user})

        username_taken = UniqUser.objects.filter(username=username).exclude(pk=current_user.pk).exists()
        if username_taken:
            messages.error(request, 'This username is already taken.')
            return render(request, 'edit_profile.html', {'profile_user': current_user})

        if not bio:
            bio = 'I use Build Box.'

        current_user.username = username
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.bio = bio[:500]

        if request.FILES.get('profile_image'):
            current_user.profile_image = request.FILES['profile_image']

        current_user.save(update_fields=['username', 'first_name', 'last_name', 'bio', 'profile_image'])
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('login_view')
