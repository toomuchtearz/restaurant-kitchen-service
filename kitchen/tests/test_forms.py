from django.test import TestCase

from kitchen.forms import (
    CookCreationForm,
    CookUpdateForm,
    CookPasswordResetForm,
    SuggestionForm,
    CookSearchForm,
    DishSearchForm,
    IngredientSearchForm,
    DishTypeSearchForm,
    SuggestionSearchForm,
)


class CookCreationFormTests(TestCase):
    def test_form_includes_custom_fields(self):
        form = CookCreationForm()
        expected_fields = {
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "is_staff",
            "email",
            "years_of_experience",
        }
        self.assertTrue(expected_fields.issubset(form.fields.keys()))


class CookUpdateFormTests(TestCase):
    def test_form_contains_expected_fields_only(self):
        form = CookUpdateForm()
        self.assertEqual(
            list(form.fields.keys()),
            [
                "username",
                "first_name",
                "last_name",
                "email",
                "years_of_experience"
            ],
        )


class CookPasswordResetFormTests(TestCase):
    def test_form_has_password_fields(self):
        form = CookPasswordResetForm()
        self.assertEqual(
            list(form.fields.keys()),
            ["password1", "password2"]
        )


class SuggestionFormTests(TestCase):
    def test_form_uses_only_text_field(self):
        form = SuggestionForm()
        self.assertEqual(list(form.fields.keys()), ["text"])

    def test_form_is_valid_with_text(self):
        suggestion = SuggestionForm(data={"text": "Test suggestion"})
        self.assertTrue(suggestion.is_valid())


class SearchFormsTests(TestCase):
    def assertPlaceholder(self, form_field, expected_placeholder):
        self.assertIn("placeholder", form_field.widget.attrs)
        self.assertEqual(
            form_field.widget.attrs["placeholder"],
            expected_placeholder
        )

    def test_cook_search_form_placeholder(self):
        form = CookSearchForm()
        self.assertPlaceholder(
            form.fields["username"], "Search by username or name"
        )

    def test_dish_search_form_placeholder(self):
        form = DishSearchForm()
        self.assertPlaceholder(form.fields["name"], "Search by dish name")

    def test_ingredient_search_form_placeholder(self):
        form = IngredientSearchForm()
        self.assertPlaceholder(
            form.fields["name"],
            "Search by ingredient name"
        )

    def test_dishtype_search_form_placeholder(self):
        form = DishTypeSearchForm()
        self.assertPlaceholder(form.fields["name"], "Search by DishType name")

    def test_suggestion_search_form_placeholder(self):
        form = SuggestionSearchForm()
        self.assertPlaceholder(form.fields["dish_name"], "Search by dish name")
