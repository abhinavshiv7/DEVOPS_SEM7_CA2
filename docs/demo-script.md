# DevOps Semester 7 demonstration script

## 1. Show the architecture

Explain that both Ubuntu Server VMs use NAT only for outbound downloads and the
VirtualBox host-only network for administrative and monitoring traffic:

- Windows host: `192.168.56.1`
- Application VM: `192.168.56.10`
- DevOps/monitoring VM: `192.168.56.20`

Show that only frontend port `5173` is reachable from Windows. Backend port
`4000`, MongoDB port `27017`, and Nagios agent port `5666` are not exposed as
public application endpoints.

## 2. Demonstrate Ansible

On `devops-monitor`, run the three playbooks a second time and show that they
report no unnecessary changes:

```bash
cd ~/devops_sem7/ansible
ansible-playbook playbooks/install_docker.yml
ansible-playbook playbooks/deploy_application.yml
ansible-playbook playbooks/configure_monitoring_agent.yml
ansible-playbook playbooks/install_nagios.yml
```

Use the appropriate target account's sudo password for each playbook. Explain
that secrets are stored outside the repository and hidden from Ansible output.

## 3. Show the healthy baseline

Open `http://192.168.56.20/nagios4/` and show:

- one monitored host in the UP state;
- eight project services in the OK state;
- frontend, API payload/response time, CPU, memory, disk, Docker, and MongoDB
  monitoring.

Capture the healthy-services screenshot before triggering a failure.

## 4. Trigger a controlled backend failure

From `devops-monitor`:

```bash
ssh app@192.168.56.10
cd /opt/student-attendance-tracker
docker compose stop backend
docker compose ps
```

Do not run `docker compose down -v`; the `-v` option would remove the MongoDB
volume. Stopping only the backend preserves all application data and keeps the
frontend and database containers running.

In Nagios, force an immediate check or wait for the next scheduled checks. Show:

- the host remains UP;
- Frontend HTTP remains OK;
- API Health and Response Time becomes CRITICAL;
- Docker Application Stack becomes CRITICAL;
- MongoDB Container Health remains OK.

If an unrelated service is not already OK before the demonstration, correct it
before collecting failure evidence so the screenshot clearly distinguishes the
controlled backend failure from configuration problems.

Capture the critical-state screenshot.

## 5. Recover the application

On `attendance-app`:

```bash
docker compose up -d backend
docker compose restart frontend
docker compose ps
curl -fsS http://192.168.56.10:5173/api/v1/health
```

Restarting the frontend refreshes Nginx's resolved address for the backend in
case Docker assigned a different container address during recovery. The curl
command must return the JSON health payload. Force another Nagios check or wait
for its scheduler, then capture the recovered OK state.

## 6. Prove data persistence

Log back into the application after recovery and show that the previously
created account or sample attendance data remains. Explain that MongoDB uses the
named `mongodb_data` volume, which survives container stops and restarts.

