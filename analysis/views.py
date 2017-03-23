from django.shortcuts import render
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests
from collections import Counter
import unicodedata
from stop_words import get_stop_words
import json
import string
from django.utils.safestring import mark_safe
from django.template import Library


# Create your views here.

def index(request, article, thepageid, article_two, thepageid2, lang1, lang2, name, url1, url2):

    pages = article['query']['pages']
    pages2 = article_two['query']['pages']

    # session variables for language
    # lang1 = request.session["lang1"]
    # lang2 = request.session["lang2"]

    # page length
    length = article_length(pages, thepageid)
    length2 = article_length(pages2, thepageid2)

    #  wordcount
    wordcount1 = get_wordcount(article['query'])
    wordcount2 = get_wordcount(article_two['query'])

    # number of watchers
    watchers1 = article_watchers(pages, thepageid)
    watchers2 = article_watchers(pages2, thepageid2)

    watchers_exists = number_check(watchers1, watchers2)

    # article image
    image1 = get_image_url(pages, thepageid)
    image2 = get_image_url(pages2, thepageid2)

    lang1_users = get_wiki_users(lang1)
    lang2_users = get_wiki_users(lang2)
    # all_users = get_wiki_users("Other")
    # other_users = all_users - (lang1_users + lang2_users)

    # Check to see if extract data exists and assign boolean to variable
    extract_exists = check_extract(pages, thepageid, pages2, thepageid2)

    context = {
        "name": name,
        "respURL": url1,
        "respURL2": url2,
        "lang1": lang1,
        "lang2": lang2,
        "length": length,
        "length2": length2,
        "wordcount1": wordcount1,
        "wordcount2": wordcount2,
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

        if lang1 != "English":
            # make translation request
            yandex = translate_request(lang1, extract)
            context['yandexurl1'] = yandex.url
            # return translation
            translation1 = get_translated_extract(yandex.json())
            context['translation1'] = translation1
            # word bubble list
            cleaned1 = clean_data(translation1)
            cloud_list1 = find_most_frequent_words(cleaned1)
            context['cloud1'] = cloud_list1

        else:
            # return translation
            translation1 = extract
            context['translation1'] = translation1
            # word bubble list
            cleaned1 = clean_data(translation1)
            cloud_list1 = find_most_frequent_words(cleaned1)
            context['cloud1'] = cloud_list1
            # context['cloud1'] = mark_safe(json.dumps(cloud_list1))

        if lang2 != "English":
            # make translation request
            yandex2 = translate_request(lang2, extract2)
            context['yandexurl2'] = yandex2.url
            # get translated extract
            translation2 = get_translated_extract(yandex2.json())
            context['translation2'] = translation2
            # word bubble list
            cleaned2 = clean_data(translation2)
            cloud_list2 = find_most_frequent_words(cleaned2)
            context['cloud2'] = cloud_list2
        else:
            translation2 = extract2
            context['translation2'] = translation2
            # word bubble list
            cleaned2 = clean_data(translation2)
            cloud_list2 = find_most_frequent_words(cleaned2)
            context['cloud2'] = cloud_list2







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
    if 'thumbnail' in pages[pageid]:
        image_link = pages[pageid]['thumbnail']['source']
        val(image_link)
    else:
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

def get_api_key():

    return "trnsl.1.1.20170314T183113Z.4a6fc904e7ea1bc5.23809eb4e1d1c082364cb9e075cae6be489b7ba9"

def translate_request(lang, text):
    """ Make request to yandex api and return data """
    api_key = get_api_key()

    mycode = {'English': 'en', 'French': 'fr', 'Italian': 'it', 'German': 'de', 'Spanish': 'es', 'Swedish': 'sv',
            'Dutch': 'nl', 'Irish': 'ga', 'Russian': 'ru'}

    # code = get_language_code(lang)
    code = mycode[lang]

    base = "https://translate.yandex.net"
    post = "/api/v1.5/tr.json/translate?key=" + api_key


    # parameters for request
    my_atts = {}

    my_atts['text'] = text
    my_atts['lang'] = code + '-en'  # prop=info
    # my_atts['lang'] = 'en-fr'

    # make request
    yandex_resp = requests.get(base+post, params=my_atts)

    return yandex_resp

def get_translated_extract(data):

    translated_extract = data['text'][0]

    return translated_extract

def clean_data(text):
    """ Remove non ascii data ad special characters"""

    stripped = strip_non_ascii(text)

    # filter all characters from the string that are not printable
    printable = set(string.printable)
    filter(lambda x: x in printable, stripped)

    # Normalise unicode data
    unicodedata.normalize('NFKD', stripped).encode('ascii', 'ignore')

    return stripped

def strip_non_ascii(text):
    """ Returns the string without non ASCII characters """
    stripped = (c for c in text if 0 < ord(c) < 127)
    return ''.join(stripped)

def find_most_frequent_words(text):
    """ find top 20 most frequent characters from text """

    # get rid of stop words
    filtered = [word for word in text.lower().split() if word not in get_stop_words('en')]

    # top 20 most frequent words
    new = Counter(filtered).most_common(15)

    # convert list of tuples to list of arrays
    new = [list(n) for n in new]

    # put number element from lists in single quotes
    for mylist in new:
        mylist[1] = str(mylist[1])

    return new

def get_wordcount(data):

    if 'wordcount' in data['search'][0]:
        wordcount = data['search'][0]['wordcount']
        print("Word count:", wordcount)
    else:
        wordcount = "wordcount could not be retrieved"
        print(wordcount)

    return wordcount
