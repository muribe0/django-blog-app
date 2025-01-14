from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

from django.views.decorators.http import require_POST

from taggit.models import Tag

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment


# Create your views here.

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    post_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag]) # find posts with the tag or including the tag

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
            {'posts': posts,
             'tag': tag}
            )

def post_detail(request, slug):
    try:
        post = Post.published.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("No post found")

    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
            'post': post,
            'comments': comments,
            'form': form
            }
    return render(
            request,
            'blog/post/detail.html',
            context
            )


def post_detail_alt(request, slug):
    post = get_object_or_404( Post, id=id,
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

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # create a Comment object but don't save it to the database yet
        comment = form.save(commit=False)
        comment.post = post
        # save the comment to the database
        comment.save()
    context = {
            'post': post,
            'form': form,
            'comment': comment
            }
    return render(request, 'blog/post/comment.html', context)


