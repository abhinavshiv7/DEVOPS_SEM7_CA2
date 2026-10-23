# Nagios monitoring

Nagios runs on `devops-monitor` and is available only on the VirtualBox
host-only network at `http://192.168.56.20/nagios4/`.

The monitored services are:

- host reachability and latency;
- frontend HTTP availability;
- API payload validity and response time;
- CPU, memory, and root disk usage through NRPE;
- Docker Compose service presence and container health;
- MongoDB container health without exposing port 27017.

NRPE on `attendance-app` binds to `192.168.56.10` and accepts only localhost
and `192.168.56.20`. The Nagios web administrator password is generated once
and stored outside the repository on `devops-monitor`.

