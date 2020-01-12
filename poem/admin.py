from django.contrib import admin

from poem.models import Poem, Genre, Category
# Register your models here.


class PoemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user']
    list_filter = ['user']

    class Meta:
        model = Poem


class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'disabled']
    list_filter = ['name']

    class Meta:
        model = Genre


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'disabled']
    list_filter = ['name']

    class Meta:
        model = Category


admin.site.register(Poem, PoemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
