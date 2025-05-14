# FROM python:3.11-slim
# RUN pip install jupyterlab --no-cache-dir
# COPY startup.sh /usr/local/bin/startup.sh
# ENTRYPOINT ["bash","/usr/local/bin/startup.sh"]

FROM python:3.11-slim

# 1. Install JupyterLab globally
RUN pip install --no-cache-dir jupyterlab

# 2. Create and switch to a non-root user
RUN useradd --create-home jupyter
USER jupyter
WORKDIR /home/jupyter

# 3. Copy your startup script
COPY --chown=jupyter:jupyter startup.sh /home/jupyter/startup.sh
RUN chmod +x /home/jupyter/startup.sh

ENTRYPOINT ["/home/jupyter/startup.sh"]

