from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.views import ProductListView, ContactView, ProductDetailView, ProductUpdateView, BlogCreateView, \
    BlogUpdateView, BlogDetailView, BlogListView, BlogDeleteView, ProductDeleteView, ProductCreateView, \
    CategoryListView, CategoryProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('create_product', never_cache(ProductCreateView.as_view()), name='product_create'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_view'),
    path('edit/<int:pk>/', never_cache(ProductUpdateView.as_view()), name='product_edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('<int:pk>/products/', CategoryProductListView.as_view(), name='category_products'),

    path('create_blog/', never_cache(BlogCreateView.as_view()), name='create_blog'),
    path('edit_blog/<slug:slug>/', never_cache(BlogUpdateView.as_view()), name='edit_blog'),
    path('view_blog/<slug:slug>/', BlogDetailView.as_view(), name='view_blog'),
    path('list_blog/', BlogListView.as_view(), name='list_blog'),
    path('delete_blog/<slug:slug>/', BlogDeleteView.as_view(), name='delete_blog')
]
