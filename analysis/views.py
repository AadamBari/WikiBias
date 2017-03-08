from django.shortcuts import render

# Create your views here.

def index(request, article, thepageid, article_two, thepageid2):

    pages = article['query']['pages']
    pages2 = article_two['query']['pages']

    # page length
    length = article_length(pages, thepageid)
    length2 = article_length(pages2, thepageid2)

    # number of watchers
    watchers1 = article_watchers(pages, thepageid)
    watchers2 = article_watchers(pages2, thepageid2)

    context = {
        "length": length,
        "length2": length2,
        "watchers1": watchers1,
        "watchers2": watchers2,
    }

    return render(request, 'analysis/index.html', context)

def article_length(pages, pageid):
    """ get article page length in bytes """

    length = pages[pageid]['length']

    return length

def article_watchers(pages, pageid):
    """ check to see if watcher data available and return it (sometimes not available if too few watchers) """

    if 'watchers' in pages[pageid]:
        watchers = pages[pageid]['watchers']

    else:
        watchers = "there are 30 watchers or less"

    return watchers
