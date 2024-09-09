
from django.shortcuts import render, redirect
from .models import Slider
from .forms import SliderForm


def home(request):
    sliders = Slider.objects.order_by('-id')[:3]  # Fetching latest 3 items
    card_image = Slider.objects.order_by('-id')[:8]  # Fetching latest 3 items
    return render(request,'home.html',{'sliders': sliders ,'card_image': card_image})


def create_slider(request):
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('slider_created')  # Redirect to a success page
    else:
        form = SliderForm()
    return render(request, 'create_slider.html', {'form': form})

def slider_created(request):
    sliders = Slider.objects.all()
    return render(request, 'create_slider.html', {'sliders': sliders})

