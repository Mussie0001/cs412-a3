from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from pytz import timezone as pytz_timezone
from django.urls import reverse


class Profile(models.Model):
    """
    Profile model to store user profile information.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the User model.
        first_name (CharField): The first name of the user, with a maximum length of 30 characters.
        last_name (CharField): The last name of the user, with a maximum length of 30 characters.
        bio (TextField): A brief biography of the user, which can be left blank.
        profile_picture_url (URLField): The URL of the user's profile picture, which can be left blank or null, with a maximum length of 500 characters.

    Methods:
        __str__(): Returns the full name of the user.
        get_absolute_url(): Returns the absolute URL for the profile detail view.
    """
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
    """
    Recipe model to store information about different recipes.

    Attributes:
        title (CharField): The title of the recipe, with a maximum length of 255 characters.
        description (TextField): A brief description of the recipe, can be left blank.
        preparation_time (PositiveIntegerField): The time required to prepare the recipe, in minutes.
        instructions (TextField): Detailed instructions on how to prepare the recipe.
        image (ImageField): An optional image of the prepared recipe, stored in the 'recipes/' directory.
        MEAL_TYPE_CHOICES (list): A list of tuples representing the meal type choices.
        meal_type (CharField): The type of meal, chosen from MEAL_TYPE_CHOICES.
        creator (ForeignKey): A reference to the User who created the recipe, can be null or blank.

    Methods:
        __str__(): Returns the title of the recipe as its string representation.
    """
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
    """
    Favorite model represents a user's favorite recipes.

    Attributes:
        user (ForeignKey): Reference to the User who favorited the recipe.
        recipe (ForeignKey): Reference to the Recipe that is favorited.
        timestamp (DateTimeField): The date and time when the recipe was favorited.

    Meta:
        unique_together (tuple): Ensures that a user cannot favorite the same recipe more than once.

    Methods:
        __str__(): Returns a string representation of the favorite instance, showing which user favorited which recipe.
    """
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
    """
    Model representing the relationship between a Recipe and an Ingredient, including the quantity of the ingredient used in the recipe.

    Attributes:
        recipe (ForeignKey): A foreign key to the Recipe model. When the referenced Recipe is deleted, this relationship is also deleted.
        ingredient (ForeignKey): A foreign key to the Ingredient model. When the referenced Ingredient is deleted, this relationship is also deleted.
        quantity (CharField): A string specifying the amount or measurement of the ingredient (e.g., '1 cup').

    Methods:
        __str__(): Returns a string representation of the RecipeIngredient instance, showing the quantity of the ingredient and the associated recipe title.
    """
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
    """
    Comment model representing a user's comment on a recipe.

    Attributes:
        recipe (ForeignKey): A foreign key to the Recipe model, indicating the recipe this comment is associated with.
        user (ForeignKey): A foreign key to the User model, indicating the user who made the comment.
        content (TextField): The text content of the comment.
        timestamp (DateTimeField): The date and time when the comment was created, automatically set to the current date and time.

    Methods:
        __str__(): Returns a string representation of the comment, including the username of the commenter and the timestamp in US Eastern time.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        est = pytz_timezone('US/Eastern')
        local_time = localtime(self.timestamp).astimezone(est)
        return f"Comment by {self.user.username} on {local_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"