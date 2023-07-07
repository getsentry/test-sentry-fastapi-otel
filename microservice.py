from fastapi import FastAPI

import sentry_sdk
sentry_sdk.init(
    dsn="https://5f9d5b81134849fb8fdcefc1b7922fd8@o447951.ingest.sentry.io/4505160413741056",
    debug=True,
    release="0.0.0",
    traces_sample_rate=1.0,
    # instrumenter="otel",
)


app = FastAPI()


@app.get("/{something}")
def microservice_api(something):
    sentry_sdk.capture_message("Microservice received request %s" % something)

    return {
        "from_microservice": f"{something}'",
    }
