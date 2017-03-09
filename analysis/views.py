from django.shortcuts import render
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

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

    watchers_exists = number_check(watchers1, watchers2)

    image1 = get_image_url(pages, thepageid)
    image2 = get_image_url(pages2, thepageid2)

    context = {
        "length": length,
        "length2": length2,
        "watchers1": watchers1,
        "watchers2": watchers2,
        "watchers_exists": watchers_exists,
        "image1": image1,
        "image2": image2,
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
        watchers = "less than 30"

    return watchers

def number_check(watcher1, watcher2):

    if (isinstance(watcher1, int)) and (isinstance(watcher2, int)):
        is_number = True

    else:
        is_number = False

    return is_number

def get_image_url(pages, pageid):

    val = URLValidator()
    try:
        image_link = pages[pageid]['thumbnail']['source']
        val(image_link)
    except ValidationError:
        image_link = "this article does not have a thumbnail image"

    return image_link
