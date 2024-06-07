from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post, Comment
from posts.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
@login_required
def ask(request):
    query = request.GET.get('q', '')  # Retrieve the search query if present
    search_type = request.GET.get('type', 'title')  # Retrieve the type of search

    if query:
        if search_type == 'title':
            all_posts = Post.objects.filter(title__icontains=query)
        elif search_type == 'author':
            all_posts = Post.objects.filter(user__username__icontains=query)
        else:
            all_posts = Post.objects.all().order_by('-created')
    else:
        all_posts = Post.objects.all().order_by('-created')

    paginator = Paginator(all_posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'posts/ask.html', {'posts': posts, 'query': query, 'search_type': search_type})

@login_required
def post_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)  # save but do not commit to db yet
            new_post.user = request.user        # assign the user from request
            new_post.save()                     # now save it to the db
            return redirect('/posts/ask/')  # redirect to a new URL
    else:
        form = PostForm()
    return render(request, 'posts/post_add.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.user and not request.user.is_staff:
        return render(request,'posts/post_detail_no_auth.html')
    
    # 댓글을 오름차순으로 정렬
    comments = post.comment_set.all().order_by('created')
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post = post
        new_comment.user = request.user
        new_comment.save()
        return redirect('post_detail', post_id=post_id)
    
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'form': form})
