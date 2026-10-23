#!/usr/bin/env python3
"""Nagios plugin that measures Linux CPU usage over a short interval."""

import argparse
import time


def read_cpu():
    with open('/proc/stat', encoding='utf-8') as stat_file:
        fields = stat_file.readline().split()[1:]
    values = [int(value) for value in fields]
    idle = values[3] + (values[4] if len(values) > 4 else 0)
    return sum(values), idle


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--warning', type=float, default=80.0)
    parser.add_argument('-c', '--critical', type=float, default=90.0)
    args = parser.parse_args()

    if not 0 <= args.warning < args.critical <= 100:
        print('CPU UNKNOWN - thresholds must satisfy 0 <= warning < critical <= 100')
        return 3

    total_before, idle_before = read_cpu()
    time.sleep(1)
    total_after, idle_after = read_cpu()
    total_delta = total_after - total_before
    idle_delta = idle_after - idle_before
    if total_delta <= 0:
        print('CPU UNKNOWN - unable to calculate CPU activity')
        return 3

    used = 100.0 * (total_delta - idle_delta) / total_delta
    if used >= args.critical:
        state, code = 'CRITICAL', 2
    elif used >= args.warning:
        state, code = 'WARNING', 1
    else:
        state, code = 'OK', 0

    print(
        f'CPU {state} - usage {used:.1f}% | '
        f'usage={used:.1f}%;{args.warning};{args.critical};0;100'
    )
    return code


if __name__ == '__main__':
    raise SystemExit(main())

