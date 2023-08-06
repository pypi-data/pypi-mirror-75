import abc


class FeatureBase(metaclass=abc.ABCMeta):
    """
    Base class for all instrument features.
    """

    def get_feature(self, resource_manager, resource_name):
        self.resource_name = resource_name
        self.resource_manager = resource_manager
        return self.feature

    @abc.abstractmethod
    def feature(self, *args, **kwgs):
        """Implements a visa query feature"""
