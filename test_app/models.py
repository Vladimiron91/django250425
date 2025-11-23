from enum import StrEnum

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

from django.utils.translation.trans_null import gettext_lazy as _
from django.utils import timezone

from django.db import models


class Role(StrEnum):  # Енам класс. Похоже как мы делали список с кортежами, только мощнее(можно создвать свои настройки, методы и прочее)
    lib_member = "Lib Member"
    admin = "Admin"
    moderator = "Moderator"
    guest = "Guest"

    @classmethod
    def choices(cls):  # choices параметр в поле требует список с кортежами, поэтому этот метод будет нам его формировать.
        return [(attr.name, attr.value) for attr in cls]


class Gender(StrEnum):
    male = "Male"
    female = "Female"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=45, unique=True)
    email = models.EmailField(_('email address'), max_length=75, unique=True)  # Вот эти _ -- это элиас функции gettext_lazy(). Так проще воспринимать. Функция помогает правильно отображать строковые значения, особенно при работающей интернационализации
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    role = models.CharField(
        max_length=35,
        choices=Role.choices(),  # Ставим чойсес как генерируемый список с кортежами из нашего класса Енам
        default=Role.lib_member
    )
    gender = models.CharField(
        choices=Gender.choices()
    )
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=45, null=True, blank=True)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(6), MaxValueValidator(120)],
        null=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()  # это специальный Менеджер, через который мы будем делать запросы в будущем.

    USERNAME_FIELD = "username"  # указываем какое поле будет восприниматься как юзернейм при входе в систему
    REQUIRED_FIELDS = ["email", "role", "age"]  # Указываем какие поля должны быть обязательными, помимо юзернейм и пароля (при создании суперпользователя)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"


class Book(models.Model):
    title = models.CharField(max_length=120)  # VARCHAR
    description = models.TextField()
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    pages = models.PositiveSmallIntegerField(default=0)
    is_bestseller = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )  # 9999.99
    discounted_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )  # 9999.99

    def __str__(self):
        return f"Book '{self.title}'  -- Author '{self.author}'"

    class Meta:
        db_table = "books"  # Название таблицы
        ordering = ["published_date",]  # Порядок сортировки при запросе данных из базы (по умолчанию сортировка по ID)
        verbose_name = "Book"  # изменение отображения названия модели в ед. числе для админ панели
        verbose_name_plural = "Books"  # изменение отображения названия модели во множественном числе для админ панели

        get_latest_by = "published_date"  # Определяет то, как будет отдаваться последний объект в базе. По умолчанию отдаётся последний по ID

        default_related_name = "books"  #  Помогает поставить related_name по умолчанию для всех связанных объектов (ForeignKey, OneToOneField, ManyToManyField)
        # unique_together = ["title", "published_date"]  # Помогает создавать ПАРЫ уникальности по двум и более колонкам

        indexes = [
            models.Index(
                fields=["title", "published_date"],
                name="idx_book_title_pub_date"
            )
        ]

        # constraints = [
        #     models.UniqueConstraint(
        #         fields=["title", "published_date"],
        #         name="unq_title_pub_date"
        #     ),
        #
        #     models.CheckConstraint(
        #         check=models.Q(pages__gte=0),
        #         name="book_pages_constraint"
        #     )
        # ]



class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "posts"  # Название таблицы

class UserProfile(models.Model):
    nickname = models.CharField(max_length=70, unique=True)
    bio = models.TextField(null=True, blank=True)
    website = models.URLField(max_length=250, blank=True, null=True)
    age = models.PositiveSmallIntegerField()
    followers_count = models.PositiveBigIntegerField()
    posts_count = models.PositiveIntegerField()
    comments_count = models.PositiveIntegerField()
    engagement_rate = models.FloatField()

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = "user_profile"  # Название таблицы

'''Домашнее задание: Проект "Менеджер задач" — продолжение
Цель:
Добавить строковое представление (str) и метаданные (Meta) к моделям менеджера задач, а также настроить административную панель для удобного управления этими моделями.
Реализуйте изменения в моделях:
Модель Task:
Добавить метод str, который возвращает название задачи.
Добавить класс Meta с настройками:
Имя таблицы в базе данных: 'task_manager_task'.
Сортировка по убыванию даты создания.
Человекочитаемое имя модели: 'Task'.
Уникальность по полю 'title'.'''

class Task(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        validators=[MinLengthValidator(10)])
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("New", "New"),
            ("In_progress", "In Progress"),
            ("Completed", "Completed"),
            ("Closed", "Closed"),
            ("Pending", "Pending"),
            ("Blocked", "Blocked"),
        ],
        default="New"
    )

    priority = models.CharField(
        max_length=20,
        choices=[
            ("Low", "Low"),
            ("Medium", "Medium"),
            ("High", "High"),
            ("Very High", "Very High"),
        ]
    )

    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    due_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    tags = models.ManyToManyField("Tag", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "task_manager_task"
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        constraints = [
            models.UniqueConstraint(fields=["title"], name="unique_task_title")
        ]

'''Модель SubTask:
Добавить метод str, который возвращает название подзадачи.
Добавить класс Meta с настройками:
Имя таблицы в базе данных: 'task_manager_subtask'.
Сортировка по убыванию даты создания.
Человекочитаемое имя модели: 'SubTask'.
Уникальность по полю 'title'.'''

class SubTask(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=[
            ("New", "New"),
            ("In_progress", "In Progress"),
            ("Completed", "Completed"),
            ("Closed", "Closed"),
            ("Pending", "Pending"),
            ("Blocked", "Blocked"),
        ],
        default="New"
    )

    deadline = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "task_manager_subtask"
        ordering = ["-created_at"]
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
        constraints = [
            models.UniqueConstraint(fields=["title"], name="unique_subtask_title")
        ]

'''Модель Category:
Добавить метод str, который возвращает название категории.
Добавить класс Meta с настройками:
Имя таблицы в базе данных: 'task_manager_category'.
Человекочитаемое имя модели: 'Category'.
Уникальность по полю 'name'.'''

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_category_name")
        ]