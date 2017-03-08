from django.shortcuts import render

# Create your views here.

def index(request, article, thepageid, article_two, thepageid_two):

    pages = article['query']['pages']
    pages2 = article_two['query']['pages']

    # get article page length in bytes
    length = article_length(pages, thepageid)
    length2 = article_length(pages2, thepageid_two)

    # check to see if watcher data in json (sometimes not available if too few watchers)
    if 'watchers' in pages[thepageid]:
        watchers = pages[thepageid]['watchers']

    else:
        watchers = "there are 30 watchers or less"



    context = {
        "length": length,
        "length2": length2,
        "watchers": watchers,
    }

    return render(request, 'analysis/index.html', context)

def article_length(pages,pageid):
    """ get article page length in bytes """

    length = pages[pageid]['length']

    return length

