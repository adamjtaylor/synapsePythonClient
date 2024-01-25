"""This utility class is to hold any utilities that are needed for async operations."""
from typing import Callable, Union
from opentelemetry import trace


tracer = trace.get_tracer("synapseclient")


def otel_trace_method(method_to_trace_name: Union[Callable[..., str], None] = None):
    """
    Decorator to trace a method with OpenTelemetry in an async environment. This function
    is specifically written to be used on a method within a class.

    This will pass the class instance as the first argument to the method. This allows
    you to modify the name of the trace to include information about the class instance.

    Example: Decorating a method within a class that will be traced with OpenTelemetry.
        Setting the trace name:

            @otel_trace_method(method_to_trace_name=lambda self, **kwargs: f"Project_Store: {self.name}")
            async def store(self):

    Args:
        method_to_trace_name: A callable that takes the class instance as the first argument
            and returns a string to be used as the trace name. If this is not provided,
            the trace name will be set to the method name.

    Returns:
        A callable decorator that will trace the method with OpenTelemetry.
    """

    def decorator(func):
        """Function decorator."""

        async def wrapper(self, *arg, **kwargs) -> None:
            """Wrapper for the function to be traced."""
            trace_name = (
                method_to_trace_name(self, *arg, **kwargs)
                if method_to_trace_name
                else None
            )
            with tracer.start_as_current_span(
                trace_name or f"Synaspse::{func.__name__}"
            ):
                return await func(self, *arg, **kwargs)

        return wrapper

    return decorator