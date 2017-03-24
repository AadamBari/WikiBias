import requests
from django.shortcuts import render
from django.http import Http404

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
        article = request.POST["article"]
        lang1 = request.POST["langOne"]
        lang2 = request.POST["langTwo"]


    # Use sessions to transfer between variables
    # article = request.session["article"]
    # lang1 = request.session["lang1"]
    # lang2 = request.session["lang2"]

    title = '{0}'.format(article)  # put the title in single quotes

    # Get information for first article
    baseurl = get_base_url(lang1)
    resp = info_request(title, baseurl)
    data = resp.json()
    pageid = validate_pageid(request, data)

    # make session variables for first article data
    # request.session['articledata'] = data
    # request.session['respURL'] = resp.url  # the url
    title_two = get_second_language_title(request, lang1, lang2, title)
    # request.session['second'] = title_two

    # Get information for second article
    baseurl_two = get_base_url(lang2)
    resp_two = info_request(title_two, baseurl_two)
    data_two = resp_two.json()
    pageid_two = validate_pageid(request, data_two)

    # make session variables for first article data
    # request.session['respURL2'] = resp_two.url

    return analysis.views.index(request, data, pageid, data_two, pageid_two, lang1, lang2, article, resp.url, resp_two.url)


def get_second_language_title(request, lang1, lang2, title):
    """get title for second language"""

    base = get_base_url(lang1)
    resp = link_request(title, base, lang2)
    # request.session['langlink'] = resp.url
    data = resp.json()
    pageid = validate_pageid(request, data)

    second_title = extract_title(data, pageid, request)

    return second_title

def get_base_url(lang):
    """Produce the base Wikipedia api url for a particular language"""

    # get wikipedia code for languages input
    code = {'English': 'en', 'French': 'fr', 'Italian': 'it', 'German': 'de', 'Spanish': 'es', 'Swedish': 'sv',
            'Dutch': 'nl', 'Irish': 'ga', 'Russian': 'ru'}

    url = "http://" + code[lang] + ".wikipedia.org/w/api.php"
    # url = "http://en.wikipedia.org/w/api.php"

    return url


def info_request(title, baseurl):
    """ Make api call and return response generated """

    # parameters for request
    my_atts = {}

    my_atts['action'] = 'query'  # action=query
    my_atts['prop'] = 'info|pageimages|extracts|pageviews'  # prop=info
    my_atts['format'] = 'json'  # format=json
    my_atts['titles'] = title  # title=brad+pitt
    my_atts['inprop'] = 'watchers'  # |protection'
    my_atts['pithumbsize'] = '500'  # thumbnail size
    my_atts['exintro'] = '1'  # content before first section
    my_atts['explaintext'] = '1'  # Return extracts as plain text instead of limited HTML.
    my_atts['pvipdays'] = '14'  # Limits page views to last 14 days
    my_atts['list'] = 'search'  # performs full search
    my_atts['srsearch'] = title  # title for search
    my_atts['srwhat'] = 'nearmatch'

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
    for key in pages:
        print("the yoke:", int(key))
        if key and int(key) > 1:
            pageidnum = pages[key]['pageid']  # holds numeric page id value]
        else:
            raise Http404("Article you have chosen does not exist in the selected language(s)."
                          "Please check your spelling")


    if isinstance(pageidnum, int):
        pass
    else:
        return render(request, 'main/failure.html')

    # Return pageid in single quotes
    return '{0}'.format(pageidnum)


def extract_title(data, mypageid, request):
    """ extract the title of the article in the second language"""

    # get langlinks
    try:
        lang_info = data['query']['pages'][mypageid]['langlinks']
    except KeyError:
        return render(request, 'main/failure.html')

    # get url for langlinks dictionary within list
    for link in  lang_info:
        url = link['url']

    title = url.rsplit('/', 1)[-1]

    return title


def get_language_code(language):
    """ Takes language as parameter and return Wikipedia language code """

    # code_dict = {'English': 'en', 'French': 'fr', 'Italian': 'it', 'German': 'de', 'Spanish': 'es', 'Swedish': 'sv',
    #         'Dutch': 'nl', 'Irish': 'ga', 'Russian': 'ru'}
    #
    # code = code_dict[language]

    all_langs = Language.objects.all()

    for lang in all_langs:
        if language == lang.name:
            code = lang.code



    return code

     #how to use context
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
