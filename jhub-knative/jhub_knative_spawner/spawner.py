# jhub_knative_spawner/spawner.py
from tornado import gen
from jupyterhub.spawner import Spawner
from traitlets import Unicode, Integer
import requests

class KnativeSpawner(Spawner):
    namespace = Unicode('serverless', config=True)
    image     = Unicode('docker.io/mpisman/jupyterlab:latest', config=True)
    min_scale = Integer(0, config=True)
    max_scale = Integer(3, config=True)
    concurrency = Integer(1, config=True)

    def get_service_name(self):
        return f"{self.user.name}-svc"

    @gen.coroutine
    def start(self):
        name = self.get_service_name()
        spec = {
            "apiVersion": "serving.knative.dev/v1",
            "kind": "Service",
            "metadata": {"name": name, "namespace": self.namespace},
            "spec": {"template": {"metadata": {"annotations": {
                "autoscaling.knative.dev/minScale": str(self.min_scale),
                "autoscaling.knative.dev/maxScale": str(self.max_scale)
            }},
            "spec": {"containerConcurrency": self.concurrency,
            "containers": [{"image": self.image,
                              "env": [{"name": "JUPYTERHUB_API_TOKEN",
                                        "value": self.user.server.token}],
                              "ports": [{"containerPort": 8888}]}]}}}
        }
        # Create or replace Knative Service
        requests.post(
            f"/apis/serving.knative.dev/v1/namespaces/{self.namespace}/services",
            json=spec, headers={'Content-Type': 'application/json'})
        # Wait for readiness (poll status.url)
        url = None
        for _ in range(30):
            res = requests.get(f"/apis/serving.knative.dev/v1/namespaces/{self.namespace}/services/{name}")
            status = res.json().get('status', {})
            url = status.get('url')
            if url:
                break
            time.sleep(1)
        return url

    @gen.coroutine
    def stop(self):
        name = self.get_service_name()
        requests.delete(
            f"/apis/serving.knative.dev/v1/namespaces/{self.namespace}/services/{name}")

    @gen.coroutine
    def poll(self):
        name = self.get_service_name()
        res = requests.get(
            f"/apis/serving.knative.dev/v1/namespaces/{self.namespace}/services/{name}")
        return res.status_code != 200