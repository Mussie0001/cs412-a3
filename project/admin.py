from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient, Category, Profile, Comment

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)