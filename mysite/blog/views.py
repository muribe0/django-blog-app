from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def post_list(request):
    post_list = Post.published.all()
    # Pagination with 2 posts per page
    paginator = Paginator(post_list, 2)

    # if there is not a page parameter, display the page 1
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # if the page number is out of range
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # if the page number is not an integer
        posts = paginator.page(1)

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
