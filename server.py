import requests

from fastapi import FastAPI


MICROSERVICE_PORT = 5001
MICROSERVICE_URL = f"http://localhost:{MICROSERVICE_PORT}"


import sentry_sdk
sentry_sdk.init(
    dsn="https://c65a02f670a844deac27c2b8373d8a45@o447951.ingest.sentry.io/4505160410333184",
    debug=True,
    release="0.0.0",
    traces_sample_rate=1.0, 
    # instrumenter="otel",
)

# tracer_provider = TracerProvider(resource=resource)
# tracer_provider.add_span_processor(SentrySpanProcessor())
# trace.set_tracer_provider(tracer_provider)
# set_global_textmap(SentryPropagator())
# ... 
# RequestsInstrumentor().instrument(tracer_provider=tracer_provider)
# ...
# FastAPIInstrumentor.instrument_app(app, tracer_provider=trace.get_tracer_provider())


app = FastAPI()


@app.get("/{something}")
async def server_api(something):
    sentry_sdk.capture_message("Server received request %s" % something)

    r = requests.get(f"{MICROSERVICE_URL}/{something.upper()}")

    return {
        "given_by_you": f"{something}'",
        "returned_from_microservice": r.json(),
    }
