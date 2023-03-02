from slugify import slugify

from django.db import models

from account.models import User


class Category(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Category name'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Parent Category'
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        verbose_name='The slug is filled in automatically'
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Book(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Book name'
    )
    cover_image = models.ImageField(
        upload_to='book_covers/',
        verbose_name='Cover photo'
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Price'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Category'
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name='The slug is filled in automatically'
    )
    publisher = models.ManyToManyField(
        'Publisher',
        blank=True,
        related_name='books',
        verbose_name='Publisher'
    )
    author = models.ManyToManyField(
        'Author',
        blank=True,
        related_name='books',
        verbose_name='Author'
    )
    series = models.ManyToManyField(
        'Series',
        blank=True,
        related_name='books',
        verbose_name='Series'
    )
    interpreter = models.ManyToManyField(
        'Interpreter',
        blank=True,
        related_name='books',
        verbose_name='Interpreter'
    )
    illustrator = models.ManyToManyField(
        'Illustrator',
        blank=True,
        related_name='books',
        verbose_name='Illustrator'
    )
    illustrations = models.ManyToManyField(
        'Illustrations',
        blank=True,
        verbose_name='Illustrations'
    )
    paper = models.ManyToManyField(
        'Paper',
        blank=True,
        verbose_name='Paper'
    )
    font = models.ManyToManyField(
        'Font',
        blank=True,
        verbose_name='Font'
    )
    binding = models.ManyToManyField(
        'Binding',
        blank=True,
        verbose_name='Binding'
    )
    language = models.ManyToManyField(
        'Language',
        blank=True,
        verbose_name='Language'
    )
    year_of_first_publication = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Year of first publication'
    )
    year_of_publication = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Year of publication'
    )
    amount_pages = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Amount pages'
    )
    weight = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Weight'
    )
    edition = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Edition'
    )
    literature_of_the_countries_of_the_world = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Literature of the countries of the world'
    )
    format = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Format'
    )
    isbn = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='ISBN'
    )

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Author(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Author name'
    )
    image = models.ImageField(
        upload_to='authors/',
        null=True,
        blank=True,
        verbose_name='Author photo'
    )
    biography = models.TextField(
        null=True,
        blank=True,
        verbose_name='Biography'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='The slug is filled in automatically'
    )

    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Publisher(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Publisher name'
    )
    image = models.ImageField(
        upload_to='publishers/',
        null=True,
        blank=True,
        verbose_name='Publisher photo'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Description'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='The slug is filled in automatically'
    )

    class Meta:
        verbose_name = 'publisher'
        verbose_name_plural = 'Publishers'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Series(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Book series'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='The slug is filled in automatically'
    )

    class Meta:
        verbose_name = 'book series'
        verbose_name_plural = 'Book series'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Interpreter(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Interpreter name'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='The slug is filled in automatically'
    )

    class Meta:
        verbose_name = 'interpreter'
        verbose_name_plural = 'Interpreters'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Illustrator(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Illustrator name'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='The slug is filled in automatically'
    )

    class Meta:
        verbose_name = 'illustrator'
        verbose_name_plural = 'Illustrators'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Language(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Language'
    )

    class Meta:
        verbose_name = 'language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.title


class Binding(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Binding'
    )

    class Meta:
        verbose_name = 'binding'
        verbose_name_plural = 'Bindings'

    def __str__(self):
        return self.title


class Illustrations(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Illustrations'
    )

    class Meta:
        verbose_name = 'illustrations'
        verbose_name_plural = 'Illustrations'

    def __str__(self):
        return self.title


class Paper(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Paper'
    )

    class Meta:
        verbose_name = 'paper'
        verbose_name_plural = 'Paper'

    def __str__(self):
        return self.title


class Font(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Font'
    )

    class Meta:
        verbose_name = 'Font'
        verbose_name_plural = 'Fonts'

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING = (
        (1, 'Terribly'),
        (2, 'Badly'),
        (3, 'Normally'),
        (4, 'Fine'),
        (5, 'Perfectly'),
    )

    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Book review'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author of the review'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Title'
    )
    content = models.TextField(
        verbose_name='Content'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING,
        verbose_name='Rating'
    )
    created = models.DateField(
        auto_now_add=True,
        verbose_name='Date of creation'
    )

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f'{self.user} : {self.book}'
