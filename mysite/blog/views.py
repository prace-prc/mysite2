from django.core import paginator
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.shortcuts import render
from django.views.decorators.http import require_POST
from taggit.models import Tag

from .forms import EmailPostForm, CommentModelForm
from .models import Post


# Create your views here.
def post_list(request, tag_slug=None):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    page = request.GET.get('page')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 3)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)

    return render(request, 'blog/post/list.html',
                  {'posts': posts,
                   'page_obj': page_obj,
                   'paginator': paginator})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentModelForm(data=request.POST)
    comments = post.comments.filter(active=True)
    return render(request, 'blog/post/detail.html', {'post': post, 'form': form, 'comments': comments})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{data['sender']} has recommended {post.title}"
            message = f"hello {post_url}"
            send_mail(subject, message, [data['email']], [data['to']])
            sent = True
    else:
        form = EmailPostForm()
    comments = post.comments.filter(active=True)
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent, 'comments': comments})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    form = CommentModelForm(request.POST)
    comment = None
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(post)

    return render(request, 'blog/post/detail.html', {'post': post, 'form': form})
