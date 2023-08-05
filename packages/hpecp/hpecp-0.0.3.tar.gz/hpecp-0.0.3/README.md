[![Build & Test](https://github.com/hpe-container-platform-community/hpecp-python-library/workflows/Build%20&%20Test/badge.svg?branch=master&event=push)](https://github.com/hpe-container-platform-community/hpecp-python-library/actions?query=workflow%3A%22Build+%26+Test%22+branch%3Amaster)
[![Code Checks](https://github.com/hpe-container-platform-community/hpecp-python-library/workflows/Code%20Checks/badge.svg?branch=master&event=push)](https://github.com/hpe-container-platform-community/hpecp-python-library/actions?query=workflow%3A%22Code+Checks%22+branch%3Amaster)
[![Issues](https://img.shields.io/github/issues/hpe-container-platform-community/hpecp-python-library/bug.svg)](https://github.com/hpe-container-platform-community/hpecp-python-library/issues?q=is%3Aissue+is%3Aopen+label%3A"bug")
[![Coverage Status](https://coveralls.io/repos/github/hpe-container-platform-community/hpecp-python-library/badge.png?branch=master)](https://coveralls.io/github/hpe-container-platform-community/hpecp-python-library?branch=master)
[![Pyversions](https://img.shields.io/badge/Pyversions-2.7,%203.5,%203.6,%203.7,%203.8,%203.9-green.svg)](https://github.com/hpe-container-platform-community/hpecp-python-library/blob/master/tox.ini#L7)
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/hpe-container-platform-community/hpecp-python-library)
[![Good first issues open](https://img.shields.io/github/issues/hpe-container-platform-community/hpecp-python-library/good%20first%20issue.svg?label=good%20first%20issue)](https://github.com/hpe-container-platform-community/hpecp-python-library/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)


----

```diff
- This project is under active development.
- Method APIs may change between commits.
- Not all HPE CP APIs have been implemented.
- Help Wanted - please consider contributing!
```

## Documentation

See [here](https://hpe-container-platform-community.github.io/hpecp-python-library/index.html) for User Documentation.

## Contributing

See:

- [Developing Guide](./DEVELOPING.md)
- [Contribution Guide](./CONTRIBUTING.md)

## Installation

```shell
# ensure you have an up-to-date pip
pip3 install -U pip

# install hpecp directly from git
pip3 install --upgrade git+https://github.com/hpe-container-platform-community/hpecp-client@master
```

If you are installing on Centos 7.7 with only Python 2.7 see [here](./docs/README-INSTALL-HPECP-HOSTS.md) for a workaround


## CLI examples

CLI is installed with pip ([as above](#installation))

First you need to create a config file with your endpoint details.

Note that you can have multiple profiles:

```ini
cat > ~/.hpecp.conf <<EOF
[default]
api_host = 127.0.0.1
api_port = 8080
use_ssl = True
verify_ssl = False
warn_ssl = False
username = admin
password = admin123

[tenant1]
tenant = /api/v1/tenant/15
admin = ad_admin1
password = pass123
EOF
```

Setup bash autocomplete:
```sh
source <(hpecp autocomplete bash)
```

Autocompletion:
```sh
hpecp TAB
```

K8s versions:
```sh
hpecp k8scluster k8s-supported-versions --major-filter 1 --minor-filter 17
```

Create k8s cluster:
```sh
hpecp k8scluster create --name myclus1 --k8shosts-config /api/v2/worker/k8shost/1:master --k8s_version=1.17.0
```

List with columns parameter:
```sh
hpecp k8scluster list --columns [id,description,status]
```

List with (jmespath) query parameter:
```sh
hpecp catalog list --query "[?state!='installed' && state!='installing'] | [*].[_links.self.href] | []"  --output text
```

List --query examples:
```sh
hpecp tenant examples
```

Tenant kube config:
```sh
PROFILE=tenant1 hpecp tenant k8skubeconfig > tenant1_kube.conf
```

Http call:
```sh
hpecp httpclient get /some/uri
```

Logging with HTTP tracing:
```sh
export LOG_LEVEL=DEBUG
hpecp do-something
```

More sophisticated CLI examples [here](https://github.com/bluedata-community/bluedata-demo-env-aws-terraform/tree/master/bin/experimental) 


## Basic Library Usage

See docs: https://hpe-container-platform-community.github.io/hpecp-python-library/index.html

Example:

```py3
from hpecp import ContainerPlatformClient

client = ContainerPlatformClient(username='admin',
                                password='admin123',
                                api_host='127.0.0.1',
                                api_port=8080,
                                use_ssl=True,
                                verify_ssl='/certs/hpecp-ca-cert.pem')
client.create_session() # Login

# Alternatively:
# client = ContainerPlatformClient.create_from_config_file().create_session()

print(client.k8s_cluster.list(columns=['description', 'id']))
```

On my environment, this displays:
```
+-------------+-----------------------+
| description |          id           |
+-------------+-----------------------+
| my cluster  | /api/v2/k8scluster/20 |
+-------------+-----------------------+
```

