from abc import ABC, abstractmethod

from opencensus.trace.attributes import Attributes
from opencensus.trace.span import BoundedDict
from opencensus.trace.time_event import Annotation


class Event(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def timestamp(self):
        pass

    @property
    @abstractmethod
    def attributes(self):
        pass


class OCEventAdapter(Event):
    def __init__(self, annotation: Annotation):
        self._annotation = annotation

    @property
    def name(self):
        return self._annotation.description

    @property
    def timestamp(self):
        return self._annotation.timestamp

    @property
    def attributes(self):
        if isinstance(self._annotation.attributes, BoundedDict):
            return self._annotation.attributes._dict
        if isinstance(self._annotation.attributes, Attributes):
            return self._annotation.attributes.attributes
        return self._annotation.attributes
