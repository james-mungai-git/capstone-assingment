from django.shortcuts import render, redirect
from .forms import Register, UserProfileForm, BlogPostForm
from .models import  BlogPost
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout as auth_logout
from datetime import date

def logout(request):
    auth_logout(request)
    return redirect('/login/')

# Signup view
def signup(request):
    if request.method == "POST":
        form = Register(request.POST)  
        if form.is_valid():
            form.save()  
            return redirect('login')  
    else:
        form = Register()

    return render(request, 'base/registration/sign_up.html', {'form': form})

def userprofile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('user-profile')
    else:
        form = UserProfileForm()

    return render(request, 'base/user-profile.html', {'form': form})

# blogpost crud operations

class BlogPostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = BlogPost
    template_name = "base/blog/blog-post.html"
    form_class = BlogPostForm
    success_url = reverse_lazy("blog-list")
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return True

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "base/blog/blog-detail.html"
    context_object_name = 'post'
    

class BlogPostListView(ListView):
    model = BlogPost
    template_name = "base/blog/blog-list.html"
    context_object_name = 'posts'
    ordering = ['-published_date']
    def search(request):
        search = request.queryset_params.get('search')
        if search:
            items = items.filter(title__icontains=search)
    

class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = "base/blog/blog-delete.html"
    success_url = reverse_lazy("blog-list")  # usually list view

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author
   
            
        
class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ["title", "content"]
    template_name = "base/blog/blog-post.html"
    success_url = reverse_lazy("blog-post")
    
    def test_func(self):
        post = self.get_object
        return self.request.author == post.author
    
# mealitem crud





