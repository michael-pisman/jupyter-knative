from setuptools import setup, find_packages

setup(
    name='jhub_knative_spawner',
    version='0.1',
    install_requires=[
        'jupyterhub>=3.0',
        'requests',
        'kubernetes-asyncio'
    ],
    author='Michael Pisman',
    author_email='mpisman@ucmerced.edu',
    description='A custom JupyterHub Spawner for Knative Serving',
    classifiers=[
        'Framework :: Jupyter',
        'Programming Language :: Python :: 3'
    ],
    entry_points={
        'jupyterhub.spawners': [
            'jhub_knative_spawner = jhub_knative_spawner.spawner.KnativeSpawner',
        ],
    },
)