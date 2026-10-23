#!/usr/bin/env python3
"""Check Compose containers and Docker health without exposing Docker remotely."""

import argparse
import json
import subprocess


DEFAULT_SERVICES = {'mongodb', 'backend', 'frontend'}


def docker(*arguments):
    return subprocess.run(
        ['docker', *arguments],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', default='student-attendance-tracker')
    parser.add_argument('--service')
    args = parser.parse_args()

    try:
        ids = docker(
            'ps', '-aq',
            '--filter', f'label=com.docker.compose.project={args.project}',
        ).split()
        if not ids:
            print(f'DOCKER CRITICAL - no containers found for project {args.project}')
            return 2
        containers = json.loads(docker('inspect', *ids))
    except (subprocess.SubprocessError, OSError, json.JSONDecodeError) as error:
        print(f'DOCKER UNKNOWN - {error}')
        return 3

    statuses = {}
    problems = []
    for container in containers:
        labels = container.get('Config', {}).get('Labels') or {}
        service = labels.get('com.docker.compose.service')
        if not service:
            continue
        if args.service and service != args.service:
            continue
        state = container.get('State', {})
        running = bool(state.get('Running'))
        health = (state.get('Health') or {}).get('Status')
        statuses[service] = health or ('running' if running else state.get('Status', 'stopped'))
        if not running:
            problems.append(f'{service}=not-running')
        elif health and health != 'healthy':
            problems.append(f'{service}={health}')

    expected = {args.service} if args.service else DEFAULT_SERVICES
    missing = expected - statuses.keys()
    problems.extend(f'{service}=missing' for service in sorted(missing))

    relevant = {key: value for key, value in statuses.items() if key in expected}
    summary = ', '.join(f'{key}={relevant[key]}' for key in sorted(relevant))
    if problems:
        print(f'DOCKER CRITICAL - {", ".join(problems)} | containers={len(statuses)};;;0;')
        return 2

    label = 'MONGODB' if args.service == 'mongodb' else 'DOCKER'
    print(f'{label} OK - {summary} | containers={len(relevant)};;;0;')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

