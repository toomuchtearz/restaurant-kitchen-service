from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class DishType(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.IntegerField()


class Dish(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField()
    price = models.DecimalField()
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        related_name="dishes"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name="dishes"
    )
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="dishes"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "dish"
        verbose_name_plural = "dishes"
