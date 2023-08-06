from django.contrib.admin import ModelAdmin


class CategoryModelAdmin(ModelAdmin):
    list_display = ['title', 'pk', 'author', 'status']
    list_filter = ['created_at', 'updated_at', 'status']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}