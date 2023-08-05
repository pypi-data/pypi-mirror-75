# -*- coding: utf-8 -*-
"""
Newspaper uses much of python-goose's extraction code. View their license:
https://github.com/codelucas/newspaper/blob/master/GOOSE-LICENSE.txt

Keep all html page extraction code within this file. Abstract any
lxml or soup parsing code in the parser.py file!
"""

import copy
import logging
import re
from collections import defaultdict
from urllib.parse import urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup

from . import urls
from .urls import prepare_url, is_url
from .utils import StringReplacement, StringSplitter, parse_date_str

__title__ = 'stimson-web-scraper'
__author__ = 'Lucas Ou-Yang'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014, Lucas Ou-Yang'
__maintainer__ = "The Stimson Center"
__maintainer_email = "cooper@pobox.com"

log = logging.getLogger(__name__)

MOTLEY_REPLACEMENT = StringReplacement("&#65533;", "")
ESCAPED_FRAGMENT_REPLACEMENT = StringReplacement(
    "#!", "?_escaped_fragment_=")
TITLE_REPLACEMENTS = StringReplacement("&raquo;", "»")
PIPE_SPLITTER = StringSplitter("\\|")
DASH_SPLITTER = StringSplitter(" - ")
UNDERSCORE_SPLITTER = StringSplitter("_")
SLASH_SPLITTER = StringSplitter("/")
ARROWS_SPLITTER = StringSplitter(" » ")
COLON_SPLITTER = StringSplitter(":")
SPACE_SPLITTER = StringSplitter(' ')
NO_STRINGS = set()
A_REL_TAG_SELECTOR = "a[rel=tag]"
A_HREF_TAG_SELECTOR = ("a[href*='/tag/'], a[href*='/tags/'], "
                       "a[href*='/topic/'], a[href*='?keyword=']")
RE_LANG = r'^[A-Za-z]{2}$'

good_paths = ['story', 'article', 'feature', 'featured', 'slides',
              'slideshow', 'gallery', 'news', 'video', 'media',
              'v', 'radio', 'press']
bad_chunks = ['careers', 'contact', 'about', 'faq', 'terms', 'privacy',
              'advert', 'preferences', 'feedback', 'info', 'browse', 'howto',
              'account', 'subscribe', 'donate', 'shop', 'admin']
bad_domains = ['amazon', 'doubleclick', 'twitter']


class ContentExtractor(object):
    def __init__(self, config):
        self.config = config
        self.parser = self.config.get_parser()
        self.language = config.language
        self.stopwords_class = config.stopwords_class

    def update_language(self, meta_lang):
        """Required to be called before the extraction process in some
        cases because the stopwords_class has to set incase the lang
        is not latin based
        """
        if meta_lang:
            self.language = meta_lang
            self.stopwords_class = \
                self.config.get_stopwords_class(meta_lang)

    def get_authors(self, doc):
        """Fetch the authors of the article, return as a list
        Only works for english articles
        """
        _digits = re.compile(r'\d')

        def contains_digits(d):
            return bool(_digits.search(d))

        def uniqify_list(lst):
            """Remove duplicates from provided list but maintain original order.
              Derived from http://www.peterbe.com/plog/uniqifiers-benchmark
            """
            seen = {}
            result = []
            for item in lst:
                if item.lower() in seen:
                    continue
                seen[item.lower()] = 1
                result.append(item.title())
            return result

        def author_is_url(element_unicode_results):
            for element_unicode_result in element_unicode_results:
                if is_url(element_unicode_result.__str__()):
                    element_unicode_results.remove(element_unicode_result)
            return element_unicode_results

        def parse_byline(search_str):
            """
            Takes a candidate line of html or text and
            extracts out the name(s) in list form:
            >>> parse_byline('<div>By: <strong>Lucas Ou-Yang</strong>,<strong>Alex Smith</strong></div>')
            ['Lucas Ou-Yang', 'Alex Smith']
            """
            # Remove HTML boilerplate
            # RE: literally "<", none of <, once or more, literally ">"
            search_str = re.sub('<[^<]+?>', '', search_str)

            # Remove original By statement
            # RE: any of ((one of "bB", one of "yY", one of ":\s"), (one of "fF", literally "rom", one of ":\s"))
            search_str = re.sub(r'[bB][yY][:\s]|[fF]rom[:\s]', '', search_str)

            search_str = search_str.strip()

            # Chunk the line by non alphanumeric tokens (few name exceptions)
            # >>> re.split("[^\w\'\-\.]", "Tyler G. Jones, Lucas Ou, Dean O'Brian and Ronald")
            # ['Tyler', 'G.', 'Jones', '', 'Lucas', 'Ou', '', 'Dean', "O'Brian", 'and', 'Ronald']
            # RE: any character except: word characters (a-z, A-Z, 0-9, _), '\'', '\-', '.'
            name_tokens = re.split(r'[^\w\'\-.]', search_str)
            name_tokens = [s.strip() for s in name_tokens]

            _authors = []
            # List of first, last name tokens
            curname = []
            delimiters = ['and', ',', '']

            for token in name_tokens:
                if token in delimiters:
                    if len(curname) > 0:
                        _authors.append(' '.join(curname))
                        curname = []

                elif not contains_digits(token):
                    curname.append(token)

            # One last check at end
            valid_name = (len(curname) >= 2)
            if valid_name:
                _authors.append(' '.join(curname))

            return _authors

        # Try 1: Search popular author tags for authors

        ATTRS = ['property', 'name', 'rel', 'itemprop', 'class', 'id']
        VALS = ['article:author', 'article:author_name', 'parsely-author',
                'sailthru.author', 'citation_author', 'author', 'byline',
                'dc.creator', 'byl']
        matches = []
        authors = []

        for attr in ATTRS:
            for val in VALS:
                # found = doc.xpath('//*[@%s="%s"]' % (attr, val))
                elements = self.parser.get_elements_by_tag(doc, attr=attr, value=val)
                for element in elements:
                    if element not in matches:
                        matches.append(element)

        TAGS = ['meta', 'div', 'iframe', 'a', 'span', 'section']
        for match in matches:
            content = ''
            if match.tag in TAGS:
                mm = match.xpath('@content')
                mm = author_is_url(mm)
                if not mm:
                    mm = str(match.text_content()).split()
                if len(mm) > 0:
                    content = mm[0]
            else:
                content = match.text_content() or ''
            if len(content) > 0:
                authors.extend(parse_byline(content))

        return uniqify_list(authors)

        # TODO Method 2: Search raw html for a by-line
        # match = re.search('By[\: ].*\\n|From[\: ].*\\n', html)
        # try:
        #    # Don't let zone be too long
        #    line = match.group(0)[:100]
        #    authors = parse_byline(line)
        # except:
        #    return [] # Failed to find anything
        # return authors

    def get_publishing_date(self, url, doc):
        """3 strategies for publishing date extraction. The strategies
        are descending in accuracy and the next strategy is only
        attempted if a preferred one fails.

        1. Pubdate from URL
        2. Pubdate from metadata
        3. Raw regex searches in the HTML + added heuristics
        """

        date_match = re.search(urls.STRICT_DATE_REGEX, url)
        if date_match:
            date_str = date_match.group(0)
            datetime_obj = parse_date_str(date_str)
            if datetime_obj:
                return datetime_obj

        PUBLISH_DATE_TAGS = [
            {'attribute': 'property', 'value': 'rnews:datePublished',
             'content': 'content'},
            {'attribute': 'property', 'value': 'article:published_time',
             'content': 'content'},
            {'attribute': 'name', 'value': 'OriginalPublicationDate',
             'content': 'content'},
            {'attribute': 'itemprop', 'value': 'datePublished',
             'content': 'datetime'},
            {'attribute': 'property', 'value': 'og:published_time',
             'content': 'content'},
            {'attribute': 'name', 'value': 'article_date_original',
             'content': 'content'},
            {'attribute': 'name', 'value': 'publication_date',
             'content': 'content'},
            {'attribute': 'name', 'value': 'sailthru.date',
             'content': 'content'},
            {'attribute': 'name', 'value': 'PublishDate',
             'content': 'content'},
            {'attribute': 'pubdate', 'value': 'pubdate',
             'content': 'datetime'},
            {'attribute': 'name', 'value': 'publish_date',
             'content': 'content'},
            # https://www.bangkokpost.com/world/711600/myawaddy-industrial-zone-set-for-2017-opening
            {'attribute': 'name', 'value': 'cXenseParse:recs:publishtime',
             'content': 'content'},
        ]
        for known_meta_tag in PUBLISH_DATE_TAGS:
            meta_tags = self.parser.get_elements_by_tag(
                doc,
                attr=known_meta_tag['attribute'],
                value=known_meta_tag['value'])
            if meta_tags:
                date_str = self.parser.get_attribute(
                    meta_tags[0],
                    known_meta_tag['content'])
                datetime_obj = parse_date_str(date_str)
                if datetime_obj:
                    return datetime_obj

        return None

    def get_title(self, doc):
        """Fetch the article title and analyze it

        Assumptions:
        - title tag is the most reliable (inherited from Goose)
        - h1, if properly detected, is the best (visible to users)
        - og:title and h1 can help improve the title extraction
        - python == is too strict, often we need to compare filtered
          versions, i.e. lowercase and ignoring special chars

        Explicit rules:
        1. title == h1, no need to split
        2. h1 similar to og:title, use h1
        3. title contains h1, title contains og:title, len(h1) > len(og:title), use h1
        4. title starts with og:title, use og:title
        5. use title, after splitting
        """
        title = ''
        title_element = self.parser.get_elements_by_tag(doc, tag='title')
        # no title found
        if title_element is None or len(title_element) == 0:
            return title

        # title elem found
        title_text = self.parser.get_text(title_element[0])
        used_delimeter = False

        # title from h1
        # - extract the longest text from all h1 elements
        # - too short texts (fewer than 2 words) are discarded
        # - clean double spaces
        title_text_h1 = ''
        title_element_h1_list = self.parser.get_elements_by_tag(doc,
                                                                tag='h1') or []
        title_text_h1_list = [self.parser.get_text(tag) for tag in
                              title_element_h1_list]
        if title_text_h1_list:
            # sort by len and set the longest
            title_text_h1_list.sort(key=len, reverse=True)
            title_text_h1 = title_text_h1_list[0]
            # discard too short texts
            if len(title_text_h1.split(' ')) <= 2:
                title_text_h1 = ''
            # clean double spaces
            title_text_h1 = ' '.join([x for x in title_text_h1.split() if x])

        # title from og:title
        title_text_fb = (
                self.get_meta_content(doc, 'meta[property="og:title"]') or
                self.get_meta_content(doc, 'meta[name="og:title"]') or '')

        # create filtered versions of title_text, title_text_h1, title_text_fb
        # for finer comparison
        filter_regex = re.compile(r'[^\u4e00-\u9fa5a-zA-Z0-9 ]')
        filter_title_text = filter_regex.sub('', title_text).lower()
        filter_title_text_h1 = filter_regex.sub('', title_text_h1).lower()
        filter_title_text_fb = filter_regex.sub('', title_text_fb).lower()

        # check for better alternatives for title_text and possibly skip splitting
        if title_text_h1 == title_text:
            used_delimeter = True
        elif filter_title_text_h1 and filter_title_text_h1 == filter_title_text_fb:
            title_text = title_text_h1
            used_delimeter = True
        elif filter_title_text_h1 and filter_title_text_h1 in filter_title_text \
                and filter_title_text_fb and filter_title_text_fb in filter_title_text \
                and len(title_text_h1) > len(title_text_fb):
            title_text = title_text_h1
            used_delimeter = True
        elif filter_title_text_fb and filter_title_text_fb != filter_title_text \
                and filter_title_text.startswith(filter_title_text_fb):
            title_text = title_text_fb
            used_delimeter = True

        # split title with |
        if not used_delimeter and '|' in title_text:
            title_text = self.split_title(title_text, PIPE_SPLITTER,
                                          title_text_h1)
            used_delimeter = True

        # split title with -
        if not used_delimeter and '-' in title_text:
            title_text = self.split_title(title_text, DASH_SPLITTER,
                                          title_text_h1)
            used_delimeter = True

        # split title with _
        if not used_delimeter and '_' in title_text:
            title_text = self.split_title(title_text, UNDERSCORE_SPLITTER,
                                          title_text_h1)
            used_delimeter = True

        # split title with /
        if not used_delimeter and '/' in title_text:
            title_text = self.split_title(title_text, SLASH_SPLITTER,
                                          title_text_h1)
            used_delimeter = True

        # split title with »
        if not used_delimeter and ' » ' in title_text:
            title_text = self.split_title(title_text, ARROWS_SPLITTER,
                                          title_text_h1)
            # noinspection PyUnusedLocal
            used_delimeter = True

        title = MOTLEY_REPLACEMENT.replaceAll(title_text)

        # in some cases the final title is quite similar to title_text_h1
        # (either it differs for case, for special chars, or it's truncated)
        # in these cases, we prefer the title_text_h1
        filter_title = filter_regex.sub('', title).lower()
        if filter_title_text_h1 == filter_title:
            title = title_text_h1

        return title

    def split_title(self, title, splitter, hint=None):
        """Split the title to best part possible
        """
        large_text_length = 0
        large_text_index = 0
        title_pieces = splitter.split(title)

        filter_regex = re.compile(r'[^a-zA-Z0-9 ]')
        if hint:
            hint = filter_regex.sub('', hint).lower()

        # find the largest title piece
        for i, title_piece in enumerate(title_pieces):
            current = title_piece.strip()
            if hint and hint in filter_regex.sub('', current).lower():
                large_text_index = i
                break
            if len(current) > large_text_length:
                large_text_length = len(current)
                large_text_index = i

        # replace content
        title = title_pieces[large_text_index]
        return TITLE_REPLACEMENTS.replaceAll(title).strip()

    def get_favicon(self, doc):
        """Extract the favicon from a website http://en.wikipedia.org/wiki/Favicon
        <link rel="shortcut icon" type="image/png" href="favicon.png" />
        <link rel="icon" type="image/png" href="favicon.png" />
        """
        kwargs = {'tag': 'link', 'attr': 'rel', 'value': 'icon'}
        meta = self.parser.get_elements_by_tag(doc, **kwargs)
        if meta:
            favicon = self.parser.get_attribute(meta[0], 'href')
            return favicon
        return ''

    def get_meta_lang(self, doc):
        """Extract content language from meta
        """
        # we have a lang attribute in html
        attr = self.parser.get_attribute(doc, attr='lang')
        if attr is None:
            # look up for a Content-Language in meta
            items = [
                {'tag': 'meta', 'attr': 'http-equiv',
                 'value': 'content-language'},
                {'tag': 'meta', 'attr': 'name', 'value': 'lang'}
            ]
            for item in items:
                meta = self.parser.get_elements_by_tag(doc, **item)
                if meta:
                    attr = self.parser.get_attribute(
                        meta[0], attr='content')
                    break
        if attr:
            value = attr[:2]
            if re.search(RE_LANG, value):
                return value.lower()

        return None

    def get_meta_content(self, doc, metaname):
        """Extract a given meta content form document.
        Example metaNames:
            "meta[name=description]"
            "meta[name=keywords]"
            "meta[property=og:type]"
        """
        meta = self.parser.css_select(doc, metaname)
        content = None
        if meta is not None and len(meta) > 0:
            content = self.parser.get_attribute(meta[0], 'content')
        if content:
            return content.strip()
        return ''

    def get_meta_img_url(self, article_url, doc):
        """Returns the 'top img' as specified by the website
        """
        top_meta_image, try_one, try_two, try_three, try_four = [None] * 5
        try_one = self.get_meta_content(doc, 'meta[property="og:image"]')
        if not try_one:
            link_img_src_kwargs = \
                {'tag': 'link', 'attr': 'rel', 'value': 'img_src|image_src'}
            elems = self.parser.get_elements_by_tag(doc, use_regex=True, **link_img_src_kwargs)
            try_two = elems[0].get('href') if elems else None

            if not try_two:
                try_three = self.get_meta_content(doc, 'meta[name="og:image"]')

                if not try_three:
                    link_icon_kwargs = {'tag': 'link', 'attr': 'rel', 'value': 'icon'}
                    elems = self.parser.get_elements_by_tag(doc, **link_icon_kwargs)
                    try_four = elems[0].get('href') if elems else None

        top_meta_image = try_one or try_two or try_three or try_four

        if top_meta_image:
            return urljoin(article_url, top_meta_image)
        return ''

    def get_meta_type(self, doc):
        """Returns meta type of article, open graph protocol
        """
        return self.get_meta_content(doc, 'meta[property="og:type"]')

    def get_meta_site_name(self, doc):
        """Returns site name of article, open graph protocol
        """
        return self.get_meta_content(doc, 'meta[property="og:site_name"]')

    def get_meta_description(self, doc):
        """If the article has meta description set in the source, use that
        """
        meta_name_text = self.get_meta_content(doc, "meta[name=description]")
        meta_property_text = self.get_meta_content(doc, "meta[property=description]")
        if len(meta_name_text) > len(meta_property_text):
            return meta_name_text
        return meta_property_text

    def get_meta_keywords(self, doc):
        """If the article has meta keywords set in the source, use that
        """
        return self.get_meta_content(doc, "meta[name=keywords]")

    def get_meta_data(self, doc):
        data = defaultdict(dict)
        properties = self.parser.css_select(doc, 'meta')
        for prop in properties:
            key = prop.attrib.get('property') or prop.attrib.get('name')
            value = prop.attrib.get('content') or prop.attrib.get('value')

            if not key or not value:
                continue

            key, value = key.strip(), value.strip()
            if value.isdigit():
                value = int(value)

            if ':' not in key:
                data[key] = value
                continue

            key = key.split(':')
            key_head = key.pop(0)
            ref = data[key_head]

            if isinstance(ref, str) or isinstance(ref, int):
                data[key_head] = {key_head: ref}
                ref = data[key_head]

            for idx, part in enumerate(key):
                if idx == len(key) - 1:
                    ref[part] = value
                    break
                if not ref.get(part):
                    ref[part] = dict()
                elif isinstance(ref.get(part), str) or isinstance(ref.get(part), int):
                    # Not clear what to do in this scenario,
                    # it's not always a URL, but an ID of some sort
                    ref[part] = {'identifier': ref[part]}
                ref = ref[part]
        return data

    def get_canonical_link(self, article_url, doc):
        """
        Return the article's canonical URL

        Gets the first available value of:
        1. The rel=canonical tag
        2. The og:url tag
        """
        links = self.parser.get_elements_by_tag(doc, tag='link', attr='rel',
                                                value='canonical')

        canonical = self.parser.get_attribute(links[0], 'href') if links else ''
        og_url = self.get_meta_content(doc, 'meta[property="og:url"]')
        meta_url = canonical or og_url or ''
        if meta_url:
            meta_url = meta_url.strip()
            parsed_meta_url = urlparse(meta_url)
            if not parsed_meta_url.hostname:
                # MIGHT not have a hostname in meta_url
                # parsed_url.path might be 'example.com/article.html' where
                # clearly example.com is the hostname
                parsed_article_url = urlparse(article_url)
                strip_hostname_in_meta_path = re. \
                    match(".*{}(?=/)/(.*)".
                          format(parsed_article_url.hostname),
                          parsed_meta_url.path)
                try:
                    true_path = strip_hostname_in_meta_path.group(1)
                except AttributeError:
                    true_path = parsed_meta_url.path

                # true_path may contain querystrings and fragments
                meta_url = urlunparse((parsed_article_url.scheme,
                                       parsed_article_url.hostname, true_path,
                                       '', '', ''))

        return prepare_url(meta_url)

    def get_img_urls(self, article_url, doc):
        """Return all of the images on an html page, lxml root
        """
        img_kwargs = {'tag': 'img'}
        img_tags = self.parser.get_elements_by_tag(doc, **img_kwargs)
        urls = [img_tag.get('src')
                for img_tag in img_tags if img_tag.get('src')]
        img_links = set([urljoin(article_url, url)
                         for url in urls])
        return img_links

    def get_first_img_url(self, article_url, top_node):
        """Retrieves the first image in the 'top_node'
        The top node is essentially the HTML markdown where the main
        article lies and the first image in that area is probably significant.
        """
        node_images = self.get_img_urls(article_url, top_node)
        node_images = list(node_images)
        if node_images:
            return urljoin(article_url, node_images[0])
        return ''


    def extract_tags(self, doc):
        if len(list(doc)) == 0:
            return NO_STRINGS
        elements = self.parser.css_select(
            doc, A_REL_TAG_SELECTOR)
        if not elements:
            elements = self.parser.css_select(
                doc, A_HREF_TAG_SELECTOR)
            if not elements:
                return NO_STRINGS

        tags = []
        for el in elements:
            tag = self.parser.get_text(el)
            if tag:
                tags.append(tag)
        return set(tags)

    def calculate_best_node(self, doc, html):
        nodes_to_check = self.nodes_to_check(doc)
        if not nodes_to_check:
            nodes_to_check = self.nodes_to_check_soap(html)
        starting_boost = float(1.0)
        cnt = 0
        parent_nodes = []
        nodes_with_text = []

        for node in nodes_to_check:
            text_node = self.parser.get_text(node)
            if text_node:
                word_stats = self.stopwords_class(language=self.language).get_stopword_count(text_node)
                high_link_density = self.is_highlink_density(node)
                if word_stats.get_stopword_count() > 2 and not high_link_density:
                    nodes_with_text.append(node)

        nodes_number = len(nodes_with_text)
        negative_scoring = 0
        bottom_negativescore_nodes = float(nodes_number) * 0.25

        for i, node in enumerate(nodes_with_text):
            if i == 0:
                continue
            boost_score = float(0)
            # boost
            if self.is_boostable(node):
                if cnt >= 0:
                    boost_score = float((1.0 / starting_boost) * 50)
                    starting_boost += 1
            # nodes_number
            if nodes_number > 15:
                if (nodes_number - i) <= bottom_negativescore_nodes:
                    booster = float(
                        bottom_negativescore_nodes - (nodes_number - i))
                    boost_score = float(-pow(booster, float(2)))
                    negscore = abs(boost_score) + negative_scoring
                    if negscore > 40:
                        boost_score = float(5)

            text_node = self.parser.get_text(node)
            word_stats = self.stopwords_class(language=self.language). \
                get_stopword_count(text_node)
            upscore = int(word_stats.get_stopword_count() + boost_score)

            parent_node = self.parser.get_parent(node)
            self.update_score(parent_node, upscore)
            self.update_node_count(parent_node, 1)

            if parent_node not in parent_nodes:
                parent_nodes.append(parent_node)

            # Parent of parent node
            parent_parent_node = self.parser.get_parent(parent_node)
            if parent_parent_node is not None:
                self.update_node_count(parent_parent_node, 1)
                self.update_score(parent_parent_node, upscore / 2)
                if parent_parent_node not in parent_nodes:
                    parent_nodes.append(parent_parent_node)
            cnt += 1
            i += 1

        return max(parent_nodes, key=self.get_score, default=None)

    def is_boostable(self, node):
        """A lot of times the first paragraph might be the caption under an image
        so we'll want to make sure if we're going to boost a parent node that
        it should be connected to other paragraphs, at least for the first n
        paragraphs so we'll want to make sure that the next sibling is a
        paragraph and has at least some substantial weight to it.
        """
        para = "p"
        steps_away = 0
        minimum_stopword_count = 5
        max_stepsaway_from_node = 3

        nodes = self.walk_siblings(node)
        for current_node in nodes:
            # <p>
            current_node_tag = self.parser.get_tag(current_node)
            if current_node_tag == para:
                if steps_away >= max_stepsaway_from_node:
                    return False
                paragraph_text = self.parser.get_text(current_node)
                word_stats = self.stopwords_class(language=self.language). \
                    get_stopword_count(paragraph_text)
                if word_stats.get_stopword_count() > minimum_stopword_count:
                    return True
                steps_away += 1
        return False

    def walk_siblings(self, node):
        return self.parser.previous_siblings(node)

    def add_siblings(self, top_node):
        baseline_score_siblings_para = self.get_siblings_score(top_node)
        results = self.walk_siblings(top_node)
        for current_node in results:
            ps = self.get_siblings_content(
                current_node, baseline_score_siblings_para)
            for p in ps:
                top_node.insert(0, p)
        return top_node

    def get_siblings_content(
            self, current_sibling, baseline_score_siblings_para):
        """Adds any siblings that may have a decent score to this node
        """
        if current_sibling.tag == 'p' and \
                len(self.parser.get_text(current_sibling)) > 0:
            e0 = current_sibling
            if e0.tail:
                e0 = copy.deepcopy(e0)
                e0.tail = ''
            return [e0]
        else:
            potential_paragraphs = self.parser.get_elements_by_tag(
                current_sibling, tag='p')
            if potential_paragraphs is None:
                return None
            else:
                ps = []
                for first_paragraph in potential_paragraphs:
                    text = self.parser.get_text(first_paragraph)
                    if len(text) > 0:
                        word_stats = self.stopwords_class(
                            language=self.language). \
                            get_stopword_count(text)
                        paragraph_score = word_stats.get_stopword_count()
                        sibling_baseline_score = float(.30)
                        high_link_density = self.is_highlink_density(
                            first_paragraph)
                        score = float(baseline_score_siblings_para *
                                      sibling_baseline_score)
                        if score < paragraph_score and not high_link_density:
                            p = self.parser.create_element(tag='p', text=text, tail=None)
                            ps.append(p)
                return ps

    def get_siblings_score(self, top_node):
        """We could have long articles that have tons of paragraphs
        so if we tried to calculate the base score against
        the total text score of those paragraphs it would be unfair.
        So we need to normalize the score based on the average scoring
        of the paragraphs within the top node.
        For example if our total score of 10 paragraphs was 1000
        but each had an average value of 100 then 100 should be our base.
        """
        base = 100000
        paragraphs_number = 0
        paragraphs_score = 0
        nodes_to_check = self.parser.get_elements_by_tag(top_node, tag='p')

        for node in nodes_to_check:
            text_node = self.parser.get_text(node)
            word_stats = self.stopwords_class(language=self.language). \
                get_stopword_count(text_node)
            high_link_density = self.is_highlink_density(node)
            if word_stats.get_stopword_count() > 2 and not high_link_density:
                paragraphs_number += 1
                paragraphs_score += word_stats.get_stopword_count()

        if paragraphs_number > 0:
            base = paragraphs_score / paragraphs_number

        return base

    def update_score(self, node, add_to_score):
        """Adds a score to the gravityScore Attribute we put on divs
        we'll get the current score then add the score we're passing
        in to the current.
        """
        current_score = 0
        score_string = self.parser.get_attribute(node, 'gravityScore')
        if score_string:
            current_score = float(score_string)

        new_score = current_score + add_to_score
        self.parser.set_attribute(node, "gravityScore", str(new_score))

    def update_node_count(self, node, add_to_count):
        """Stores how many decent nodes are under a parent node
        """
        current_score = 0
        count_string = self.parser.get_attribute(node, 'gravityNodes')
        if count_string:
            current_score = int(count_string)

        new_score = current_score + add_to_count
        self.parser.set_attribute(node, "gravityNodes", str(new_score))

    def is_highlink_density(self, e):
        """Checks the density of links within a node, if there is a high
        link to text ratio, then the text is less likely to be relevant
        """
        links = self.parser.get_elements_by_tag(e, tag='a')
        if not links:
            return False

        text = self.parser.get_text(e)
        words = [word for word in text.split() if word.isalnum()]
        if not words:
            return True
        words_number = float(len(words))
        sb = []
        for link in links:
            sb.append(self.parser.get_text(link))

        link_text = ''.join(sb)
        link_words = link_text.split()
        num_link_words = float(len(link_words))
        num_links = float(len(links))
        link_divisor = float(num_link_words / words_number)
        score = float(link_divisor * num_links)
        if score >= 1.0:
            return True
        return False
        # return True if score > 1.0 else False

    def get_score(self, node):
        """Returns the gravityScore as an integer from this node
        """
        return self.get_node_gravity_score(node) or 0

    def get_node_gravity_score(self, node):
        gravity_score = self.parser.get_attribute(node, 'gravityScore')
        if not gravity_score:
            return None
        return float(gravity_score)

    def nodes_to_check(self, doc):
        """Returns a list of nodes we want to search
        on like paragraphs and tables
        """
        nodes_to_check = []
        for tag in ['p', 'pre', 'td']:
            nodes = self.parser.get_elements_by_tag(doc, tag=tag)
            for node in nodes:
                if node.text:
                    nodes_to_check.append(node)
        return nodes_to_check

    def nodes_to_check_soap(self, html):
        """Returns a list of nodes we want to search
        on like paragraphs and tables
        """
        # soup = BeautifulSoup(html, 'lxml')
        soup = BeautifulSoup(html, 'html.parser')
        VALID_TAGS = ['p', 'pre', 'td']
        fake_parent_node = self.parser.create_element(tag='body', text="")
        nodes_to_check = [fake_parent_node]
        for tag in VALID_TAGS:
            for match in soup.find_all(tag):
                if match.name not in VALID_TAGS:
                    match.replaceWith(match.renderContents())
                node = self.parser.create_element(tag=tag, text=match.text)
                if node.text:
                    fake_parent_node.append(node)
                    nodes_to_check.append(node)
        return nodes_to_check

    def post_cleanup(self, top_node):
        """Remove any divs that looks like non-content, clusters of links,
        or paras with no gusto; add adjacent nodes which look contenty
        """
        node = self.add_siblings(top_node)
        for e in self.parser.get_children(node):
            e_tag = self.parser.get_tag(e)
            if e_tag != 'p':
                if self.is_highlink_density(e):
                    self.parser.remove(e)
        return node
