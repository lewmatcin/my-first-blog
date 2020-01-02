from django.http import HttpRequest, HttpResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)
from django.utils import timezone

from .forms import PostForm
from .models import Post


def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request=request,
                  template_name='blog/post_list.html',
                  context={'posts': posts})


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(klass=Post, pk=pk)

    return render(request=request,
                  template_name='blog/post_detail.html',
                  context={'post': post})


def post_new(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(to='post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request=request,
                  template_name='blog/post_edit.html',
                  context={'form': form})


def post_edit(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(klass=Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(to='post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request=request,
                  template_name='blog/post_edit.html',
                  context={'form': form})


def post_draft_list(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')

    return render(request=request,
                  template_name='blog/post_draft_list.html',
                  context={'posts': posts})


def post_publish(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(klass=Post, pk=pk)
    post.publish()

    return redirect(to='post_detail', pk=pk)
