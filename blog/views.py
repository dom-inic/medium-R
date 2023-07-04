from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views import generic
from django.core.mail import send_mail
from . models import Post, Comment
from . forms import EmailPostForm, CommentForm
from taggit.models import Tag
# Create your views here.

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
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

    return render(request, 'blog/post/post_list.html', {'page': page,'posts': posts, 'tag': tag})

class PostList(generic.ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/post_list.html'

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)

    # list or active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create comment object but dont save to database yet
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post = post
            # save comment to the database 
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/post_detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment,
                                                            'comment_form': comment_form})

def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # form submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n\n {cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@medium-R.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


