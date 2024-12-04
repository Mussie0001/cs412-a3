from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Profile, Recipe, MealPlan, Category
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(TemplateView):
    """
    Displays the homepage with login, profile creation, or logout options.
    Redirects authenticated users to the recipes list.
    """
    template_name = "project/home.html"
    extra_context = {'hide_navbar': True}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('recipe_list')  # Redirect logged-in users to recipes page
        return super().dispatch(request, *args, **kwargs)


class RecipeListView(ListView):
    model = Recipe
    template_name = 'project/recipe_list.html'
    context_object_name = 'recipes'


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'project/recipe_detail.html'
    context_object_name = 'recipe'



class MealPlanListView(LoginRequiredMixin, ListView):
    model = MealPlan
    template_name = 'project/mealplans.html'
    context_object_name = 'meal_plans'

    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user).select_related('recipe').order_by('-date')

class CategoryListView(ListView):
    model = Category
    template_name = 'project/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'project/category_detail.html'
    context_object_name = 'category'


class CustomLoginView(LoginView):
    template_name = 'project/login.html'
    extra_context = {'hide_navbar': True}

    def get_success_url(self):
        return reverse_lazy('recipe_list')

class CustomLogoutView(LogoutView):
    template_name = 'project/logout.html'
    extra_context = {'hide_navbar': True}


class ProfileCreateView(View):
    """
    Handles creating a new Django User along with a Profile.
    """
    template_name = 'project/create_profile.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Redirect authenticated users to a separate view for creating only a profile.
        """
        if request.user.is_authenticated:
            return redirect('profile_create_only')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_creation_form = UserCreationForm()
        profile_form = ProfileForm()
        return render(request, self.template_name, {
            'user_creation_form': user_creation_form,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):
        user_creation_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_creation_form.is_valid() and profile_form.is_valid():
            user = user_creation_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('recipe_list')

        return render(request, self.template_name, {
            'user_creation_form': user_creation_form,
            'profile_form': profile_form
        })


class ProfileOnlyCreateView(LoginRequiredMixin, CreateView):
    """
    View for logged-in users to create only a profile.
    """
    model = Profile
    form_class = ProfileForm
    template_name = "project/create_profile_only.html"

    def form_valid(self, form):
        form.instance.user = self.request.user  # Attach the logged-in user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'pk': self.request.user.user_profile.pk})

class ProfileDetailView(DetailView):
    model = Profile
    template_name = "project/profile_detail.html"
    context_object_name = "profile"