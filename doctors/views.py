from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import (
    DoctorRegisterForm,
    DoctorLoginForm,
    DoctorProfileForm,
    RemedyForm,
    ResponseForm,
    StatusForm,
)
from .models import Doctor, Remedy
from consultations.models import Consultation
from plants.models import Plant


def _get_doctor_or_none(user):
    try:
        return user.doctor
    except Doctor.DoesNotExist:
        return None


def doctor_login(request):
    if request.method == 'POST':
        form = DoctorLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                doc = _get_doctor_or_none(user)
                if doc and not doc.is_verified:
                    messages.info(request, 'Your account is pending admin verification.')
                return redirect('doctor_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = DoctorLoginForm()
    return render(request, 'doctors/login.html', {'form': form})


def doctor_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('doctor_login')


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
            return redirect('doctor_login')
    else:
        form = DoctorRegisterForm()
    return render(request, 'doctors/register.html', {'form': form})


@login_required
def doctor_dashboard(request):
    doc = _get_doctor_or_none(request.user)
    if not doc:
        messages.error(request, 'You are not registered as a doctor.')
        return redirect('doctor_login')

    if not doc.is_verified:
        return render(request, 'doctors/pending.html', {'doctor': doc})

    assigned = Consultation.objects.filter(doctor=doc)
    total = assigned.count()
    pending = assigned.filter(status='pending').count()
    completed = assigned.filter(status='completed').count()

    return render(request, 'doctors/dashboard.html', {
        'doctor': doc,
        'total': total,
        'pending': pending,
        'completed': completed,
    })


@login_required
def consultation_list(request):
    doc = _get_doctor_or_none(request.user)
    if not doc or not doc.is_verified:
        return render(request, 'doctors/pending.html', {'doctor': doc})

    consultations = Consultation.objects.filter(doctor=doc).order_by('-created_at')
    return render(request, 'doctors/consultations.html', {'consultations': consultations})


@login_required
def consultation_detail(request, pk):
    doc = _get_doctor_or_none(request.user)
    if not doc or not doc.is_verified:
        return render(request, 'doctors/pending.html', {'doctor': doc})

    consult = get_object_or_404(Consultation, pk=pk, doctor=doc)

    response_form = ResponseForm()
    status_form = StatusForm(initial={'status': consult.status})
    try:
        remedy = consult.remedy
    except Remedy.DoesNotExist:
        remedy = None

    if request.method == 'POST':
        if 'response_submit' in request.POST:
            response_form = ResponseForm(request.POST)
            if response_form.is_valid():
                consult.response = response_form.cleaned_data['response']
                consult.save()
                messages.success(request, 'Response submitted')
                return redirect('doctor_consultation_detail', pk=pk)

        if 'status_submit' in request.POST:
            status_form = StatusForm(request.POST)
            if status_form.is_valid():
                consult.status = status_form.cleaned_data['status']
                consult.save()
                messages.success(request, 'Status updated')
                return redirect('doctor_consultation_detail', pk=pk)

    return render(request, 'doctors/consultation_detail.html', {
        'consult': consult,
        'response_form': response_form,
        'status_form': status_form,
        'remedy': remedy,
    })


@login_required
def remedy_form(request, pk):
    doc = _get_doctor_or_none(request.user)
    if not doc or not doc.is_verified:
        return render(request, 'doctors/pending.html', {'doctor': doc})

    consult = get_object_or_404(Consultation, pk=pk, doctor=doc)
    try:
        remedy = consult.remedy
    except Remedy.DoesNotExist:
        remedy = None

    if request.method == 'POST':
        form = RemedyForm(request.POST, instance=remedy)
        if form.is_valid():
            rem = form.save(commit=False)
            rem.consultation = consult
            rem.save()
            messages.success(request, 'Remedy saved')
            return redirect('doctor_consultation_detail', pk=pk)
    else:
        form = RemedyForm(instance=remedy)

    return render(request, 'doctors/remedy_form.html', {'form': form, 'consult': consult})


@login_required
def doctor_profile(request):
    doc = _get_doctor_or_none(request.user)
    if not doc:
        messages.error(request, 'You are not registered as a doctor.')
        return redirect('doctor_login')

    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doc)
        if form.is_valid():
            form.save()
            # allow editing basic user fields too
            request.user.email = request.POST.get('email', request.user.email)
            request.user.first_name = request.POST.get('first_name', request.user.first_name)
            request.user.last_name = request.POST.get('last_name', request.user.last_name)
            request.user.save()
            messages.success(request, 'Profile updated')
            return redirect('doctor_profile')
    else:
        form = DoctorProfileForm(instance=doc)

    return render(request, 'doctors/profile.html', {'form': form, 'doctor': doc})
