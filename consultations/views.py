from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ConsultationForm
from .models import Consultation


@login_required
def upload_consultation(request):
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
