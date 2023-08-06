# -*- coding: utf-8 -*-
"""
    pip_services3_container.refer.BuildReferencesDecorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Build references decorator implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services3_commons.refer import IReferences
from pip_services3_commons.refer import Descriptor
from pip_services3_commons.refer import ReferenceException
from pip_services3_components.build import IFactory

from .ReferencesDecorator import ReferencesDecorator

class BuildReferencesDecorator(ReferencesDecorator):
    """
    References decorator that automatically creates missing components using
    available component factories upon component retrival.
    """
    def __init__(self, base_references, parent_references):
        """
        Creates a new instance of the decorator.

        :param base_references: the next references or decorator in the chain.

        :param parent_references: the decorator at the top of the chain.
        """
        super(BuildReferencesDecorator, self).__init__(base_references, parent_references)


    def find_factory(self, locator):
        """
        Finds a factory capable creating component by given descriptor
        from the components registered in the references.

        :param locator: a locator of component to be created.

        :return: found factory or null if factory was not found.
        """
        components = self.get_all()
        for component in components:
            if isinstance(component, IFactory):
                if component.can_create(locator) != None:
                    return component
        return None


    def create(self, locator, factory):
        """
        Creates a component identified by given locator.

        :param locator: a locator to identify component to be created.

        :param factory: a factory that shall create the component.

        :return: the created component.
        """
        if factory == None:
            return None

        try:
            # Create component
            return factory.create(locator)
        except Exception as ex:
            return None


    def clarify_locator(self, locator, factory):
        """
        Clarifies a component locator by merging two descriptors into one to replace missing fields.
        That allows to get a more complete descriptor that includes all possible fields.

        :param locator: a component locator to clarify.

        :param factory: a factory that shall create the component.

        :return: clarified component descriptor (locator)
        """
        if factory == None:
            return locator
        if not isinstance(locator, Descriptor):
            return locator
        
        another_locator = factory.can_create(locator)
        if another_locator == None:
            return locator
        if not isinstance(another_locator, Descriptor):
            return locator
        
        descriptor = locator
        another_descriptor = another_locator
        
        return Descriptor(
            descriptor.get_group() if descriptor.get_group() != None else another_descriptor.get_group(),
            descriptor.get_type() if descriptor.get_type() != None else another_descriptor.get_type(),
            descriptor.get_kind() if descriptor.get_kind() != None else another_descriptor.get_kind(),
            descriptor.get_name() if descriptor.get_name() != None else another_descriptor.get_name(),
            descriptor.get_version() if descriptor.get_version() != None else another_descriptor.get_version()
        )


    def find(self, locator, required):
        """
        Gets all component references that match specified locator.

        :param locator: the locator to find a reference by.

        :param required: forces to raise an exception if no reference is found.

        :return: a list with matching component references.
        """
        components = super(BuildReferencesDecorator, self).find(locator, False)

        # Try to create component
        if len(components) == 0:
            factory = self.find_factory(locator)
            component = self.create(locator, factory)
            if component != None:
                try:
                    locator = self.clarify_locator(locator, factory)
                    self.parent_references.put(locator, component)
                    components.append(component)
                except Exception as ex:
                    # Ignore exception
                    pass

        # Throw exception is no required components found
        if required and len(components) == 0:
            raise ReferenceException(None, locator)

        return components
