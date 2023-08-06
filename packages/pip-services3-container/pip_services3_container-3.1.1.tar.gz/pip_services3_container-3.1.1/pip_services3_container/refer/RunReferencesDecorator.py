# -*- coding: utf-8 -*-
"""
    pip_services3_container.refer.RunReferencesDecorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Run references decorator implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services3_commons.refer import IReferences
from pip_services3_commons.run import Opener
from pip_services3_commons.run import Closer

from .ReferencesDecorator import ReferencesDecorator

class RunReferencesDecorator(ReferencesDecorator):
    """
    References decorator that automatically opens to newly added components
    that implement IOpenable interface and closes removed components that implement ICloseable interface.
    """
    _opened = False

    def __init__(self, base_references, parent_references):
        """
        Creates a new instance of the decorator.

        :param base_references: the next references or decorator in the chain.

        :param parent_references: the decorator at the top of the chain.
        """
        super(RunReferencesDecorator, self).__init__(base_references, parent_references)


    def is_opened(self):
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self._opened

    def open(self, correlation_id):
        """
        Opens the component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        if not self._opened:
            components = self.get_all()
            Opener.open(correlation_id, components)
            self._opened = True

    def close(self, correlation_id):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        if self._opened:
            components = self.get_all()
            Closer.close(correlation_id, components)
            self._opened = False


    def put(self, locator = None, component = None):
        """
        Puts a new reference into this reference map.

        :param locator: a locator to find the reference by.

        :param component: a component reference to be added.
        """
        super(RunReferencesDecorator, self).put(locator, component)

        if self._opened:
            Opener.open_one(None, component)


    def remove(self, locator):
        """
        Removes a previously added reference that matches specified locator.
        If many references match the locator, it removes only the first one.
        When all references shall be removed, use [[removeAll]] method instead.

        :param locator: a locator to remove reference

        :return: the removed component reference.
        """
        component = super(RunReferencesDecorator, self).remove(locator)

        if self._opened:
            Closer.close_one(None, component)

        return component


    def remove_all(self, locator):
        """
        Removes all component references that match the specified locator.

        :param locator: the locator to remove references by.

        :return: a list, containing all removed references.
        """
        components = super(RunReferencesDecorator, self).remove_all(locator)

        if self._opened:
            Closer.close(None, components)

        return components
