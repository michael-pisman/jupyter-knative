# Serverless Jupyter Notebooks: Comparing Deployment Models

## Overview

This project compares two ways to run JupyterLab on Kubernetes:

- **Traditional JupyterHub Deployment** (using KubeSpawner)
  - Each user gets a dedicated pod
  - Pods are not automatically scaled down to zero
  - Uses Horizontal Pod Autoscaler (HPA) for scaling
- **Serverless Deployments** (using Knative Serving)
  - Each user gets a dedicated pod
  - Pods are automatically scaled down to zero when not in use
  - Uses Knative for scaling

The goal is to find which method is more efficient, faster, and easier to scale.

## Folder Structure

- `jhub-knative/`: Contains the JupyterHub and Knative deployment files.
  - `jhub_knative_spawner/`: Contains the custom spawner code for Knative.
    - `spawner.py`: The main spawner code.
  - `setup.py`: The setup script for the package.
  - `Dockerfile`: The Dockerfile for the custom spawner.

- `jupyterlab-knative/`: Contains the JupyterLab deployment files.
  - `startup.sh`: The entrypoint script for the JupyterLab container.
  - `Dockerfile`: The Dockerfile for the JupyterLab container.
  - `knative-service.yaml`: The Knative service definition.

## Background

### What is Knative?

Knative is a Kubernetes extension that provides serverless capabilities. It allows you to run applications in a serverless manner, automatically scaling them up and down based on demand. This means that when there are no requests, the application can scale down to zero, saving resources.

### What is JupyterHub?

JupyterHub is a multi-user server for Jupyter notebooks. It allows multiple users to run their own Jupyter notebook servers, each in their own container. This is great for isolation and resource management, but it can lead to higher idle costs since each user has a dedicated pod that remains running even when not in use. JupyterHub has a proxy server that handles user authentication and routing. It uses a spawner to create jupyterlab servers for each user.

### What is KubeSpawner?

KubeSpawner is a spawner for JupyterHub that uses Kubernetes to create and manage user notebook servers. It allows you to customize how user servers are spawned, including using different images, resource limits, and more.


### 

## Test Setup

- **Cluster:** MicroK8s, 3 nodes, each with 2 CPUs and 128GB RAM
- **Workload:** Simulated HTTP requests to JupyterLab
- **Metrics:** Cold start time, warm start time, scaling speed, resource use

## Results

- **Cold Start:** Knative starts pods about 3× faster than HPA.
- **Warm Start:** Both are fast, Knative is slightly quicker.
- **Scaling:** Knative adds pods faster and can scale to zero.
- **Resource Use:** Knative uses less CPU and memory when idle.

## Summary Table

| Feature                | Knative Serverless | Kubernetes HPA      |
|------------------------|-------------------|---------------------|
| Cold Start Latency     | ~3.2s             | Higher              |
| Warm Start Latency     | ~150ms            | ~200ms              |
| Scale to Zero          | Yes               | No (manual)         |
| Resource Efficiency    | High              | Lower               |
| Setup Complexity       | Moderate          | Easier              |

## Next Steps

- Improve session handling (sticky sessions)
- Test multi-user scaling
- Add more detailed performance tests

## Future Plans

- Build a custom kernel manager for HTTP-based execution
- Store notebook state in Redis or a database for multi-pod support

## Roadmap

1. Prototype serverless notebooks with Knative
2. Integrate with JupyterHub
3. Measure latency and cost
4. Add secure execution and prepare for production

## References

- [Knative documentation](https://knative.dev)
- [Kubernetes documentation](https://kubernetes.io)
- [Jupyter Enterprise Gateway](https://jupyter-enterprise-gateway.readthedocs.io)
- [Zero-to-JupyterHub](https://zero-to-jupyterhub.readthedocs.io)
