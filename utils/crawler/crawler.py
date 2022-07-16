#/usr/bin/env python
# -*- coding:utf-8 -*-
from unittest import result
from urllib.error import URLError
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver

HEADERS = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}


# HEADERS = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

class Crawler:
    """
    A class used to represent an Crawler machine

    ...

    Attributes
    ----------
    url : str
        The current url that crawler is scraping from
    raw_html : str
        The whole html content of the page that crawler
        scrapes

    Methods
    -------
    get_raw_content(url)
        Get all html component of a page from given url
        then assign it to raw_html attribute
    get_tags_by_css_selector(content, css_selector)
        Find element by css selector in content
    """
    def __init__(self):
        self.url = ''
        self.raw_html = ''

    def get_raw_content(self, url=None):
        """
            Get all html component of a page from given url

            * Consists of:
                . tags: The html tag
                . contents: The text of each tag
                . attributes: The attribute inside tag

            Parameters
            ----------
            url : str
                The current url that crawler is scraping from
            
            Returns
            -------
            True
                If crawling is successful
            Fale 
                If crawling is fail (URLError)
            
            Raises
            ------
            NotImplementedError
                If no url is set or passed in as a parameter
        """
        if url is None:
            raise NotImplementedError("Url is invalid, it can't be None type")
        self.url = url
        try:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome()
            driver.get(url=self.url)
            # responses = requests.get(url=self.url, headers=HEADERS)

        except URLError as url_error:
            print("Server Not Found, invalid url")
            return False
        else:
            # print("Access successfully!")
            # self.raw_html = BeautifulSoup(responses.content, "html.parser")
            self.raw_html = driver
            return True

    # def get_tags_by_xpath(self) -> list:
    #     '''
    #         Find elements by xpath
    #     '''
    #     pass
    
    def get_tags_by_css_selector(self, content=None, css_selector=None):
        """
            Find elements by css selector. If content is None, find through 
            the raw_html.

            Parameters
            ----------
            content : Selenium element
                The raw scraped content of the page (Default is None)
            css_selector : str
                The css selector that is condition to find elements
                (Default is None)

            Returns
            -------
            list
                List of tags which founded by css_selector
            int
                The number of tags are founded
            
            Raises
            ------
            NotImplementedError
                If no css_selector is set or passed in as a parameter
        """
        if css_selector is None:
            raise NotImplementedError('Invalid conditions')
        if content is None:
            content = self.raw_html
        # result = content.select(css_selector)
        result = content.find_elements_by_css_selector(css_selector)
        return result

# if __name__ == "__main__":
#     bs4_crawler = Crawler('https://quotes.toscrape.com/')
#     result = bs4_crawler.get_tags_by_css_selector(None,'.quote')

#     print(result)