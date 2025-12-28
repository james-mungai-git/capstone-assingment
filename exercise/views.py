from .forms import  Exerciseform
from .models import  Exercise
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


class ExerciseCreateView(CreateView):
    model = Exercise
    form_class = Exerciseform
    template_name = "exercise/log_exercise.html"
    success_url = reverse_lazy("dashboard")
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ExerciseListView(ListView):
    model = Exercise
    template_name = "exercise/exercise_list.html"
    context_object_name = 'exercises'
    


class ExerciseUpdateView(UpdateView):
    model = Exercise
    template_name = "exercise/log_exercise.html"
    success_url = reverse_lazy ("dashboard")
    
    def get_object(self,):
        obj = super().get_object()
        
        if obj.user != self.request.user:
            raise PermissionDenied("you are jot allowed to updatethis item")
        
        return obj
    

class ExerciseDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Exercise
    template_name = "excercise/delete-log.html"
    success_url = reverse_lazy ("dashboard")
    
    def get_object(self,):
        obj = super().get_object()
    
        if obj.user != self.request.user:
            raise PermissionDenied("you are jot allowed to delete this item")
        
        return obj
        
    def test_func(self):
        obj = self.get_object
        return self.request.user == obj.user






