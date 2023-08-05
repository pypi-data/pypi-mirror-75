# -*- coding: utf-8 -*-
"""
This class holds configuration objects, which can be thought of
as settings.py but dynamic and changing for whatever parent object
holds them. For example, pass in a config object to an Article
object, Source object, or even network methods, and it just works.
"""

import logging

from .parser import Parser
from .text import (StopWords, StopWordsArabic, StopWordsChinese,
                   StopWordsKorean, StopWordsHindi, StopWordsJapanese, StopWordsThai, StopWordsNepali)
from .version import __version__

__title__ = 'stimson-web-scraper'
__author__ = 'Lucas Ou-Yang'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014, Lucas Ou-Yang'
__maintainer__ = "The Stimson Center"
__maintainer_email = "cooper@pobox.com"

log = logging.getLogger(__name__)


class Configuration(object):
    def __init__(self):
        """
        Modify any of these Article / Source properties
        TODO: Have a separate ArticleConfig and SourceConfig extend this!
        """
        self.MIN_WORD_COUNT = 300  # num of word tokens in text
        self.MIN_SENT_COUNT = 7  # num of sentence tokens
        self.MAX_TITLE = 200  # num of chars
        self.MAX_TEXT = 100000  # num of chars
        self.MAX_KEYWORDS = 35  # num of strings in list
        self.MAX_AUTHORS = 10  # num strings in list
        self.MAX_SUMMARY = 5000  # num of chars
        self.MAX_SUMMARY_SENT = 5  # num of sentences
        self.KEYWORD_COUNT = 10  # num of keywords to extract for a URL

        # max number of urls we cache for each news source
        self.MAX_FILE_MEMO = 20000

        # Cache and save articles run after run
        # https://en.wikipedia.org/wiki/Memoization
        self.memoize_articles = True

        # Set this to false if you don't care about getting images
        self.fetch_images = True
        self.image_dimension_ration = 16 / 9.0

        # Follow meta refresh redirect when downloading
        self.follow_meta_refresh = False

        # Don't toggle this variable, done internally
        self.use_meta_language = True

        # You may keep the html of just the main article body
        self.keep_article_html = False

        # Fail for error responses (e.g. 404 page)
        self.http_success_only = True

        # English is the fallback
        self._language = 'en'

        # Unique stopword classes for oriental languages, don'tcanonical_link toggle
        self.stopwords_class = StopWords

        self.browser_user_agent = 'scraper/%s' % __version__
        self.headers = {}
        self.request_timeout = 120
        self.proxies = {}
        self.number_threads = 10

        self.verbose = False  # for debugging

        self.thread_timeout_seconds = 1
        self.ignored_content_types_defaults = {}
        self.additional_remove_nodes_re = None
        # If Article's url does not match canonical_link after building, regenerate Article with canonical_link instead
        self.use_canonical_link = True

    def get_language(self):
        return self._language

    def del_language(self):
        raise Exception('wtf are you doing?')

    def set_language(self, language):
        """Language setting must be set in this method b/c non-occidental
        (western) languages require a separate stopwords class.
        """
        if not language or len(language) != 2:
            raise Exception("Your input language must be a 2 char language code, \
                for example: english-->en \n and german-->de")

        # If explicitly set language, don't use meta
        self.use_meta_language = False

        # Set oriental language stopword class
        self._language = language.lower()
        self.stopwords_class = self.get_stopwords_class(language)

    def get_json(self):
        return {
            "language": self.get_language()
        }

    language = property(get_language, set_language,
                        del_language, "language prop")

    @staticmethod
    def get_stopwords_class(language):
        if language == 'ko':
            return StopWordsKorean
        elif language == 'hi':
            return StopWordsHindi
        elif language == 'np':
            return StopWordsNepali
        elif language == 'zh':
            return StopWordsChinese
        # Persian and Arabic Share an alphabet
        # There is a persian parser https://github.com/sobhe/hazm, but nltk is likely sufficient
        elif language == 'ar' or language == 'fa':
            return StopWordsArabic
        elif language == 'ja':
            return StopWordsJapanese
        elif language == 'th':
            return StopWordsThai
        return StopWords

    @staticmethod
    def get_parser():
        return Parser


class ArticleConfiguration(Configuration):
    pass


class SourceConfiguration(Configuration):
    pass
