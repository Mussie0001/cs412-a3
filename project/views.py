from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe, Ingredient, Category, MealPlan
# Create your views here.
class RecipeListView(ListView):
    model = Recipe
    template_name = 'project/recipe_list.html'
    context_object_name = 'recipes'


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'project/recipe_detail.html'
    context_object_name = 'recipe'


class MealPlanListView(ListView):
    model = MealPlan
    template_name = 'project/mealplans.html'
    context_object_name = 'meal_plans'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meal_plans = MealPlan.objects.all().select_related('recipe', 'user')
        meal_plans_by_date = {}
        for plan in meal_plans:
            meal_plans_by_date.setdefault(plan.date, []).append(plan)
        context['meal_plans_by_date'] = meal_plans_by_date
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'project/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'project/category_detail.html'
    context_object_name = 'category'
