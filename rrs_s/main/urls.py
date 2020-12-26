from django.urls import path

from main.views import home, docs, CLogin, CLogout, ChangeUserInfo, ChangeClientPassword, DeleteClientView, ClientRegView, ClientRegisterDone, user_activate, add_posts, delete_posts, change_posts, detail_post, by_rubric, ClientResetView, ClientPasswordResetDone, ClientPasswordResetConfirmView

urlpatterns = [
    # other
    path('', home, name='home'),
    path('docs/<str:page>/', docs, name='docs'),

    # user and profile
    path('profile/login/', CLogin.as_view(), name='login'),
    path('profile/logout/', CLogout.as_view(), name='logout'),
    path('profile/change_info/', ChangeUserInfo.as_view(), name='change_info'),
    path('profile/change_pass/', ChangeClientPassword.as_view(), name='change_pass'),
    path('profile/delete_user/', DeleteClientView.as_view(), name='delete_user'),

    # register user
    path('profile/register/register_user/', ClientRegView.as_view(), name='client_register'),
    path('profile/register/register_done/', ClientRegisterDone.as_view(), name='register_done'),
    path('profile/register/activate/<str:sign>/', user_activate, name='activate'),
    # path('profile/detail/', profile, name = 'profile')

    # reset password
    path('profile/password_reset_form/', ClientResetView.as_view(), name='password_reset_form'),
    path('profile/password_reset_done/', ClientPasswordResetDone.as_view(), name='password_reset_done'),
    path('profile/password_reset_confirm/<uidb64>/<token>/', ClientPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # posts
    path('posts/add/', add_posts, name='add_posts'),
    path('posts/delete/<slug:slug>/', delete_posts, name='delete_posts'),
    path('posts/change/<slug:slug>/', change_posts, name='change_posts'),
    path('posts/detail/<slug:slug>/', detail_post, name='detail_post'),
    path('posts/rubric/<slug:slug>/', by_rubric, name='by_rubric'),

]
