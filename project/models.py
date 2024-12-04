from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from pytz import timezone as pytz_timezone
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(blank=True, help_text="")
    profile_picture_url = models.URLField(max_length=500, blank=True, null=True, help_text="")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    preparation_time = models.PositiveIntegerField(help_text="(time in minutes)")
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    MEAL_TYPE_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    ]
    meal_type = models.CharField(max_length=50, choices=MEAL_TYPE_CHOICES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_recipes", null=True, blank=True)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favorited_by")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} favorited {self.recipe.title}"


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


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        est = pytz_timezone('US/Eastern')
        local_time = localtime(self.timestamp).astimezone(est)
        return f"Comment by {self.user.username} on {local_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"