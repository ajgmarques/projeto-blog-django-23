from django.db import models
from django.contrib.auth.models import User
from django_summernote.models import AbstractAttachment
from utils.rands import slugify_new
from utils.images import resize_image


# Create your models here.
class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True,
        max_length=255,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 8)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True,
        max_length=255,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 8)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True,
        max_length=255,
    )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado '
            'para a página ser exibida publicamente.'
        ),
    )
    content = models.TextField(blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 8)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True,
        max_length=255,
    )
    excerpt = models.CharField(max_length=150)
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado '
            'para a página ser exibida publicamente.'
        ),
    )
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default='')
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='Exibir a imagem de capa também no conteúdo do post?',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # user.post_created_by.all
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_created_by'
    )
    updated_at = models.DateTimeField(auto_now=True)
    # user.post_updated_by.all
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_updated_by'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 8)

        current_cover_name = str(self.cover.name)  # name antes do save
        super_save = super().save(*args, **kwargs)

        # verifica se o favicon mudou
        cover_changed = False
        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        # Caso tenha sido alterado faz o resize da imagem que está já salva,
        # pelo save anterior, na pasta dos assets
        if cover_changed:
            resize_image(self.cover, 900)

        return super_save

    def __str__(self) -> str:
        return self.title


# sobrescrever o método save do summernote para redimensionar imagens
class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)  # name antes do save
        super_save = super().save(*args, **kwargs)

        # verifica se o favicon mudou
        file_changed = False
        if self.file:
            file_changed = current_file_name != self.file.name

        # Caso tenha sido alterado faz o resize da imagem que está já salva,
        # pelo save anterior, na pasta dos assets
        if file_changed:
            resize_image(self.file, 900, True, 70)

        return super_save
