from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from functools import wraps
import os

from doctors.models import Doctor
from plants.models import Plant, Remedy
from consultations.models import Consultation


def admin_required(view_func):
    """Simple decorator to require staff (admin) users for the custom admin panel."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)

    return _wrapped


def admin_login(request):
    """Admin login using email + password. Only users with is_staff=True can login here."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            user = authenticate(request, username=user.username, password=password)
            if user and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
        messages.error(request, 'Invalid admin credentials')

    return render(request, 'adminpanel/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@admin_required
def dashboard(request):
    """Admin dashboard with summary cards."""
    total_users = User.objects.count()
    total_doctors = Doctor.objects.count()
    pending_doctors = Doctor.objects.filter(is_verified=False).count()
    total_plants = Plant.objects.count()
    total_consultations = Consultation.objects.count()

    context = {
        'total_users': total_users,
        'total_doctors': total_doctors,
        'pending_doctors': pending_doctors,
        'total_plants': total_plants,
        'total_consultations': total_consultations,
    }
    return render(request, 'adminpanel/dashboard.html', context)


@admin_required
def doctor_requests(request):
    doctors = Doctor.objects.all().select_related('user')
    return render(request, 'adminpanel/doctor_requests.html', {'doctors': doctors})


@admin_required
def approve_doctor(request, pk):
    doc = get_object_or_404(Doctor, pk=pk)
    doc.is_verified = True
    doc.save()
    messages.success(request, 'Doctor approved')
    return redirect('doctor_requests')


@admin_required
def reject_doctor(request, pk):
    doc = get_object_or_404(Doctor, pk=pk)
    doc.is_verified = False
    # optional: mark as rejected using a flag or delete user; here we leave record
    messages.info(request, 'Doctor marked as not verified')
    return redirect('doctor_requests')


@admin_required
def manage_users(request):
    q = request.GET.get('q', '')
    users = User.objects.all()
    if q:
        users = users.filter(username__icontains=q) | users.filter(email__icontains=q)
    return render(request, 'adminpanel/users.html', {'users': users, 'q': q})


@admin_required
def view_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    consultations = Consultation.objects.filter(user=user).select_related('doctor')
    return render(request, 'adminpanel/user_detail.html', {'user_obj': user, 'consultations': consultations})


@admin_required
def deactivate_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.save()
    messages.success(request, 'User deactivated')
    return redirect('manage_users')


@admin_required
def manage_doctors(request):
    doctors = Doctor.objects.select_related('user')
    return render(request, 'adminpanel/doctors.html', {'doctors': doctors})


@admin_required
def edit_doctor(request, pk):
    doc = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        qual = request.POST.get('qualification', '')
        exp = request.POST.get('experience', 0)
        doc.qualification = qual
        try:
            doc.experience = int(exp)
        except ValueError:
            doc.experience = 0
        doc.save()
        messages.success(request, 'Doctor updated')
        return redirect('manage_doctors')

    return render(request, 'adminpanel/edit_doctor.html', {'doc': doc})


@admin_required
def remove_doctor(request, pk):
    doc = get_object_or_404(Doctor, pk=pk)
    # remove doctor record but keep user
    doc.delete()
    messages.success(request, 'Doctor removed')
    return redirect('manage_doctors')


@admin_required
def doctor_remedies(request, pk):
    doc = get_object_or_404(Doctor, pk=pk)
    remedies = Remedy.objects.filter(doctor=doc).select_related('plant')
    return render(request, 'adminpanel/doctor_remedies.html', {'doc': doc, 'remedies': remedies})


@admin_required
def manage_plants(request):
    plants = Plant.objects.all()
    return render(request, 'adminpanel/plants.html', {'plants': plants})


@admin_required
def add_plant(request):
    if request.method == 'POST':
        name = request.POST.get('plant_name')
        description = request.POST.get('description', '')
        uses = request.POST.get('medicinal_uses', '')
        safety = request.POST.get('safety_guidelines', '')
        Plant.objects.create(
            plant_name=name,
            description=description,
            medicinal_uses=uses,
            safety_guidelines=safety
        )
        messages.success(request, 'Plant added')
        return redirect('manage_plants')

    return render(request, 'adminpanel/add_plant.html')


@admin_required
def edit_plant(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == 'POST':
        plant.plant_name = request.POST.get('plant_name')
        plant.description = request.POST.get('description', '')
        plant.medicinal_uses = request.POST.get('medicinal_uses', '')
        plant.safety_guidelines = request.POST.get('safety_guidelines', '')
        plant.save()
        messages.success(request, 'Plant updated')
        return redirect('manage_plants')
    return render(request, 'adminpanel/edit_plant.html', {'plant': plant})


@admin_required
def delete_plant(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    plant.delete()
    messages.success(request, 'Plant deleted')
    return redirect('manage_plants')


@admin_required
def manage_remedies(request):
    remedies = Remedy.objects.select_related('plant', 'doctor')
    plants = Plant.objects.all()
    doctors = Doctor.objects.select_related('user')
    return render(request, 'adminpanel/remedies.html', {'remedies': remedies, 'plants': plants, 'doctors': doctors})


@admin_required
def add_remedy(request):
    if request.method == 'POST':
        plant_id = request.POST.get('plant')
        doctor_id = request.POST.get('doctor')
        desc = request.POST.get('remedy_description', '')
        plant = get_object_or_404(Plant, pk=plant_id)
        doctor = None
        if doctor_id:
            doctor = get_object_or_404(Doctor, pk=doctor_id)
        Remedy.objects.create(plant=plant, doctor=doctor, remedy_description=desc)
        messages.success(request, 'Remedy added')
        return redirect('manage_remedies')

    return redirect('manage_remedies')


@admin_required
def edit_remedy(request, pk):
    rem = get_object_or_404(Remedy, pk=pk)
    if request.method == 'POST':
        rem.remedy_description = request.POST.get('remedy_description', '')
        rem.save()
        messages.success(request, 'Remedy updated')
        return redirect('manage_remedies')
    return render(request, 'adminpanel/edit_remedy.html', {'remedy': rem})


@admin_required
def delete_remedy(request, pk):
    rem = get_object_or_404(Remedy, pk=pk)
    rem.delete()
    messages.success(request, 'Remedy deleted')
    return redirect('manage_remedies')


@admin_required
def consultations_list(request):
    consultations = Consultation.objects.select_related('user', 'doctor').order_by('-created_at')
    return render(request, 'adminpanel/consultations.html', {'consultations': consultations})


@admin_required
def dataset_management(request):
    """Handle simple dataset image uploads and list uploaded images."""
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'dataset')
    os.makedirs(upload_dir, exist_ok=True)
    uploaded_files = []

    if request.method == 'POST' and request.FILES.getlist('images'):
        files = request.FILES.getlist('images')
        fs = FileSystemStorage(location=upload_dir)
        for f in files:
            fs.save(f.name, f)
        messages.success(request, 'Images uploaded to dataset folder')
        return redirect('dataset_management')

    # list files
    for fn in os.listdir(upload_dir):
        uploaded_files.append(fn)

    return render(request, 'adminpanel/dataset.html', {'files': uploaded_files})
