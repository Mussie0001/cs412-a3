from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient, Category, MealPlan, Profile

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(Category)
admin.site.register(MealPlan)
admin.site.register(Profile)