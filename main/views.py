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

    # Using session variables, remove context from return parameters
    if request.method == "POST":
        request.session["article"] = request.POST["article"]
        request.session["lang1"] = request.POST["langOne"]
        request.session["lang2"] = request.POST["langTwo"]


    # Use sessions to transfer between variables
    article = request.session["article"]
    lang1 = request.session["lang1"]
    lang2 = request.session["lang2"]

    title = '{0}'.format(article)  # put the title in single quotes

    baseurl = get_base_url(lang1)
    # eg if english: "http://en.wikipedia.org/w/api.php"

    # Make api call and return response generated
    resp = info_request(title, baseurl)

    # extract data i json format from response
    data = resp.json()

    request.session['articledata'] = data

    # make url session variable
    request.session['respURL'] = resp.url  # the url

    pageidnum = validate_pageid(request, data)


    # put pageid into single quotes so can access json later
    request.session['ArticlePageID'] = '{0}'.format(pageidnum)  # pageid = 'pageid'

    request.session['second'] = get_second_language_title(request, lang1, lang2, title)

    return analysis.views.index(request)



def get_base_url(lang):
    """Produce the base Wikipedia api url for a particular language"""

    # get wikipedia code for languages input
    code = {'English': 'en', 'French': 'fr', 'Italian': 'it', 'German': 'de', 'Spanish': 'es', 'Swedish': 'sv',
            'Dutch': 'nl', 'Irish': 'ga', 'Russian': 'ru'}

    url = "http://" + code[lang] + ".wikipedia.org/w/api.php"
    # url = "http://en.wikipedia.org/w/api.php"

    return url


def info_request(title, baseurl):


    # parameters for request
    my_atts = {}

    my_atts['action'] = 'query'  # action=query
    my_atts['prop'] = 'info'  # prop=info
    my_atts['format'] = 'json'  # format=json
    my_atts['titles'] = title  # title=brad+pitt
    my_atts['inprop'] = 'watchers'  # |protection'

    # make request
    resp = requests.get(baseurl, params=my_atts)

    # return response
    return resp


def link_request(title, baseurl, lang):
    """ make request to get second language choice link for """

    # get code for the second language
    code = get_language_code(lang)

    # parameters for request
    my_atts = {}

    my_atts['action'] = 'query'  # action=query
    my_atts['prop'] = 'langlinks'  # prop=info
    my_atts['format'] = 'json'  # format=json
    my_atts['titles'] = title  # title=brad+pitt
    my_atts['llprop'] = 'url' #llprop=url
    my_atts['lllang'] = code #lllang=fr

    # make request
    resp = requests.get(baseurl, params=my_atts)

    # return response
    return resp

def validate_pageid(request, data):
    """ check to see if a page id exists within the page, if so return pageid from api json """
    pages = data['query']['pages']


    # i.e. checking if page exists and assigning page id
    try:
        for id in pages:
            pageidnum = pages[id]['pageid']  # holds numeric page id value]
            if pageidnum:
                break
    except KeyError:
        # Key is not present
        return render(request, 'main/failure.html')
        # exit()

    return pageidnum


def extract_title(data, pageidnum):

    # put in single quotes
    mypageid = '{0}'.format(pageidnum)  # pageid = 'pageid'

    # get langlinks
    lang_info = data['query']['pages'][mypageid]['langlinks']

    # get url for langlinks dictionary within list
    for link in  lang_info:
        url = link['url']

    title = url.rsplit('/', 1)[-1]

    return title

def get_second_language_title(request, lang1, lang2, title):
    """get title for second language"""

    base = get_base_url(lang1)
    resp = link_request(title, base, lang2)
    data = resp.json()
    my_url = resp.url
    pageid = validate_pageid(request, data)

    second_title = extract_title(data, pageid)

    return second_title


def get_language_code(language):

    code_dict = {'English': 'en', 'French': 'fr', 'Italian': 'it', 'German': 'de', 'Spanish': 'es', 'Swedish': 'sv',
            'Dutch': 'nl', 'Irish': 'ga', 'Russian': 'ru'}

    code = code_dict[language]

    return code

     #how to use context
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
