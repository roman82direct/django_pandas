from django.contrib import admin

from .models import Group, MainCategory, SecondCategory


class CommonSettings(admin.ModelAdmin):

    list_display_links = ('title',)
    list_editable = ('description', )
    list_per_page = 10


class MainCategoryInline(admin.TabularInline):
    model = MainCategory
    extra = 1
    show_change_link = True


@admin.register(Group)
class GroupAdmin(CommonSettings):
    list_display = (
        'articul',
        'title',
        'description',
        'created_at',
        'updated_at'
    )
    search_fields = ('title', 'articul',)
    inlines = (MainCategoryInline,)


class SecondCategoryInline(admin.TabularInline):
    model = SecondCategory
    extra = 1
    show_change_link = True


@admin.register(MainCategory)
class MainCategoryAdmin(CommonSettings):
    list_display = (
        'articul',
        'title',
        'description',
        'group',
        'created_at',
        'updated_at'
    )
    search_fields = ('title', 'group__title', 'group__articul',)
    list_filter = ('group',)
    list_select_related = ('group',)
    inlines = (SecondCategoryInline,)


@admin.register(SecondCategory)
class SecondCategoryAdmin(CommonSettings):
    list_display = (
        'articul',
        'title',
        'description',
        'maincategory',
        'created_at',
        'updated_at'
    )
    search_fields = ('title', 'maincategory__title', 'maincategory__articul',)
    list_filter = ('articul', 'title', 'maincategory',)
    list_select_related = ('maincategory',)
