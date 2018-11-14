from django.contrib import admin

# Register your models here.
from .models import Images


class ImagesAdmin(admin.ModelAdmin):
    list_display = ["title", "image", "users", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title"]

    class Meta:
        model = Images


admin.site.register(Images, ImagesAdmin)
