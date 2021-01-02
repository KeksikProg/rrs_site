from django.contrib import admin

from main.models import AdditionalImage, Post, Rubric, Client, Comments


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    """Админка для постов"""

    class AdditionalImageInline(admin.TabularInline):
        """Для того, чтобы вместе с постами выводилис их дополнительные изображения"""

        model = AdditionalImage

    list_display = ('rubric', 'link', 'title', 'author', 'created_at', 'is_active')
    list_filter = ('rubric', 'is_active')
    search_fields = ('rubric', 'title', 'author', 'created_at')
    readonly_fields = ('created_at', 'author')
    inlines = (AdditionalImageInline,)

    fieldsets = (
        (None, {
            'fields': (('title', 'rubric'), 'content', 'image', ('author', 'created_at'), 'slug'),
            'classes': ('wide',)
        }),
        ('Дополнительная информация, если пост видео', {
            'fields': ('link', 'published')
        })
    )


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    """Для админки рубрик"""

    list_display = ('title',)
    readonly_fields = ('slug',)


@admin.register(Client)
class ClientsAdmin(admin.ModelAdmin):
    """Для админки клиентов (кроме поля активации ни одно изменить нельзя)"""

    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active', 'slug')
    readonly_fields = ('username', 'first_name', 'last_name', 'email', 'slug')
    search_fields = ('username', 'email', 'slug')
    list_editable = ('is_active',)
    fields = ('username', ('first_name', 'last_name'), 'email', ('is_staff', 'is_active'), 'slug')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Для админки комментариев"""

    list_display = ('post', 'author', 'created_at')
    fields = ('post', 'content', ('author', 'created_at'))


admin.site.register(AdditionalImage) # Решил не делать админку для доп. изображений тк не вижк смысла

admin.site.site_title = 'Администрирование'
admin.site.site_header = 'Russian Red Skins'
admin.site.index_title = 'Каталоги'
# Register your models here.
