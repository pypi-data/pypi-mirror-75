# -*- coding: utf-8 -*-
"""
    pip_services3_container.refer.LinkReferencesDecorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Link references decorator implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services3_commons.refer import IReferences
from pip_services3_commons.refer import Referencer
from pip_services3_commons.run import IOpenable

from .ReferencesDecorator import ReferencesDecorator

class LinkReferencesDecorator(ReferencesDecorator, IOpenable):
    """
    References decorator that automatically sets references to newly added components
    that implement IReferenceable interface and unsets references
    from removed components that implement IUnreferenceable interface.
    """
    _opened = False

    def __init__(self, base_references, parent_references):
        """
        Creates a new instance of the decorator.

        :param base_references: the next references or decorator in the chain.

        :param parent_references: the decorator at the top of the chain.
        """
        super(LinkReferencesDecorator, self).__init__(base_references, parent_references)


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
            Referencer.set_references(self.parent_references, components)
            self._opened = True

    def close(self, correlation_id):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        if self._opened:
            components = self.get_all()
            Referencer.unset_references(components)
            self._opened = False


    def put(self, locator = None, component = None):
        """
        Puts a new reference into this reference map.

        :param locator: a locator to find the reference by.

        :param component: a component reference to be added.
        """
        super(LinkReferencesDecorator, self).put(locator, component)

        if self._opened:
            Referencer.set_references_for_one(self.parent_references, component)


    def remove(self, locator):
        """
        Removes a previously added reference that matches specified locator.
        If many references match the locator, it removes only the first one.
        When all references shall be removed, use [[removeAll]] method instead.

        :param locator: a locator to remove reference

        :return: the removed component reference.
        """
        component = super(LinkReferencesDecorator, self).remove(locator)

        if self._opened:
            Referencer.unset_references_for_one(component)

        return component


    def remove_all(self, locator):
        """
        Removes all component references that match the specified locator.

        :param locator: the locator to remove references by.

        :return: a list, containing all removed references.
        """
        components = super(LinkReferencesDecorator, self).remove_all(locator)

        if self._opened:
            Referencer.unset_references(components)

        return components
