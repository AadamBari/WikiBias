from django.shortcuts import render
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# Create your views here.

def index(request, article, thepageid, article_two, thepageid2):

    pages = article['query']['pages']
    pages2 = article_two['query']['pages']

    # session variables for language
    lang1 = request.session["lang1"]
    lang2 = request.session["lang2"]

    # page length
    length = article_length(pages, thepageid)
    length2 = article_length(pages2, thepageid2)

    # number of watchers
    watchers1 = article_watchers(pages, thepageid)
    watchers2 = article_watchers(pages2, thepageid2)

    watchers_exists = number_check(watchers1, watchers2)

    image1 = get_image_url(pages, thepageid)
    image2 = get_image_url(pages2, thepageid2)

    lang1_users = get_wiki_users(lang1)
    lang2_users = get_wiki_users(lang2)
    # all_users = get_wiki_users("Other")
    # other_users = all_users - (lang1_users + lang2_users)

    # Get the percentage of watchers relative to the total number of watchers
    watchers1_relative = percentage(watchers1, lang1_users)
    watchers2_relative = percentage(watchers2, lang2_users)


    context = {
        "lang1": lang1,
        "lang2": lang2,
        "length": length,
        "length2": length2,
        "watchers1": watchers1,
        "watchers2": watchers2,
        "watchers_exists": watchers_exists,
        "image1": image1,
        "image2": image2,
        "lang1_users": lang1_users,
        "lang2_users": lang2_users,
        # "other_users": other_users,
        "watchers1_relative": watchers1_relative,
        "watchers2_relative": watchers2_relative,
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

def get_wiki_users(lang):
    """
    Return the number of users for the wikipedia language
    Source: https://en.wikipedia.org/wiki/List_of_Wikipedias
    """

    # dictionary to store number of users per wikipedia language version
    wiki_no_of_users = {'English': '30433146', 'French': '2738662', 'Dutch': '824911', 'German': '2600919',
                        'Swedish': '539662', 'Italian': '1478718', 'Spanish': '4537032', 'Russian': '2065967',
                        'Other': '67108835'}

    wiki_users = wiki_no_of_users[lang]

    return wiki_users

def percentage(part, whole):
    """ Returns percentage """
    percent = 100 * float(part) / float(whole)
    return percent
