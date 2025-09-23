import uuid
from django.db import models, transaction
from django.utils import timezone
from accounts.models import User

class Address(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    postal_code = models.CharField(max_length=20, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        db_table = "address"
        indexes = [models.Index(fields=["city", "state"])]

    def __str__(self):
        return f"{self.city}, {self.state}"
    

class College(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    name = models.CharField(max_length=255, db_index=True, null=False, blank=False)
    handle = models.CharField(max_length=255, db_index=True, unique=True, null=False, blank=False)
    website = models.URLField(blank=True, null=True)
    established_date = models.DateField(null=False, blank=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name="colleges")
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="colleges")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    is_deleted = models.BooleanField(default=False, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "College"
        verbose_name_plural = "Colleges"
        db_table = "colleges"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name", "handle"]),
        ]

    def __str__(self):
        return self.name


class Course(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=120, db_index=True)
    specialization = models.CharField(max_length=120, blank=True, null=True)
    duration_years = models.PositiveSmallIntegerField(help_text="Duration in years")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        db_table = "courses"
        unique_together = ("college", "name", "specialization")
        indexes = [models.Index(fields=["college", "name"])]

    def __str__(self):
        spec = f" - {self.specialization}" if self.specialization else ""
        return f"{self.name}{spec} ({self.duration_years} yrs)"


class Membership(models.Model):
    ROLE_STUDENT = "student"
    ROLE_FACULTY = "faculty"
    ROLE_ALUMNI = "alumni"
    ROLE_SUBADMIN = "sub_admin"
    ROLE_CHOICES = [
        (ROLE_STUDENT, "Student"),
        (ROLE_FACULTY, "Faculty"),
        (ROLE_ALUMNI, "Alumni"),
        (ROLE_SUBADMIN, "Sub-Admin"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # generic contact snapshot (copied at time of membership) to preserve history
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"
        db_table = "members"
        unique_together = ("user", "college", "role")
        indexes = [
            models.Index(fields=["college", "role"]),
            models.Index(fields=["user", "role"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} as {self.role} @ {self.college}"

    def promote_to_alumni(self):
        if self.role != self.ROLE_ALUMNI:
            self.role = self.ROLE_ALUMNI
            self.save(update_fields=["role"])



class SocialLink(models.Model):
    type = models.CharField(max_length=40)
    url = models.URLField()
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=True, blank=True, related_name='socials')
    member = models.ForeignKey(Membership, on_delete=models.CASCADE, null=True, blank=True, related_name='socials')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"
        db_table = "socials"
        ordering = ["type"]

    def __str__(self):
        if self.college:
            return f"{self.college.name} - {self.type}"
        elif self.member:
            return f"{self.member.user} - {self.type}"
        return f"{self.type}"


class Enrollment(models.Model):
    """
    A student's enrollment record. Students may have multiple enrollments for different courses
    or for multiple stints (eg: integrated programs).
    """
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name="enrollments")
    enrollment_number = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField()
    is_confirmed = models.BooleanField(default=False)  # admin confirms import or creation
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        db_table = 'enrollments'
        indexes = [
            models.Index(fields=["enrollment_number"]),
            models.Index(fields=["start_year", "end_year"]),
        ]
        ordering = ["-start_year"]

    def __str__(self):
        return f"{self.membership.user} [{self.course}] {self.start_year}-{self.end_year}"

    @property
    def is_graduated(self):
        return timezone.now().year > self.end_year


class AcademicRecord(models.Model):
    """
    Normalized academic result per enrollment (could be per semester/aggregate).
    Keep flexible - store semester-wise rows as needed.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="academic_records")
    semester = models.PositiveSmallIntegerField(blank=True, null=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    sgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    marks_json = models.JSONField(default=list, blank=True, null=True, help_text="raw/structured marks if available")
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["enrollment", "semester"])]
        verbose_name = "Academic Record"
        verbose_name_plural = "Academic Records"
        db_table = "academic_records"
        ordering = ["-semester", "-created_at"]

    def __str__(self):
        return f"{self.enrollment} sem:{self.semester} cgpa:{self.cgpa}"


class AlumniImport(models.Model):
    """
    Staging model to track CSV/Excel import jobs.
    The uploaded file is placed on storage (S3/local) and processed asynchronously.
    """
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_DONE = "done"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_DONE, "Done"),
        (STATUS_FAILED, "Failed"),
    ]

    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="alumni_imports")
    uploaded_by = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, related_name="uploads")
    file = models.FileField(upload_to="alumni_imports/%Y/")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    total_rows = models.PositiveIntegerField(default=0)
    processed_rows = models.PositiveIntegerField(default=0)
    errors = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Alumni Import"
        verbose_name_plural = "Alumni Imports"
        db_table = "alumni_imports"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["college", "status"])]

    def __str__(self):
        return f"Import {self.id} for {self.college.name} by {self.uploaded_by or 'System'}"


class ImportedAlumniRow(models.Model):
    """
    Staged single row from CSV/Excel. Keeps raw row for audit and retry.
    """
    import_job = models.ForeignKey(AlumniImport, on_delete=models.CASCADE, related_name="rows")
    row_number = models.PositiveIntegerField()
    raw_data = models.JSONField()  # the parsed row mapped to columns
    processed = models.BooleanField(default=False)
    success = models.BooleanField(null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imported Alumni Row"
        verbose_name_plural = "Imported Alumni Rows"
        db_table = "imported_alumni_rows"
        
        indexes = [models.Index(fields=["import_job", "processed"])]
        ordering = ["row_number"]

    def __str__(self):
        return f"Row {self.row_number} import {self.import_job.id}"