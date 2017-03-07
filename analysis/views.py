from django.shortcuts import render

# Create your views here.

def index(request, article, thepageid):

    # article = request.session['articledata'] #same as data in main\view
    pages = article['query']['pages']
    # thepageid = request.session['ArticlePageID']

    # get article page length in  bytes
    length = article['query']['pages'][thepageid]['length']

    #
    # check to see if watcher data in json (sometimes not available if too few watchers)
    if 'watchers' in pages[thepageid]:
        watchers = pages[thepageid]['watchers']

    else:
        watchers = "there are 30 watchers or less"



    context = {
        "length": length,
        "watchers": watchers,
    }

    return render(request, 'analysis/index.html', context)