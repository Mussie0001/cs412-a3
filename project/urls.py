from django.urls import path
"""
URL configuration for the project.

This module defines the URL patterns for the Django project. It maps URL paths to their corresponding views.

Views:
    - HomePageView: Renders the home page.
    - RecipeListView: Displays a list of recipes.
    - RecipeDetailView: Displays details of a specific recipe.
    - CategoryListView: Displays a list of categories.
    - CategoryDetailView: Displays details of a specific category.
    - CustomLoginView: Handles user login.
    - ProfileCreateView: Allows users to create a profile.
    - ProfileDetailView: Displays details of a specific profile.
    - ProfileOnlyCreateView: Allows users to create a profile with limited access.
    - CustomLogoutView: Handles user logout.
    - CommentUpdateView: Allows users to edit a comment.
    - CommentDeleteView: Allows users to delete a comment.
    - RecipeCreateView: Allows users to create a new recipe.
    - MyRecipesView: Displays a list of recipes created by the logged-in user.
    - ToggleFavoriteView: Toggles the favorite status of a recipe.
    - RecipeUpdateView: Allows users to edit a recipe.
    - RecipeDeleteView: Allows users to delete a recipe.
    - ProfileUpdateView: Allows users to edit their profile.

URL Patterns:
    - '': Home page.
    - 'recipes/': List of recipes.
    - 'recipe/<int:pk>/': Recipe details.
    - 'categories/': List of categories.
    - 'category/<int:pk>/': Category details.
    - 'profile/create/': Create a profile.
    - 'profile/<int:pk>/': Profile details.
    - 'login/': User login.
    - 'logout/': User logout.
    - 'profile/create-only/': Create a profile with limited access.
    - 'comment/<int:pk>/edit/': Edit a comment.
    - 'comment/<int:pk>/delete/': Delete a comment.
    - 'my-recipes/': List of recipes created by the logged-in user.
    - 'recipe/<int:pk>/favorite/': Toggle favorite status of a recipe.
    - 'recipe/create/': Create a new recipe.
    - 'recipe/<int:pk>/edit/': Edit a recipe.
    - 'recipe/<int:pk>/delete/': Delete a recipe.
    - 'profile/edit/': Edit user profile.
"""
from .views import (
    HomePageView,
    RecipeListView,
    RecipeDetailView,
    CategoryListView,
    CategoryDetailView,
    CustomLoginView,
    ProfileCreateView,
    ProfileDetailView,
    ProfileOnlyCreateView,
    CustomLogoutView,
    CommentUpdateView,
    CommentDeleteView,
    RecipeCreateView,
    MyRecipesView,
    ToggleFavoriteView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    ProfileUpdateView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('recipes/', RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('profile/create/', ProfileCreateView.as_view(), name='profile_create'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('login/', CustomLoginView.as_view(), name='project_login'),
    path('logout/', CustomLogoutView.as_view(), name='project_logout'),
    path('profile/create-only/', ProfileOnlyCreateView.as_view(), name='profile_create_only'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('my-recipes/', MyRecipesView.as_view(), name='my_recipes'),
    path('recipe/<int:pk>/favorite/', ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('recipe/create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]