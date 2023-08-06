# -*- coding: utf-8 -*-
"""
    pip_services3_container.config.ContainerConfig
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Container configuration implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services3_commons.config import ConfigParams
from .ComponentConfig import ComponentConfig

class ContainerConfig(list):
    """
    Container configuration defined as a list of component configurations.
    """
    def __init__(self, components = None):
        """
        Creates a new instance of container configuration.

        :param components: (optional) a list of component configurations.
        """
        super(ContainerConfig, self).__init__()
        if components != None:
            for component in components:
                self.append(component)

    @staticmethod
    def from_value(value):
        """
        Creates a new ContainerConfig object filled with key-value pairs from specified object.
        The value is converted into ConfigParams object which is used to create the object.

        :param value: an object with key-value pairs used to initialize a new ContainerConfig.

        :return: a new ContainerConfig object.
        """
        config = ConfigParams.from_value(value)
        return ContainerConfig.from_config(config)

    @staticmethod
    def from_config(config):
        """
        Creates a new ContainerConfig object based on configuration parameters.
        Each section in the configuration parameters is converted into a component configuration.

        :param config: an object with key-value pairs used to initialize a new ContainerConfig.

        :return: a new ContainerConfig object.
        """
        result = ContainerConfig()
        if config == None:
            return result
        
        for section in config.get_section_names():
            component_config = config.get_section(section)
            result.append(ComponentConfig.from_config(component_config))
        
        return result
