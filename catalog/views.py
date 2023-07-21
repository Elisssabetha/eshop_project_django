from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, CreateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Blog


class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Главная'
    }


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'
    extra_context = {
        'title': 'Контакты'
    }

    def get_context_data(self, **kwargs):
        if self.request.method == 'POST':
            name = self.request.POST.get('name')
            email = self.request.POST.get('email')
            message = self.request.POST.get('message')
            print(f'You have new message from {name} ({email}): {message}')
        return super().get_context_data(**kwargs)


class ProductDetailView(DetailView):
    model = Product


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'description', 'preview', 'price')
    success_url = reverse_lazy('product_list')


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'image',)
    success_url = reverse_lazy('list_blog')  # куда редиректит - здесь переход к списку созданных

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'image', 'is_published')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_blog', args=[self.kwargs.get('slug')])


class BlogListView(ListView):
    model = Blog
    extra_context = {
        'title': 'Блог'
    }

    def get_queryset(self, *args, **kwargs):
        """Выводить только те, у которых положительный признак публикации"""
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        """  Увеличивает количество просмотров """

        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save(update_fields=['views_count'])
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('list_blog')

# def contacts(request):
#     context = {
#         'title': 'Контакты'
#     }
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')
#         print(f'You have new message from {name} ({email}): {message}')
#     return render(request, 'catalog/contacts.html', context)
