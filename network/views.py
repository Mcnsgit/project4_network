from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from notification.models import Notification
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post, User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import random

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'network/index.html')

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()

    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', {
        'form': form,
        'posts': posts,
        'page_obj': page_obj
    })

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' 
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self):
        context = super(PostListView, self).get_context_data()
        users = list(User.objects.exclude(pk=self.request.user.pk))
        if len(users) > 3:
            cnt = 3
        else:
            cnt = len(users)
        random_users = random.sample(users, cnt)
        context['random_users'] = random_users
        return context


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', reverse('index'))

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            return render(request, 'network/login.html', {
                'message': 'Invalid username and/or password.',
                'next': next_url
            })
    else:
        next_url = request.GET.get('next', reverse('index'))
        return render(request, 'network/login.html', {'next': next_url})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')
        next_url = request.POST.get('next', reverse('index'))

        if password != confirmation:
            return render(request, 'network/register.html', {
                'message': 'Passwords must match.',
                'next': next_url
            })

        try:
            user = User.objects.create_user(username, email, password)
            login(request, user)
            return HttpResponseRedirect(next_url)
        except IntegrityError:
            return render(request, 'network/register.html', {
                'message': 'Username already taken.',
                'next': next_url
            })
    else:
        next_url = request.GET.get('next', reverse('index'))
        return render(request, 'network/register.html', {'next': next_url})


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()

    return render(request, 'network/create_post.html', {'form': form})


def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user_profile).order_by('-created_at')

    is_following = (request.user.is_authenticated and request.user in user_profile.following.all())

    return render(request, 'network/profile.html', {
        'user_profile': user_profile,
        'posts': posts,
        'is_following': is_following
    })


@login_required
def toggle_follow(request, username):
    user_profile = get_object_or_404(User, username=username)
    if user_profile in request.user.following.all():
        request.user.following.remove(user_profile)
    else:
        request.user.following.add(user_profile)

    return redirect('profile', username=username)


@login_required
def following(request):
    followed_users = request.user.following.all()
    posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/following.html', {'page_obj': page_obj})


def update_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id, user=request.user)

        content = request.POST.get('content')
        if content:
            post.content = content
            post.save()
            return JsonResponse({'message': 'Post updated successfully'})

        return JsonResponse({'error': 'Invalid or empty content'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def toggle_like(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
        notify = Notification.objects.filter(post=post, sender=request.user, notification_type=1)
        notify.delete()
    else:
        post.likes.add(request.user)
        liked = True
        notify = Notification(post=post, sender=request.user, user=post.user, notification_type=1)
        notify.save()

    # context = {
    #     'post':post,
    #     'total_likes':post.total_likes(),
    #     'liked':liked,
    # }

    return JsonResponse({'likes': post.likes.count(), 'liked': liked})

""" Like post comments """
@login_required
def LikeCommentView(request): # , id1, id2              id1=post.pk id2=reply.pk
    post = get_object_or_404(Post, id=request.POST.get('id'))
    cliked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        cliked = False
    else:
        post.likes.add(request.user)
        cliked = True

    cpost = get_object_or_404(Post, id=request.POST.get('pid'))
    total_comments2 = cpost.comments.all().order_by('-id')
    total_comments = cpost.comments.all().filter(reply=None).order_by('-id')
    tcl={}
    for cmt in total_comments2:
        cliked = False
        if cmt.likes.filter(id=request.user.id).exists():
            cliked = True

        tcl[cmt.id] = cliked


    context = {
        'post':cpost,
        'comments':total_comments,
        'total_clikes':post.total_clikes(),
        'clikes':tcl
    }

    return JsonResponse(context)  

""" Post save """
@login_required
def SaveView(request):

    post = get_object_or_404(Post, id=request.POST.get('id'))
    saved = False
    if post.saves.filter(id=request.user.id).exists():
        post.saves.remove(request.user)
        saved = False
    else:
        post.saves.add(request.user)
        saved = True
    
    context = {
        'post':post,
        'total_saves':post.total_saves(),
        'saved':saved,
    }

    return JsonResponse(context) if saved else JsonResponse(None)

""" Create post """
@login_required
class PostCreateView(CreateView):
    model = Post
    fields =['title', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



""" Update post """
class PostUpdateView( UpdateView):
    @login_required
    def get(self, request):
        return super().get(request)
    model = Post
    fields =['title', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


""" Delete post """
class PostDeleteView( DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
