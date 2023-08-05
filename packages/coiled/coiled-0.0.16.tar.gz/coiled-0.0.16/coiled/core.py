import asyncio
import copy
import json
import pathlib
import sys
import threading
from typing import Tuple, Union
import warnings
import weakref
import yaml

import aiohttp
import toolz
from tornado.ioloop import IOLoop

import dask
import dask.distributed
from distributed.utils import thread_state, sync, LoopRunner

from .utils import GatewaySecurity, handle_credentials, Spinner, parse_identifier


def delete_docstring(func):
    delete_doc = """ Delete a {kind}

Parameters
---------
name
    Name of {kind} to delete.
"""
    func_name = func.__name__
    kind = " ".join(
        func_name.split("_")[1:]
    )  # delete_software_environments -> software environments
    func.__doc__ = delete_doc.format(kind=kind)
    return func


def list_docstring(func):

    list_doc = """ List {kind}s

Parameters
---------
account
    Name of the Coiled account to list {kind}s.
    If not provided, will use the ``coiled.account`` configuration
    value.

Returns
-------
:
    Dictionary with information about each {kind} in the
    specified account. Keys in the dictionary are names of {kind}s,
    while the values contain information about the corresponding {kind}.
"""
    func_name = func.__name__
    kind = " ".join(func_name.split("_")[1:])
    kind = kind[:-1]  # drop trailing "s"
    func.__doc__ = list_doc.format(kind=kind)
    return func


async def handle_api_exception(response):
    try:
        # First see if it's an error we created that has a more useful
        # message
        error_body = await response.json()
        if "message" in error_body:
            raise Exception(error_body["message"])
        else:
            raise Exception(error_body)
    except (aiohttp.ContentTypeError, json.JSONDecodeError):
        pass

    error_text = await response.text()
    raise Exception(error_text)


# This lock helps avoid a race condition between cluster creation in the
# in process backend, which temporarily modify coiled's dask config values,
# and the creation of new Cloud objects, with load those same config values.
# This works, but is not ideal.
_cluster_creation_lock = threading.RLock()


class Cloud:
    """ Connect to Coiled

    Parameters
    ----------
    user
        Username for Coiled account. If not specified, will check the
        ``coiled.user`` configuration value.
    token
        Token for Coiled account. If not specified, will check the
        ``coiled.token`` configuration value.
    server
        Server to connect to. If not specified, will check the
        ``coiled.server`` configuration value.
    account
        The coiled account to use. If not specified,
        will check the ``coiled.account`` configuration value.
    asynchronous
        Set to True if using this Cloud within ``async``/``await`` functions or
        within Tornado ``gen.coroutines``. Otherwise this should remain
        ``False`` for normal use. Default is ``False``.
    loop
        If given, this event loop will be re-used, otherwise an appropriate one
        will be looked up or created.
    """

    _instances = weakref.WeakSet()
    _recent = list()

    def __init__(
        self,
        user: str = None,
        token: str = None,
        server: str = None,
        account: str = None,
        asynchronous: bool = False,
        loop: IOLoop = None,
    ):
        with _cluster_creation_lock:
            self.user = user or dask.config.get("coiled.user")
            self.token = token or dask.config.get("coiled.token")
            self.server = server or dask.config.get("coiled.server")
            if "://" not in self.server:
                self.server = "http://" + self.server
            self.server = self.server.rstrip("/")
            self._default_account = account or dask.config.get("coiled.account")
        self.session = None
        self.status = "init"
        self._asynchronous = asynchronous
        self._loop_runner = LoopRunner(loop=loop, asynchronous=asynchronous)
        self._loop_runner.start()

        Cloud._instances.add(self)
        Cloud._recent.append(weakref.ref(self))

        if not self.asynchronous:
            self._sync(self._start)

    def __repr__(self):
        return f"<Cloud: {self.user}@{self.server} - {self.status}>"

    def _repr_html_(self):
        text = (
            '<h3 style="text-align: left;">Cloud</h3>\n'
            '<ul style="text-align: left; list-style: none; margin: 0; padding: 0;">\n'
            f"  <li><b>User: </b>{self.user}</li>\n"
            f"  <li><b>Server: </b>{self.server}</li>\n"
            f"  <li><b>Account: </b>{self.default_account}</li>\n"
        )

        return text

    @property
    def loop(self):
        return self._loop_runner.loop

    @classmethod
    def current(cls, asynchronous=False):
        try:
            cloud = cls._recent[-1]()
            while cloud is None or cloud.status != "running":
                cls._recent.pop()
                cloud = cls._recent[-1]()
        except IndexError:
            try:
                return Cloud(asynchronous=asynchronous)
            except Exception:
                raise ValueError("Please first connect with coiled.Cloud(...)")
        else:
            return cloud

    @property
    def closed(self) -> bool:
        if self.session:
            return self.session.closed
        # If we haven't opened, we must be closed?
        return True

    async def _start(self):
        # Log in if we don't have a token
        if self.status != "init":
            return self
        if not self.token:
            self.user, self.token, self.server = await handle_credentials(
                server=self.server
            )

        self.session = aiohttp.ClientSession(
            headers={"Authorization": "Token " + self.token}
        )
        # do normal queries
        response = await self.session.request("GET", self.server + "/api/v1/users/me/")
        if response.status >= 400:
            await handle_api_exception(response)

        data = await response.json()
        self.user = data["username"]
        self.accounts = {
            d["account"]["slug"]: toolz.merge(d["account"], {"admin": d["is_admin"]},)
            for d in data["membership_set"]
        }
        if self._default_account:
            self._verify_account(self._default_account)

        self.status = "running"

        return self

    @property
    def default_account(self):
        if self._default_account:
            return self._default_account
        elif len(self.accounts) == 1:
            return toolz.first(self.accounts)
        elif self.user in self.accounts:
            return self.user
        else:
            raise ValueError(
                "Please provide an account among the following options",
                list(self.accounts),
            )

    async def _close(self):
        if self.session:
            await self.session.close()
        self.status = "closed"

    def close(self):
        """ Close connection to Coiled
        """
        return self._sync(self._close)

    def __await__(self):
        return self._start().__await__()

    async def __aenter__(self):
        return await self._start()

    async def __aexit__(self, typ, value, tb):
        await self.close()

    def __enter__(self):
        return self

    def __exit__(self, typ, value, tb):
        self.close()

    @property
    def asynchronous(self) -> bool:
        """ Are we running in the event loop? """
        return self._asynchronous and self.loop is IOLoop.current()

    def _sync(self, func, *args, asynchronous=None, callback_timeout=None, **kwargs):
        if (
            asynchronous
            or self.asynchronous
            or getattr(thread_state, "asynchronous", False)
        ):
            future = func(*args, **kwargs)
            if callback_timeout is not None:
                future = asyncio.wait_for(future, callback_timeout)
            return future
        else:
            return sync(
                self.loop, func, *args, callback_timeout=callback_timeout, **kwargs
            )

    async def _list_clusters(self, account: str = None):
        account = account or self.default_account
        response = await self.session.request(
            "GET", self.server + "/api/v1/{}/clusters/".format(account),
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)

        data = await response.json()
        return {
            d["name"]: format_cluster_output(d)
            for d in data["results"]
            if d["status"] in ("pending", "running")
        }

    @list_docstring
    def list_clusters(self, account: str = None):
        return self._sync(self._list_clusters, account)

    async def _create_cluster(
        self,
        name: str,
        configuration: str = None,
        account: str = None,
        log_output=sys.stdout,
    ):
        account = account or self.default_account
        self._verify_account(account)
        data = {"name": name, "server": self.server, "configuration": configuration}
        ws_server = self.server.replace("http", "ws", 1)
        ws_endpoint = f"{ws_server}/ws/api/v1/{account}/clusters/"
        try:
            ws = await self.session.ws_connect(ws_endpoint)
        except aiohttp.WSServerHandshakeError:
            raise ValueError(
                "Unable to connect to server, do you have permissions to "
                f'create clusters in the "{account}" account?'
            )
        await ws.send_json(data)
        error_details = await self._websocket_stream(
            "Creating Cluster. This takes about a minute", ws, log_output
        )
        if error_details:
            raise ValueError(f"Unable to create cluster: {error_details}")

    def create_cluster(
        self, name: str, configuration: str, account: str = None, log_output=sys.stdout
    ):
        # TODO cleanup repetition of explaining a configuration identifier (see docstring for
        # creating software_environments)
        return self._sync(
            self._create_cluster,
            name=name,
            configuration=configuration,
            account=account,
        )

    async def _delete_cluster(self, name: str, account: str = None):
        account = account or self.default_account
        response = await self.session.request(
            "DELETE", self.server + "/api/v1/{}/clusters/{}/".format(account, name),
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)

    @delete_docstring
    def delete_cluster(self, name: str, account: str = None):
        return self._sync(self._delete_cluster, name, account)

    async def _cluster_status(self, name: str, account: str = None) -> dict:
        account = account or self.default_account
        response = await self.session.request(
            "GET", self.server + "/api/v1/{}/clusters/{}/".format(account, name),
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)

        data = await response.json()
        return data

    async def _security(
        self, name: str, account: str = None
    ) -> Tuple[dask.distributed.Security, dict]:
        while True:
            data = await self._cluster_status(name=name, account=account)
            if data["status"] != "pending" and data["public_address"]:
                break
            else:
                await asyncio.sleep(1.0)

        security = GatewaySecurity(data["tls_key"], data["tls_cert"])

        return security, data

    def security(
        self, name: str, account: str = None
    ) -> Tuple[dask.distributed.Security, dict]:
        return self._sync(self._security, name, account)

    async def _scale(self, name: str, n: int, account: str = None) -> None:
        account = account or self.default_account
        response = await self.session.request(
            "PATCH",
            self.server + "/api/v1/{}/clusters/{}/scale/".format(account, name),
            data={"worker_count_requested": n},
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)

    def scale(self, name: str, n: int, account: str = None) -> None:
        """ Scale cluster to ``n`` workers

        Parameters
        ----------
        name
            Name of cluster.
        n
            Number of workers to scale cluster size to.
        account
            Name of Coiled account which the cluster belongs to.
            If not provided, will default to ``Cloud.default_account``.
        """
        return self._sync(self._scale, name, n, account)

    def _verify_account(self, account: str):
        """ Perform sanity checks on account values

        In particular, this raises and informative error message if the
        account is not found, and provides a list of possible options.
        """
        account = account or self.default_account
        if account not in self.accounts:
            raise PermissionError(
                "Account not found: '{}'\n"
                "Possible accounts: {}".format(account, sorted(self.accounts))
            )

    def create_software_environment(
        self,
        name: str = None,
        conda: Union[list, dict, str] = None,
        pip: Union[list, str] = None,
        container: str = None,
        log_output=sys.stdout,
    ) -> dict:
        return self._sync(
            self._create_software_environment,
            name=name,
            conda=conda,
            pip=pip,
            container=container,
            log_output=log_output,
        )

    async def _create_software_environment(
        self, name=None, conda=None, pip=None, container=None, log_output=sys.stdout
    ):
        # TODO: Eventually this should be v1/<str:account>/software_environments/<int:pk>
        if isinstance(conda, list):
            conda = {"dependencies": conda}
        elif isinstance(conda, (str, pathlib.Path)):
            # Local conda environment YAML file
            with open(conda, mode="r") as f:
                conda = yaml.safe_load(f)

        if isinstance(pip, (str, pathlib.Path)):
            # Local pip requirements file
            with open(pip, mode="r") as f:
                pip = f.read().splitlines()

        # Conda supports specifying pip packages via their CLI, but not when
        # using conda.api.Solver. So we move any pip packages to the pip portion
        # of this software environment
        if conda is not None:
            for idx, dep in enumerate(conda["dependencies"]):
                if isinstance(dep, dict) and list(dep.keys()) == ["pip"]:
                    # Copy conda to avoid mutating input from users
                    conda = copy.deepcopy(conda)
                    pip_packages = conda["dependencies"].pop(idx)["pip"]
                    if pip is not None:
                        pip = pip + pip_packages
                    else:
                        pip = pip_packages

        # Remove duplicates and ensure consistent package ordering which helps with
        # downstream tokenization of package spec
        if pip is not None:
            pip = sorted(set(pip))
        if conda is not None:
            conda["dependencies"] = sorted(set(conda["dependencies"]))

        if name is None and conda is not None and "name" in conda:
            name = conda["name"]
        if name is None:
            raise ValueError("Must provide a name when creating a software environment")

        account, name = self._normalize_name(name)

        # Connect to the websocket, send the data and get some logs
        # TODO add other types as well
        data = {"container": container, "conda": conda, "pip": pip}
        # TODO shouldn't this be "wss" in production?
        ws_server = self.server.replace("http", "ws", 1)
        ws_endpoint = f"{ws_server}/ws/api/v1/{account}/software_environments/{name}/"

        try:
            ws = await self.session.ws_connect(ws_endpoint)
        except aiohttp.WSServerHandshakeError:
            raise ValueError(
                "Unable to connect to server, do you have permissions to "
                f'create environments in the "{account}" account?'
            )
        await ws.send_json(data)
        error_details = await self._websocket_stream(
            "Updating Software Environment", ws, log_output
        )
        if error_details:
            raise ValueError(f"Unable to update Environment: {error_details}")

    async def _list_software_environments(self, account=None):
        account = account or self.default_account
        response = await self.session.request(
            "GET", self.server + "/api/v1/{}/software_environments/".format(account),
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)
        else:
            results = (await response.json())["results"]
            results = {
                r["name"]: format_software_environment_output(r) for r in results
            }
            return results

    @list_docstring
    def list_software_environments(self, account=None) -> dict:
        return self._sync(self._list_software_environments, account=account)

    @delete_docstring
    def delete_software_environment(self, name):
        return self._sync(self._delete_software_environment, name)

    def _normalize_name(self, name: str) -> Tuple[str, str]:
        account, name = parse_identifier(name)
        account = account or self.default_account
        return account, name

    async def _delete_software_environment(self, name):
        account, name = self._normalize_name(name)
        response = await self.session.request(
            "DELETE", self.server + f"/api/v1/{account}/software_environments/{name}/",
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)

    def create_cluster_configuration(
        self,
        name: str,
        software: str,
        worker_cpu: int = 1,
        worker_gpu: int = 0,
        worker_memory: str = "4 GiB",
        scheduler_cpu: int = 1,
        scheduler_memory: str = "4 GiB",
    ) -> dict:
        return self._sync(
            self._create_cluster_configuration,
            name=name,
            software=software,
            worker_cpu=worker_cpu,
            worker_gpu=worker_gpu,
            worker_memory=worker_memory,
            scheduler_cpu=scheduler_cpu,
            scheduler_memory=scheduler_memory,
        )

    async def _create_cluster_configuration(
        self,
        name: str,
        software: str,
        worker_cpu: int,
        worker_gpu: int,
        worker_memory: str,
        scheduler_cpu: int,
        scheduler_memory: str,
    ):
        account, name = self._normalize_name(name)
        data = {
            "software_environment": software,
            "worker_cpu": worker_cpu,
            "worker_gpu": worker_gpu,
            "worker_memory": max(
                # TODO we should be throwing an error instead of choosing
                # 1 if they give use something below 1.
                dask.utils.parse_bytes(worker_memory) // 2 ** 30,
                1,
            ),
            "scheduler_cpu": scheduler_cpu,
            "scheduler_memory": max(
                dask.utils.parse_bytes(scheduler_memory) // 2 ** 30, 1
            ),
            # TODO environments
        }
        # Check if we already have a config
        response = await self.session.request(
            "GET", self.server + f"/api/v1/{account}/cluster_configurations/{name}/"
        )
        if response.status == 404:
            data.update({"name": name})
            response = await self.session.request(
                "POST",
                self.server + f"/api/v1/{account}/cluster_configurations/",
                data=data,
            )
        else:
            response = await self.session.request(
                "PATCH",
                self.server + f"/api/v1/{account}/cluster_configurations/{name}/",
                data=data,
            )

        if response.status >= 400:
            await handle_api_exception(response)

    @list_docstring
    def list_cluster_configurations(self, account=None) -> dict:
        return self._sync(self._list_cluster_configurations, account=account)

    async def _list_cluster_configurations(self, account=None):
        account = account or self.default_account
        response = await self.session.request(
            "GET", self.server + f"/api/v1/{account}/cluster_configurations/",
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)
        else:
            results = (await response.json())["results"]
            results = {
                r["name"]: format_cluster_configuration_output(r) for r in results
            }
            return results

    @delete_docstring
    def delete_cluster_configuration(self, name):
        return self._sync(self._delete_cluster_configuration, name)

    async def _delete_cluster_configuration(self, name):
        if "/" in name:
            account, name = name.split("/")
        else:
            account = self.default_account
        response = await self.session.request(
            "DELETE", self.server + f"/api/v1/{account}/cluster_configurations/{name}/",
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)

    async def _websocket_stream(self, initial_message, ws, log_output):
        error_details = None
        with Spinner(f"{initial_message} ... "):
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = msg.json()
                    message = data["message"]
                    if data.get("raise", False):
                        error_details = message
                    print(f"\n{message}", file=log_output)
                elif msg.type == aiohttp.WSMsgType.CLOSE:
                    await ws.close()

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    # TODO find out what would be in one of these messages
                    error_details = str(msg.extra)
                    break
        return error_details


# Utility functions for formatting list_* endpoint responses to be more user-friendly


def format_account_output(d):
    return d["slug"]


def format_software_environment_output(d):
    d = d.copy()
    for i in ["id", "name", "private", "image_name"]:
        d.pop(i)
    d["account"] = format_account_output(d["account"])
    return d


def format_cluster_configuration_output(d):
    d = d.copy()
    d.pop("id")
    d.pop("name")
    d["account"] = format_account_output(d["account"])
    for process in ["scheduler", "worker"]:
        d[process].pop("id")
        d[process].pop("name")
        d[process].pop("account")
        d[process]["software"] = "/".join(
            [
                d[process]["software_environment"]["account"]["slug"],
                d[process]["software_environment"]["name"],
            ]
        )
        d[process].pop("software_environment")
    return d


def format_cluster_output(d):
    d = d.copy()
    for key in ["auth_token", "preload_key", "private_address", "name", "last_seen"]:
        d.pop(key)
    d["account"] = format_account_output(d["account"])
    # Rename "public_address" to "address"
    d["address"] = d["public_address"]
    d.pop("public_address")
    return d


# Public API


def create_software_environment(
    name: str = None,
    conda: Union[list, dict, str] = None,
    pip: Union[list, str] = None,
    container: str = None,
    log_output=sys.stdout,
) -> dict:
    """ Create a software environment

    Parameters
    ---------
    name
        Name of software environment.
    conda
        Specification for packages to install into the software environment using conda.
        Can be a list of packages, a dictionary, or a path to a conda environment YAML file.
    pip
        Packages to install into the software environment using pip.
        Can be a list of packages or a path to a pip requirements file.
    container
        Docker image to use for the software environment. Must be the name of a docker image
        on Docker hub.
    log_output
        Stream to output logs to. Defaults to ``sys.stdout``.
    """
    with Cloud() as cloud:
        return cloud.create_software_environment(
            name=name, conda=conda, pip=pip, container=container, log_output=log_output
        )


@list_docstring
def list_software_environments(account=None):
    with Cloud(account=account) as cloud:
        return cloud.list_software_environments(account=account)


@delete_docstring
def delete_software_environment(name):
    with Cloud() as cloud:
        return cloud.delete_software_environment(name=name)


def create_cluster_configuration(
    name: str,
    software: str,
    worker_cpu: int = 1,
    worker_gpu: int = 0,
    worker_memory: str = "4 GiB",
    scheduler_cpu: int = 1,
    scheduler_memory: str = "4 GiB",
) -> dict:
    """ Create a cluster configuration

    Parameters
    ----------
    name
        Name of cluster configuration.
        Optionally prefixed with an account name like "myaccount/myname"
    software
        Identifier of the software environment to use, in the format (<account>/)<name>. If the software environment
        is owned by the same account as that passed into "account", the (<account>/) prefix is optional.

        For example, suppose your account is "wondercorp", but your friends at "friendlycorp" have an environment
        named "xgboost" that you want to use; you can specify this with "friendlycorp/xgboost". If you simply
        entered "xgboost", this is shorthand for "wondercorp/xgboost".

        The "name" portion of (<account>/)<name> can only contain ASCII letters, hyphens and underscores.
    worker_cpu
        Number of CPUs allocated for each worker. Defaults to 1.
    worker_gpu
        Number of GPUs allocated for each worker. Defaults to 0 (no GPU support). Note that this will _always_
        allocate GPU-enabled workers, so is expensive.
    worker_memory
        Amount of memory to allocate for each worker. Defaults to 4 GiB.
    scheduler_cpu
        Number of CPUs allocated for the scheduler. Defaults to 1.
    scheduler_memory
        Amount of memory to allocate for the scheduler. Defaults to 4 GiB.

    See Also
    --------
    dask.utils.parse_bytes
    """
    with Cloud() as cloud:
        return cloud.create_cluster_configuration(
            name=name,
            software=software,
            worker_cpu=worker_cpu,
            worker_gpu=worker_gpu,
            worker_memory=worker_memory,
            scheduler_cpu=scheduler_cpu,
            scheduler_memory=scheduler_memory,
        )


@list_docstring
def list_cluster_configurations(account=None):
    with Cloud(account=account) as cloud:
        return cloud.list_cluster_configurations(account=account)


@delete_docstring
def delete_cluster_configuration(name):
    with Cloud() as cloud:
        return cloud.delete_cluster_configuration(name=name)


def create_cluster(
    name: str, configuration: str, account: str = None, log_output=sys.stdout
):
    """ Create a cluster

    Parameters
    ---------
    name
        Name of cluster.
    configuration
        Identifier of the cluster configuration to use, in the format (<account>/)<name>. If the configuration
        is owned by the same account as that passed into "account", the (<account>/) prefix is optional.

        For example, suppose your account is "wondercorp", but your friends at "friendlycorp" have a configuration
        named "xgboost" that you want to use; you can specify this with "friendlycorp/xgboost". If you simply
        entered "xgboost", this is shorthand for "wondercorp/xgboost".
    account
        Name of the Coiled account to create the cluster in.
        If not provided, will default to ``Cloud.default_account``.

    See Also
    --------
    coiled.Cluster
    """
    warnings.warn(
        "Please use coiled.Cluster() for creating clusters instead of coiled.create_cluster()."
        "coiled.Cluster() offers more control over the cluster you create and is the recommended approach."
    )
    with Cloud(account=account) as cloud:
        return cloud.create_cluster(
            name=name,
            configuration=configuration,
            account=account,
            log_output=log_output,
        )


@list_docstring
def list_clusters(account=None):
    with Cloud() as cloud:
        return cloud.list_clusters(account=account)


@delete_docstring
def delete_cluster(name: str, account: str = None):
    with Cloud() as cloud:
        return cloud.delete_cluster(name=name, account=account)
