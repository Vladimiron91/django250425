from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from test_app.models import Book, Post, UserProfile, User, Task, SubTask, Category


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'nickname',
        'age',
        'followers_count',
        'posts_count',
        'comments_count',
        'engagement_rate',
    )

    list_filter = (
        'age',
        'posts_count',
        'engagement_rate'
    )

    search_fields = (
        'nickname',
        'age'
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created_at'
    )
    list_filter = (
        'created_at',
    )
    search_fields = (
        'title',
    )

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (  # Специальный параметр, который поможет задавать группы полей. при обновлении и Выделять определённый поля прям в группки
        (None, {'fields': ('username', 'password')}), # безымянная группа, базовые стартовые поля пароля и имени
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'birth_date', 'gender', 'role', 'age')}),  # Группа полей "Персональная информация"
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  # Группа полей "Разрешения"
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),  # Группа полей "Важные даты"
    )
    add_fieldsets = (  # а это будет отдельная группа тех полей, которые должны быть при СОЗДАНИИ
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'gender', 'is_staff')  # Список полей на отображение
    search_fields = ('username', 'first_name', 'last_name', 'email')  # список полей на поиск
    ordering = ('username',)  # порядок оторбажения данных (сортировка)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title", "project", "status", "priority",
        "created_at", "due_date"
    )
    list_filter = ("status", "priority", "project", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    list_per_page = 20


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "status", "created_at")
    list_filter = ("status", "task")
    search_fields = ("title",)
    ordering = ("-created_at",)
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

admin.site.register(Book)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(Group)
admin.site.register(Group)
