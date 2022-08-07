
import imp
#from turtle import pos
from django.utils import timezone
from .models import Post , Comment
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm , CommentForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import Http404

# linked in +
from django.views.generic import ListView  , DetailView
from django.contrib.auth.views import LoginView, LogoutView


# from linkedin
class LoginInterfaceView(LoginView):
    template_name="blog/login.html"
    

class LogoutInterfaceView(LoginRequiredMixin ,LogoutView):
    template_name="blog/logout.html"
    login_url="/login"
    

# Create your views here.
""" def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
  # posts=Post.objects.filter(published_date__year='2022',published_date__month='5').order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts}) """
# به جای بالایی می توانیم کلاس زیر را تعریف کنیم

class PostsListView(ListView):
    model=Post
    context_object_name="posts"

""" def post_detail(request, pk):
    
    # post = get_object_or_404(Post, pk=pk)
    # به جای خط بالا می توانیم خط زیر را می نویسیم
    try:
        post= Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return redirect('post_list')
#        raise Http404('پست مورد نظر وجود ندارد')  # یا به لیست پست ها ریدایرکت می کنیم
   
    return render(request, 'blog/post_detail.html', {'post': post})     """

# به جای تابع بالا در حالت کلاس  - کلاس زیر را می نویسیم

class PostDetailsView(DetailView):
    model=Post
    context_object_name="post"

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})    


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})



@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
