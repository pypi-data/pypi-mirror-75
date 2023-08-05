# arvestust:admin
from django.contrib import admin
from ..models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = [
        'slug',
        'created_at',
        'updated_at',
        'uploaded_by',
        'content_type',
        'object_id',
        'file',
    ]

    # Ensure current user is assigned as author of post instance.
    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by_id:
            obj.uploaded_by = request.user
        obj.save()
