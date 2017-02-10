
# Create your views here.
from django.http import Http404
from analysis.models import Language
from django.shortcuts import render


def index(request):
    all_langs = Language.objects.all()

    # information template needs
    context = {'all_langs' : all_langs}

    # render incorporates hhtp response behind the scenes
    return render(request, 'main/index.html', context)

