import requests
import sys

import sentry_sdk


SERVER_PORT = 5000
SERVER_URL = f"http://localhost:{SERVER_PORT}"


def main(value):
    sentry_sdk.init(
        dsn="https://e0f002c997e841828595584ace084210@o447951.ingest.sentry.io/4505160406990848",
        debug=True,
        release="0.0.0",
        traces_sample_rate=1.0,
    )

    sentry_sdk.capture_message("main.py started")

    r = requests.get(f"{SERVER_URL}/{value}")

    print()
    print("OUTPUT of main.py:")
    print(r.json())
    print()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "some_default_value_asdf")
