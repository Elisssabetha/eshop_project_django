from django.urls import path

from catalog.views import ProductListView, ContactView, ProductDetailView, ProductUpdateView, BlogCreateView, \
    BlogUpdateView, BlogDetailView, BlogListView, BlogDeleteView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_view'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('create_blog/', BlogCreateView.as_view(), name='create_blog'),
    path('edit_blog/<slug:slug>/', BlogUpdateView.as_view(), name='edit_blog'),
    path('view_blog/<slug:slug>/', BlogDetailView.as_view(), name='view_blog'),
    path('list_blog/', BlogListView.as_view(), name='list_blog'),
    path('delete_blog/<slug:slug>/', BlogDeleteView.as_view(), name='delete_blog'),

]
