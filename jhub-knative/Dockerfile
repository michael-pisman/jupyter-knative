FROM jupyterhub/jupyterhub:3.0.0
USER root
COPY jhub_knative_spawner /srv/jupyterhub/
COPY setup.py /srv/jupyterhub/
RUN pip install --no-cache-dir /srv/jupyterhub
USER jovyan