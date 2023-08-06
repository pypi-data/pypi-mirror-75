# -*- coding: utf-8 -*-
"""
    pip_services3_container.refer.ReferencesDecorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    References decorator implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services3_commons.refer import IReferences

class ReferencesDecorator(IReferences):
    """
    Chainable decorator for IReferences that allows to inject additional capabilities
    such as automatic component creation, automatic registration and opening.
    """
    base_references = None
    parent_references = None

    def __init__(self, base_references, parent_references):
        """
        Creates a new instance of the decorator.

        :param base_references: the next references or decorator in the chain.

        :param parent_references: the decorator at the top of the chain.
        """
        self.base_references = base_references if base_references != None else parent_references
        self.parent_references = parent_references if parent_references != None else base_references


    def put(self, locator = None, reference = None):
        """
        Puts a new reference into this reference map.

        :param locator: a locator to find the reference by.

        :param component: a component reference to be added.
        """
        self.base_references.put(locator, reference)

    def remove(self, locator):
        """
        Removes a previously added reference that matches specified locator.
        If many references match the locator, it removes only the first one.
        When all references shall be removed, use [[removeAll]] method instead.

        :param locator: a locator to remove reference

        :return: the removed component reference.
        """
        return self.base_references.remove(locator)

    def remove_all(self, locator):
        """
        Removes all component references that match the specified locator.

        :param locator: the locator to remove references by.

        :return: a list, containing all removed references.
        """
        return self.base_references.remove_all(locator)

    def get_all_locators(self):
        """
        Gets locators for all registered component references in this reference map.

        :return: a list with component locators.
        """
        return self.base_references.get_all_locators()

    def get_all(self):
        """
        Gets all component references registered in this reference map.

        :return: a list with component references.
        """
        return self.base_references.get_all()
        
    def get_one_optional(self, locator):
        """
        Gets an optional component reference that matches specified locator.

        :param locator: the locator to find references by.

        :return: a matching component reference or null if nothing was found.
        """
        try:
            components = self.find(locator, False)
            return components[0] if len(components) > 0 else None
        except Exception as ex:
            return None

    def get_one_required(self, locator):
        """
        Gets a required component reference that matches specified locator.

        :param locator: the locator to find a reference by.

        :return: a matching component reference.

        :raises: a [[ReferenceException]] when no references found.
        """
        components = self.find(locator, True)
        return components[0] if len(components) > 0 else None

    def get_optional(self, locator):
        """
        Gets all component references that match specified locator.

        :param locator: the locator to find references by.

        :return: a list with matching component references or empty list if nothing was found.
        """
        try:
            return self.find(locator, False)
        except Exception as ex:
            return []

    def get_required(self, locator):
        """
        Gets all component references that match specified locator.
        At least one component reference must be present. If it doesn't the method throws an error.

        :param locator: the locator to find references by.

        :return: a list with matching component references.

        :raises: a [[ReferenceException]] when no references found.
        """
        return self.find(locator, True)

    def find(self, locator, required):
        """
        Gets all component references that match specified locator.

        :param locator: the locator to find a reference by.

        :param required: forces to raise an exception if no reference is found.

        :return: a list with matching component references.

        :raises: a [[ReferenceException]] when required is set to true but no references found.
        """
        return self.base_references.find(locator, required)
