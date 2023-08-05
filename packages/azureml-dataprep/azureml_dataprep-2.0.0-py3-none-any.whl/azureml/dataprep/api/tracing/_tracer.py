from typing import List, Optional

from ._span import OCSpanAdapter
from ._span_processor import SpanProcessor
from opencensus.trace import execution_context


class AmlTracer:
    def __init__(self, span_processors: List[SpanProcessor]):
        self._span_processors = span_processors

    def start_as_current_span(self, name: str, parent: Optional[OCSpanAdapter] = None) -> OCSpanAdapter:
        parent = parent or execution_context.get_current_span()
        span = OCSpanAdapter(name, parent, self._span_processors)
        span.__enter__()
        return span

    def start_span(self, name: str, parent: Optional[OCSpanAdapter] = None) -> OCSpanAdapter:
        return OCSpanAdapter(name, parent, self._span_processors)


class DefaultTraceProvider:
    def __init__(self, tracer: AmlTracer):
        self._tracer = tracer

    def get_tracer(self, name: str) -> AmlTracer:
        return self._tracer

    def get_current_span(self):
        return execution_context.get_current_span()
