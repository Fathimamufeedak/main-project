from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ConsultationForm
from .models import Consultation


@login_required
def upload_consultation(request):
    # Block admins from accessing upload consultation page
    if request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = ConsultationForm(request.POST, request.FILES)
        if form.is_valid():
            cons = form.save(commit=False)
            cons.user = request.user
            cons.save()
            return redirect('user_consultations')
    else:
        form = ConsultationForm()
    return render(request, 'consultations/upload.html', {'form': form})


@login_required
def user_consultations(request):
    consultations = Consultation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'consultations/list.html', {'consultations': consultations})


@login_required
def consultation_detail(request, pk):
    cons = get_object_or_404(Consultation, pk=pk)
    # enforce owner or staff
    if cons.user != request.user and not request.user.is_staff:
        return redirect('user_consultations')
    return render(request, 'consultations/detail.html', {'cons': cons})


@login_required
def edit_consultation(request, pk):
    cons = get_object_or_404(Consultation, pk=pk)
    if cons.user != request.user:
        return redirect('user_consultations')
    if cons.status != 'pending':
        # only pending consultations can be edited by user
        return redirect('consultation_detail', pk=cons.pk)

    if request.method == 'POST':
        form = ConsultationForm(request.POST, request.FILES, instance=cons)
        if form.is_valid():
            form.save()
            return redirect('consultation_detail', pk=cons.pk)
    else:
        form = ConsultationForm(instance=cons)
    return render(request, 'consultations/upload.html', {'form': form, 'editing': True})


@login_required
def delete_consultation(request, pk):
    cons = get_object_or_404(Consultation, pk=pk)
    if cons.user != request.user and not request.user.is_staff:
        return redirect('user_consultations')
    if request.method == 'POST':
        cons.delete()
        return redirect('user_consultations')
    return render(request, 'consultations/confirm_delete.html', {'cons': cons})
