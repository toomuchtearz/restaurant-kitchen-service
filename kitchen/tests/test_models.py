from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import DishType, Ingredient, Dish, Suggestion


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cook_data ={
            "username": "test_username",
            "password": "test_password",
            "years_of_experience": 1
        }
        cls.dish_type = DishType.objects.create(name="test type")
        cls.ingredient = Ingredient.objects.create(name="test ingredient")
        cls.cook = get_user_model().objects.create_user(
            username=cls.cook_data["username"],
            password=cls.cook_data["password"],
            years_of_experience=cls.cook_data["years_of_experience"]
        )
        cls.dish = Dish.objects.create(
            name="test_dish",
            description="some desc",
            price = 1,
            dish_type=cls.dish_type
        )
        cls.suggestion = Suggestion.objects.create(
            cook=cls.cook,
            dish=cls.dish,
            text="some text"
        )

    def test_str_dish_type_ingredient_dish(self):
        instances = (
            self.dish_type,
            self.ingredient,
            self.dish
        )
        for instance in instances:
            with self.subTest(model=instance.__class__.__name__):
                self.assertEqual(str(instance), instance.name)

    def test_suggestion_str(self):
        self.assertEqual(
            str(self.suggestion),
            f"Suggestion by {self.suggestion.cook.username} on {self.suggestion.dish.name}"
        )

    def test_create_author_with_years_of_experience(self):
        self.assertEqual(
            self.cook.username,
            self.cook_data["username"]
        )
        self.assertEqual(
            self.cook.years_of_experience,
            self.cook_data["years_of_experience"]
        )
        self.assertTrue(
            self.cook.check_password(self.cook_data["password"])
        )
