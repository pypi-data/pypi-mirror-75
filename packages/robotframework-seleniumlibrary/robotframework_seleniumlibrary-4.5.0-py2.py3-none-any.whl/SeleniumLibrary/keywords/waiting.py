# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time

from selenium.common.exceptions import StaleElementReferenceException

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.errors import ElementNotFound
from SeleniumLibrary.utils import is_noney, secs_to_timestr


class WaitingKeywords(LibraryComponent):

    @keyword
    def wait_for_condition(self, condition, timeout=None, error=None):
        """Waits until ``condition`` is true or ``timeout`` expires.

        The condition can be arbitrary JavaScript expression but it
        must return a value to be evaluated. See `Execute JavaScript` for
        information about accessing content on pages.

        Fails if the timeout expires before the condition becomes true. See
        the `Timeouts` section for more information about using timeouts
        and their default value.

        ``error`` can be used to override the default error message.

        Examples:
        | `Wait For Condition` | return document.title == "New Title" |
        | `Wait For Condition` | return jQuery.active == 0            |
        | `Wait For Condition` | style = document.querySelector('h1').style; return style.background == "red" && style.color == "white" |
        """
        if 'return' not in condition:
            raise ValueError("Condition '%s' did not have mandatory 'return'."
                             % condition)
        self._wait_until(
            lambda: self.driver.execute_script(condition) is True,
            "Condition '%s' did not become true in <TIMEOUT>." % condition,
            timeout, error
        )

    @keyword
    def wait_until_location_is(self, expected, timeout=None, message=None):
        """Waits until the current URL is ``expected``.

        The ``expected`` argument is the expected value in url.

        Fails if ``timeout`` expires before the location is. See
        the `Timeouts` section for more information about using timeouts
        and their default value.

        The ``message`` argument can be used to override the default error
        message.

        New in SeleniumLibrary 4.0
        """

        expected = str(expected)
        self._wait_until(lambda: expected == self.driver.current_url,
                         "Location did not become '%s' in <TIMEOUT>." % expected,
                         timeout, message)

    @keyword
    def wait_until_location_is_not(self, location, timeout=None, message=None):
        """Waits until the current URL is not ``location``.

        The ``location`` argument is the unexpected value in url.

        Fails if ``timeout`` expires before the location is not. See
        the `Timeouts` section for more information about using timeouts
        and their default value.

        The ``message`` argument can be used to override the default error
        message.

        New in SeleniumLibrary 4.3
        """
        location = str(location)
        self._wait_until(lambda: location != self.driver.current_url,
                         "Location is '%s' in <TIMEOUT>." % location,
                         timeout, message)

    @keyword
    def wait_until_location_contains(self, expected, timeout=None, message=None):
        """Waits until the current URL contains ``expected``.

        The ``expected`` argument contains the expected value in url.

        Fails if ``timeout`` expires before the location contains. See
        the `Timeouts` section for more information about using timeouts
        and their default value.

        The ``message`` argument can be used to override the default error
        message.

        New in SeleniumLibrary 4.0
        """
        expected = str(expected)
        self._wait_until(lambda: expected in self.driver.current_url,
                         "Location did not contain '%s' in <TIMEOUT>." % expected,
                         timeout, message)

    @keyword
    def wait_until_location_does_not_contain(self, location, timeout=None, message=None):
        """Waits until the current URL does not contains ``location``.

        The ``location`` argument contains value not expected in url.

        Fails if ``timeout`` expires before the location not contains. See
        the `Timeouts` section for more information about using timeouts
        and their default value.

        The ``message`` argument can be used to override the default error
        message.

        New in SeleniumLibrary 4.3
        """
        location = str(location)
        self._wait_until(lambda: location not in self.driver.current_url,
                         "Location did contain '%s' in <TIMEOUT>." % location,
                         timeout, message)

    @keyword
    def wait_until_page_contains(self, text, timeout=None, error=None):
        """Waits until ``text`` appears on the current page.

        Fails if ``timeout`` expires before the text appears. See
        the `Timeouts` section for more information about using timeouts
        and their default value.

        ``error`` can be used to override the default error message.
        """
        self._wait_until(lambda: self.is_text_present(text),
                         "Text '%s' did not appear in <TIMEOUT>." % text,
                         timeout, error)

    @keyword
    def wait_until_page_does_not_contain(self, text, timeout=None,
                                         error=None):
        """Waits until ``text`` disappears from the current page.

        Fails if ``timeout`` expires before the text disappears. See
        the `Timeouts` section for more information about using timeouts
        and their default value.

        ``error`` can be used to override the default error message.
        """
        self._wait_until(lambda: not self.is_text_present(text),
                         "Text '%s' did not disappear in <TIMEOUT>." % text,
                         timeout, error)

    @keyword
    def wait_until_page_contains_element(self, locator, timeout=None,
                                         error=None, limit=None):
        """Waits until the element ``locator`` appears on the current page.

        Fails if ``timeout`` expires before the element appears. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.

        The ``limit`` argument can used to define how many elements the
        page should contain. When ``limit`` is `None` (default) page can
        contain one or more elements. When limit is a number, page must
        contain same number of elements.

        ``limit`` is new in SeleniumLibrary 4.4
        """
        if is_noney(limit):
            return self._wait_until(
                lambda: self.find_element(locator, required=False) is not None,
                "Element '%s' did not appear in <TIMEOUT>." % locator,
                timeout, error
            )
        limit = int(limit)
        self._wait_until(
            lambda: len(self.find_elements(locator)) == limit,
            'Page should have contained "%s" %s element(s) within <TIMEOUT>.' % (limit, locator),
            timeout, error
        )

    @keyword
    def wait_until_page_does_not_contain_element(self, locator, timeout=None,
                                                 error=None, limit=None):
        """Waits until the element ``locator`` disappears from the current page.

        Fails if ``timeout`` expires before the element disappears. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.

        The ``limit`` argument can used to define how many elements the
        page should not contain. When ``limit`` is `None` (default) page can`t
        contain any elements. When limit is a number, page must not
        contain same number of elements.

        ``limit`` is new in SeleniumLibrary 4.4
        """
        if is_noney(limit):
            return self._wait_until(
                lambda: self.find_element(locator, required=False) is None,
                "Element '%s' did not disappear in <TIMEOUT>." % locator,
                timeout, error
            )
        limit = int(limit)
        self._wait_until(
            lambda: len(self.find_elements(locator)) != limit,
            'Page should have not contained "%s" %s element(s) within <TIMEOUT>.' % (limit, locator),
            timeout, error
        )

    @keyword
    def wait_until_element_is_visible(self, locator, timeout=None,
                                      error=None):
        """Waits until the element ``locator`` is visible.

        Fails if ``timeout`` expires before the element is visible. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.
        """
        self._wait_until(
            lambda: self.is_visible(locator),
            "Element '%s' not visible after <TIMEOUT>." % locator,
            timeout, error
        )

    @keyword
    def wait_until_element_is_not_visible(self, locator, timeout=None,
                                          error=None):
        """Waits until the element ``locator`` is not visible.

        Fails if ``timeout`` expires before the element is not visible. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.
        """
        self._wait_until(
            lambda: not self.is_visible(locator),
            "Element '%s' still visible after <TIMEOUT>." % locator,
            timeout, error
        )

    @keyword
    def wait_until_element_is_enabled(self, locator, timeout=None,
                                      error=None):
        """Waits until the element ``locator`` is enabled.

        Element is considered enabled if it is not disabled nor read-only.

        Fails if ``timeout`` expires before the element is enabled. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.

        Considering read-only elements to be disabled is a new feature
        in SeleniumLibrary 3.0.
        """
        self._wait_until(
            lambda: self.is_element_enabled(locator),
            "Element '%s' was not enabled in <TIMEOUT>." % locator,
            timeout, error
        )

    @keyword
    def wait_until_element_contains(self, locator, text, timeout=None,
                                    error=None):
        """Waits until the element ``locator`` contains ``text``.

        Fails if ``timeout`` expires before the text appears. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.
        """
        self._wait_until(
            lambda: text in self.find_element(locator).text,
            "Element '%s' did not get text '%s' in <TIMEOUT>." % (locator, text),
            timeout, error
        )

    @keyword
    def wait_until_element_does_not_contain(self, locator, text, timeout=None,
                                            error=None):
        """Waits until the element ``locator`` does not contain ``text``.

        Fails if ``timeout`` expires before the text disappears. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.
        """
        self._wait_until(
            lambda: text not in self.find_element(locator).text,
            "Element '%s' still had text '%s' after <TIMEOUT>." % (locator, text),
            timeout, error
        )

    def _wait_until(self, condition, error, timeout=None, custom_error=None):
        timeout = self.get_timeout(timeout)
        if is_noney(custom_error):
            error = error.replace('<TIMEOUT>', secs_to_timestr(timeout))
        else:
            error = custom_error
        self._wait_until_worker(condition, timeout, error)

    def _wait_until_worker(self, condition, timeout, error):
        max_time = time.time() + timeout
        not_found = None
        while time.time() < max_time:
            try:
                if condition():
                    return
            except ElementNotFound as err:
                not_found = str(err)
            except StaleElementReferenceException as err:
                self.info('Suppressing StaleElementReferenceException from Selenium.')
                not_found = err
            else:
                not_found = None
            time.sleep(0.2)
        raise AssertionError(not_found or error)
