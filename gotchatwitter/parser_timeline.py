import json
from random import random
from time import sleep

from bs4 import BeautifulSoup

from parser_utils import *


def parse_user_timeline(u_screen_name, connector, header, **kwargs):
    adv_search = kwargs.get('adv_search', dict())
    date_since = adv_search.get('date_since', kwargs.get('date_since', ''))
    date_until = adv_search.get('date_until', kwargs.get('date_since', ''))

    tid_start = ''
    tid = ''
    error_count = 0
    is_page_one = True
    _next = True
    while _next:
        if adv_search or date_since or date_until:
            if is_page_one:
                url = 'https://twitter.com/search?q=from%3A' + u_screen_name + \
                      '%20since%3A' + date_since + \
                      '%20until%3A' + date_until + '&src=typd&lang=en'
                html = connector.get(url)._content
                is_page_one = False
            else:
                url = 'https://twitter.com/i/search/timeline?vertical=default&q=from%3A' + u_screen_name + \
                      '%20since%3A' + date_since + \
                      '%20until%3A' + date_until + \
                      '&src=typd&include_available_features=1&include_entities=1&' + \
                      'max_position=TWEET-' + tid + '-' + tid_start + '-' + \
                      'BD1UO2FFu9QAAAAAAAAETAAAAAcAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' + \
                      '&reset_error_state=false'
                html_json = json.loads(connector.get(url)._content)
                if html_json.get('errors', ''):
                    sleep(random() * 10)
                    error_count += 1
                    if error_count <= 5:
                        continue
                    else:
                        break
                html = html_json['items_html'].strip()
                _next = html_json['has_more_items']
        else:
            if is_page_one:
                url = 'https://twitter.com/' + re.sub('\@', '', u_screen_name)
                html = connector.get(url)._content
                is_page_one = False
            else:
                url = 'https://twitter.com/i/profiles/show/' \
                      + re.sub('\@', '', u_screen_name) \
                      + '/timeline/tweets?include_available_features=1&include_entities=1&max_position=' \
                      + tid \
                      + '&reset_error_state=false'
                html_json = json.loads(connector.get(url)._content)
                html = html_json['items_html'].strip()
                _next = html_json['has_more_items']

        soup = BeautifulSoup(html, 'lxml')
        tweet_cardwraps = soup.find_all(lambda tag: re.compile('js-stream-item').search(str(tag))
                                                    and not re.compile('scroll-bump').search(str(tag))
                                                    and tag.name == 'li')

        if len(tweet_cardwraps) == 0:
            break

        for tweet_cardwrap in tweet_cardwraps:
            status, uid, screen_name, tid, rid, timestamp, location_id, location_name = \
                parse_header(tweet_cardwrap)
            language, text = parse_text(tweet_cardwrap)
            n_retweets, n_likes = parse_footer(tweet_cardwrap)
            quote_status, quote_text = parse_quote(tweet_cardwrap)
            status = quote_status if quote_status else status
            text = text + ' <quote> ' + quote_text + ' <quote>' if quote_text else text
            media = parse_media(tweet_cardwrap)
            yield [locals()[head] for head in header]
            if not tid_start:
                tid_start = rid if rid else tid
