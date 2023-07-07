import requests

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


MICROSERVICE_PORT = 5001
MICROSERVICE_URL = f"http://localhost:{MICROSERVICE_PORT}"


sentry_sdk.init(
    dsn="https://c65a02f670a844deac27c2b8373d8a45@o447951.ingest.sentry.io/4505160410333184",
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


@app.get("/{server_something}")
async def server_api(server_something):
    sentry_sdk.capture_message("Server received request %s" % server_something)

    r = requests.get(f"{MICROSERVICE_URL}/{server_something.upper()}")

    return {
        "given_by_you": f"{server_something}'",
        "returned_from_microservice": r.json(),
    }


# Instrument FastAPI with OTel
FastAPIInstrumentor.instrument_app(app, tracer_provider=trace.get_tracer_provider())