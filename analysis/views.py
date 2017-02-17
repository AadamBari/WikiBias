from django.shortcuts import render
from analysis.models import Language


# Create your views here.

def index(request):



    return render(request, 'analysis/index.html')




