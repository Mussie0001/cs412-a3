from django.urls import path
from .views import (
    RecipeListView,
    RecipeDetailView,
    MealPlanListView,
    CategoryListView,
    CategoryDetailView,
)

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('mealplans/', MealPlanListView.as_view(), name='mealplan_list'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
]
