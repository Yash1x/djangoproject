from django.db import models
from django.urls import reverse


# Create your models here.
class Publication(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1,  'Опубликовано'
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    picture = models.ImageField(upload_to='publications/%Y/%m', blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='publications')
    factors = models.ManyToManyField('InvestmentFactor', blank=True, related_name='publications')
    passport = models.OneToOneField(
        'ProjectPassport',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='publication',
    )
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


class InvestmentFactor(models.Model):
    factor = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.factor

    def get_absolute_url(self):
        return reverse('factor', kwargs={'factor_slug': self.slug})


class ProjectPassport(models.Model):
    project_code = models.CharField(max_length=100, unique=True, db_index=True)
    initiator = models.CharField(max_length=100)
    budget_mln_rub = models.IntegerField(null=True, blank=True)
    horizon_years = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.project_code
