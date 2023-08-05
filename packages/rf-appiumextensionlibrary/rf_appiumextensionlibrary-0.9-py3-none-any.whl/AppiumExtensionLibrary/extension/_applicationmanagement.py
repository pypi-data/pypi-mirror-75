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

import os

from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.keys import Keys

from collections import namedtuple
from AppiumLibrary import (
    _ApplicationManagementKeywords,
    _ElementKeywords
    )


class _ApplicationManagementExtension(
    _ApplicationManagementKeywords,
    _ElementKeywords
):

    js_marker = 'JAVASCRIPT'
    arg_marker = 'ARGUMENTS'

    def __init__(self):
        super().__init__()

    @staticmethod
    def _log(*args, **kwargs):
        BuiltIn().log(*args, **kwargs)

    def execute_javascript(self, *code):
        """ Executes the given JavaScript code with possible arguments.

            ``code`` may be divided into multiple cells in the test data and
            ``code`` may contain multiple lines of code and arguments. In that case,
            the JavaScript code parts are concatenated together without adding
            spaces and optional arguments are separated from ``code``.

            If ``code`` is a path to an existing file, the JavaScript
            to execute will be read from that file. Forward slashes work as
            a path separator on all operating systems.

            The JavaScript executes in the context of the currently selected
            frame or window as the body of an anonymous function. Use ``window``
            to refer to the window of your application and ``document`` to refer
            to the document object of the current frame or window, e.g.
            ``document.getElementById('example')``.

            This keyword returns whatever the executed JavaScript code returns.
            Return values are converted to the appropriate Python types.

            Starting from SeleniumLibrary 3.2 it is possible to provide JavaScript
            [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#selenium.webdriver.remote.webdriver.WebDriver.execute_script|
            arguments] as part of ``code`` argument. The JavaScript code and
            arguments must be separated with `JAVASCRIPT` and `ARGUMENTS` markers
            and must be used exactly with this format. If the Javascript code is
            first, then the `JAVASCRIPT` marker is optional. The order of
            `JAVASCRIPT` and `ARGUMENTS` markers can be swapped, but if `ARGUMENTS`
            is the first marker, then `JAVASCRIPT` marker is mandatory. It is only
            allowed to use `JAVASCRIPT` and `ARGUMENTS` markers only one time in the
            ``code`` argument.

            Examples:
            | `Execute JavaScript` | window.myFunc('arg1', 'arg2') |
            | `Execute JavaScript` | ${CURDIR}/js_to_execute.js    |
            | `Execute JavaScript` | alert(arguments[0]); | ARGUMENTS | 123 |
            | `Execute JavaScript` | ARGUMENTS | 123 | JAVASCRIPT | alert(arguments[0]); |

            *AppiumExtensionLibrary Only Keyword*.
        """
        js_code, js_args = self._get_javascript_to_execute(code)
        return self._current_application().execute_script(js_code, *js_args)

    def element_execute_javascript(self, locator, *code):
        """ Executes the given JavaScript code given using locator element

            Similar to `Execute Javascript` except that keyword accepts locator parameter
            and can use locator element in javascript command.

            ``code`` may be divided into multiple cells in the test data and
            ``code`` may contain multiple lines of code and arguments. In that case,
            the JavaScript code parts are concatenated together without adding
            spaces and optional arguments are separated from ``code``.

            If ``code`` is a path to an existing file, the JavaScript
            to execute will be read from that file. Forward slashes work as
            a path separator on all operating systems.

            The JavaScript executes in the context of the currently selected
            frame or window as the body of an anonymous function. Use ``window``
            to refer to the window of your application and ``document`` to refer
            to the document object of the current frame or window, e.g.
            ``document.getElementById('example')``.

            This keyword returns whatever the executed JavaScript code returns.
            Return values are converted to the appropriate Python types.

            Starting from SeleniumLibrary 3.2 it is possible to provide JavaScript
            [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#selenium.webdriver.remote.webdriver.WebDriver.execute_script|
            arguments] as part of ``code`` argument. The JavaScript code and
            arguments must be separated with `JAVASCRIPT` and `ARGUMENTS` markers
            and must be used exactly with this format. If the Javascript code is
            first, then the `JAVASCRIPT` marker is optional. The order of
            `JAVASCRIPT` and `ARGUMENTS` markers can be swapped, but if `ARGUMENTS`
            is the first marker, then `JAVASCRIPT` marker is mandatory. It is only
            allowed to use `JAVASCRIPT` and `ARGUMENTS` markers only one time in the
            ``code`` argument.

            Examples:
            | `Execute JavaScript` | css=#id | | ${CURDIR}/js_to_execute.js | ARGUMENTS | 123 |

            Sample ${CURDIR}/js_to_execute.js file:

            ``arguments[0].value=arguments[1]``

            *AppiumExtensionLibrary Only Keyword*.
        """

        element = self._element_find(locator, True, True)
        self._log("Element " + str(element))

        js_code, js_args = self._get_javascript_to_execute(code)
        actual_js_args = list()
        actual_js_args.append(element)
        actual_js_args += js_args
        return self._current_application().execute_script(js_code, *actual_js_args)

    def input_text(self, locator, text, clear=True, events=False):
        """ Types the given ``text`` into the text field identified by ``locator``.

            When ``clear`` is true, the input element is cleared before
            the text is typed into the element. When false, the previous text
            is not cleared from the element. Use `Input Password` if you
            do not want the given ``text`` to be logged.

            When ``events`` is true, ``focus`` is triggered before and ``blur`` is triggered after input on field.
            Also, if ``event`` is true, text deletion is via send keys (CRTL+a,DELETE)

            If [https://github.com/SeleniumHQ/selenium/wiki/Grid2|Selenium Grid]
            is used and the ``text`` argument points to a file in the file system,
            then this keyword prevents the Selenium to transfer the file to the
            Selenium Grid hub. Instead, this keyword will send the ``text`` string
            as is to the element. If a file should be transferred to the hub and
            upload should be performed, please use `Choose File` keyword.

            See the `Locating elements` section for details about the locator
            syntax. See the `Boolean arguments` section how Boolean values are
            handled.

            Disabling the file upload the Selenium Grid node and the `clear`
            argument are new in SeleniumLibrary 4.0

            *AppiumExtensionLibrary Only Keyword*.
        """
        self._input_text_into_text_field(locator, text, clear, events)

    def _input_text_into_text_field(self, locator, text, clear, events):
        element = self._element_find(locator, True, True)
        self._log("Element " + str(element))

        if events:
            self._log("Element focus")
            self._current_application().execute_script("arguments[0].focus();", element)

        if events and clear:
            self._log("Element clear by send keys")
            element.send_keys(Keys.CONTROL, 'a')
            element.send_keys(Keys.DELETE)
        elif clear:
            self._log("Element cleared by js")
            self._current_application().execute_script("arguments[0].value='';", element)

        if text:
            self._log(f"Element sendkeys *{text}*")
            element.send_keys(str(text))
        if events:
            self._log("Element onblur")
            self._current_application().execute_script("arguments[0].blur();", element)

    def _get_javascript_to_execute(self, code):
        js_code, js_args = self._separate_code_and_args(code)
        if not js_code:
            raise ValueError('JavaScript code was not found from code argument.')
        js_code = ''.join(js_code)
        path = js_code.replace('/', os.sep)
        if os.path.isfile(path):
            js_code = self._read_javascript_from_file(path)
        return js_code, js_args

    def _separate_code_and_args(self, code):
        code = list(code)
        self._check_marker_error(code)
        index = self._get_marker_index(code)
        if self.arg_marker not in code:
            return code[index.js + 1:], []
        if self.js_marker not in code:
            return code[0:index.arg], code[index.arg + 1:]
        else:
            if index.js == 0:
                return code[index.js + 1:index.arg], code[index.arg + 1:]
            else:
                return code[index.js + 1:], code[index.arg + 1:index.js]

    def _check_marker_error(self, code):
        if not code:
            raise ValueError('There must be at least one argument defined.')
        message = None
        template = '%s marker was found two times in the code.'
        if code.count(self.js_marker) > 1:
            message = template % self.js_marker
        if code.count(self.arg_marker) > 1:
            message = template % self.arg_marker
        index = self._get_marker_index(code)
        if index.js > 0 and index.arg != 0:
            message = template % self.js_marker
        if message:
            raise ValueError(message)

    def _get_marker_index(self, code):
        Index = namedtuple('Index', 'js arg')
        if self.js_marker in code:
            js = code.index(self.js_marker)
        else:
            js = -1
        if self.arg_marker in code:
            arg = code.index(self.arg_marker)
        else:
            arg = -1
        return Index(js=js, arg=arg)

    def _read_javascript_from_file(self, path):
        self._log('Reading JavaScript from file %s.' % path.replace(os.sep, '/'))
        with open(path) as file:
            return file.read().strip()
