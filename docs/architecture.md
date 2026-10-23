# Local VirtualBox architecture

## Nodes

The project uses two Ubuntu Server 24.04 VMs and the Windows host:

```text
Windows host (192.168.56.1)
  |-- SSH/browser over VirtualBox host-only network
  |
  +-- attendance-app (192.168.56.10)
  |     Docker: frontend + backend + MongoDB
  |
  +-- devops-monitor (192.168.56.20)
        Ansible controller + Nagios Core
```

Each VM also has a NAT interface (`10.0.2.15` inside each separate VirtualBox
NAT segment) for outbound downloads. The repeated NAT address is normal; VM to
VM communication uses the unique host-only addresses.

## Exposure policy

- Frontend: bound to `192.168.56.10:5173`, accessible only from the host-only LAN.
- Backend: available only inside the Docker network; no host port is published.
- MongoDB: available only inside the Docker network; no host port is published.
- SSH: reachable only through the host-only network.
- Nagios UI: will be bound to the DevOps VM's host-only address.

The lab initially uses HTTP on an isolated network, so the deployment explicitly
sets `SESSION_COOKIE_SECURE=false`. This is a documented local-demo limitation.
For any public deployment, HTTPS is required and this value must be `true`.

## Automation flow

1. The Windows workspace is the source of truth.
2. Project files are copied to `devops-monitor`.
3. Ansible connects to `attendance-app` at `192.168.56.10` using an SSH key.
4. The Docker role installs and verifies Docker Engine idempotently.
5. The application role (next stage) copies the app, creates protected runtime
   configuration, starts Compose, and verifies the health endpoints.
6. Nagios monitors the host, frontend, API health, resources, and containers.

