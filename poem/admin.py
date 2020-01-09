from django.contrib import admin

from poem.models import Poem, Genre, Category
# Register your models here.


class PoemAdmin(admin.ModelAdmin):
    class Meta:
        fields = ['title', 'genre', 'user']


class GenreAdmin(admin.ModelAdmin):
    class Meta:
        fields = ['name', 'disabled']


class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        fields = ['name', 'disabled']


admin.site.register(Poem, PoemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
