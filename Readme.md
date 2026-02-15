
# truenas_netdata_to_prometheus_metrics

Lightweight adapter that queries Netdata and exposes the results as Prometheus-style metrics for scraping.

## How it works

- The service periodically queries a running Netdata instance (HTTP API).
- It converts selected Netdata metrics into Prometheus exposition format.
- It serves those metrics on an HTTP endpoint (by default `/metrics`) so Prometheus can scrape them.

This project is intended to run as a small container next to Netdata or inside the same Docker network.

## Quickstart (Docker Compose)

Use the below compose file in TrueNas server to "Install via YAML". Ensure that the EXPORTER_USERNAME and EXPORTER_USERNAME are changed as per your need and safety

```yaml
version: "3.8"
services:
  netdata-exporter:
    image: cray2015/netdata-to-prometheus-metrics-exporter:latest
    network_mode: host
    restart: unless-stopped
    read_only: true
    user: "10001:10001"
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    environment:
      EXPORTER_USERNAME: prom
      EXPORTER_PASSWORD: strongpassword
```

## Prometheus integration (sample `prometheus.yml`)

Add a scrape job to your Prometheus configuration. If you run Prometheus in the same Docker network, use the service name and port. If you map ports to the host, use `host:port` instead.

Example scrape config:

```yaml
scrape_configs:
  - job_name: "truenas-node"
    static_configs:
      - targets:
          - IP_OF_YOUR_TRUENAS_NODE:9101
    basic_auth:
      username: prom # update the username if changed
      password: strongpassword  # update the password if changed

```

Reload Prometheus after updating the config (or restart Prometheus).

## Troubleshooting

- Check the exporter's logs for errors connecting to `NETDATA_HOST` or for metric conversion errors.
- Ensure Netdata is reachable from the container/network and that any required Netdata API keys are correct.
- Verify Prometheus can reach the exporter via the target address used in `prometheus.yml`.

## Files of interest
- Dockerfile — container build

## Tested With
- TrueNas Community - 25.04.2.6
- Netdata - 1.37.1 (pre installed)