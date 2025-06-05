from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Login pakai username (karena Django default pakai username)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # ✅ redirect ke dashboard setelah login
        else:
            messages.error(request, 'Email atau password salah.')

    return render(request, 'myapp/login.html')

def sistem_view(request):
    return render(request, 'myapp/sistem.html')

def dashboard_view(request):
    return render(request, 'myapp/dashboard.html')


