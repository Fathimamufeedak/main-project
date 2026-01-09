from django.shortcuts import render, get_object_or_404
from .models import Plant


def plant_list(request):
    plants = Plant.objects.all()
    return render(request, 'plants/list.html', {'plants': plants})


def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    return render(request, 'plants/detail.html', {'plant': plant})
