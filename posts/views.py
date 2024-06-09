# posts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegisterForm, EditProfileForm
from .models import Post
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group, User
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import CalculatorForm, TwoSumForm
from typing import List, Tuple, Optional



class DeletePostView(UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return self.request.user == post.author or \
            Group.objects.get(name='manager') in self.request.user.groups.all()

    def handle_no_permission(self):
        return render(self.request, 'posts/protected.html')

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        return render(request, 'posts/delete_post.html', {'post': post})

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return redirect('all_posts')


class DeleteUserView(UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self):
        return Group.objects.get(name='manager') \
            in self.request.user.groups.all()

    def handle_no_permission(self):
        return render(self.request, 'posts/protected.html')

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, 'posts/delete_user.html', {'user': user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('user_list')


def index(request):
    return render(request, 'posts/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'posts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    return render(request, 'posts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('index')


def user_list(request):
    users = User.objects.all()
    is_manager = request.user.groups.filter(name='manager').exists()
    return render(request, 'posts/users.html', {'users': users,
                                                'is_manager': is_manager})


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'posts/edit_profile.html', args)


def protected_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'posts/protected.html')


# Create your views here.
def all_posts(request):
    filter_option = request.GET.get('filter')
    if filter_option == 'my_posts':
        # Filter posts by the current user
        posts = Post.objects.filter(author=request.user)
    else:
        # Show only public posts
        posts = Post.objects.filter(Q(privacy='public')
                                    | Q(author=request.user))
    return render(request, 'posts/all_posts.html', {'posts': posts})


def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        privacy = request.POST.get('privacy')  # Get the privacy value
        # Create the BlogPost record
        post = Post(author=request.user, title=title,
                    content=content, privacy=privacy)
        post.save()
        # Redirect to the view_post page
        return redirect('view_post', post_id=post.id)
    return render(request, 'posts/add_post.html')


@login_required
def view_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_manager = request.user.groups.filter(name='manager').exists()
    return render(request, 'posts/view_post.html', {
        'post': post,
        'is_manager': is_manager,
        'user_is_author': request.user == post.author
    })


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        privacy = request.POST.get('privacy')
        # Update the BlogPost record
        post.title = title
        post.content = content
        post.privacy = privacy
        post.save()
        # Redirect to the view_post page
        return redirect('view_post', post_id=post.id)
    return render(request, 'posts/edit_post.html', {'post': post})


def __delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('all_posts')
    return render(request, 'posts/delete_post.html', {'post': post})


def calculator_view(request):
    result = None
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            operand1 = form.cleaned_data.get('operand1')
            operator = form.cleaned_data.get('operator')
            operand2 = form.cleaned_data.get('operand2')

            if operator == '+':
                result = operand1 + operand2
            elif operator == '-':
                result = operand1 - operand2
            elif operator == '*':
                result = operand1 * operand2
            elif operator == '/':
                if operand2 != 0:
                    result = operand1 / operand2
                else:
                    result = 'Error: Division by zero'
    else:
        form = CalculatorForm()

    return render(request, 'posts/calculator.html', {'form': form, 'result': result})


def two_sum(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    This function takes a list of integers and a target integer. It returns a tuple of two indices such that the 
    numbers at these indices add up to the target. If no such pair exists, it returns None.

    Args:
        nums (List[int]): A list of integers.
        target (int): The target integer.

    Returns:
        Optional[Tuple[int, int]]: A tuple of two indices if a pair is found, None otherwise.
    """

    # Initialize an empty dictionary. This will store the numbers from the list as keys and their indices as values.
    h = {}

    # This loop populates the dictionary. The enumerate function provides both the index (i) and the number (num).
    for i, num in enumerate(nums):
        h[num] = i

    # This loop checks for each number, if there is another number in the dictionary that adds up to the target.
    for i, num in enumerate(nums):
        # Calculate the desired number that will add up to the target.
        desired = target - num

        # Check if the desired number is in the dictionary and its index is not the same as the current number's index.
        if desired in h and h[desired] != i:
            # If such a pair is found, return the indices as a tuple.
            return i, h[desired]

    # If no pair is found in the entire loop, return None.
    return None


def two_sum_view(request):
    result = None
    if request.method == 'POST':
        form = TwoSumForm(request.POST)
        if form.is_valid():
            nums = list(map(int, form.cleaned_data.get('nums').split(',')))
            target = form.cleaned_data.get('target')
            result = two_sum(nums, target)  # Call your two_sum function here
    else:
        form = TwoSumForm()

    return render(request, 'posts/twosum.html', {'form': form, 'result': result})