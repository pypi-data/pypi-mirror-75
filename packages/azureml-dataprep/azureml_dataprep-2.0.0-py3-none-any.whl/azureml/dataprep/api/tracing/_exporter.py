import json
import os
from abc import ABC, abstractmethod
from typing import Optional, Sequence

from opencensus.trace.span_context import SpanContext
from opencensus.trace.span_data import SpanData

from ._span import Span
from ._event import Event

logger = None


def get_logger():
    from azureml.dataprep.api._loggerfactory import _LoggerFactory

    global logger
    if logger is not None:
        return logger

    logger = _LoggerFactory.get_logger("JsonLineExporter")
    return logger


class SpanExporter(ABC):
    @abstractmethod
    def export(self, spans: Sequence[Span]) -> None:
        pass

    @abstractmethod
    def shutdown(self) -> None:
        pass


class JsonLineExporter(SpanExporter):
    def __init__(self, session_id: str, base_directory: Optional[str] = None):
        path = os.path.join(base_directory, 'python_span_{}.jsonl'.format(session_id))
        self._file = open(path, 'w')

    def export(self, spans: Sequence[Span]) -> None:
        json_lines = '\n'.join(map(self.__class__.to_json, spans))
        self._file.write('{}\n'.format(json_lines))
        self._file.flush()

    def shutdown(self) -> None:
        self._file.close()

    @staticmethod
    def to_json(span_data: Span) -> str:
        if not span_data:
            return ''

        def serialize_span(span: Span):
            return json.dumps({
                'traceId': span.get_context().trace_id.to_bytes(16, 'big').hex(),
                'spanId': span.get_context().span_id.to_bytes(8, 'big').hex(),
                'parentSpanId': span.parent.span_id.to_bytes(8, 'big').hex() if span.parent else '',
                'name': span.name,
                'kind': str(span.kind),
                'startTime': to_iso_8601(span.start_time),
                'endTime': to_iso_8601(span.end_time),
                'attributes': convert_attributes(span.attributes),
                'events': convert_events(span.events)
            })

        def convert_events(events: Sequence[Event]):
            return list(map(lambda event: {
                'name': event.name,
                'timeStamp': to_iso_8601(event.timestamp),
                'attributes': convert_attributes(event.attributes)
            }, events))

        def convert_attributes(attributes):
            return attributes

        def to_iso_8601(time):
            return time

        return serialize_span(span_data)


class OCJaegerExporterAdapter(SpanExporter):
    def __init__(self):
        from opencensus.ext.jaeger.trace_exporter import JaegerExporter

        self._exporter = JaegerExporter(service_name="AzureML")

    def export(self, spans: Sequence[Span]) -> None:
        self._exporter.emit(self.__class__._to_span_data(spans))

    def shutdown(self) -> None:
        pass

    @staticmethod
    def _to_span_data(spans: Sequence[Span]):
        return [
            SpanData(
                name=ss.name,
                context=SpanContext(trace_id=encode_trace_id(ss.trace_id), span_id=encode_trace_id(ss.span_id)),
                span_id=encode_trace_id(ss.span_id),
                parent_span_id=encode_trace_id(ss.parent.span_id) if ss.parent else None,
                attributes=ss.attributes,
                start_time=ss.start_time,
                end_time=ss.end_time,
                child_span_count=len(ss._span.children),
                stack_trace=None,
                annotations=ss._span.annotations,
                message_events=ss._span.message_events,
                links=ss._span.links,
                status=ss._span.status,
                same_process_as_parent_span=ss._span.same_process_as_parent_span,
                span_kind=ss._span.span_kind
            )
            for ss in spans
        ]


def encode_trace_id(trace_id: int) -> str:
    return trace_id.to_bytes(16, 'big').hex()


def encode_span_id(span_id: int) -> str:
    return span_id.to_bytes(8, 'big').hex
