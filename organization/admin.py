from django.contrib import admin
from .models import (
    Address,
    College,
    Course,
    Membership,
    SocialLink,
    Enrollment,
    AcademicRecord,
    AlumniImport,
    ImportedAlumniRow,
)

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    readonly_fields = ("created_at",)


class AcademicRecordInline(admin.TabularInline):
    model = AcademicRecord
    extra = 0
    readonly_fields = ("created_at",)


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0
    readonly_fields = ("created_at", "updated_at")


class ImportedAlumniRowInline(admin.TabularInline):
    model = ImportedAlumniRow
    extra = 0
    readonly_fields = ("created_at",)
    can_delete = False


# Admin Classes

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("city", "state", "country", "postal_code")
    list_filter = ("state", "country")
    search_fields = ("city", "state", "postal_code")


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ("name", "handle", "established_date", "admin", "is_deleted")
    list_filter = ("is_deleted", "established_date")
    search_fields = ("name", "handle", "admin__email")
    readonly_fields = ("created_at", "updated_at")
    inlines = [SocialLinkInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "college", "duration_years", "is_active")
    list_filter = ("is_active", "college")
    search_fields = ("name", "specialization", "college__name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "college", "role", "contact_email", "contact_phone", "created_at")
    list_filter = ("role", "college")
    search_fields = ("user__email", "user__name", "contact_email", "college__name")
    readonly_fields = ("created_at",)
    inlines = [EnrollmentInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("membership", "course", "enrollment_number", "start_year", "end_year", "is_confirmed")
    list_filter = ("is_confirmed", "start_year", "end_year", "course__college")
    search_fields = ("enrollment_number", "membership__user__email", "course__name")
    readonly_fields = ("created_at",)
    inlines = [AcademicRecordInline]


@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "semester", "cgpa", "sgpa", "percentage", "created_at")
    list_filter = ("semester",)
    search_fields = ("enrollment__enrollment_number", "enrollment__membership__user__email")
    readonly_fields = ("created_at",)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("type", "url", "college", "member", "created_at")
    list_filter = ("type",)
    search_fields = ("type", "college__name", "member__user__email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(AlumniImport)
class AlumniImportAdmin(admin.ModelAdmin):
    list_display = ("id", "college", "uploaded_by", "status", "total_rows", "processed_rows", "created_at")
    list_filter = ("status", "college")
    search_fields = ("college__name", "uploaded_by__user__email")
    readonly_fields = ("created_at",)
    inlines = [ImportedAlumniRowInline]


@admin.register(ImportedAlumniRow)
class ImportedAlumniRowAdmin(admin.ModelAdmin):
    list_display = ("import_job", "row_number", "processed", "success", "created_at")
    list_filter = ("processed", "success")
    search_fields = ("import_job__id", "row_number")
    readonly_fields = ("created_at",)
