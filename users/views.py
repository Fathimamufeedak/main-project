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


def unified_login(request):
    """
    Unified login page with role selection (User, Doctor, Admin).
    Single form with radio buttons for role selection.
    """
    # If user is already logged in, redirect based on their role
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif request.user.is_staff:
            # Check if user has a Doctor instance
            try:
                from doctors.models import Doctor
                if hasattr(request.user, 'doctor'):
                    return redirect('doctor_dashboard')
            except:
                pass
            return redirect('admin_dashboard')
        else:
            return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'user')  # user, doctor, admin
        
        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return render(request, 'users/unified_login.html', {'selected_role': role})
        
        # Authenticate user by email or username
        from django.contrib.auth.models import User
        user = None
        try:
            user_obj = User.objects.get(email__iexact=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            # Fallback: try authenticate with provided value as username
            user = authenticate(request, username=email, password=password)
        
        if user is None:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'users/unified_login.html', {'selected_role': role})
        
        # Verify role matches user permissions
        # Admin → is_superuser
        # Doctor → is_staff (and has Doctor instance)
        # User → normal authenticated user (not superuser, not staff)
        
        if role == 'admin':
            if not user.is_superuser:
                messages.error(request, 'You do not have admin privileges. Please select the correct role.')
                return render(request, 'users/unified_login.html', {'selected_role': role})
            login(request, user)
            return redirect('admin_dashboard')
        
        elif role == 'doctor':
            # Doctor must have is_staff=True and a Doctor instance
            if not user.is_staff:
                messages.error(request, 'You do not have doctor privileges. Please select the correct role.')
                return render(request, 'users/unified_login.html', {'selected_role': role})
            # Verify user has a Doctor instance
            try:
                from doctors.models import Doctor
                if not hasattr(user, 'doctor'):
                    messages.error(request, 'Doctor profile not found. Please contact administrator.')
                    return render(request, 'users/unified_login.html', {'selected_role': role})
            except Exception:
                messages.error(request, 'Doctor profile not found. Please contact administrator.')
                return render(request, 'users/unified_login.html', {'selected_role': role})
            login(request, user)
            return redirect('doctor_dashboard')
        
        else:  # role == 'user'
            # User should not be superuser or staff
            if user.is_superuser:
                messages.error(request, 'This account has admin privileges. Please select Admin role.')
                return render(request, 'users/unified_login.html', {'selected_role': role})
            if user.is_staff:
                messages.error(request, 'This account has doctor/admin privileges. Please select Doctor or Admin role.')
                return render(request, 'users/unified_login.html', {'selected_role': role})
            login(request, user)
            return redirect('dashboard')
    
    # GET request - show login form
    return render(request, 'users/unified_login.html', {'selected_role': 'user'})


# Keep old function name for backwards compatibility
def user_login(request):
    return unified_login(request)


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    # Role-based redirection: staff users should never see user dashboard
    if request.user.is_staff:
        return redirect('admin_dashboard')
    
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
