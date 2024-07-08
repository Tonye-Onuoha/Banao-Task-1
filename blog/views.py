from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import PostModelForm
from .models import Post, Category
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.
@login_required
def post_create(request):
    """This view is used to create a new post."""

    # raise an exception if the user is a patient.
    if request.user.identity != "DC":
        raise PermissionDenied

    if request.method == "POST":
        form = PostModelForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid() and request.user.identity == "DC":
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(reverse("post-detail", args=[str(post.id)]))
        else:
            raise PermissionDenied

    else:
        form = PostModelForm()

    context = {"form": form}
    return render(request, "post_new.html", context)


@login_required
def post_detail(request, pk):
    """This view returns the details of a particular post."""

    post = get_object_or_404(Post, pk=pk)

    # raise an exception if the user is a patient and post is marked as draft.
    if request.user.identity != "DC" and post.is_draft:
        raise PermissionDenied

    context = {"post": post}
    return render(request, "post_detail.html", context)


@login_required
def user_posts(request):
    """This view returns the posts of a particular user (A Doctor)."""

    user_posts = Post.objects.filter(user=request.user)
    context = {"user_posts": user_posts}

    # raise an exception if the user is a patient.
    if request.user.identity != "DC":
        raise PermissionDenied

    return render(request, "user_posts.html", context)


@login_required
def all_posts(request, pk):
    """This view filters posts by a category and returns them.
    If the current logged-in user is a Patient, it will not
    return posts that have been marked as drafts."""

    if request.user.identity == "DC":
        posts = Post.objects.filter(category=pk)
    else:
        posts = Post.objects.filter(category=pk, is_draft=False)

    if Post.objects.filter(category=pk).count() > 0:
        category = Post.objects.filter(category=pk).first().category
    else:
        category = None

    context = {"category": category, "posts": posts}
    return render(request, "posts.html", context)


@login_required
def posts_categories(request):
    """This view returns the categories of all posts."""

    posts_categories = Category.objects.all()
    context = {"posts_categories": posts_categories}
    return render(request, "posts_categories.html", context)
