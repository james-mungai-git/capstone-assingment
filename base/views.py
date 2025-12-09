from django.shortcuts import render, redirect
from .forms import Register, UserProfileForm
from .models import UserProfile, FoodItem

# Home view
def home(request):
    return render(request, 'base/home.html')

# Signup view
def signup(request):
    if request.method == "POST":
        form = Register(request.POST)  # <-- use uppercase POST
        if form.is_valid():
            form.save()  # Save the user
            return redirect('login')  # Redirect to login after successful signup
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


        
