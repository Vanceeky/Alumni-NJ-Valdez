from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"),
    path('login-user/', views.login_user, name="login-user"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),

    path('user-profile/', views.alumni_profile, name="alumni-profile"),
    path('edit-avatar/', views.edit_avatar, name="edit-avatar"),
    
    path('register/', views.register_page, name="register"),
    path('profile/', views.profile, name="profile"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('alumni/', views.alumni, name="alumni"),
    path('transcript-of-records/', views.transcript, name="transcript"),
    path('diploma/', views.diploma, name="diploma"),
    path('jobs/', views.jobs, name="jobs"),

    path('post-job/', views.post_job, name="post-job"),
    path('request-file/', views.request_file, name="request-file"),
    path('approve-request/', views.approve_request, name="approve-request"),

    path('approve-user/<str:request_id>/', views.approve_user, name="approve-user"),
    path('approve-job/<str:request_id>/', views.approve_job, name="approve-job"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)