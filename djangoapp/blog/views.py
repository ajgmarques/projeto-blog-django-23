from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView  # class based view
from blog.models import Post, Page

# posts = list(range(1000))  # para testar - ELIMINAR

PER_PAGE = 9  # variável para definir quantos posts por página no paginator

posts = Post.objects.get_published()  # type: ignore


class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Home - '
            }
        )
        return context


def page(request, slug):

    page_obj = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first()
    )

    if page_obj is None:
        raise Http404

    page_title = f'{page_obj.title} - Página - '

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }
    )


def post(request, slug):
    post_obj = (
        Post.objects.get_published().filter(slug=slug).first()
    )
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if post_obj is None:
        raise Http404

    page_title = f'{post_obj.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}
    # # VER A ORDEM EM QUE OS MÉTODOS SÃO EXECUTADOS:

    # def setup(self, *args, **kwargs):
    #     super_setup = super().setup(*args, **kwargs)
    #     print('Método setup')
    #     return super_setup


    # def dispatch(self, *args, **kwargs):
    #     super_dispatch = super().dispatch(*args, **kwargs)
    #     print('Método dispatch')
    #     return super_dispatch


    # def get(self, *args, **kwargs):
    #     super_get = super().get(*args, **kwargs)
    #     print('Método get')
    #     return super_get


    # def get_queryset(self, *args, **kwargs):
    #     super_get_queryset = super().get_queryset(*args, **kwargs)
    #     print('Método get_queryset')
    #     return super_get_queryset


    # def get_context_data(self, *args, **kwargs):
    #         super_get_context_data = super().get_context_data(*args, **kwargs)
    #         print('Método get_context_data')
    #         return super_get_context_data


    # def get_context_object_name(self, *args, **kwargs):
    #         super_get_context_object_name = super().get_context_object_name(*args, **kwargs)
    #         print('Método get_context_object_name')
    #         return super_get_context_object_name


    # def get_template_names(self, *args, **kwargs):
    #         super_get_template_names = super().get_template_names(*args, **kwargs)
    #         print('Método get_template_names')
    #         return super_get_template_names


    # def render_to_response(self, *args, **kwargs):
    #         super_render_to_response = super().render_to_response(*args, **kwargs)
    #         print('Método render_to_response')
    #         return super_render_to_response


    # def http_method_not_allowed(self, *args, **kwargs):
    #         super_http_method_not_allowed = super().http_method_not_allowed(*args, **kwargs)
    #         print('Método http_method_not_allowed')
    #         return super_http_method_not_allowed

    # Ordem dos métodos que é executada:
    # Método setup
    # Método get_queryset
    # Método get_context_object_name
    # Método get_context_data
    # Método get_template_names
    # Método render_to_response
    # Método get
    # Método dispatch


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Posts de ' + user_full_name + ' - '

        ctx.update({
            'page_title': page_title,
        })
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        query_set = super().get_queryset()
        query_set = query_set.filter(
            created_by__pk=self._temp_context['user'].pk
        )
        return query_set

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


# def created_by(request, author_pk):
#     user = User.objects.filter(pk=author_pk).first()

#     if user is None:
#         raise Http404()

#     posts = Post.objects.get_published().filter(created_by__pk=author_pk)
#     user_full_name = user.username
#     if user.first_name:
#         user_full_name = f'{user.first_name} {user.last_name}'
#     page_title = 'Posts de ' + user_full_name + ' - '

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )


def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404

    page_title = f'Categoria - {page_obj[0].category.name} - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404

    page_title = f'Tag - {page_obj[0].tags.first().name} - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def search(request):
    search_value = request.GET.get('search', '').strip()

    posts = (
        Post.objects.get_published().filter(

            # title -> contém search value OU
            Q(title__contains=search_value) |
            # excerpt -> contém search value OU
            Q(excerpt__contains=search_value) |
            # content -> conteém search value
            Q(content__contains=search_value)
        )[:PER_PAGE]
    )

    page_title = f'{search_value[:10]} - Search - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
        }
    )
