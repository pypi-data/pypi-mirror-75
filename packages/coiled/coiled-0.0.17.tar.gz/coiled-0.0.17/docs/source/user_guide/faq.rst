===
FAQ
===


- :ref:`free-beta`
- :ref:`feedback-faq`
- :ref:`why-local-software`
- :ref:`why-should-packages-match`
- :ref:`version-mismatch-warning`


.. _free-beta:

How much does Coiled cost?
--------------------------

Coiled is currently in a closed beta stage. During this time **Coiled is free for all beta users**.
You will not be charged for any of the compute resources you use, however there is a limit of
100 concurrently running cores per user. This policy will change in the future when Coiled is opened
up to a broader audience, but until then we are happy to provide beta users cloud computing
resources at no cost. Thank you for trying out Coiled!


.. _feedback-faq:

How can I report a feature request, bug, etc?
---------------------------------------------

Please `open an issue <https://github.com/coiled/coiled-issues/issues/new>`_ on the
`Coiled issue tracker <https://github.com/coiled/coiled-issues>`_. Feel free to report bugs, submit
feature requests, ask questions, or provide other input. Your feedback is valued and will help influence
the future of Coiled.


.. _why-local-software:

Why do I need a local software environment?
-------------------------------------------

When performing distributed computation with Dask, you’ll create a :class:`distributed.Client`
object which connects your local Python process (e.g. your laptop) to your remote Dask cluster
(e.g. running on AWS). Dask ``Client`` s are the user-facing entry point for submitting tasks to
a Dask cluster. When using a ``Client`` to submit tasks to your cluster, Dask will package up and send data,
functions, and other Python objects needed for your computations *from* your local Python process
where your ``Client`` is running *to* your remote Dask cluster in order for them to be executed.

This means that if you want to run a function on your Dask cluster, for example NumPy’s :func:`numpy.mean`
function, then you must have NumPy installed in your local Python process so Dask can send the ``numpy.mean``
function from your local Dask ``Client`` to the workers in your Dask cluster. For this reason,
it’s recommended to have the same libraries installed on both your local machine and on the remote
workers in your cluster.

See the :ref:`managing-software-environments` section for more details on how to easily
synchronize your local and remote software environments using Coiled.


.. _why-should-packages-match:

Why should my local and remote libraries match?
-----------------------------------------------

When performing distributed computations Dask will serialize data, functions, and other
Python objects needed for the computation in order to send them between your local Python
process (e.g. your laptop) and the scheduler and workers in your Dask cluster
(e.g. running on AWS). Mismatches in library versions between your local Python process and
cluster worker processes can disrupt this serialization / deserialization process in a variety
of ways. For example, widely used serialization libraries like
`Cloudpickle <https://github.com/cloudpipe/cloudpickle>`_ aren’t guaranteed to work across
different versions of Python, so in some cases you may run into errors when using different
Python versions on your laptop and the workers in your cluster.

Because of this it’s recommended that library versions match on both your local machine
and on the remote workers in your cluster. Coiled allows you to seamlessly synchronize your local
and remote software environments using the ``coiled`` command line interface.
See the :ref:`managing-software-environments` section for more details.


.. _version-mismatch-warning:

Why do I see a version mismatch warning?
----------------------------------------

Dask will emit a warning when it finds multiple versions of the same package on a cluster.
When using Coiled this most often means there's a version mismatch between a package in
your local environment and the remote cluster environment. For example, you might have NumPy 1.18.2
installed in your local Python environment on your laptop, while the remote Dask cluster on AWS
has NumPy 1.18.4 installed.

Ensuring package versions match is something that we're working on. In the meantime you might
want to install the following packages locally:

.. code-block::

    conda install --yes \
        -c conda-forge \
        python==3.8 \
        python-blosc \
        cytoolz \
        dask==2.16.0 \
        lz4 \
        nomkl \
        numpy==1.18.1 \
        pandas==1.0.1
