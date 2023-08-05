# Docker Entrypoint

`docker-entrypoint` is a basic utility to proxy a container's normal entrypoint. This avoid a few pitfalls in developing and debugging processes running in kubernetes pods, namely:

- Starting/stopping debugging sessions without restarting the container, and subsequently losing state of the filesystem.
- Changing environment variables without restarting the container, so environment changes can be made without redeploying to kubernetes.

## How to Install

`docker-entrypoint` can be installed in your docker image via `pip`:

```bash
pip install docker-entrypoint
```

Since there is no mechanism for injecting the entrypoint script into your image, you'll likely want to install `docker-entrypoint` at image build time (i.e. in your Dockerfile). Here's a basic, incomplete example:

```dockerfile
FROM python:3.7
...
# Install via pip:
RUN pip install docker-entrypoint

# Continue as normal:
WORKDIR /path/to/my/app
ENTRYPOINT ["python", "main.py"]
```

## How to Use

### Running your process through `entrypoint`

`docker-entrypoint` will install an `entrypoint` driver globally which accepts your normal entrypoint command as arguments.

```bash
root@my-pod:/path/to/my/app# entrypoint python main.py
```

Since `entrypoint` must be running as PID 1 in the pod's container to have any value, we must modify the configured entrypoint for the container at launch. There are two options to do so.

#### Option one: Kubernetes Container Spec

Specify an alternate entrypoint in the container spec for your pod/deploy/statefulset manifest:

```yaml
spec:
  containers:
  - name: my-app
    command: ["entrypoint"]
    args: ["python", "main.py"]
```

#### Option two: Dockerfile `ENTRYPOINT`

Use `entrypoint` as your entrypoint in the Dockerfile itself:

```dockerfile
FROM python:3.7
...
# Install via pip:
RUN pip install docker-entrypoint

# Note the ENTRYPOINT change:
WORKDIR /path/to/my/app
ENTRYPOINT ["entrypoint", "python", "main.py"]
```

### <a name="debug"></a> Starting a debug session

Simply import the `Debugger` class, make an instance, and call `Debugger.start()`

```python
from entrypoint.debug import Debugger

dbg = Debugger()
dbg.start() # Will wait for debugger to attach, depending on configuration.

```

`docker-entrypoint` includes a module that supports remote debugging for VS Code and PyCharm. The `Debugger` class currently makes several assumptions:

| Environment Variable | Valid Options | Default |
|---|---|---|
| `DEBUGGER_ENABLED` | `true`, `false` | `false` |
| `DEBUGGER_ADDRESS` | any hostname/IP | `localhost` |
| `DEBUGGER_EDITOR` | `vscode`, `pycharm` | `vscode` |
| `DEBUGGER_WAIT` | `true`, `false` | `true`  |

These values are pulled from a "dotenv" file located at `/.env` (hidden file at root of filesystem). This is hardcoded. Additionally, the ports used for forwarding and reverse forwarding are hardcoded to `9000` and `9001`, respectively. When launching port-forwarding commands, be sure to use these ports for the pod-side binding.

Get the name of your pod:

```bash
POD_NAME=$(kubectl get pods -l release=my-app --field-selector status.phase=Running -o jsonpath={.items[0].metadata.name})
```

Restart your process. This does _not_ restart your container, only the process being managed by `entrypoint`.

```bash
kubectl exec $POD_NAME -- bash -c "kill -HUP 1"
```

Environment variables are loaded from the in-pod `.env` file prior to each launch of the debugger, so they can be updated on-demand from a local `.env` file. Simply copy your local .env file into the pod and restart your process. Again, this does _not_ restart the container.

```bash
kubectl cp .env $POD_NAME:/.env
kubectl exec $POD_NAME -- bash -c "kill -HUP 1"
```

For IDEs that create a debug server and require the remote process to attach to it (i.e. PyCharm), `Debugger.start()` will wait until `SIGUSR1` OS signal is received. Start your debug server in your IDE and send your pod a signal when its waiting for a connection.

```bash
kubectl exec $POD_NAME -- bash -c "kill -USR1 1"
```

## Module Breakdown

### main.py

Defines an `asyncio` loop for managing the process proxied by `entrypoint`. This includes forwarding relevant signals and restarting your process when it exits. The following table documents the signals that are currently handled:

| Signal | Outcome |
|---|---|
| `SIGTERM` | Causes `entrypoint` to stop managing and exit. This restarts the container as normal. |
| `SIGINT` | Causes `entrypoint` to stop managing and exit. This restarts the container as normal. |
| `SIGHUP` | Signal `entrypoint` to forward `SIGTERM` to process, and then spawns another process. |
| `SIGUSR1` | Signal `entrypoint` to continue with establishing a debugging session. Only necessary when `DEBUGGER_EDITOR=pycharm`. |

### debug.py

Defines a `Debugger` class that will start a debugging session based on environment variables (as documented [here](#debug)).

#### `Debugger.__init__()`

Loads environment variables into `os.environ` from a dotenv file located at `/.env`, and then parses these values for use in a debugging session.

#### `Debugger.start()`

Starts a debugging session.
