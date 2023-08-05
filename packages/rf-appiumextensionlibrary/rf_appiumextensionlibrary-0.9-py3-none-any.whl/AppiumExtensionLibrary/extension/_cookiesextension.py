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


class _CookiesExtension(
    _ApplicationManagementKeywords
):

    def __init__(self):
        super().__init__()

    def get_cookie(self, name):
        """ Get a single cookie by name. Returns the cookie if found, None if not. \
            (Web context only).

            *AppiumExtensionLibrary Only Keyword.*
        """
        return self._current_application().get_cookie(name)

    def get_cookies(self):
        """ Retrieves all cookies visible to the current page \
            (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        return self._current_application().get_cookies

    def add_cookie(self, **kwargs):
        """ Set a cookie (Web context only).
            Arguments should be given like the example:
            NOTE: ``name`` and ``value`` arguments are required, \
               ``path``, ``domain``, ``expiry`` and ``secure`` \
                   are optional.
            | Set Cookie   | name=_cookieName   | value=someValue |
            | Set Cookie   | name=_cookieName   | value=someValue \
               | path=some/path | domain=.cookie.com |

            *AppiumExtensionLibrary Only Keyword*.
        """
        try:
            self._current_application().add_cookie(kwargs)
        except Exception as err:
            raise err

    def delete_cookie(self, cookieName):
        """ Delete the cookie with the given name (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        try:
            self._current_application().delete_cookie(cookieName)
        except Exception as err:
            raise err

    def delete_all_cookies(self):
        """ Delete the cookie with the given name (Web context only).

            *AppiumExtensionLibrary Only Keyword*.
        """
        self._current_application().delete_all_cookies()
