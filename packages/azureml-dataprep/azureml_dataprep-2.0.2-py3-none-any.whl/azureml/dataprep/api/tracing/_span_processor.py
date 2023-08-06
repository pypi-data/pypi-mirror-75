from abc import ABC, abstractmethod


try:
    from azureml.core import Run
    _run_id = Run.get_context().id
except:
    _run_id = None

logger = None


def get_logger():
    global logger
    if logger is not None:
        return logger

    from .._loggerfactory import _LoggerFactory

    logger = _LoggerFactory.get_logger("SpanProcessor")
    return logger


class SpanProcessor(ABC):
    @abstractmethod
    def on_start(self, span: 'Span') -> None:
        pass

    @abstractmethod
    def on_end(self, span: 'Span') -> None:
        pass

    @abstractmethod
    def shutdown(self) -> None:
        pass

    @abstractmethod
    def force_flush(self, timeout_millis: int = 30000) -> bool:
        pass


class AmlSimpleSpanProcessor(SpanProcessor):
    def __init__(self, span_exporter: 'SpanExporter'):
        self._span_exporter = span_exporter

    def on_start(self, span: 'Span') -> None:
        _add_aml_context(span)

    def on_end(self, span: 'Span') -> None:
        try:
            self._span_exporter.export((span,))
        except Exception as e:
            get_logger().error('Exception of type {} while exporting spans.'.format(type(e).__name__))

    def shutdown(self) -> None:
        self._span_exporter.shutdown()

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


def _add_aml_context(span: 'Span'):
    from .._loggerfactory import session_id

    span.set_attribute('sessionId', session_id)
    span.set_attribute('runId', _run_id)
