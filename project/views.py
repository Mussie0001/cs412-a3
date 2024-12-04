from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Profile, Recipe, Category, Comment, Favorite
from .forms import ProfileForm, CommentForm, RecipeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.db.models import Q



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

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        meal_type = self.request.GET.get('meal_type', '')
        max_preparation_time = self.request.GET.get('max_time', '')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )

        if meal_type:
            queryset = queryset.filter(meal_type=meal_type)

        if max_preparation_time:
            try:
                queryset = queryset.filter(preparation_time__lte=int(max_preparation_time))
            except ValueError:
                pass  
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the meal type choices to the template
        context['meal_type_choices'] = Recipe.MEAL_TYPE_CHOICES
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'project/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-timestamp')
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
            context['is_favorited'] = Favorite.objects.filter(user=self.request.user, recipe=self.object).exists()
        else:
            context['is_favorited'] = False
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('project_login')

        recipe = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.recipe = recipe
            comment.save()
            return redirect('recipe_detail', pk=recipe.pk)

        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)

class MyRecipesView(LoginRequiredMixin, TemplateView):
    template_name = 'project/my_recipes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get recipes created by the user
        context['created_recipes'] = Recipe.objects.filter(creator=self.request.user)
        # Get recipes favorited by the user (excluding their own created recipes)
        context['favorited_recipes'] = Recipe.objects.filter(
            favorited_by__user=self.request.user
        ).exclude(creator=self.request.user)
        return context
 
class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'project/recipe_create.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_recipes')


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'project/recipe_update.html'

    def test_func(self):
        """Ensure the user is the creator of the recipe."""
        recipe = self.get_object()
        return self.request.user == recipe.creator

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})



class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'project/recipe_delete.html'

    def test_func(self):
        return self.get_object().creator == self.request.user

    def get_success_url(self):
        return reverse_lazy('my_recipes')

class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)

        if not created:
            favorite.delete()
            is_favorited = False
        else:
            is_favorited = True

        return JsonResponse({"success": True, "is_favorited": is_favorited})


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

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'project/comment_edit.html'

    def test_func(self):
        """Ensure the user is the owner of the comment."""
        comment = self.get_object()
        return self.request.user == comment.user

    def get_success_url(self):
        """Redirect back to the recipe detail page after editing."""
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.recipe.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'project/comment_delete.html'

    def test_func(self):
        """Ensure the user is the owner of the comment."""
        comment = self.get_object()
        return self.request.user == comment.user

    def get_success_url(self):
        """Redirect back to the recipe detail page after deletion."""
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.recipe.pk})