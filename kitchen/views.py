from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from kitchen.forms import CookCreationForm, CookUpdateForm, DishSearchForm, CookSearchForm, DishTypeSearchForm
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

@login_required
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


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 15

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type").prefetch_related(
            "ingredients", "cooks"
        )
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={
                "name": name
            }
        )

        return context


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    fields = "__all__"

    def get_success_url(self):
        return reverse(
            "kitchen:dish-detail",
            kwargs={"pk": self.object.pk}
        )


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    paginate_by = 15

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={
                "name": name
            }
        )

        return context


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 21

    def get_queryset(self):
        queryset = DishType.objects.all()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(
            initial={
                "name": name
            }
        )

        return context


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")
    context_object_name = "dish_type"


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    context_object_name = "dish_type"
    template_name = "kitchen/dish_type detail.html"


class CookListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5

    def get_queryset(self):
        queryset = get_user_model().objects.all()

        username = self.request.GET.get("username")
        if username:
            username = username.strip()
            queryset = queryset.filter(
                Q(username__icontains=username)
                | Q(first_name__icontains=username)
                | Q(last_name__icontains=username)
            )

        return queryset

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(
            initial={
                "username": username.strip()
            }
        )
        return context


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.prefetch_related("dishes__dish_type")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = CookCreationForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = CookUpdateForm

    def get_success_url(self):
        return reverse(
            "kitchen:cook-detail",
            kwargs={"pk": self.object.pk}
        )


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("kitchen:cook-list")
