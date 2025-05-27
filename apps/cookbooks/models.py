# D:\PythonProject\WebPagesParsing\cookbooks\models.py

import uuid
from django.db import models


class MediaType(models.TextChoices):
    IMAGE = 'image', 'Изображение'
    YOUTUBE = 'youtube', 'YouTube'


'''абстрактная модель для повторяющихся полей'''
# class BaseContent(models.Model):
#     slug = models.SlugField(max_length=70, unique=True, db_index=True)
#     title = models.CharField(max_length=255, unique=True)
#     description = models.TextField(blank=True)
#     type = models.CharField(max_length=50, choices=MediaType.choices, default=MediaType.IMAGE)
#     media_source_url = models.URLField(max_length=500, blank=True)
#     media_cloud_url = models.URLField(max_length=500, blank=True)
#     media_local_url = models.URLField(max_length=500, blank=True)
#     is_active = models.BooleanField(default=True)
#
#     class Meta:
#         abstract = True


# модель Категории
class Category(models.Model):
    """
    Категории рецептов (например, 'Завтрак', 'Обед')
    таблица БД "cookbooks_category"
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )

    slug = models.SlugField(
        max_length=70, unique=True, db_index=True, verbose_name="URL"
    )

    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название категории"
    )

    source_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на категорию первоисточника"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Краткое описание"
    )

    type = models.CharField(
        max_length=50,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
        verbose_name="Тип медиа"
    )

    media_source_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа из первоисточника"
    )

    media_cloud_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа в облаке"
    )

    media_local_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа в Django (media/...)"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна ли категория"
    )

    position = models.PositiveIntegerField(
        default=0,
        verbose_name="Позиция в списке"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['position', 'title']

    def __str__(self):
        return self.title


# модель Подкатегории
class Subcategory(models.Model):
    """
    Подкатегории рецептов (например, 'Овощные супы' внутри 'Супы')
    таблица БД "cookbooks_subcategory"
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name="Родительская категория"
    )

    slug = models.SlugField(
        max_length=70, unique=True, db_index=True, verbose_name="URL"
    )

    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название подкатегории"
    )

    source_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на подкатегорию первоисточника"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Краткое описание"
    )

    type = models.CharField(
        max_length=50,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
        verbose_name="Тип медиа"
    )

    media_source_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа из первоисточника"
    )

    media_cloud_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа в облаке"
    )

    media_local_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа в Django (media/...)"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна ли подкатегория"
    )

    position = models.PositiveIntegerField(
        default=0,
        verbose_name="Позиция в списке"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['position', 'title']

    def __str__(self):
        return f"{self.title} ({self.category.title})"


# модель Карточка рецептов
class RecipeCard(models.Model):
    """
    Карточка рецепта (например, 'Щи из квашеной капусты' внутри 'Овощные супы')
    таблица БД "cookbooks_recipecard"
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID рецепта"
    )

    slug = models.SlugField(
        max_length=70, unique=True, db_index=True, verbose_name="URL"
    )

    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Подкатегория рецепта"
    )

    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название рецепта"
    )

    source_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на рецепт в первоисточнике"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Краткое описание рецепта"
    )

    type = models.CharField(
        max_length=50,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
        verbose_name="Тип медиа"
    )

    media_source_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа из первоисточника"
    )

    media_cloud_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа в облаке"
    )

    media_local_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа в Django (media/...)"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна ли карточка рецепта"
    )

    position = models.PositiveIntegerField(
        default=0,
        verbose_name="Позиция в списке"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    # Дополнения внутри класса RecipeCard

    rating = models.FloatField(
        default=0.0,
        verbose_name="Средняя оценка рецепта"
    )

    comments_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество комментариев"
    )

    comments_anchor_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Якорная ссылка на комментарии"
    )

    has_video = models.BooleanField(
        default=False,
        verbose_name="Есть ли видео к рецепту"
    )

    is_vegetarian = models.BooleanField(
        default=False,
        verbose_name="Вегетарианский рецепт"
    )

    cooking_time = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Время приготовления (строка)"
    )

    author_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Имя автора рецепта"
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата публикации рецепта"
    )

    class Meta:
        verbose_name = "Карточка рецепта"
        verbose_name_plural = "Карточки рецептов"
        ordering = ['position', 'title']

    def __str__(self):
        return f"{self.title} ({self.subcategory.title})"


# модель "Единица измерения"
class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Единица измерения")

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"
        ordering = ['name']

    def __str__(self):
        return self.name


# модель Ингредиенты
class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID ингредиента")
    name = models.CharField(max_length=255, unique=True, verbose_name="Название ингредиента")

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.unit}"


# модель Хэштеги
class Hashtag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID хэштега")
    name = models.CharField(max_length=100, unique=True, verbose_name="Хэштег")


# модель Экран рецепта
class RecipeScreen(models.Model):
    """
    Модель Экран рецепта (например, 'Щи из квашеной капусты' внутри 'Овощные супы')
    связана с моделью карточки рецепта один-к-одному
    таблица БД "cookbooks_recipescreen"
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID рецепта"
    )

    slug = models.SlugField(
        max_length=70, unique=True, db_index=True, verbose_name="URL"
    )

    recipe_card = models.OneToOneField(
        RecipeCard,
        on_delete=models.CASCADE,
        related_name="screen",
        verbose_name="Карточка рецепта"
    )

    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название рецепта"
    )

    source_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на рецепт в первоисточнике"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание рецепта"
    )

    type = models.CharField(
        max_length=50,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
        verbose_name="Тип медиа"
    )

    media_source_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа из первоисточника"
    )

    media_cloud_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа в облаке"
    )

    media_local_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа в Django (media/...)"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна ли карточка рецепта"
    )

    hashtags = models.ManyToManyField(
        Hashtag,
        through='RecipeHashtags',
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )

    count = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='Количество порций')

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = "Экран рецепта"
        verbose_name_plural = "Экраны рецептов"
        ordering = ['title', ]

    def __str__(self):
        return f"{self.title} ({self.recipe_card.title})"


# Явная модель связи рецептов и ингредиентов (многие-к-многим)
class RecipeIngredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(RecipeScreen, on_delete=models.CASCADE, related_name="recipe_ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="ingredient_recipes")
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Количество ингредиента")
    original_amount = models.CharField(max_length=50, verbose_name="Оригинальное количество", blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name="Единица измерения")


# Связи рецептов и хэштегом (многие-к-многим) Создаётся автоматически.
# Явная модель связи рецептов и хэштегом (многие-к-многим).
class RecipeHashtags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(RecipeScreen, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)


class RecipeStep(models.Model):
    """
    Пошаговая инструкция приготовления рецепта.
    Связана с RecipeScreen (один рецепт — много шагов).
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID шага"
    )

    recipe = models.ForeignKey(
        RecipeScreen,
        on_delete=models.CASCADE,
        related_name="steps",
        verbose_name="Рецепт"
    )

    step_number = models.PositiveIntegerField(
        verbose_name="Номер шага"
    )

    description = models.TextField(
        verbose_name="Описание шага"
    )

    # Медиа-информация
    type = models.CharField(
        max_length=50,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
        verbose_name="Тип медиа"
    )

    media_source_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа из первоисточника"
    )

    media_cloud_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа в облаке"
    )

    media_local_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа в Django (media/...)"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Шаг рецепта"
        verbose_name_plural = "Шаги рецепта"
        ordering = ['recipe', 'step_number']
        unique_together = ('recipe', 'step_number')  # для уникальности номера шага в рамках рецепта

    def __str__(self):
        return f"Шаг {self.step_number} для рецепта: {self.recipe.title}"


# Связь между рецептом и похожими рецептами.
class SimilarRecipe(models.Model):
    """
    Связь между рецептом и похожими рецептами.
    На первом этапе хранится только URL другого рецепта как строка.
    Позже можно связать через ForeignKey.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    recipe = models.ForeignKey(
        RecipeScreen,
        on_delete=models.CASCADE,
        related_name="similar_recipes",
        verbose_name="Исходный рецепт"
    )

    related_recipe_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="URL похожего рецепта"
    )

    related_recipe_uuid = models.UUIDField(
        verbose_name="ID похожего рецепта"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    class Meta:
        verbose_name = "Похожий рецепт"
        verbose_name_plural = "Похожие рецепты"
        ordering = ['recipe']

    def __str__(self):
        return f"Похожий рецепт для: {self.recipe.title} — {self.related_recipe_uuid}"


class CommentUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    author_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Имя автора комментария"
    )

    nickname = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Псевдоним автора комментария"
    )

    picture_source_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа из первоисточника"
    )

    picture_local_link = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на медиа в Django (media/...)"
    )

    def __str__(self):
        return self.author_name or "Аноним"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    recipe = models.ForeignKey(
        RecipeScreen,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Рецепт"
    )

    user_comment = models.ForeignKey(
        CommentUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Пользователь"
    )

    text = models.TextField(verbose_name="Текст комментария")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Комментарий от {self.user_comment} к рецепту {self.recipe}"
