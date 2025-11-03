from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import CheckboxSelectMultiple

from kitchen.models import Suggestion, Dish, Ingredient


class CookCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "is_staff",
            "email",
            "years_of_experience",
        )


class CookUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience"
        )


class CookPasswordResetForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ()


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ("text",)


class DishForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.SelectMultiple(attrs={"id": "id_ingredients"}),
        required=False,
    )

    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.SelectMultiple(attrs={"id": "id_cooks"}),
        required=False,
    )

    class Meta:
        model = Dish
        fields = "__all__"

class CookSearchForm(forms.Form):
    username = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username or name"
            }
        )
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by dish name"
            }
        )
    )


class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by ingredient name"
            }
        )
    )


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by DishType name"
            }
        )
    )


class SuggestionSearchForm(forms.Form):
    dish_name = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by dish name"
            }
        )
    )
