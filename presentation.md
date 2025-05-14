---
marp: true
author: Michael Pisman
title: Serverless Jupyter Notebooks
paginate: true
header: ''
footer: '
<div class="footer-logo">
  <img src="./assets/UCM_Logo.svg" alt="UCM Logo" />
  <img src="./assets/UCM_Logos_TextInverse.svg" alt="UCM Logos Text Inverse" />
</div>
<span>Spring 2025 | EECS 268 | Michael Pisman</span>'
transition: fade
style: |
    /* @theme ucm */

    section {
        color: #0F2D52;
        font-family: 'Calibri', sans-serif;
        font-size: 24px;
    }

    section::after {
        left: 0;
        bottom: 0;
        width: 99%;
        text-align: right;
        color: #EFEFEF;
        background-color: #0F2D52;
        padding-right: 1% !important;
    }

    footer {
        position: fixed !important;
        bottom: 0 !important;
        left: 10px !important;
        z-index: 1;
        color: #EFEFEF;
        width: 100%;
    }

    footer span{
        width: 100%;
        text-align: center;
        position: fixed;
        bottom: 4px;
        left: 0;
    }

    .footer-logo {
        text-align: left;
        position: fixed;
        bottom: -2px;
        left: 4px;
        margin: 0 !important;
    }

    .footer-logo img {
        height: 24px;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
    }

    h1 {
        /* position: relative;
        top: 80px; */
        color: #0F2D52;
        font-family: 'Calibri', sans-serif;
        font-size: 36px;
        border-bottom: 3px solid #DAA900;
    }

    h3 strong, h2 strong {
        color: #005487;
    }

    section.title-slide img:first-child {
        margin: auto 45%;
    }

    section.sm {
        text-align: left;
        font-size: 20px;
    }

    section.title-slide h1 {
        color: #0F2D52;
        font-family: 'Calibri', sans-serif;
        font-size: 48px;
        border-bottom: none;
        text-align: center;
    }

    section.title-slide h2, section.title-slide h3 {
        color: #005487;
        font-family: 'Calibri', sans-serif;
        border-bottom: none;
        text-align: center;
    }


---

<!-- _class: title-slide -->

![100px](./assets/UCM_Logos_Primary.svg)

# Serverless Jupyter Notebooks
## Comparative Analysis of JupyterLab Deployment Models: **Serverless (Knative) vs. Kubernetes Deployment**  
### Michael Pisman
---

# Agenda

* Project Motivation
* Background & Architectures
* Testbed & Configuration
* Performance Metrics & Methodology
* Key Results
* Conclusions & Next Steps

<!-- Keynote: Overview of what we will cover in this presentation. -->

---

# Background: Knative

* CNCF project adding serverless primitives on Kubernetes
* Key features: Serving (scale-to-zero, concurrency), Eventing (CloudEvents), standard CRDs
* Benefits: request-driven autoscaling, scale-to-zero, traffic splitting

<!-- Keynote: Knative allows serverless-style deployments on Kubernetes. -->

---

# Background: Kubernetes Deployment

* Standard Deployment + HPA approach
* Pod replicas based on CPU/memory
* Scale-to-zero manually when needed
* One user per pod; limited density and higher idle cost

<!-- Keynote: Kubernetes Deployments scale using metrics like CPU; manual zero-scaling. -->

---

# Project Motivation

* **Resource Efficiency**: minimize idle consumption and scale-to-zero
* **Latency & UX**: reduce cold-start delays for interactive sessions
* **Comparison Gap**: serverless notebooks vs. traditional one-pod-per-user

<!-- Keynote: We aim to improve resource use and user experience by comparing different JupyterLab deployment strategies. -->

---

# Traditional JupyterHub Deployment

* Zero-to-JupyterHub Helm chart on Kubernetes
* KubeSpawner: one pod per user
* Authentication via OAuth/LDAP
* Persistent storage via PVC per user
* Strong isolation but high idle resource cost

<!-- Keynote: JupyterHub isolates users with separate pods but incurs high idle resource usage. -->

---

# Kubernetes Deployment + HPA

* Standard Deployment (apps/v1)
* **HPA**: scales pods on CPU utilization
* **Scale-to-zero**: manual or zero replicas
* **One user → one pod** (no request multiplexing)

<!-- Keynote: Kubernetes Deployments scale by CPU, manually managed zero-scaling. -->

---

# Jupyter Enterprise Gateway

* Decouples notebook UI from remote kernel execution
* Kernels run on Kubernetes, YARN, Spark clusters
* Single notebook server + remote per-kernel pods
* **Comparison to Serverless Kernel Farm:**

  * Enterprise Gateway: per-kernel pod vs. shared in-pod hosts
  * Enterprise Gateway: multi-tenancy via resource managers; ours: function grouping for density

<!-- Keynote: Enterprise Gateway provides remote kernels but still uses one pod per kernel. -->

---

# Serverless JupyterLab (Knative)

* JupyterLab container on Knative Serving
* **Autoscale**: 0 → n pods on HTTP load
* **Buffering**: queue-proxy smooths cold starts
* **Concurrency**: multiple requests per pod

<!-- Keynote: Knative scales JupyterLab dynamically based on requests. -->

---

# Testbed & Configuration

* **Hardware**: 3-node cluster (DL380 Gen9, 2x E5-2690v4, 128GB RAM)
* **Kubernetes Cluster**: MicroK8s 1.32 HA
* **Knative Serving**: 1.17
* **Images**: same `docker.io/mpisman/jupyterlab:latest`
* **Workload:** cold/warm HTTP GET `/lab?token=test-token`, 10 concurrent requests

<!-- Keynote: Set up identical JupyterLab environments to test deployments fairly. -->

---

# Performance Metrics

* **Cold-Start Latency:** request → first “200 OK”
* **Warm-Start Latency:** subsequent requests under active pod(s)
* **Scale-Out Behavior:** pod count over time
* **Resource Utilization:** CPU-sec & memory-MB during test

<!-- Keynote: Metrics include latency, pod scaling, and resource consumption. -->

---

# Methodology

1. **Cold Test:** 0 replicas → single request → record latency
2. **Warm Test:** 1 pod Running → single request → record latency
3. **Load Test:** 10 concurrent requests → observe scaling & latencies
4. **Data Collection:** `curl` timings + `kubectl get pods -w` + Prometheus

<!-- Keynote: Clear testing steps for accurate performance measurement. -->

---

<!-- _class: title-slide -->

# Key Findings

---

# Cold-Start Latency

![](./figures/cold_warm_latency.png)

* **Knative:** ~3.19 s
* **HPA:** ?

<!-- Keynote: Knative significantly reduces cold-start latency compared to standard Kubernetes deployments. -->

---

# Warm-Start Latency

![](./figures/warm_latency.png)

* **Knative:** 150 ms
* **HPA:** ?

<!-- Keynote: Both deployments have comparable warm-start latency, Knative slightly faster. -->

---

# Scale-Out Under Load

![](./figures/scale_out.png)

* **Knative:** scaled to 3 pods at 10 RPS
* **HPA:** ?

<!-- Keynote: Knative dynamically scaled faster and slightly more than HPA under load. -->

---

# Conclusions

* **Knative Serverless:** faster cold-starts (3× improvement), zero idle cost, seamless request-driven scaling
* **Kubernetes + HPA:** simpler setup, slower cold-starts, manual scale-to-zero, one pod per user limits density

<!-- Keynote: Knative provides clear efficiency benefits but requires careful session management. -->

---

# Next Steps

* **Sticky Sessions:** configure Traefik affinity or shared session store
* **Multi-Tenant Scaling:** prototype serverless kernel farm
* **Extended Metrics:** cell-level latency & cost modeling
* **Demo:** live comparison & Grafana dashboards

<!-- Keynote: Immediate next steps include improving session handling and deeper analysis. -->

---

# Future Plans: Serverless IPyKernel

* Develop custom `KernelManager` for HTTP-based cell execution
* Build in-pod execution broker with process/WASM isolation
* Externalize notebook state to Redis/DB for multi-pod sessions

---

# Tentative Roadmap

* **Phase 1:** prototype `serverless_notebooks` with Knative
* **Phase 2:** integrate into JupyterHub as RemoteKernel
* **Phase 3:** evaluate cell latency, cost, density
* **Phase 4:** secure sandboxing & production hardening

---

<!-- _class: title-slide -->

# Thank You
## Questions?