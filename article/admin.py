from django.contrib import admin

# 别忘了导入 ArticlePost
from .models import ArticlePost, ArticleColumn


class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ('author', 'avatar_admin', 'column', 'tag_list', 'total_views', 'likes', 'updated', 'created')
    list_filter = ['author', 'column', 'tags', 'total_views', 'likes', ]

    # def get_queryset(self, request):
    #     return super().get_queryset(request).prefetch_related('tags')
    #
    # def tag_list(self, obj):
    #     return u",".join(o.name for o in obj.tags.all())


class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    list_filter = ['title', 'created']


# 注册ArticlePost到admin中
admin.site.register(ArticlePost, ArticlePostAdmin)

# 注册文章栏目
admin.site.register(ArticleColumn, ArticleColumnAdmin)
