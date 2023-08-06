=============
Release Notes
=============

0.0.17
======

Released July 31, 2020.

- Move documentation page to docs.coiled.io
- Added ``--version`` flag to ``coiled`` CLI
- Raise an informative error when using an outdated version of the ``coiled`` Python API
- Several documentation updates
- Added ``coiled.Cluster.get_logs`` method
- Added top-level ``coiled.config`` attribute
- Use fully qualified ``coiled.Cluster`` name in the cluster interactive IPython repr


0.0.16
======

Released July 27, 2020.

- Added getting started video to docs.
- Added support GPU enabled workers.
- Added new documentation page on configuring JupyterLab.
- Added support for specifying pip, conda, and/or container inputs when creating software environments.
- Remove account argument from ``coiled.delete_software_environment``.
- Added cost and feedback FAQs.


0.0.15
======

Released July 22, 2020.

- Removed "cloud" namespace in configuration values.
- Several documentation updates.
- Added new security and privacy page to the docs.
- Added ``coiled upload`` command for creating a Coiled software environment
  from a local conda environment.
- Added tests for command line tools.


0.0.14
======

Released July 17, 2020.


0.0.13
======

Released July 16, 2020.

- Update "Getting Started" documentation page.
- Update ``coiled.create_software_environment`` to use name provided by ``conda=`` input, if provided.
- Send AWS credentials when making a ``Cluster`` object.


0.0.12
======

Released July 14, 2020.

- Switch to using full ``coiled`` Python namespace and rename ``CoiledCluster`` to ``coiled.Cluster``
- Raise informative error when attempting to create a cluster with a non-existent cluster configuration
- Bump supported ``aiobotocore`` version to ``aiobotocore>=1.0.7``
- Add ``coiled install`` command to create conda software environments locally
- Repeated calls to ``Cloud.create_cluster_configuration`` will now update an existing configuration

0.0.11
======

Released July 9, 2020.

-  Don't shut down clusters if we didn't create them
-  Slim down the outputs of ``list_software_environments`` and ``list_cluster_configurations``

0.0.10
======

Released July 8, 2020.

-  Use websockets to create clusters due to long-running requests
-  Avoid excess endlines when printing out status in the CLI
-  Allow calling coiled env create repeatedly on the same environment

0.0.9
=====

Released July 7, 2020.

-  Change default to coiled/default
-  Add ``coiled login`` CLI command
-  Use account namespaces everywhere, remove ``account=`` keyword
-  Allow the use of public environments and configurations

0.0.8
=====

Released on July 1, 2020.

- Update to use new API endpoint scheme
- Adds ``conda env create`` command line interface


0.0.7
=====

Released on June 29, 2020.

- Adds ``Cloud.create_software_environment``, ``Cloud.delete_software_environment``, and ``Cloud.list_software_environments`` methods
- Adds ``Cloud.create_cluster_configuration``, ``Cloud.delete_cluster_configuration``, and ``Cloud.list_cluster_configurations`` methods
- Update ``Cloud`` object to use a token rather than a password
- Changed name of package from ``coiled_cloud`` to ``coiled``


0.0.6
=====

Released on May 26, 2020.

- Includes ``requirements.txt`` in ``MANIFEST.in``


0.0.5
=====

Released on May 26, 2020.

- Includes versioneer in ``MANIFEST.in``


0.0.4
=====

Released on May 26, 2020.

- Adds ``LICENSE`` to project


0.0.3
=====

Released on May 21, 2020.

Deprecations
------------

- Renamed ``Cluster`` to ``CoiledCluster``
