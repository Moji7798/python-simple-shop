from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("admin-panel/", views.ProductAdminListView.as_view(), name="admin_index"),
    path(
        "admin-panel/create/", views.ProductCreateView.as_view(), name="product_create"
    ),
    path(
        "admin-panel/<int:pk>/edit/",
        views.ProductUpdateView.as_view(),
        name="product_edit",
    ),
    path(
        "admin-panel/<int:pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
]
