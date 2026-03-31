from django.urls import path 
from .views import *

urlpatterns = [
    path('' , LoginView.as_view() , name='login_view') , 
    path('registration/' , RegistrationView.as_view() , name='registration_view') , 
    path('email_sent/' , EmailConfirmationSentView.as_view() , name='email_confirmation_sent') , 
    path('confirm_email/<str:token>/' , ConfirmEmailView.as_view() , name='confirm_email') , 
    path('forgot_password/' , ForgotPasswordView.as_view() , name='forgot_password') , 
    path('reset_password/<str:token>/' , ResetPasswordView.as_view() , name='reset_password') ,
    path('change_password/' , ChangePasswordView.as_view() , name='change_password') , 
    path('profile/' , ProfileView.as_view() , name='profile') ,
    path('profile/edit/' , EditProfileView.as_view() , name='edit_profile') ,
    path('logout/' , LogoutView.as_view() , name='logout')
]
