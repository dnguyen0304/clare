# -*- coding: utf-8 -*-

import abc

import selenium.common
import selenium.webdriver

from nose.tools import (assert_false,
                        assert_is_none,
                        assert_is_not_none,
                        assert_true,
                        raises)

from .. import download_strategies


class MockServerUtilitiesMixin(object):

    __metaclass__ = abc.ABCMeta

    def set_web_driver_page(self, path):
        url = self.construct_url(path=path)
        self.web_driver.get(url=url)

    @staticmethod
    def construct_url(path):
        url = 'http://127.0.0.1:9090/{}/'.format(path)
        return url


class NopDownloadStrategy(download_strategies.Base):

    def do_download(self):
        pass


class TestBase(MockServerUtilitiesMixin):

    def __init__(self):
        self.web_driver = None
        self.strategy = None

    def setup(self):
        self.web_driver = selenium.webdriver.Chrome()
        self.strategy = NopDownloadStrategy(web_driver=self.web_driver,
                                            timeout=None)

    @raises(download_strategies.HttpError)
    def test_download_server_error_raises_http_error(self):
        url = self.construct_url(path='server_error')
        self.strategy.download(url=url)

    @raises(download_strategies.DownloadFailed)
    def test_download_expired_room_raises_download_failed(self):
        url = self.construct_url(path='expired_room')
        self.strategy.download(url=url)

    def test_confirm_rendered_page_title_correct_content(self):
        self.set_web_driver_page(path='title_correct_content')
        self.strategy._confirm_rendered_page(timeout=None)

    @raises(selenium.common.exceptions.TimeoutException)
    def test_confirm_rendered_page_title_incorrect_content(self):
        self.set_web_driver_page(path='title_incorrect_content')
        self.strategy._confirm_rendered_page(timeout=None)

    def test_confirm_server_error_correct_css_selector(self):
        self.set_web_driver_page(path='server_error_correct_css_selector')
        encountered_server_error = self.strategy._confirm_server_error(
            timeout=None)
        assert_false(encountered_server_error)

    def test_confirm_server_error_correct_css_selector_and_content(self):
        self.set_web_driver_page(path='server_error_correct_css_selector_and_content')
        encountered_server_error = self.strategy._confirm_server_error(
            timeout=None)
        assert_true(encountered_server_error)

    def teardown(self):
        self.strategy.dispose()


class TestFindDownloadButton(MockServerUtilitiesMixin):

    def __init__(self):
        self.web_driver = None
        self.timeout = None

    def setup(self):
        self.web_driver = selenium.webdriver.Chrome()

    def test_correct_class_name(self):
        self.set_web_driver_page(path='download_button_correct_class_name')
        download_button = download_strategies.find_download_button(
            web_driver=self.web_driver,
            timeout=self.timeout)
        assert_is_not_none(download_button)

    def test_incorrect_class_name(self):
        self.set_web_driver_page(path='download_button_incorrect_class_name')
        download_button = download_strategies.find_download_button(
            web_driver=self.web_driver,
            timeout=self.timeout)
        assert_is_none(download_button)

    def teardown(self):
        self.web_driver.quit()
