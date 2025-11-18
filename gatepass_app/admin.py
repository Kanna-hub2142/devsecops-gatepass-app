from django.contrib import admin
from django.utils import timezone
from .models import Hostel, StudentProfile, GatePass

# -----------------------------
# HOSTEL ADMIN
# -----------------------------
@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# -----------------------------
# STUDENT PROFILE ADMIN
# -----------------------------
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "hostel", "phone")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    list_filter = ("hostel",)


# -----------------------------
# GATE PASS ADMIN
# -----------------------------
@admin.register(GatePass)
class GatePassAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "status",
        "from_datetime",
        "to_datetime",
        "applied_at",
        "approved_by",
    )
    list_filter = ("status", "applied_at", "from_datetime", "to_datetime")
    search_fields = ("student__user__username",)

    actions = ["approve_passes", "reject_passes"]

    # Approve action
    def approve_passes(self, request, queryset):
        for obj in queryset:
            obj.status = GatePass.STATUS_APPROVED
            obj.approved_by = request.user
            obj.approved_at = timezone.now()
            obj.save()
    approve_passes.short_description = "Approve selected Gate Passes"

    # Reject action
    def reject_passes(self, request, queryset):
        queryset.update(status=GatePass.STATUS_REJECTED)
    reject_passes.short_description = "Reject selected Gate Passes"
