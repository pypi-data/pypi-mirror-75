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

from robot.utils import is_truthy, plural_or_not as s

from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebElement

from AppiumLibrary import (
        _ElementKeywords
    )


class _SelectElement(_ElementKeywords):

    def get_list_items(self, locator, values=False):
        """Returns all labels or values of selection list ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        Returns visible labels by default, but values can be returned by
        setting the ``values`` argument to a true value (see `Boolean
        arguments`).

        Example:
        | ${labels} = | `Get List Items` | mylist              |             |
        | ${values} = | `Get List Items` | css=#example select | values=True |

        Web Context Only.

        New in AppiumExtensionLibrary 0.9.

        *AppiumExtensionLibrary Only Keyword*.
        """
        options = self._get_options(locator)
        if is_truthy(values):
            return self._get_values(options)
        else:
            return self._get_labels(options)

    def get_selected_list_label(self, locator):
        """Returns the label of selected option from selection list ``locator``.

        If there are multiple selected options, the label of the first option
        is returned.

        See the `Locating elements` section for details about the locator
        syntax.

        Web Context Only.

        New in AppiumExtensionLibrary 0.9.

        *AppiumExtensionLibrary Only Keyword*.
        """
        select = self._get_select_list(locator)
        return select.first_selected_option.text

    def get_selected_list_labels(self, locator):
        """Returns labels of selected options from selection list ``locator``.

        Returns an empty list if there
        are no selections. In earlier versions, this caused an error.

        See the `Locating elements` section for details about the locator
        syntax.

        Web Context Only.

        New in AppiumExtensionLibrary 0.9.

        *AppiumExtensionLibrary Only Keyword*.
        """
        options = self._get_selected_options(locator)
        return self._get_labels(options)

    def get_selected_list_value(self, locator):
        """Returns the value of selected option from selection list ``locator``.

        If there are multiple selected options, the value of the first option
        is returned.

        See the `Locating elements` section for details about the locator
        syntax.

        Web Context Only.

        New in AppiumExtensionLibrary 0.9.

        *AppiumExtensionLibrary Only Keyword*.
        """
        select = self._get_select_list(locator)
        return select.first_selected_option.get_attribute('value')

    def get_selected_list_values(self, locator):
        """Returns values of selected options from selection list ``locator``.

        Returns an empty list if there
        are no selections. In earlier versions, this caused an error.

        See the `Locating elements` section for details about the locator
        syntax.

        Web Context Only.

        New in AppiumExtensionLibrary 0.9.

        *AppiumExtensionLibrary Only Keyword*.
        """
        options = self._get_selected_options(locator)
        return self._get_values(options)

    def list_selection_should_be(self, locator, *expected):
        """Verifies selection list ``locator`` has ``expected`` options selected.

        It is possible to give expected options both as visible labels and
        as values. Mixing labels and
        values is not possible. Order of the selected options is not
        validated.

        If no expected options are given, validates that the list has
        no selections. A more explicit alternative is using `List Should
        Have No Selections`.

        See the `Locating elements` section for details about the locator
        syntax.

        Examples:
        | `List Selection Should Be` | gender    | Female          |        |
        | `List Selection Should Be` | interests | Test Automation | Python |

        Web Context Only.

        New in AppiumExtensionLibrary 0.9.

        *AppiumExtensionLibrary Only Keyword*.
        """
        self._info("Verifying list '%s' has option%s [ %s ] selected."
                   % (locator, s(expected), ' | '.join(expected)))
        self.page_should_contain_list(locator)
        options = self._get_selected_options(locator)
        labels = self._get_labels(options)
        values = self._get_values(options)
        if sorted(expected) not in [sorted(labels), sorted(values)]:
            raise AssertionError("List '%s' should have had selection [ %s ] "
                                 "but selection was [ %s ]."
                                 % (locator, ' | '.join(expected),
                                    self._format_selection(labels, values)))

    def _format_selection(self, labels, values):
        return ' | '.join('%s (%s)' % (label, value)
                          for label, value in zip(labels, values))

    def list_should_have_no_selections(self, locator):
        """Verifies selection list ``locator`` has no options selected.

        See the `Locating elements` section for details about the locator
        syntax.

        Web Context Only.

        New in AppiumExtensionLibrary 0.9.

        *AppiumExtensionLibrary Only Keyword*.
        """
        self._info("Verifying list '%s' has no selections." % locator)
        options = self._get_selected_options(locator)
        if options:
            selection = self._format_selection(self._get_labels(options),
                                               self._get_values(options))
            raise AssertionError("List '%s' should have had no selection "
                                 "but selection was [ %s ]."
                                 % (locator, selection))

    def page_should_contain_list(self, locator, message=None, loglevel='TRACE'):
        """Verifies selection list ``locator`` is found from current page.

        See `Page Should Contain Element` for an explanation about ``message``
        and ``loglevel`` arguments.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.page_should_contain_element(locator, loglevel)

    def select_from_list_by_index(self, locator, *indexes):
        """Selects options from selection list ``locator`` by ``indexes``.

        Indexes of list options start from 0.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        Web Context Only.

        New in AppiumExtensionLibrary 0.9.

        *AppiumExtensionLibrary Only Keyword*.
        """
        if not indexes:
            raise ValueError("No indexes given.")
        self._html("Selecting options from selection list '%s' by index%s %s."
                   % (locator, '' if len(indexes) == 1 else 'es',
                      ', '.join(indexes)))
        select = self._get_select_list(locator)
        for index in indexes:
            select.select_by_index(int(index))

    def select_from_list_by_value(self, locator, *values):
        """Selects options from selection list ``locator`` by ``values``.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.

        Web Context Only.

        New in AppiumExtensionLibrary 0.9.

        *AppiumExtensionLibrary Only Keyword*.
        """
        if not values:
            raise ValueError("No values given.")
        self._info("Selecting options from selection list '%s' by value%s %s."
                   % (locator, s(values), ', '.join(values)))
        select = self._get_select_list(locator)
        for value in values:
            select.select_by_value(value)

    def select_from_list_by_label(self, locator, *labels):
        """Selects options from selection list ``locator`` by ``labels``.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.

        Web Context Only.

        New in AppiumExtensionLibrary 0.9.

        *AppiumExtensionLibrary Only Keyword*.
        """
        if not labels:
            raise ValueError("No labels given.")
        self._info("Selecting options from selection list '%s' by label%s %s."
                   % (locator, s(labels), ', '.join(labels)))
        select = self._get_select_list(locator)
        for label in labels:
            select.select_by_visible_text(label)

    def _get_select_list(self, locator):
        el = self._element_find(locator, False, True, tag='list')
        # if not self._is_webelement(el):
        #     el = WebElement(el)
        return Select(el[0])

    def _get_options(self, locator):
        return self._get_select_list(locator).options

    def _get_selected_options(self, locator):
        return self._get_select_list(locator).all_selected_options

    def _get_labels(self, options):
        return [opt.text for opt in options]

    def _get_values(self, options):
        return [opt.get_attribute('value') for opt in options]

    def _is_webelement(self, element):
        # Hook for unit tests
        return isinstance(element, (WebElement, EventFiringWebElement))
