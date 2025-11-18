from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ---------------------------------------------------
# HOSTEL MODEL
# ---------------------------------------------------
class Hostel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ---------------------------------------------------
# STUDENT PROFILE MODEL
# ---------------------------------------------------
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.hostel})"


# ---------------------------------------------------
# GATE PASS MODEL
# ---------------------------------------------------
class GatePass(models.Model):
    STATUS_PENDING = "P"
    STATUS_APPROVED = "A"
    STATUS_REJECTED = "R"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="passes"
    )

    reason = models.TextField()
    from_datetime = models.DateTimeField()
    to_datetime = models.DateTimeField()

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    applied_at = models.DateTimeField(default=timezone.now)
    approved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="approved_passes"
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-applied_at"]

    def __str__(self):
        return f"GatePass #{self.id} - {self.get_status_display()}"
