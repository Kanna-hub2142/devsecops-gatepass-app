from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import GatePass
from .forms import StudentSignUpForm, GatePassForm, StudentProfileUpdateForm
from .models import StudentProfile, GatePass, Hostel


# =====================================================
# AUTH / SIGNUP / LOGIN REDIRECT
# =====================================================

def signup_view(request):
    """Student signup — stays on same page after registration."""
    if request.method == "POST":
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()

            messages.success(request, "Registration successful! Please login.")
            return redirect("signup")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentSignUpForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def login_redirect_view(request):
    """Decide where to send the user based on role."""
    if request.user.is_staff:
        return redirect("admin_dashboard")
    return redirect("student_dashboard")


@login_required
def home(request):
    """Root path — redirect based on user type."""
    if request.user.is_staff:
        return redirect("admin_dashboard")
    return redirect("student_dashboard")


# =====================================================
# STUDENT VIEWS
# =====================================================

@login_required
def student_dashboard(request):
    """Dashboard for students."""
    if request.user.is_staff:
        return redirect("admin_dashboard")

    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect("signup")

    recent_passes = profile.passes.all()[:10]

    return render(request, "student/dashboard.html", {
        "profile": profile,
        "recent": recent_passes,
    })


@login_required
def apply_gatepass(request):
    """Student applies for a gate pass."""
    if request.user.is_staff:
        return redirect("admin_dashboard")

    profile = request.user.studentprofile

    if request.method == "POST":
        form = GatePassForm(request.POST)
        if form.is_valid():
            gp = form.save(commit=False)
            gp.student = profile
            gp.save()
            messages.success(request, "Gate pass request submitted!")
            return redirect("my_requests")
    else:
        form = GatePassForm()

    return render(request, "student/apply_pass.html", {"form": form})


@login_required
def my_requests(request):
    """Student views all their gate pass requests."""
    if request.user.is_staff:
        return redirect("admin_dashboard")

    profile = request.user.studentprofile
    passes = profile.passes.all()

    return render(request, "student/my_requests.html", {"passes": passes})


@login_required
def student_profile_update(request):
    """Student edits name + phone."""
    if request.user.is_staff:
        return redirect("admin_dashboard")

    profile = request.user.studentprofile

    if request.method == "POST":
        form = StudentProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, "Profile updated successfully.")
            return redirect("student_profile_update")
    else:
        form = StudentProfileUpdateForm(
            instance=profile,
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }
        )

    return render(request, "student/profile_update.html", {"form": form})


# =====================================================
# ADMIN VIEWS
# =====================================================

@login_required
def admin_dashboard(request):
    """Admin dashboard showing stats."""
    if not request.user.is_staff:
        return redirect("student_dashboard")

    total_students = StudentProfile.objects.count()
    total_passes = GatePass.objects.count()
    pending = GatePass.objects.filter(status="P").count()

    return render(request, "admin/dashboard.html", {
        "total_students": total_students,
        "total_passes": total_passes,
        "pending": pending,
    })


# -----------------------
# HOSTEL CRUD (ADMIN ONLY)
# -----------------------

@login_required
def hostel_list(request):
    if not request.user.is_staff:
        return redirect("student_dashboard")

    hostels = Hostel.objects.all()
    return render(request, "admin/hostels_list.html", {"hostels": hostels})


@login_required
def hostel_add(request):
    if not request.user.is_staff:
        return redirect("student_dashboard")

    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Hostel.objects.create(name=name)
            messages.success(request, "Hostel added successfully.")
            return redirect("hostel_list")
        else:
            messages.error(request, "Hostel name cannot be empty.")

    return render(request, "admin/hostels_add.html")


@login_required
def hostel_edit(request, pk):
    if not request.user.is_staff:
        return redirect("student_dashboard")

    hostel = get_object_or_404(Hostel, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            hostel.name = name
            hostel.save()
            messages.success(request, "Hostel updated successfully.")
            return redirect("hostel_list")
        else:
            messages.error(request, "Name cannot be empty.")

    return render(request, "admin/hostels_edit.html", {"hostel": hostel})


@login_required
def hostel_delete(request, pk):
    if not request.user.is_staff:
        return redirect("student_dashboard")

    hostel = get_object_or_404(Hostel, pk=pk)
    hostel.delete()
    messages.success(request, "Hostel deleted successfully.")
    return redirect("hostel_list")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def admin_gatepass_list(request):
    if not request.user.is_staff:
        return redirect("student_dashboard")

    passes = GatePass.objects.all().order_by("-applied_at")

    return render(request, "admin/gatepass_list.html", {
        "passes": passes
    })


@login_required
def admin_gatepass_approve(request, pk):
    if not request.user.is_staff:
        return redirect("student_dashboard")

    gp = get_object_or_404(GatePass, pk=pk)
    
    gp.status = GatePass.STATUS_APPROVED
    gp.approved_by = request.user
    gp.approved_at = timezone.now()
    gp.save()

    messages.success(request, "Gate pass approved successfully.")
    return redirect("admin_gatepass_list")


@login_required
def admin_gatepass_reject(request, pk):
    if not request.user.is_staff:
        return redirect("student_dashboard")

    gp = get_object_or_404(GatePass, pk=pk)
    
    gp.status = GatePass.STATUS_REJECTED
    gp.approved_by = None
    gp.approved_at = None
    gp.save()

    messages.success(request, "Gate pass rejected.")
    return redirect("admin_gatepass_list")