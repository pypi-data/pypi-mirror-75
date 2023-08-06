from django.contrib.admin import ModelAdmin


class BasicInformationModelAdmin(ModelAdmin):
    list_display = ['username', 'email', 'pk', 'category', 'author', 'status']
    list_filter = ['created_at', 'updated_at', 'status']
    search_fields = ['username', 'email', 'pk']