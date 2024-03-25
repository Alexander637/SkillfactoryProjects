from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, PostCategory
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from .tasks import send_on_monday, send_every_morning


class FilteredListView(LoginRequiredMixin, ListView):
    raise_exception = True
    paginate_by = 10
    filter_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filter_class(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostList(FilteredListView):
    model = Post
    queryset = Post.objects.order_by('-dateCreation')
    filter_class = PostFilter
    template_name = 'posts.html'
    context_object_name = 'posts'


class NewsList(FilteredListView):
    model = Post
    queryset = Post.objects.filter(categoryType="NW").order_by('-dateCreation')
    filter_class = PostFilter
    template_name = 'news.html'
    context_object_name = 'news'


class ArticlesList(FilteredListView):
    model = Post
    queryset = Post.objects.filter(categoryType="AR").order_by('-dateCreation')
    filter_class = PostFilter
    template_name = 'articles.html'
    context_object_name = 'articles'


class CategoryList(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateCreation')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['category'] = self.postCategory

        return context


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostTypeMixin(LoginRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_path = self.request.path
        category_label = 'News' if 'news' in url_path else 'Article'

        if 'create' in url_path:
            context['post_type'] = f'Create {category_label}'
        elif 'edit' in url_path:
            context['post_type'] = f'Edit {category_label}'

        return context

    def form_invalid(self, form):
        errors = form.errors

        for field in errors:
            if 'Ensure this value has at most' in str(errors[field]):
                value = form[field].value()
                truncated_value = value[:128]
                form.add_error(field, f'Сократите до: {truncated_value}')

        return super().form_invalid(form)


class PostCreate(PostTypeMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'

    def form_valid(self, form):
        url_path = self.request.path
        post = form.save(commit=False)

        if 'articles' in url_path:
            post.categoryType = 'AR'
        elif 'news' in url_path:
            post.categoryType = 'NW'
        post.author_id = form.cleaned_data['author'].id
        category = form.cleaned_data['category']
        post_category = PostCategory(postThrough=post, categoryThrough=category)

        if form.is_valid():
            post.save()
            post_category.save()

        return super().form_valid(form)


class PostUpdate(PostTypeMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author_id = form.cleaned_data['author'].id
        post.save()
        return super().form_valid(form)


class PostDelete(PostTypeMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'post_confirm_delete.html'
    permission_required = 'news.delete_post'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_path = self.request.path

        if 'news' in url_path:
            context['delete_message'] = 'Are you sure you want to delete this news?'
        elif 'articles' in url_path:
            context['delete_message'] = 'Are you sure you want to delete this article?'

        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы подписались на расссылку новостей категории'

    return render(request, 'subscribe.html', {'category': category, 'message': message})
