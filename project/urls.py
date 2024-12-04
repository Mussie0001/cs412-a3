from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    HomePageView,
    RecipeListView,
    RecipeDetailView,
    MealPlanListView,
    CategoryListView,
    CategoryDetailView,
    CustomLoginView,
    ProfileCreateView,
    ProfileDetailView,
    ProfileOnlyCreateView,
    CustomLogoutView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('recipes/', RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('mealplans/', MealPlanListView.as_view(), name='mealplan_list'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('profile/create/', ProfileCreateView.as_view(), name='profile_create'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('login/', CustomLoginView.as_view(), name='project_login'),
    path('logout/', CustomLogoutView.as_view(), name='project_logout'),
    path('profile/create-only/', ProfileOnlyCreateView.as_view(), name='profile_create_only'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]



