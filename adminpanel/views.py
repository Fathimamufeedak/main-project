from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from doctors.models import Doctor


@staff_member_required
def doctor_requests(request):
    doctors = Doctor.objects.filter(is_verified=False)
    return render(request, 'adminpanel/doctor_requests.html', {'doctors': doctors})


@staff_member_required
def approve_doctor(request, pk):
    doc = get_object_or_404(Doctor, pk=pk)
    doc.is_verified = True
    doc.save()
    return redirect('doctor_requests')


@staff_member_required
def dataset_placeholder(request):
    return render(request, 'adminpanel/dataset.html')
