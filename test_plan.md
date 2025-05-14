## Startup Latency

### Cold-Start

* **Knative:**

  1. Scale service to zero (ensure no pods).
  2. Issue first HTTP GET to `/lab?token=…`.
  3. Measure time from TCP SYN to first byte of HTML.
* **KubeSpawner:**

  1. Stop the user server (delete pod).
  2. Trigger “Start My Server” via API or UI.
  3. Measure time from spawn request to first HTTP byte.

### Warm-Start

* With one pod already Running:

  * Send a GET to `/lab?token=…` and record request-response time.



## Concurrency & Scale-Out

### Concurrency per Pod

* **Knative:**

  * Configure `containerConcurrency=N`.
  * Fire N+M simultaneous connections; note latency tail (p95/p99).
* **KubeSpawner:**

  * Spawn M additional users simultaneously (M pods).
  * Measure how long until all M pods are Ready.

### Autoscaling Behavior

* **Knative:**

  * Drive a steady RPS ramp (e.g. from 1 to 10 RPS).
  * Observe pod count vs. RPS in Grafana.
* **HPA on Hub:**

  * Generate CPU load inside single-user pods (e.g. Python loop).
  * Observe HPA scaling thresholds, pod counts vs. CPU%.



## Resource Utilization

* **CPU & Memory:**

  * Record per-pod CPU-sec and MB under idle, light, and heavy loads.
* **Idle Overhead:**

  * Note node-level resource usage with zero active sessions for each model.



## Idle Cleanup & Scale-To-Zero

* **Knative:**

  * Measure time from last request to pods scaled to zero.
* **JupyterHub Idle Culler:**

  * Configure cull timeout (e.g. 10 min).
  * Measure actual time until pod deletion.



## Cost Modeling

* Convert CPU-sec and pod-hours into \$ using a cloud rate (e.g. \$0.10/CPU-hour).
* Compare total cost for a simulated 8 h day with intermittent use.



##  User-Perceived Experience

* **Page Load**: time-to-interactive for JupyterLab UI (e.g. using Selenium or Puppeteer).
* **Kernel Startup**: time from “Run cell”, first output for an empty Python cell.



## Resilience & Reliability

* **Pod Failover:** kill a running pod and measure recovery time.
* **Network Flakiness:** introduce latency or packet loss (e.g. via `tc qdisc`) and observe user impact.



### Tools & Automation

* **Load generation:** `k6`, `hey`, or simple `curl`+`time`.
* **Metrics:** MicroK8s Prometheus + Grafana; `kubectl get events -w`.
* **Scripting:** bash or Python to orchestrate scale and request sequences, and collect logs.



Running through these scenarios should provide a comprehensive, quantitative comparison of startup latency, scalability, resource efficiency, cost, and user experience between Knative and KubeSpawner deployments.