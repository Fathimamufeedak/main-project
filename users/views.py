from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from plants.models import Remedy as PlantRemedy


def index(request):
    return render(request, 'home.html')


def auth_select(request):
    """Render authentication role selection page."""
    return render(request, 'auth_select.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created. You can now log in using your email.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email') or request.POST.get('username')
        password = request.POST.get('password')
        # allow login by email: find username for given email
        from django.contrib.auth.models import User
        user = None
        try:
            user_obj = User.objects.get(email__iexact=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            # fallback: try authenticate with provided value as username
            user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    from consultations.models import Consultation
    total_queries = Consultation.objects.filter(user=request.user).count()
    pending = Consultation.objects.filter(user=request.user, status='pending').count()
    in_progress = Consultation.objects.filter(user=request.user, status='in_progress').count()
    completed = Consultation.objects.filter(user=request.user, status='completed').count()
    context = {
        'total_queries': total_queries,
        'pending': pending,
        'in_progress': in_progress,
        'completed': completed,
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})


def search_remedies(request):
    query = request.GET.get('q') or request.POST.get('q')
    results = []
    if query:
        results = PlantRemedy.objects.filter(symptom__icontains=query).select_related('doctor').order_by('-created_at')
    return render(request, 'users/search_remedies.html', {'results': results, 'query': query})
