#처리된 데이터를 갖고 어떠한 기능을 하는게 뷰이다
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


#리스트의 화면
def post_list(request):#여기서의 매개변수는 해당하는 페이지의 값을 가진다
    # posts = Post.published.all()
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
####페이지 범위를 벗어나거나 페이지 범위를 설정할 때 완전 다른 값이 들어오면 그 오류를 처리하는 try except
    try:
        posts=paginator.page(page_number)#설정한 페이지로 작없을 하다가
    except PageNotAnInteger:###페이지 범위값이 인트형 정수가 아닌 다른 값이 들어왔을 때 처음으로 돌아간다
        posts=paginator.page(1)
    except EmptyPage:#### 페이지의 범위가 넘어갔을 때 마지막으로 넘어간다
        posts=paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'posts':posts})
#게시물 상세 뷰
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                                status=Post.Status.PUBLISHED,
                                slug=post,
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    return render(request,
    'blog/post/detail.html',
            { 'post': post,
                    'comments': comments,
                    'form': form})

class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, \
                                    status=Post.Status.PUBLISHED)

    sent = False

    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name' ]} recommends you read " \
                    f"{post. title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                    f"{cd['name']}\'s comments: {cd['comments' ]}"
            send_mail(subject, message, '1116milk@gmail.com',
                        [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                                        'form': form,
                                                                        'sent': sent})
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, \
                                    status=Post.Status.PUBLISHED)

    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
    # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
    # Assign the post to the comment
        comment.post = post
    # Save the comment to the database
        comment. save()
    return render(request, 'blog/post/comment.html',
                                        {'post': post,
                                        'form': form,
                                        'comment': comment})