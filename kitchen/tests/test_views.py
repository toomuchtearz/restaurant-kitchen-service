from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Ingredient, Dish, Suggestion
from kitchen.forms import (
    DishTypeSearchForm,
    DishSearchForm,
    CookSearchForm,
    SuggestionSearchForm,
)


class BaseViewTest(TestCase):
    """Reusable setup for all view tests"""

    @classmethod
    def setUpTestData(cls):
        cls.staff_user = get_user_model().objects.create_user(
            username="staff",
            password="pass",
            years_of_experience=5,
            is_staff=True,
        )
        cls.normal_user = get_user_model().objects.create_user(
            username="normal",
            password="pass",
            years_of_experience=2,
        )
        cls.dish_type = DishType.objects.create(name="Test Type")
        cls.ingredient = Ingredient.objects.create(name="Tomato")
        cls.dish = Dish.objects.create(
            name="Pizza",
            description="Cheese pizza",
            price=12.5,
            dish_type=cls.dish_type,
        )
        cls.dish.ingredients.add(cls.ingredient)
        cls.suggestion = Suggestion.objects.create(
            cook=cls.normal_user,
            dish=cls.dish,
            text="Try adding basil!"
        )


class IndexViewTests(BaseViewTest):
    def test_index_requires_login(self):
        response = self.client.get(reverse("kitchen:index"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('kitchen:index')}"
        )

    def test_index_logged_in_displays_counts_and_visits(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse("kitchen:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("num_visits", response.context)
        self.assertEqual(response.context["num_dishes"], 1)
        self.assertEqual(response.context["num_ingredients"], 1)
        self.assertEqual(response.context["num_dish_types"], 1)
        self.assertEqual(response.context["num_cooks"], 2)


class DishToggleButtonTests(BaseViewTest):
    def test_toggle_add_and_remove_dish(self):
        self.client.force_login(self.normal_user)
        url = reverse("kitchen:dish-toggle-button", args=[self.dish.pk])

        self.client.get(url)
        self.normal_user.refresh_from_db()
        self.assertIn(self.dish, self.normal_user.dishes.all())

        self.client.get(url)
        self.normal_user.refresh_from_db()
        self.assertNotIn(self.dish, self.normal_user.dishes.all())


class DishViewTests(BaseViewTest):
    def test_dish_list_filters_by_name(self):
        self.client.force_login(self.normal_user)
        url = f"{reverse('kitchen:dish-list')}?name=piz"
        response = self.client.get(url)
        self.assertContains(response, "Pizza")
        self.assertIsInstance(response.context["search_form"], DishSearchForm)
        self.assertEqual(
            response.context["search_form"].initial["name"],
            "piz"
        )

    def test_dish_detail_view_prefetches_related(self):
        self.client.force_login(self.normal_user)
        url = reverse("kitchen:dish-detail", args=[self.dish.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "ingredients",
            response.context["dish"]._prefetched_objects_cache
        )


class IngredientViewTests(BaseViewTest):
    def test_ingredient_list_search_and_form(self):
        self.client.force_login(self.normal_user)
        Ingredient.objects.create(name="Cheese")

        url = f"{reverse('kitchen:ingredient-list')}?name=tom"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tomato")
        self.assertNotContains(response, "Cheese")
        form = response.context["search_form"]
        self.assertIsInstance(form, DishSearchForm)
        self.assertEqual(form.initial["name"], "tom")

    def test_staff_can_create_update_delete(self):
        self.client.force_login(self.staff_user)
        urls = [
            reverse("kitchen:ingredient-create"),
            reverse("kitchen:ingredient-update", args=[self.ingredient.pk]),
            reverse("kitchen:ingredient-delete", args=[self.ingredient.pk]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_non_staff_cannot_access_create_update_delete(self):
        self.client.force_login(self.normal_user)
        urls = [
            reverse("kitchen:ingredient-create"),
            reverse("kitchen:ingredient-update", args=[self.ingredient.pk]),
            reverse("kitchen:ingredient-delete", args=[self.ingredient.pk]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)


class DishTypeViewTests(BaseViewTest):
    def test_dish_type_list_search_and_form(self):
        self.client.force_login(self.normal_user)
        DishType.objects.create(name="Another Type")
        url = f"{reverse('kitchen:dish-type-list')}?name=test"
        response = self.client.get(url)
        dish_types = response.context["dish_type_list"]
        self.assertEqual(dish_types.count(), 1)
        self.assertContains(response, "Test Type")
        self.assertNotContains(response, "Another Type")
        form = response.context["search_form"]
        self.assertIsInstance(form, DishTypeSearchForm)
        self.assertEqual(form.initial["name"], "test")

    def test_dish_type_detail_view(self):
        self.client.force_login(self.normal_user)
        url = reverse("kitchen:dish-type-detail", args=[self.dish_type.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dish_type.name)

    def test_staff_can_access_crud_views(self):
        self.client.force_login(self.staff_user)
        urls = [
            reverse("kitchen:dish-type-create"),
            reverse("kitchen:dish-type-update", args=[self.dish_type.pk]),
            reverse("kitchen:dish-type-delete", args=[self.dish_type.pk]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)


class CookViewTests(BaseViewTest):
    def test_cook_list_search_and_form(self):
        self.client.force_login(self.staff_user)
        url = f"{reverse('kitchen:cook-list')}?username=normal"
        response = self.client.get(url)
        self.assertContains(response, "normal")
        form = response.context["search_form"]
        self.assertIsInstance(form, CookSearchForm)
        self.assertEqual(form.initial["username"], "normal")

    def test_cook_detail_prefetches_dishes(self):
        self.client.force_login(self.normal_user)
        url = reverse("kitchen:cook-detail", args=[self.normal_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "dishes",
            response.context["object"]._prefetched_objects_cache
        )

    def test_user_can_update_own_profile(self):
        self.client.force_login(self.normal_user)
        url = reverse("kitchen:cook-update", args=[self.normal_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_update_others_profile(self):
        self.client.force_login(self.normal_user)
        url = reverse("kitchen:cook-update", args=[self.staff_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_cook_password_reset_and_delete_own(self):
        self.client.force_login(self.normal_user)
        reset_url = reverse(
            "kitchen:cook-password-reset",
            args=[self.normal_user.pk]
        )
        delete_url = reverse("kitchen:cook-delete", args=[self.normal_user.pk])
        self.assertEqual(self.client.get(reset_url).status_code, 200)
        self.assertEqual(self.client.post(delete_url).status_code, 302)


class SuggestionViewTests(BaseViewTest):
    def test_create_suggestion_assigns_cook_and_dish(self):
        self.client.force_login(self.normal_user)
        url = reverse("kitchen:suggestion-create", args=[self.dish.pk])
        data = {"text": "New suggestion!"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Suggestion.objects.filter(text="New suggestion!").exists()
        )

    def test_suggestion_list_for_staff_and_normal_user(self):
        # staff sees all
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("kitchen:suggestion-list"))
        self.assertContains(response, "Try adding basil!")
        self.client.logout()

        # normal sees only own
        other = get_user_model().objects.create_user(
            username="another",
            password="pass",
            years_of_experience=1
        )
        Suggestion.objects.create(cook=other, dish=self.dish, text="Other one")
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse("kitchen:suggestion-list"))
        self.assertContains(response, "Try adding basil!")
        self.assertNotContains(response, "Other one")

        # test search form
        url = f"{reverse('kitchen:suggestion-list')}?dish_name=pizza"
        response = self.client.get(url)
        form = response.context["search_form"]
        self.assertIsInstance(form, SuggestionSearchForm)
        self.assertEqual(form.initial["dish_name"], "pizza")

    def test_suggestion_detail_and_approve(self):
        self.client.force_login(self.staff_user)
        detail_url = reverse(
            "kitchen:suggestion-detail",
            args=[self.suggestion.pk]
        )
        approve_url = reverse(
            "kitchen:suggestion-approve",
            args=[self.suggestion.pk]
        )
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.client.get(approve_url)
        self.suggestion.refresh_from_db()
        self.assertTrue(self.suggestion.approved)
