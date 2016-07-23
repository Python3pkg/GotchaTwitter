import re
import warnings


HEADERS = {'authority': 'twitter.com',
           'method': 'GET',
           # 'path': '/i/trends?k=&lang=en&pc=true&query=from%3ATomaasNavarrete+since%3A2016-02-05+until%3A2016-02-10&show_context=true&src=module',
           'scheme': 'https',
           'accept': 'application/json, text/javascript, */*; q=0.01',
           # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'accept-encoding': 'gzip, deflate, sdch, br',
           'accept-language': 'en-US,en;q=0.8',
           'cache-control': 'max-age=0',
           'upgrade-insecure-requests': '1',
           # 'cookie': 'guest_id=v1%3A143633553636973156; kdt=Nfw6w4LLnEdRrKgUxa9S6RkhBi5EjifOYjYEjUT7; remember_checked_on=1; auth_token=9b88cbfd12b890a7ef12bcae0e2880a633e411fa; pid="v3:1437887547279707935822773"; lang=en; _gat=1; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0; _ga=GA1.2.1819401238.1437630704; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDW3U%252BlUAToMY3NyZl9p%250AZCIlYjY5MGMyOTM2MzExODJhY2NlNTA1NjdlOWNiZWY3ODc6B2lkIiUxY2Q5%250AM2UzZTc1M2Q4M2QzODE4MzJmNGYyYTgyZjIzMA%253D%253D--23984f61b0a5266b27251a0a36095331c54d8ba2',
           # 'referer': 'https://twitter.com/search?q=from%3ATomaasNavarrete%20since%3A2016-02-05%20until%3A2016-02-10&src=typd&lang=en',
           # 'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
           'x-requested-with': 'XMLHttpRequest'}


def parse_header(tweet_cardwrap):
    """
    return (status, uid, screen_name, tid, rid, tms, location_id, location_name) of a tweet
    """
    properties = tweet_cardwrap.find('div', class_=re.compile('js-stream-tweet')).attrs
    uid = properties.get('data-user-id', '')
    tid = properties.get('data-item-id', '')
    screen_name = properties.get('data-screen-name', '')
    rid = properties.get('data-retweet-id', '')

    tms = tweet_cardwrap.find('span', re.compile('timestamp')).attrs.get('data-time', '')

    icon = tweet_cardwrap.find('div', class_=re.compile('context'))
    status = ''
    if icon.get_text(strip=True):
        if icon.find('span', class_=re.compile('retweet')):
            status = 'retweeted by '
        elif icon.find('span', re.compile('reply')):
            status = 'replied to '
        status += icon.find('a', class_=re.compile('user-profile')).attrs['href'][1:]

    geo = tweet_cardwrap.find('span', re.compile('Tweet-geo'))
    if geo:
        location = geo.find('a', class_=re.compile('actionButton'))
        location_id = location.attrs.get('data-place-id')
        location_name = geo.attrs.get('title')
    else:
        location_id, location_name = '', ''
    return [status, uid, screen_name, tid, rid, tms, location_id, location_name]


def parse_text(tweet_cardwrap, tag='p'):
    """
    return (language, text) of a target tweet
    """
    textwrap = tweet_cardwrap.find(tag, re.compile('tweet-text', re.IGNORECASE))
    [img.replace_with(img.attrs.get('alt')) for img in textwrap.find_all('img', re.compile('^Emoji$'))]
    [a.extract() for a in textwrap.find_all('a', re.compile('u-hidden|twitter-timeline-link'))]
    [a.replace_with(a.text) for a in textwrap.find_all('a', re.compile('hashtag|atreply'))]
    language = textwrap.attrs.get('lang')
    return [language, textwrap.get_text(' ', strip=True)]


def parse_footer(tweet_cardwrap):
    """
    return number of (retweets, likes)
    """
    n_retweets = tweet_cardwrap.find('span', re.compile('retweet$')).span.attrs.get('data-tweet-stat-count')
    n_likes = tweet_cardwrap.find('span', re.compile('favorite$')).span.attrs.get('data-tweet-stat-count')
    return n_retweets, n_likes


def parse_quote(tweet_cardwrap):
    """
    return (status, text) for quote
    """
    quote = tweet_cardwrap.find('div', re.compile('QuoteTweet-container'))
    if quote:
        href = quote.find('a', re.compile('QuoteTweet-link')).attrs.get('href')
        lang, text = parse_text(quote, 'div')
        return 'quote from ' + href[1:], text
    else:
        return '', ''


def parse_media(tweet_cardwrap):
    """
    return url of media
    """
    photo = tweet_cardwrap.find('div', class_=re.compile('Media-(singlePhoto|videoPreview)'))
    if photo:
        return photo.find('img').attrs.get('src')
    video = tweet_cardwrap.find('div', class_=re.compile('Media-player'))
    if video:
        return re.search('\(\'(.*?)\'\)', video.attrs.get('style', '')).group(1)
    return ''
