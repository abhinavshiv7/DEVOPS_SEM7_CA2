#!/usr/bin/env python3
"""Nagios plugin that checks memory consumption using /proc/meminfo."""

import argparse


def read_memory():
    values = {}
    with open('/proc/meminfo', encoding='utf-8') as meminfo:
        for line in meminfo:
            key, raw_value = line.split(':', 1)
            values[key] = int(raw_value.strip().split()[0])
    return values['MemTotal'], values['MemAvailable']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--warning', type=float, default=80.0)
    parser.add_argument('-c', '--critical', type=float, default=90.0)
    args = parser.parse_args()

    if not 0 <= args.warning < args.critical <= 100:
        print('MEMORY UNKNOWN - thresholds must satisfy 0 <= warning < critical <= 100')
        return 3

    total_kib, available_kib = read_memory()
    used_kib = total_kib - available_kib
    used_percent = 100.0 * used_kib / total_kib
    if used_percent >= args.critical:
        state, code = 'CRITICAL', 2
    elif used_percent >= args.warning:
        state, code = 'WARNING', 1
    else:
        state, code = 'OK', 0

    used_mib = used_kib / 1024
    total_mib = total_kib / 1024
    print(
        f'MEMORY {state} - used {used_percent:.1f}% '
        f'({used_mib:.0f} MiB/{total_mib:.0f} MiB) | '
        f'used={used_percent:.1f}%;{args.warning};{args.critical};0;100'
    )
    return code


if __name__ == '__main__':
    raise SystemExit(main())

