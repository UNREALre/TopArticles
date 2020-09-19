from django.contrib import admin

from .models import Source, Article


class SourceAdmin(admin.ModelAdmin):
    pass


class ArticleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Source, SourceAdmin)
admin.site.register(Article, ArticleAdmin)
