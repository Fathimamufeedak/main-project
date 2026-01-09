from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import DoctorRegisterForm
from .models import Doctor
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, email=email, password=password)
            doctor = form.save(commit=False)
            doctor.user = user
            doctor.is_verified = False
            doctor.save()
            messages.success(request, 'Doctor account created. Await admin approval.')
            return redirect('login')
    else:
        form = DoctorRegisterForm()
    return render(request, 'doctors/register.html', {'form': form})


@login_required
def doctor_dashboard(request):
    # Only show basic dashboard; doctors must be verified by admin to access full features
    try:
        doc = request.user.doctor
    except Doctor.DoesNotExist:
        doc = None
    return render(request, 'doctors/dashboard.html', {'doctor': doc})
