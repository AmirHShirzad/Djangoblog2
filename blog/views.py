from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# Create your views here.


def index(request):
    # we use context to add data to our template
    # in context we loping post object
    context = {'posts': Post.objects.all()}

    return render(request, 'blog/index.html', context=context)

# ClassView Vs FunctionView
# the most important thing about deiffrence of class based view and function base view
# is that in class view we have shorter code line and we save code with variable but in 
# function base view we render a function and have longer line code.  

class PostListView(ListView):
    model = Post
    
    # the default template for PostListView class is post_list.html in blog app. that structure 
    #  is blog/post_list.html
    template_name = 'blog/index.html' #<app>/<model>_<viewtype>.html

    # in this class we should loping variable like the variable in index function,
    #  that we loping post variable, the default variable of PostListView class is object list
    # but we need to define our variable as post so we use context_object_name
    context_object_name = 'posts'
    ordering = ['-created_date']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-created_date')

class PostDetailView(DetailView):
    model = Post

# LoginRequiredMixin, this class added a functionality to our PostCreateView class, that 
# verify the current user is authenticated or not
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # we need to overwrite form_valid method to added logined user to new created post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    #success_url: this means that when we delete a post we redirect to index page
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    # we send title from context to template to made some changes in title in tab of each page
    return render(request, 'blog/about.html', {'title': 'About'})
