import random
from abc import ABC, abstractmethod
from typing import Optional, List, Any, Dict, Union

from ._context import Context
from ._event import OCEventAdapter
from ._span_processor import SpanProcessor
from opencensus.trace import Span as OCSpan, execution_context
from opencensus.trace.span import BoundedDict


class Span(ABC, Context):
    @property
    @abstractmethod
    def parent(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def trace_id(self):
        pass

    @property
    @abstractmethod
    def span_id(self):
        pass

    @property
    @abstractmethod
    def kind(self):
        pass

    @property
    @abstractmethod
    def start_time(self):
        pass

    @property
    @abstractmethod
    def end_time(self):
        pass

    @property
    @abstractmethod
    def attributes(self):
        pass

    @property
    @abstractmethod
    def events(self):
        pass

    @abstractmethod
    def set_attribute(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def add_event(self, name: str, attributes: Dict[str, Any]):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def end(self):
        pass

    @abstractmethod
    def get_context(self) -> Context:
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class OCSpanAdapter(Span):
    def __init__(self, name: str, parent: Optional[Union['OCSpanAdapter', Context]], span_processors: List[SpanProcessor]):
        parent_span = self.__class__._get_parent(parent)
        self._name = name
        self._span = OCSpan(name, parent_span=parent_span, span_id=generate_span_id())
        self._parent = parent
        self._span_processors = span_processors
        self._trace_id = parent.trace_id if parent else generate_trace_id()

    @property
    def parent(self):
        return self._parent

    @property
    def name(self):
        return self._name

    @property
    def trace_id(self):
        return self._trace_id

    @property
    def span_id(self):
        return self._span.span_id

    @property
    def start_time(self):
        return self._span.start_time

    @property
    def end_time(self):
        return self._span.end_time

    @property
    def kind(self):
        return 'Internal'

    @property
    def attributes(self):
        if isinstance(self._span.attributes, BoundedDict):
            return self._span.attributes._dict
        return self._span.attributes

    @property
    def events(self):
        return list(map(OCEventAdapter, self._span.annotations))

    def set_attribute(self, key: str, value: Any) -> None:
        self._span.add_attribute(key, str(value))

    def add_event(self, name: str, attributes: Dict[str, Any]):
        self._span.add_annotation(name, **attributes)

    def start(self):
        if self._span.start_time is not None:
            return

        self._span.start()

        for span_processor in self._span_processors:
            span_processor.on_start(self)

    def set_as_current(self):
        execution_context.set_current_span(self)

    def end(self):
        if self._span.end_time is not None:
            return

        self._span.finish()

        for span_processor in self._span_processors:
            span_processor.on_end(self)

    def set_parent_as_current(self):
        execution_context.set_current_span(self._parent)

    def get_context(self) -> Context:
        return Context(self._trace_id, self._span.span_id)

    def __enter__(self):
        self.set_as_current()
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set_parent_as_current()
        self.end()

    @staticmethod
    def _get_parent(parent: Optional[Union['OCSpanAdapter', Context]]):
        if isinstance(parent, OCSpanAdapter):
            return parent._span
        return parent



def generate_span_id() -> int:
    return random.getrandbits(64)


def generate_trace_id() -> int:
    return random.getrandbits(128)
