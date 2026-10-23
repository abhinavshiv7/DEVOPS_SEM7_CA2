#!/usr/bin/env python3
"""Validate the attendance API payload and report response-time thresholds."""

import argparse
import json
import time
import urllib.error
import urllib.request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', required=True)
    parser.add_argument('-p', '--port', type=int, default=5173)
    parser.add_argument('-w', '--warning', type=float, default=1.0)
    parser.add_argument('-c', '--critical', type=float, default=3.0)
    args = parser.parse_args()

    if not 0 <= args.warning < args.critical:
        print('API UNKNOWN - warning threshold must be below critical threshold')
        return 3

    url = f'http://{args.host}:{args.port}/api/v1/health'
    started = time.monotonic()
    try:
        with urllib.request.urlopen(url, timeout=args.critical + 2) as response:
            payload = json.loads(response.read().decode('utf-8'))
            status_code = response.status
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f'API CRITICAL - {error}')
        return 2

    elapsed = time.monotonic() - started
    payload_ok = (
        status_code == 200
        and payload.get('status') == 'ok'
        and payload.get('service') == 'student-attendance-tracker-api'
    )
    if not payload_ok:
        print(f'API CRITICAL - unexpected response: HTTP {status_code}, payload={payload}')
        return 2

    if elapsed >= args.critical:
        state, code = 'CRITICAL', 2
    elif elapsed >= args.warning:
        state, code = 'WARNING', 1
    else:
        state, code = 'OK', 0

    print(
        f'API {state} - health payload valid in {elapsed:.3f}s | '
        f'time={elapsed:.3f}s;{args.warning};{args.critical};0;'
    )
    return code


if __name__ == '__main__':
    raise SystemExit(main())

