from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

def post_list(request):
    posts = Post.published.all()
    return render(
            request,
            'blog/post/list.html',
            {'posts': posts}
            )

def post_detail(request, slug):
    try:
        post = Post.published.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("No post found")
    return render(
            request,
            'blog/post/detail.html',
            {'post': post}
            )

def post_detail_alt(request, slug):
    post = get_object_or_404(
            Post,
            id=id,
            status=Post.Status.PUBLISHED,
            slug=slug)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post}
                  )
