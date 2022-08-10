from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User

POSTS_PER_PAGE = settings.POSTS_PER_PAGE


def get_page_context(queryset, request):
    paginator = Paginator(queryset, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj,
    }


def index(request):
    context = get_page_context(Post.objects.all(), request)
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    context = {
        'group': group,
    }
    context.update(get_page_context(posts, request))
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    counter = posts.count()
    context = {
        'counter': counter,
        'author': author,
    }
    context.update(get_page_context(posts, request))
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    counter = Post.objects.filter(author=post.author).count()
    context = {
        'post': post,
        'counter': counter,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required(login_url="user:login")
def post_create(request):
    form = PostForm(request.POST or None)

    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('posts:profile', request.user.username)

    return render(request, 'posts/create_post.html', {'form': form})


@login_required(login_url="user:login")
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    form = PostForm(request.POST or None, instance=post)

    if post.author != request.user:
        return redirect('posts:post_detail', post.id)

    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post.id)

    return render(
        request,
        'posts/create_post.html',
        {'form': form, 'is_edit': is_edit}
    )
