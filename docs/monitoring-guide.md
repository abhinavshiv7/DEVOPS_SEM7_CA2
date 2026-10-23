# Nagios monitoring guide

## Deployment order

Transfer the updated `ansible/` and `nagios/` directories to `devops-monitor`.
Run the playbooks separately because the `app` and `devops` accounts may have
different sudo passwords:

```bash
cd ~/devops_sem7/ansible
ansible-playbook playbooks/configure_monitoring_agent.yml
ansible-playbook playbooks/install_nagios.yml
```

The first playbook requires the `app` sudo password. The second requires the
`devops` sudo password.

## Dashboard access

Open `http://192.168.56.20/nagios4/` from Windows. The username is
`nagiosadmin`. Display the generated password locally on `devops-monitor`:

```bash
cat ~/.ansible/nagios/admin_password
```

Never paste or commit that password.

## Verification commands

```bash
/usr/lib/nagios/plugins/check_nrpe -H 192.168.56.10 -c check_memory
/usr/lib/nagios/plugins/check_attendance_api -H 192.168.56.10 -p 5173 -w 1 -c 3
sudo /usr/sbin/nagios4 -v /etc/nagios4/nagios.cfg
```

The dashboard may initially show `PENDING`; allow one or two check intervals
for all services to become green.

After intentionally stopping and recovering the backend, run
`docker compose restart frontend` as well. Nginx resolves the Compose service
name when it starts, so this refreshes its upstream address if the backend's
container address changed.

The automation disables Ubuntu's sample `localhost` object. Its default HTTP
check targets `127.0.0.1:80`, while this project intentionally binds Apache only
to `192.168.56.20`; its swap check also reports critical on a VM with no swap.
Removing those examples leaves the eight project-specific checks and avoids
misleading red states.

