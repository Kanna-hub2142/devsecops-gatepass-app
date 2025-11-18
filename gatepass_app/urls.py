from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import logout

urlpatterns = [

    # -------------------------------
    # AUTH
    # -------------------------------
    path("signup/", views.signup_view, name="signup"),

    path("login/",
         auth_views.LoginView.as_view(
             template_name="registration/login.html",
             redirect_authenticated_user=True
         ),
         name="login"),

    path("logout/", views.logout_view, name="logout"),

    path("login-redirect/", views.login_redirect_view, name="login_redirect"),


    # -------------------------------
    # HOME (decides admin/student)
    # -------------------------------
    path("", views.home, name="home"),


    # -------------------------------
    # STUDENT
    # -------------------------------
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("student/apply-pass/", views.apply_gatepass, name="apply_pass"),
    path("student/my-requests/", views.my_requests, name="my_requests"),
    path("student/profile/", views.student_profile_update, name="student_profile_update"),


    # -------------------------------
    # ADMIN DASHBOARD
    # -------------------------------
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # Hostel management
    path("admin/hostels/", views.hostel_list, name="hostel_list"),
    path("admin/hostels/add/", views.hostel_add, name="hostel_add"),
    path("admin/hostels/edit/<int:pk>/", views.hostel_edit, name="hostel_edit"),
    path("admin/hostels/delete/<int:pk>/", views.hostel_delete, name="hostel_delete"),

    # Admin GatePass management
    path("admin/gatepasses/", views.admin_gatepass_list, name="admin_gatepass_list"),
    path("admin/gatepasses/approve/<int:pk>/", views.admin_gatepass_approve, name="admin_gatepass_approve"),
    path("admin/gatepasses/reject/<int:pk>/", views.admin_gatepass_reject, name="admin_gatepass_reject"),

]
