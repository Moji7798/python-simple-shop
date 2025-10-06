from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .mixins import AdminRequiredMixin
from .models import Category, Product


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = "products"
    paginate_by = 12
    template_name = "products/product_list.html"

    def get_queryset(self):
        qs = Product.objects.filter(stock__gt=0).prefetch_related("categories")
        q = self.request.GET.get("q")
        cat = self.request.GET.get("category")
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        if cat:
            qs = qs.filter(categories__slug=cat)
        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        ctx["q"] = self.request.GET.get("q", "")
        ctx["current_category"] = self.request.GET.get("category", "")
        return ctx


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"


class ProductAdminListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    template_name = "products/admin_list.html"
    model = Product
    context_object_name = "products"
    paginate_by = 20


class ProductCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Product
    fields = ["name", "description", "price", "image", "stock", "categories"]
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:admin_index")


class ProductUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Product
    fields = ["name", "description", "price", "image", "stock", "categories"]
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:admin_index")


class ProductDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("products:admin_index")
