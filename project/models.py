from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Profile(models.Model):
    """
    Represents a user profile tied to a Django User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(blank=True, help_text="")
    profile_picture_url = models.URLField(max_length=500, blank=True, null=True, help_text="")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        """
        Returns the URL to view this Profile object.
        """
        return reverse("profile_detail", kwargs={"pk": self.pk})


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes")
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    MEAL_TYPE_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    ]
    meal_type = models.CharField(max_length=50, choices=MEAL_TYPE_CHOICES)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients')
    quantity = models.CharField(max_length=50, help_text="Specify the amount or measurement (e.g., '1 cup')")

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} for {self.recipe.title}"


class Category(models.Model):
    name = models.CharField(max_length=255)
    recipes = models.ManyToManyField(Recipe, related_name='categories')

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    MEAL_TYPE_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    ]
    meal_type = models.CharField(max_length=50, choices=MEAL_TYPE_CHOICES)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s {self.meal_type} on {self.date}"