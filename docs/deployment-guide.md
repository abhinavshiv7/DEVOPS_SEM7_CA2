# Application deployment guide

## Prerequisites

- `attendance-app` is reachable at `192.168.56.10`.
- `devops-monitor` is reachable at `192.168.56.20`.
- Passwordless SSH from `devops-monitor` to the `app` user works.
- `ansible/playbooks/install_docker.yml` has completed successfully.

## Transfer the source of truth

From Windows PowerShell, copy both project directories to the controller:

```powershell
scp -r "C:\Users\abhin\Desktop\devops_sem7\ansible" devops@192.168.56.20:~/devops_sem7/
scp -r "C:\Users\abhin\Desktop\devops_sem7\application" devops@192.168.56.20:~/devops_sem7/
```

## Validate and deploy

On `devops-monitor`:

```bash
cd ~/devops_sem7/ansible
ansible-playbook --syntax-check playbooks/deploy_application.yml
ansible-playbook playbooks/deploy_application.yml
```

The playbook generates a persistent 64-character session secret on the Ansible
controller under `~/.ansible/student-attendance-tracker/`. It never writes that
secret into the Git workspace or prints it in normal Ansible output. The runtime
`.env` on the app VM is mode `0600`.

## Verify

From Windows:

```powershell
curl.exe http://192.168.56.10:5173/api/v1/health
```

Open `http://192.168.56.10:5173` in a browser and test registration and login.

## Local HTTP limitation

The lab exposes the frontend only on the VirtualBox host-only address. Because
it uses HTTP, `SESSION_COOKIE_SECURE` is set to `false`; otherwise browsers would
not send the login cookie. A public or internet-facing deployment must use HTTPS
and set this value to `true`.

