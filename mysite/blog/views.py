from django.core import paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.shortcuts import render
from .models import Post


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    page = request.GET.get('page')

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
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    title = post.title
    body = post.body

    return render(request, 'blog/post/share.html', {'title': title, 'body': body})


