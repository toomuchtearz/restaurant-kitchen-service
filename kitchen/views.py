from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from kitchen.forms import (
    CookCreationForm,
    CookUpdateForm,
    DishSearchForm,
    DishTypeSearchForm,
    CookSearchForm,
    CookPasswordResetForm,
    SuggestionForm,
    SuggestionSearchForm, DishForm,
)
from kitchen.models import (
    Dish,
    Ingredient,
    DishType,
    Suggestion
)


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
        context={
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
            name = name.strip()
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(
        self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={
                "name": name.strip()
            }
        )

        return context


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    queryset = Dish.objects.prefetch_related("ingredients", "cooks")


class DishCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView
):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")

    def test_func(self):
        return self.request.user.is_staff


class DishUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Dish
    form_class = DishForm

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse(
            "kitchen:dish-detail",
            kwargs={"pk": self.object.pk}
        )


class DishDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")

    def test_func(self):
        return self.request.user.is_staff


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    paginate_by = 15

    def get_queryset(self):
        queryset = Ingredient.objects.annotate(
            num_dishes=Count("dishes")
        )
        name = self.request.GET.get("name")
        if name:
            name = name.strip()
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={
                "name": name.strip()
            }
        )

        return context


class IngredientCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView,
):

    def test_func(self):
        return self.request.user.is_staff

    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")

    def test_func(self):
        return self.request.user.is_staff


class IngredientDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView,

):

    def test_func(self):
        return self.request.user.is_staff

    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 21

    def get_queryset(self):
        queryset = DishType.objects.annotate(
            num_dishes=Count("dishes")
        )
        name = self.request.GET.get("name")
        if name:
            name = name.strip()
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(
            initial={
                "name": name.strip()
            }
        )

        return context


class DishTypeCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView
):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")

    def test_func(self):
        return self.request.user.is_staff


class DishTypeUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")

    def test_func(self):
        return self.request.user.is_staff


class DishTypeDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")
    context_object_name = "dish_type"

    def test_func(self):
        return self.request.user.is_staff


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    context_object_name = "dish_type"
    template_name = "kitchen/dish_type detail.html"


class CookListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5

    def get_queryset(self):
        queryset = get_user_model().objects.annotate(
            num_dishes=Count("dishes")
        )

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
        self, *, object_list=..., **kwargs
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


class CookCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView
):
    model = get_user_model()
    form_class = CookCreationForm
    success_url = reverse_lazy("kitchen:cook-list")

    def test_func(self):
        return self.request.user.is_staff


class CookUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = get_user_model()
    form_class = CookUpdateForm

    def test_func(self):
        self.object = self.get_object()
        return (
            self.request.user.is_staff
            or self.request.user.pk == self.object.pk
        )

    def get_success_url(self):
        return reverse(
            "kitchen:cook-detail",
            kwargs={"pk": self.object.pk}
        )


class CookPasswordResetView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = get_user_model()
    form_class = CookPasswordResetForm
    template_name = "kitchen/cook_password_reset_form.html"

    def test_func(self):
        self.object = self.get_object()
        return (
            self.request.user.is_staff
            or self.request.user.pk == self.object.pk
        )

    def get_success_url(self):
        return reverse(
            "kitchen:cook-detail",
            kwargs={"pk": self.object.pk}
        )


class CookDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = get_user_model()
    success_url = reverse_lazy("kitchen:cook-list")

    def test_func(self):
        self.object = self.get_object()
        return (
            self.request.user.is_staff
            or self.request.user.pk == self.object.pk
        )


class SuggestionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Suggestion
    form_class = SuggestionForm
    template_name = "kitchen/suggestion_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dish"] = Dish.objects.get(pk=self.kwargs["dish_id"])

        return context

    def form_valid(self, form):
        form.instance.cook = self.request.user
        form.instance.dish_id = self.kwargs["dish_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "kitchen:dish-detail",
            kwargs={"pk": self.kwargs["dish_id"]}
        )


class SuggestionListView(LoginRequiredMixin, generic.ListView):
    model = Suggestion
    paginate_by = 9

    def get_queryset(self):
        queryset = Suggestion.objects.select_related(
            "dish", "cook"
        )
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                cook=self.request.user
            )

        dish_name = self.request.GET.get("dish_name")
        if dish_name:
            dish_name = dish_name.strip()
            queryset = queryset.filter(
                dish__name__icontains=dish_name
            )

        return queryset

    def get_context_data(
        self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        dish_name = self.request.GET.get("dish_name", "")
        context["search_form"] = SuggestionSearchForm(
            initial={
                "dish_name": dish_name.strip()
            }
        )
        return context


class SuggestionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Suggestion


def suggestion_approve_view(request: HttpRequest, pk: int) -> HttpResponse:
    suggestion = Suggestion.objects.get(pk=pk)
    suggestion.approved = True
    suggestion.save()

    return HttpResponseRedirect(
        reverse(
            "kitchen:suggestion-detail",
            kwargs={"pk": suggestion.pk}
        )
    )
