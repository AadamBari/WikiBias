import requests
from django.shortcuts import render

import analysis.views
from analysis.models import Language

# Create your views here.
# Views methods must return html response

def index(request):
    all_langs = Language.objects.all()

    # context information template needs
    context = {'all_langs': all_langs}

    # render incorporates hhtp response behind the scenes
    return render(request, 'main/index.html', context)


def process(request):

    #Using session variables, remove context from return parameters
    if request.method=="POST":
        request.session["article"] = request.POST["article"]
        request.session["lang1"] = request.POST["langOne"]
        request.session["lang2"] = request.POST["langTwo"]



    # Use sessions to transfer between variables
    article = request.session["article"]
    lang1 = request.session["lang1"]
    lang2 = request.session["lang2"]

    wikipage = '{0}'.format(article)  # put the title in single quotes

    # get wikipedia code for languages input
    code = {'English': 'en', 'French': 'fr', 'Italian': 'it', 'German': 'de', 'Spanish': 'es', 'Swedish': 'sv',
            'Dutch': 'nl', 'Irish': 'ga', 'Russian': 'ru'}

    baseurl = "http://" + code[lang1] + ".wikipedia.org/w/api.php"
    # eg if english: "http://en.wikipedia.org/w/api.php"

    my_atts = {}

    my_atts['action'] = 'query'  # action=query
    my_atts['prop'] = 'info'  # prop=info
    my_atts['format'] = 'json'  # format=json
    my_atts['titles'] = wikipage  # title=brad+pitt

    resp = requests.get(baseurl, params=my_atts)
    data = resp.json()

    # make url session variable
    request.session['respURL'] = resp.url  # the url

    # store the pages dictionary
    pages = data['query']['pages']

    # check to see if a page id exists within the page, if so return pageid from id dictionary
    # i.e. checking if page exists ad returning pageid
    try:
        for id in pages:
            pageidnum = pages[id]['paged']  # holds numeric page id value]
            if pageidnum:
                return analysis.views.index(request)
    except KeyError:
        # Key is not present
        return render(request, 'main/failure.html')
        # exit()









     #how to use context
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
