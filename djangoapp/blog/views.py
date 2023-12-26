from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post

# posts = list(range(1000))  # para testar - ELIMINAR

PER_PAGE = 9  # variável para definir quantos posts por página no paginator

posts = Post.objects.get_published()  # type: ignore

def index(request):

    # posts = Post.objects.get_published()  # type: ignore

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def page(request, slug):

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'blog/pages/page.html',
    )


def post(request, slug):
    post = (
        Post.objects.get_published().filter(slug=slug).first()
    )
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )


def created_by(request, author_pk):
    posts = Post.objects.get_published().filter(created_by__pk=author_pk)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )
