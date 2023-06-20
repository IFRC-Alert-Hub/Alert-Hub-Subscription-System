from django.shortcuts import render, redirect
from .forms import AlertForm
from shapely.geometry import Polygon


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


def compare_polygon(alert_polygon_string, filtered_polygon_string):
    alert_polygon_list = []
    for coordinates in alert_polygon_string.strip().split(" "):
        alert_coordinates = coordinates.split(",")
        alert_polygon_list.append((alert_coordinates[0], alert_coordinates[1]))
    alert_polygon = Polygon(alert_polygon_list)
    filtered_polygon_list = []
    for coordinates in filtered_polygon_string.strip().split(" "):
        filtered_coordinates = coordinates.split(",")
        filtered_polygon_list.append(
            (filtered_coordinates[0], filtered_coordinates[1]))
    filtered_polygon = Polygon(filtered_polygon_list)

    if alert_polygon.intersects(filtered_polygon):
        return True
    else:
        return False


