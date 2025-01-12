from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm


# Create your views here.

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'


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

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data # cleaned data
            post_url = request.build_absolute_uri(
                    post.get_absolute_url()
                    )
            subject = f"{cd['name']} ({cd['email']}) recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"

            send_mail(
                    subject = subject,
                    message = message,
                    from_email = None,
                    recipient_list = [cd['to']]
                    )
            sent = True
    else:
        form = EmailPostForm()
    context = {
           'post': post,
           'form': form,
           'sent': sent
           }
    return render(request, 'blog/post/share.html', context)
