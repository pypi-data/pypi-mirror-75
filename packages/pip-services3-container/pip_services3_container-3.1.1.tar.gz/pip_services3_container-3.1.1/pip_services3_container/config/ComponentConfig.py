# -*- coding: utf-8 -*-
"""
    pip_services3_container.config.ComponentConfig
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Component configuration implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services3_commons.reflect import TypeDescriptor
from pip_services3_commons.refer import Descriptor
from pip_services3_commons.errors import ConfigException

class ComponentConfig():
    """
    Configuration of a component inside a container.

    The configuration includes type information or descriptor, and component configuration parameters.
    """
    descriptor = None
    type = None
    config = None

    def __init__(self, descriptor = None, type = None, config = None):
        """
        Creates a new instance of the component configuration.

        :param descriptor: (optional) a components descriptor (locator).

        :param type: (optional) a components type descriptor.

        :param config: (optional) component configuration parameters.
        """
        self.descriptor = descriptor
        self.type = type
        self.config = config

    @staticmethod
    def from_config(config):
        """
        Creates a new instance of ComponentConfig based on section from container configuration.

        :param config: component parameters from container configuration

        :return: a newly created ComponentConfig
        """
        descriptor = Descriptor.from_string(config.get_as_nullable_string("descriptor"))
        type = TypeDescriptor.from_string(config.get_as_nullable_string("type"))
        
        if descriptor == None and type == None:
            raise ConfigException(None, "BAD_CONFIG", "Component configuration must have descriptor or type")
        
        return ComponentConfig(descriptor, type, config)
