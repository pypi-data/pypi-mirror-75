.. _getting-started:

===============
Getting Started
===============

Welcome to the getting started guide for Coiled! This page, and the video below,
covers installing and setting up Coiled as well as some basics on how to create
Dask clusters and manage software environments with Coiled.

.. raw:: html

   <iframe width="672"
           height="378"
           src="https://www.youtube.com/embed/qNZP_8ugN6U"
           style="margin: 0 auto 20px auto; display: block;"
           frameborder="0"
           allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
           allowfullscreen></iframe>


Install
=======

Coiled can be installed from PyPI using ``pip`` or from the conda-forge
channel using ``conda``:


.. panels::
    :body: text-center
    :header: text-center h5 bg-white

    Install with pip
    ^^^^^^^^^^^^^^^^

    .. code-block:: bash

        pip install coiled

    ---

    Install with conda
    ^^^^^^^^^^^^^^^^^^

    .. code-block:: bash

        conda install -c conda-forge coiled

.. _coiled-setup:

Setup
=====

Coiled comes with a ``coiled login`` command line tool to configure
your account credentials. From the command line enter:

.. code-block:: bash

    coiled login


You'll then be asked to navigate to https://beta.coiledhq.com/profile to log in and
retrieve your Coiled token.

.. code-block:: bash

    Please login to https://beta.coiledhq.com/profile to get your token
    Token:

Upon entering your token, your credentials will be saved to Coiled's local
configuration file. Coiled will then pull credentials from the configuration
file when needed.


.. _first-computation:

Run your first computation
==========================

When performing computations on remote Dask clusters, it's important to have the same libraries
installed both in your local Python environment (e.g. on your laptop), as well as on the remote
Dask workers in your cluster. Coiled helps you seamlessly synchronize these software environments.
While there's more detailed information on this topic is available in the User Guide,
for now we'll just use the ``coiled install`` command line tool for creating a standard
conda environment locally. From the command line:

.. code-block:: bash

    # Create local version of the coiled/default software environment
    coiled install coiled/default
    conda activate coiled-coiled-default
    ipython

The above snippet will create a local conda environment named "coiled-coiled-default",
activate it, and then launch an IPython session. Note that while we're creating a local software
environment, all Dask computations will happen on remote Dask workers on AWS, *not* on your
local machine (for more information on why local software environments
are needed, see our :ref:`FAQ page <why-local-software>`).

Now that we have our software environment set up, we can walk through the following example:

.. code-block:: python

    # Create a remote Dask cluster with Coiled

    import coiled

    cluster = coiled.Cluster(configuration="coiled/default")

    # Connect Dask to that cluster

    import dask.distributed

    client = dask.distributed.Client(cluster)
    print("Dask Dashboard:", client.dashboard_link)

.. note::

    Note that when creating a ``coiled.Cluster``, resources for our Dask cluster are
    provisioned on AWS. This provisioning process takes about a minute to complete


.. code-block:: python

    # Perform computations with data on the cloud

    import dask.dataframe as dd

    df = dd.read_csv(
        "s3://nyc-tlc/trip data/yellow_tripdata_2019-01.csv",
        parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"],
        dtype={
            "payment_type": "UInt8",
            "VendorID": "UInt8",
            "passenger_count": "UInt8",
            "RatecodeID": "UInt8",
            "store_and_fwd_flag": "category",
            "PULocationID": "UInt16",
            "DOLocationID": "UInt16",
        },
        storage_options={"anon": True},
        blocksize="16 MiB",
    ).persist()

    df.groupby("passenger_count").tip_amount.mean().compute()

The example above goes through the following steps:

- Spins up a remote Dask cluster by creating a :class:`coiled.Cluster` instance.
- Connects a Dask ``Client`` to the cluster.
- Submits a Dask DataFrame computation for execution on the cluster.


Manage Software Environments
============================

In the previous :ref:`first-computation` section, we used the pre-built ``coiled/default`` software environment to get started.
However, often you'll want to create your own custom software environment with the libraries you need.
This can be done with the :meth:`coiled.create_software_environment` and :meth:`coiled.create_software_environment` methods.

For example:

.. code-block:: python

    coiled.create_software_environment(  # Note:  This takes around five minutes
        name="my-env",
        conda={
            "channels": ["conda-forge"],
            "dependencies": ["dask", "xarray>=0.15", "numba", "s3fs"],
        },
    )

    coiled.create_cluster_configuration(
        name="my-config",
        software="my-env",
        worker_memory="16 GiB",
        worker_cpu=4,
        scheduler_memory="4 GiB",
        scheduler_cpu=1,
    )

This creates a new Coiled **software environment** named ``my-env``, with dask, version 0.15 of xarray, numba, and s3fs
from the ``conda-forge`` conda channel.

Then we create a **cluster configuration** named ``my-config`` which uses that software environment
and additionally specifies hardware constraints like how much memory and how many cores each worker should have.

We can use these software environments both locally and on our remote
distributed environment.

Local use
---------

Locally, just like in the :ref:`first-computation` section where we installed the
``coiled/default`` software environment, we can also use the
``coiled install`` command line tool to create our custom ``my-env`` software
environment locally:

.. code-block:: bash

    coiled install my-env
    conda activate coiled-my-env

Remote use
----------

Remotely we can use the ``my-config`` cluster configuration to create new Coiled clusters.

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(configuration="my-config")

    import dask.distributed

    client = dask.distributed.Client(cluster)

Although note, your local environment and your remote environment :ref:`should match <why-should-packages-match>`.
Otherwise you might experience software version issues. This may require you
to stop your current Python session, install and activate the new environment,
and then restart your Python session.


Share
=====

You can share your software environments, cluster configurations, and clusters
with friends and colleagues.  For example, others can refer to your software environment
``my-env`` by prepending your account name ``<coiled-account>/my-env``.

For example if your username is ``alice`` then anyone could install your
softare environment locally with the following command.

.. code-block:: shell

   coiled install my-env            # You can do this
   coiled install alice/my-env      # Anyone can do this

You did this at the beginning of this exercise when you installed
``coiled/default`` locally, and built a cluster with
``configuration="coiled/default"``.

So if you construct a software environment and cluster configuration that solves your particular problem,
you can point colleagues at that environment and configuration
and they will be able to reproduce your work.


Next steps
==========

This page illustrates some the core concepts of Coiled. You may want to continue playing around with these concepts.
We recommend some of the following exercises.

1.  Use the :meth:`coiled.Cluster.scale` method to ask for more resources.

    How long does it take to get new workers?  (*about a minute*)

    How many resources can you ask for before Coiled yells at you?

2.  Read in the full NYC Taxi dataset for 2019 by using the ``*`` character
    instead of ``01`` for the month of January in the filename.

3.  Try reading some of your own data on S3, or else look through the `AWS registry
    of open data <https://registry.opendata.aws/>`_.

4.  Need different libraries to access that data?  Try building your own
    software environment and cluster configuration.

5. Visit https://beta.coiledhq.com to browse the Coiled web interface.

6. Using Coiled with JupyterLab? See the :ref:`jupyterlab-guide` page for recommendations on
   configuring JupyterLab to work smoothly with Coiled


For more in-depth
discussion of these features, additional examples, and more, please see the
:ref:`User Guide <user-guide>`.

.. link-button:: user_guide/index
    :type: ref
    :text: Go To User Guide
    :classes: btn-outline-primary btn-block

Happy computing!
