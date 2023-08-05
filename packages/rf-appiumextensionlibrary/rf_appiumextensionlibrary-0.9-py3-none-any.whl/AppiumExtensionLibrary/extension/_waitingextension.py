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

from AppiumLibrary import (
    _ApplicationManagementKeywords,
    _WaitingKeywords
)


class _WaitingExtension(
    _ApplicationManagementKeywords,
    _WaitingKeywords
):

    def __init__(self):
        super().__init__()

    def wait_until_location_is(self, expected, timeout=None, case_sensitive=True):
        """Waits until the current URL is ``expected``.

            Ignores case when ```case_sensitive``` is False (default is True).

            The ``expected`` argument is the expected value in url.

            Fails if ``timeout`` expires before the location is. See
            the `Timeouts` section for more information about using timeouts
            and their default value.

            *AppiumExtensionLibrary Only Keyword*.
        """
        current_url = self._current_application().current_url.lower() if not case_sensitive \
            else self._current_application().current_url
        expected_url = str(expected).lower() if not case_sensitive else str(expected)
        self._wait_until(timeout, "Location did equal '%s' in <TIMEOUT>." % expected,
                         lambda: expected_url == current_url)
