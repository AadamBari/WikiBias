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

    # Check to see if extract data exists and assign boolean to variable
    extract_exists = check_extract(pages, thepageid, pages2, thepageid2)

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
        "extract_exists": extract_exists,
    }

    if watchers_exists:

        # Get the percentage of watchers relative to the total number of watchers
        watchers1_relative = percentage(watchers1, lang1_users)
        watchers2_relative = percentage(watchers2, lang2_users)
        # Add to context dictionary
        context['watchers1_relative'] = watchers1_relative
        context['watchers2_relative'] = watchers2_relative

    if extract_exists:
        print("the extract is here")
        # retrieve extract and assign to variable
        extract = get_extract(pages, thepageid)
        extract2 = get_extract(pages2, thepageid2)

        # add to dictionary
        context['extract1'] = extract
        context['extract2'] = extract2




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

def check_extract(pages, pageid, pages2, pageid2):
    """ Checks to see if the first paragraph from the article was returned and present in the request data """

    if ('extract' in pages[pageid]) and ('extract' in pages2[pageid2]):
        return True
    else:
        return False

def get_extract(pages, pageid):
    """ Parses data to retrieve extract """
    extract = pages[pageid]['extract']

    return extract
