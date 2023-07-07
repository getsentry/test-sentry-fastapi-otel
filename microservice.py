from fastapi import FastAPI

import sentry_sdk
from sentry_sdk.integrations.opentelemetry import SentrySpanProcessor, SentryPropagator

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.propagate import set_global_textmap


sentry_sdk.init(
    dsn="https://5f9d5b81134849fb8fdcefc1b7922fd8@o447951.ingest.sentry.io/4505160413741056",
    debug=True,
    release="0.0.0",
    traces_sample_rate=1.0,
    instrumenter="otel",
)

# Setup OTel
print_spans_to_console = SimpleSpanProcessor(ConsoleSpanExporter())

tracer_provider = TracerProvider()
tracer_provider.add_span_processor(SentrySpanProcessor())
tracer_provider.add_span_processor(print_spans_to_console)

trace.set_tracer_provider(tracer_provider)

set_global_textmap(SentryPropagator())

# Instrument requests with OTel
RequestsInstrumentor().instrument(tracer_provider=tracer_provider)


app = FastAPI()


@app.get("/{microservice_something}")
def microservice_api(microservice_something):
    sentry_sdk.capture_message("Microservice received request %s" % microservice_something)

    return {
        "from_microservice": f"{microservice_something}'",
    }


# Instrument FastAPI with OTel
FastAPIInstrumentor.instrument_app(app, tracer_provider=trace.get_tracer_provider())