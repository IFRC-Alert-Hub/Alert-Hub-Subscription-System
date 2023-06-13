from django.shortcuts import render, redirect
from .forms import AlertForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AlertForm()
    return render(request, 'index.html', {'form': form})
