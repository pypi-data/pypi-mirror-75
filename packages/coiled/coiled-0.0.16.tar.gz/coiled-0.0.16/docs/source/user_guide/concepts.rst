=============
Core Concepts
=============

.. currentmodule:: coiled

This page covers the core concepts and functionality of Coiled.
To demonstrate these features, we'll walk through the example worflow below
which uses the ``coiled`` Python package to manage custom software environments,
manage cluster configurations, and spin up a remote Dask cluster.

.. note::

    This page assumes you've already installed and set up Coiled. If you
    haven't done this yet, go check out the :ref:`getting-started` page
    first and then come back here.

.. _example-workflow:

Example workflow
----------------

Below is an example workflow using the ``coiled`` Python package.
The following sections will discuss each portion of this example step-by-step.

.. code-block:: python

    import coiled

    # Create a new software environment with the libraries you want
    coiled.create_software_environment(
        name="my-conda-env", conda=["dask", "xarray==0.15.1", "numba"]
    )

    # Control the resources of your cluster by creating a new cluster configuration
    coiled.create_cluster_configuration(
        name="my-cluster-config",
        worker_memory="16 GiB",
        worker_cpu=4,
        scheduler_memory="4 GiB",
        scheduler_cpu=1,
        software="my-conda-env",
    )

    # Spin up a Dask cluster using
    cluster = coiled.Cluster(n_workers=5, configuration="my-cluster-config")

    # Connect a Dask Client to your cluster to perform computations on the cluster
    from dask.distributed import Client

    client = Client(cluster)


.. _software-envs:

Software environments
---------------------

A crucial part of doing your work is making sure you have the software packages
you need. You can manage software environments with Coiled by providing a
name for a given software environment as well as a specification for what
packages should be installed in the environment. Specifically, Coiled
supports building software environments with
`conda <https://docs.conda.io/en/latest/>`_, `pip <https://pip.pypa.io/en/stable/>`_,,
or Docker. Any software environment can then be easily deployed for use in a Dask cluster.

Conda
^^^^^

To create a software environment using conda, use the ``conda=`` keyword
argument of :meth:`coiled.create_software_environment` to specify a list of
packages to install into the environment. From our
:ref:`example workflow <example-workflow>`:

.. code-block:: python

    coiled.create_software_environment(
        name="my-conda-env", conda=["dask", "xarray==0.15.1", "numba"]
    )

will build a software environment named "my-conda-env" and use conda to
install dask, version 0.15.1 of xarray, and numba from the ``defaults`` conda
channel. More complex package specifications, like installing packages from
additional conda channels, are supported by passing a dictionary to ``conda=``.
For example, to search for packages in both the ``conda-forge`` and
``defaults`` channels:

.. code-block::

    coiled.create_software_environment(name="my-conda-env",
                                      conda={"channels": ["conda-forge", "defaults"],
                                             "dependencies": ["dask", "xarray=0.15.1", "numba"]})

Equivalently, you can also provide an input conda environment YAML file:

.. code-block:: python

    coiled.create_software_environment(name="my-conda-env", conda="environment.yml")

where ``environment.yml`` is a local file with the following content:

.. code-block:: yaml

    # environment.yml
    channels:
      - conda-forge
      - defaults
    dependencies:
      - dask
      - xarray=0.15.1
      - numba


Pip
^^^

To create a software environment using pip, use the ``pip=`` keyword argument of
:meth:`coiled.create_software_environment` to specify a list of packages
(on `PyPI <https://pypi.org/>`_) to install into the environment. For example:

.. code-block:: python

    coiled.create_software_environment(
        name="my-pip-env", pip=["dask", "xarray==0.15.1", "numba"]
    )

will build a software environment named "my-pip-env" and use pip to
install dask, version 0.15.1 of xarray, and numba. Equivalently, you can also
provide an input pip requirements file if you prefer:

.. code-block:: python

    coiled.create_software_environment(name="my-pip-env", pip="requirements.txt")

where ``requirements.txt`` is a local file with the following content:

.. code-block::

    # requirements.txt
    dask
    xarray==0.15.1
    numba


Docker
^^^^^^

Any Docker image on `Docker Hub <https://hub.docker.com/>`_ can be used to
build a custom software environment for your cluster by using the ``container=``
keyword argument of of :meth:`coiled.create_software_environment`.
For example:

.. code-block::

    coiled.create_software_environment(name="my-docker-env",
                                       container="rapidsai/rapidsai:latest")

will build a software environment named "my-docker-env" using latest
RAPIDS Docker image.


Listing and deleting software environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :meth:`coiled.list_software_environments` method will list all available
software environments:

.. code-block:: python

    coiled.list_software_environments()

While :meth:`coiled.delete_software_environment` can be used to delete
individual software environments. For example:

.. code-block:: python

    coiled.delete_software_environments(name="my-conda-env")

will delete the software environment named "my-conda-env".

.. _managing-software-environments:

Managing local and remote software environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can manage your local and remote software environment using the ``coiled install``
and ``coiled upload`` command line tools.

.. image:: images/coiled-upload-install.svg
   :alt: Software management with Coiled
   :width: 100%
   :align: center


``coiled install`` installs an existing Coiled software environment on your machine as
a local conda environment. For example, to use the ``coiled/default`` software environment
locally:

.. code-block:: bash

    # Create local version of the coiled/default software environment
    coiled install coiled/default
    conda activate coiled-coiled-default

The ``coiled/default`` name after ``coiled install`` specifies which Coiled
software environment should be created locally. Generally Coiled software environments
are specified in the form of "<coiled-account-name>/<software-environment-name>".
So in the above example we're telling ``coiled install`` to create the Coiled
software environment named "default" in the "coiled" account locally.

Conversely, ``coiled upload`` lets you take an an existing local conda environment and
upload it to Coiled as a software environment. For example:

.. code-block:: bash

    # Upload current conda environment to Coiled
    coiled upload

will inspect the packages installed in your currently activate conda environment and
create a new Coiled software environment with the same name. Additionally, ``coiled upload``
also has a ``--name`` option for uploading local conda environments other than the
currently activated one.


.. _cluster-config:

Cluster configurations
----------------------

Cluster configurations let you specify the resources a cluster will be launched
on. Specifically, you can configure the number of CPUs, memory, and software
environment for the scheduler and workers in a cluster.

It's important to note that creating a cluster configuration doesn't create a
cluster or provision any resources. You can think of a cluster configuration as
a template, or recipe, for a cluster that you can create later
(see the :ref:`cluster-creation` section for how to create a cluster from a
cluster configuration).

Creating cluster configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cluster configurations are created using the
:meth:`coiled.create_cluster_configuration` method. From our
:ref:`example workflow <example-workflow>`:

.. code-block:: python

    # Create "my-conda-env" software environment
    coiled.create_software_environment(
        name="my-conda-env", conda=["dask", "xarray==0.15.1", "numba"]
    )

    # Create "my-cluster-config" cluster configuration
    coiled.create_cluster_configuration(
        name="my-cluster-config",
        worker_memory="16 GiB",
        worker_cpu=4,
        scheduler_memory="4 GiB",
        scheduler_cpu=1,
        software="my-conda-env",
    )

creates a cluster configuration named "my-cluster-config" where the scheduler
has 1 CPU / 4 GiB of memory, workers each have 4 CPUs / 16 GiB of memory, and
the "my-conda-env" software environment is used for the scheduler
and all workers.


Listing and deleting cluster configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :meth:`coiled.list_cluster_configurations` method will list all available
cluster configurations:

.. code-block:: python

    coiled.list_cluster_configurations()

While :meth:`coiled.delete_cluster_configuration` can be used to delete
individual configurations. For example:

.. code-block:: python

    coiled.delete_cluster_configuration(name="my-cluster-config")

deletes the cluster configuration named "my-cluster-config".


.. _cluster-creation:

Creating a cluster
------------------

Creating a Dask cluster on cloud resources is done with the
:class:`coiled.Cluster` object. ``coiled.Cluster`` manages your Dask cluster
much like other cluster object you may have seen before like
:class:`distributed.LocalCluster` or :class:`dask_kubernetes.KubeCluster`.
From our :ref:`example workflow <example-workflow>`:

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(n_workers=5, configuration="my-cluster-config")

will create a cluster with 5 workers, each with resources based on the cluster
configuration named "my-cluster-config". If no ``configuration=`` is specified,
then the "coiled/default" cluster configuration will be used.

.. note::

    Creating a cluster involves provisioning various resources on cloud-based
    infrastructure. This process takes about a minute in most cases.

Once a cluster has been created, you can attach a :class:`distributed.Client`
to the cluster and start submitting tasks:

.. code-block:: python

    from dask.distributed import Client

    client = Client(cluster)

To view the
`Dask diagnostic dashboard <https://docs.dask.org/en/latest/diagnostics-distributed.html>`_
for your cluster, navigate to the cluster's ``dashboard_link``:

.. code-block:: python

    cluster.dashboard_link

which should output an address along the lines of
``"https://ec2-...compute.amazonaws.com:8787/status"``.


Listing and deleting clusters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :meth:`coiled.list_clusters` method will list all active clusters:

.. code-block:: python

    coiled.list_clusters()

Note that when a cluster is created, by default, a unique name for the cluster
is automatically generated. You can provide your own cluster name using the
``name=`` keyword argument for ``coiled.Cluster``.

:meth:`coiled.delete_cluster` can be used to delete individual clusters.
For example:

.. code-block:: python

    coiled.delete_cluster(name="my-cluster")

deletes the cluster named "my-cluster".
