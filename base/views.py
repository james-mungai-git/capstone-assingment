from django.shortcuts import render, redirect
from .forms import Register

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
