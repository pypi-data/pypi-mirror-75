# Copyright (C) 2019 Shiela Buitizon | Joshua Kim Rivera

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from AppiumLibrary import _ApplicationManagementKeywords


class _BrowserExtension(
    _ApplicationManagementKeywords
):

    def switch_window(self, window):
        """ Change focus to another window (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        self._current_application().switch_to.window(window)

    def close_window(self):
        """ Closes the current window (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        self._current_application().close()

    def get_current_window_handle(self):
        """ Retrieves the current window handle (Web context only).
            Returns the window handle as string.

            *AppiumExtensionLibrary Only Keyword*.
        """
        return self._current_application().current_window_handle

    def get_window_handles(self):
        """ Retrieves the list of all window handles available to \
            the session (Web context only).
            Returns a list if there are more than one window active.

            *AppiumExtensionLibrary Only Keyword*.
        """
        return self._current_application().window_handles

    def get_title(self):
        """ Get the current page title (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        return self._current_application().title

    def get_location(self):
        """ Retrieve the URL of the current page (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        return self._current_application().current_url

    def reload_page(self):
        """ Refreshes the current page. (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        self._current_application().refresh()

    def go_to(self, url):
        """ Opens URL in default web browser.

            Example:
            | Open Application  | http://localhost:4755/wd/hub | platformName=iOS | platformVersion=7.0 | deviceName='iPhone Simulator' | browserName=Safari |
            | Go To URL         | http://m.webapp.com          |

            *AppiumExtensionLibrary Only Keyword*.
        """
        self.go_to_url(url)
