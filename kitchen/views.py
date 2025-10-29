from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from kitchen.models import Dish, Ingredient, DishType

@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_dishes = Dish.objects.count()
    num_ingredients = Ingredient.objects.count()
    num_dish_types = DishType.objects.count()
    num_cooks = get_user_model().objects.count()
    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits

    return render(
        request=request,
        template_name="kitchen/index.html",
        context = {
            "num_dishes": num_dishes,
            "num_ingredients": num_ingredients,
            "num_dish_types": num_dish_types,
            "num_cooks": num_cooks,
            "num_visits": num_visits
        }
    )


def dish_toggle_button(request: HttpRequest, pk: int) -> HttpResponse:
    dish = Dish.objects.get(pk=pk)
    user = request.user

    if dish in user.dishes.all():
        user.dishes.remove(dish)
    else:
        user.dishes.add(dish)

    return HttpResponseRedirect(
        reverse(
            "kitchen:dish-detail",
            kwargs={"pk": dish.pk}
        )
    )


class DishListView(generic.ListView):
    model = Dish
    paginate_by = 15


class DishDetailView(generic.DetailView):
    model = Dish


class DishCreateView(generic.CreateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(generic.UpdateView):
    model = Dish
    fields = "__all__"

    def get_success_url(self):
        return reverse(
            "kitchen:dish-detail",
            kwargs={"pk": self.object.pk}
        )


class DishDeleteView(generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class IngredientListView(generic.ListView):
    model = Ingredient
    paginate_by = 10


class IngredientCreateView(generic.CreateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientUpdateView(generic.UpdateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientDeleteView(generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")


class DishTypeListView(generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 21


class DishTypeCreateView(generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDeleteView(generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")
    context_object_name = "dish_type"


class DishTypeDetailView(generic.DetailView):
    model = DishType
    context_object_name = "dish_type"
    template_name = "kitchen/dish_type detail.html"
