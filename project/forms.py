from django import forms
from .models import Profile, Comment, Recipe, RecipeIngredient, Ingredient, Category

class ProfileForm(forms.ModelForm):
    """
    Form for creating or updating a Profile.
    """
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'profile_picture_url'] 


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }

class RecipeForm(forms.ModelForm):
    ingredients = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text="List ingredients separated by commas (e.g., 'Oats, Almond Butter, Honey')."
    )
    quantities = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text="List quantities corresponding to ingredients (e.g., '1 cup, 1/2 cup, 1/4 cup')."
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_time', 'instructions', 'image', 'meal_type', 'ingredients', 'quantities', 'categories']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            recipe_ingredients = instance.recipe_ingredients.all()
            ingredients = [ri.ingredient.name for ri in recipe_ingredients]
            quantities = [ri.quantity for ri in recipe_ingredients]

            initial = kwargs.get('initial', {})
            initial['ingredients'] = ', '.join(ingredients)
            initial['quantities'] = ', '.join(quantities)
            initial['categories'] = instance.categories.all()
            kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        recipe = super().save(commit=False)
        ingredients = self.cleaned_data.get('ingredients', '').split(',')
        quantities = self.cleaned_data.get('quantities', '').split(',')

        if commit:
            recipe.save()

            recipe.recipe_ingredients.all().delete()

            for ingredient_name, quantity in zip(ingredients, quantities):
                ingredient_name = ingredient_name.strip()
                quantity = quantity.strip()

                if ingredient_name and quantity:
                    ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, quantity=quantity)

            recipe.categories.set(self.cleaned_data.get('categories', []))

        return recipe