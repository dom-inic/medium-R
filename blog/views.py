from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views import generic
from . models import Post
# Create your views here.

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts per page
    page = request.Get.get('page')
    try:
        posts = paginator(page)
    except PageNotAnInteger:
        #if page not an interger deliver the first page
        posts = paginator(1)
    except EmptyPage:
        # if page out of range deliver last page
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/post_list.html', {'page': page,'posts': posts})

class PostList(generic.ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/post_list.html'

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    return render(request, 'blog/post/post_detail.html', {'post': post})

