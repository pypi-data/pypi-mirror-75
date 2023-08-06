"""
[![NPM version](https://badge.fury.io/js/cdk-gitlab-runner.svg)](https://badge.fury.io/js/cdk-gitlab-runner)
[![PyPI version](https://badge.fury.io/py/cdk-gitlab-runner.svg)](https://badge.fury.io/py/cdk-gitlab-runner)
![Release](https://github.com/guan840912/cdk-gitlab-runner/workflows/Release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-gitlab-runner?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-gitlab-runner?label=pypi&color=blue)

![](https://img.shields.io/badge/iam_role_self-enable-green=?style=plastic&logo=appveyor)
![](https://img.shields.io/badge/vpc_self-enable-green=?style=plastic&logo=appveyor)
![](https://img.shields.io/badge/gitlab_url-customize-green=?style=plastic&logo=appveyor)

# Welcome to `cdk-gitlab-runner`

This repository template helps you create gitlab runner on your aws account via AWS CDK one line.

## Note

### Default will help you generate below services:

* VPC

  * Public Subnet (2)
* EC2 (1 T3.micro)

## Before start you need gitlab runner token in your  `gitlab project` or   `gitlab group`

### In Group

Group > Settings > CI/CD
![group](image/group_runner_page.png)

### In Group

Project > Settings > CI/CD > Runners
![project](image/project_runner_page.png)

## Usage

Replace your gitlab runner token in `$GITLABTOKEN`

### Instance Type

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab_runner import GitlabContainerRunner

# If want change instance type to t3.large .
GitlabContainerRunner(self, "runner-instance", gitlabtoken="$GITLABTOKEN", ec2type="t3.large")
# OR
# Just create a gitlab runner , by default instance type is t3.micro .
from cdk_gitlab_runner import GitlabContainerRunner

GitlabContainerRunner(self, "runner-instance", gitlabtoken="$GITLABTOKEN")
```

### Gitlab Server Customize Url .

If you want change  what  you want tag name .

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# If you want change  what  your self Gitlab Server Url .
from cdk_gitlab_runner import GitlabContainerRunner

GitlabContainerRunner(self, "runner-instance-change-tag", gitlabtoken="$GITLABTOKEN", gitlaburl="https://gitlab.my.com/")
```

### Tags

If you want change  what  you want tag name .

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# If you want change  what  you want tag name .
from cdk_gitlab_runner import GitlabContainerRunner

GitlabContainerRunner(self, "runner-instance-change-tag", gitlabtoken="$GITLABTOKEN", tag1="aa", tag2="bb", tag3="cc")
```

### IAM Policy

If you want add runner other IAM Policy like s3-readonly-access.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# If you want add runner other IAM Policy like s3-readonly-access.
from cdk_gitlab_runner import GitlabContainerRunner
from aws_cdk.aws_iam import ManagedPolicy

runner = GitlabContainerRunner(self, "runner-instance-add-policy", gitlabtoken="$GITLABTOKEN", tag1="aa", tag2="bb", tag3="cc")
runner.runner_role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"))
```

### Security Group

If you want add runner other SG Ingress .

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# If you want add runner other SG Ingress .
from cdk_gitlab_runner import GitlabContainerRunner
from aws_cdk.aws_ec2 import Port, Peer

runner = GitlabContainerRunner(self, "runner-add-SG-ingress", gitlabtoken="GITLABTOKEN", tag1="aa", tag2="bb", tag3="cc")

# you can add ingress in your runner SG .
runner.runne_ec2.connections.allow_from(Peer.ipv4("0.0.0.0/0"), Port.tcp(80))
```

### Use self VPC

> 2020/06/27 , you can use your self exist VPC or new VPC , but please check your `vpc public Subnet` Auto-assign public IPv4 address must be Yes ,or `vpc private Subnet` route table associated `nat gateway` .

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab_runner import GitlabContainerRunner
from aws_cdk.aws_ec2 import Port, Peer, Vpc, SubnetType
from aws_cdk.aws_iam import ManagedPolicy

newvpc = Vpc(stack, "VPC",
    cidr="10.1.0.0/16",
    max_azs=2,
    subnet_configuration=[SubnetConfiguration(
        cidr_mask=26,
        name="RunnerVPC",
        subnet_type=SubnetType.PUBLIC
    )],
    nat_gateways=0
)

runner = GitlabContainerRunner(self, "testing", gitlabtoken="$GITLABTOKEN", ec2type="t3.small", selfvpc=newvpc)
```

### Use your self exist role

> 2020/06/27 , you can use your self exist role assign to runner

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab_runner import GitlabContainerRunner
from aws_cdk.aws_ec2 import Port, Peer
from aws_cdk.aws_iam import ManagedPolicy, Role, ServicePrincipal

role = Role(self, "runner-role",
    assumed_by=ServicePrincipal("ec2.amazonaws.com"),
    description="For Gitlab EC2 Runner Test Role",
    role_name="TestRole"
)

runner = GitlabContainerRunner(stack, "testing", gitlabtoken="$GITLAB_TOKEN", ec2iamrole=role)
runner.runner_role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"))
```

# Note

![](https://img.shields.io/badge/version-1.47.1-green=?style=plastic&logo=appveyor) vs ![](https://img.shields.io/badge/version-1.49.1-green=?style=plastic&logo=appveyor)

> About change instance type

This is before ![](https://img.shields.io/badge/version-1.47.1-green=?style) ( included ![](https://img.shields.io/badge/version-1.47.1-green=?style) )

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_ec2 import InstanceType, InstanceClass, InstanceSize
from cdk_gitlab_runner import GitlabContainerRunner

# If want change instance type to t3.large .
GitlabContainerRunner(self, "runner-instance", gitlabtoken="$GITLABTOKEN", ec2type=InstanceType.of(InstanceClass.T3, InstanceSize.LARGE))
```

This is ![](https://img.shields.io/badge/version-1.49.1-green=?style)

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab_runner import GitlabContainerRunner

# If want change instance type to t3.large .
GitlabContainerRunner(self, "runner-instance", gitlabtoken="$GITLABTOKEN", ec2type="t3.large")
```

## Wait about 6 mins , If success you will see your runner in that page .

![runner](image/group_runner2.png)

#### you can use tag `gitlab` , `runner` , `awscdk`  ,

## Example     *`gitlab-ci.yaml`*

[gitlab docs see more ...](https://docs.gitlab.com/ee/ci/yaml/README.html)

```yaml
dockerjob:
  image: docker:18.09-dind
  variables:
  tags:
    - runner
    - awscdk
    - gitlab
  variables:
    DOCKER_TLS_CERTDIR: ""
  before_script:
    - docker info
  script:
    - docker info;
    - echo 'test 123';
    - echo 'hello world 1228'
```

### If your want to debug you can go to aws console

# `In your runner region !!!`

## AWS Systems Manager  >  Session Manager  >  Start a session

![system manager](image/session.png)

#### click your `runner` and click `start session`

#### in the brower console in put `bash`

```bash
# become to root
sudo -i

# list runner container .
root# docker ps -a

# modify gitlab-runner/config.toml

root# cd /home/ec2-user/.gitlab-runner/ && ls
config.toml

```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.core


class GitlabContainerRunner(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-gitlab-runner.GitlabContainerRunner",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        gitlabtoken: str,
        ec2iamrole: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        ec2type: typing.Optional[str] = None,
        gitlaburl: typing.Optional[str] = None,
        selfvpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        tag1: typing.Optional[str] = None,
        tag2: typing.Optional[str] = None,
        tag3: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param gitlabtoken: Gitlab token for the Register Runner . Default: - You must to give the token !!!
        :param ec2iamrole: IAM role for the Gitlab Runner Instance . Default: - new Role for Gitlab Runner Instance , attach AmazonSSMManagedInstanceCore Policy .
        :param ec2type: Runner default EC2 instance type. Default: - t3.micro
        :param gitlaburl: Gitlab Runner register url . Default: - gitlaburl='https://gitlab.com/'
        :param selfvpc: VPC for the Gitlab Runner . Default: - new VPC will be created , 1 Vpc , 2 Public Subnet .
        :param tag1: Gitlab Runner register tag1 . Default: - tag1: gitlab .
        :param tag2: Gitlab Runner register tag2 . Default: - tag2: awscdk .
        :param tag3: Gitlab Runner register tag3 . Default: - tag3: runner .

        stability
        :stability: experimental
        """
        props = GitlabContainerRunnerProps(
            gitlabtoken=gitlabtoken,
            ec2iamrole=ec2iamrole,
            ec2type=ec2type,
            gitlaburl=gitlaburl,
            selfvpc=selfvpc,
            tag1=tag1,
            tag2=tag2,
            tag3=tag3,
        )

        jsii.create(GitlabContainerRunner, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="runnerEc2")
    def runner_ec2(self) -> aws_cdk.aws_ec2.IInstance:
        """This represents a Runner EC2 instance .

        stability
        :stability: experimental
        """
        return jsii.get(self, "runnerEc2")

    @builtins.property
    @jsii.member(jsii_name="runnerRole")
    def runner_role(self) -> aws_cdk.aws_iam.IRole:
        """The IAM role assumed by the Runner instance .

        stability
        :stability: experimental
        """
        return jsii.get(self, "runnerRole")


@jsii.data_type(
    jsii_type="cdk-gitlab-runner.GitlabContainerRunnerProps",
    jsii_struct_bases=[],
    name_mapping={
        "gitlabtoken": "gitlabtoken",
        "ec2iamrole": "ec2iamrole",
        "ec2type": "ec2type",
        "gitlaburl": "gitlaburl",
        "selfvpc": "selfvpc",
        "tag1": "tag1",
        "tag2": "tag2",
        "tag3": "tag3",
    },
)
class GitlabContainerRunnerProps:
    def __init__(
        self,
        *,
        gitlabtoken: str,
        ec2iamrole: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        ec2type: typing.Optional[str] = None,
        gitlaburl: typing.Optional[str] = None,
        selfvpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        tag1: typing.Optional[str] = None,
        tag2: typing.Optional[str] = None,
        tag3: typing.Optional[str] = None,
    ) -> None:
        """
        :param gitlabtoken: Gitlab token for the Register Runner . Default: - You must to give the token !!!
        :param ec2iamrole: IAM role for the Gitlab Runner Instance . Default: - new Role for Gitlab Runner Instance , attach AmazonSSMManagedInstanceCore Policy .
        :param ec2type: Runner default EC2 instance type. Default: - t3.micro
        :param gitlaburl: Gitlab Runner register url . Default: - gitlaburl='https://gitlab.com/'
        :param selfvpc: VPC for the Gitlab Runner . Default: - new VPC will be created , 1 Vpc , 2 Public Subnet .
        :param tag1: Gitlab Runner register tag1 . Default: - tag1: gitlab .
        :param tag2: Gitlab Runner register tag2 . Default: - tag2: awscdk .
        :param tag3: Gitlab Runner register tag3 . Default: - tag3: runner .

        stability
        :stability: experimental
        """
        self._values = {
            "gitlabtoken": gitlabtoken,
        }
        if ec2iamrole is not None:
            self._values["ec2iamrole"] = ec2iamrole
        if ec2type is not None:
            self._values["ec2type"] = ec2type
        if gitlaburl is not None:
            self._values["gitlaburl"] = gitlaburl
        if selfvpc is not None:
            self._values["selfvpc"] = selfvpc
        if tag1 is not None:
            self._values["tag1"] = tag1
        if tag2 is not None:
            self._values["tag2"] = tag2
        if tag3 is not None:
            self._values["tag3"] = tag3

    @builtins.property
    def gitlabtoken(self) -> str:
        """Gitlab token for the Register Runner .

        default
        :default: - You must to give the token !!!

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN")
        """
        return self._values.get("gitlabtoken")

    @builtins.property
    def ec2iamrole(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """IAM role for the Gitlab Runner Instance .

        default
        :default: - new Role for Gitlab Runner Instance , attach AmazonSSMManagedInstanceCore Policy .

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            role = Role(stack, "runner-role",
                assumed_by=ServicePrincipal("ec2.amazonaws.com"),
                description="For Gitlab EC2 Runner Test Role",
                role_name="Myself-Runner-Role"
            )
            
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", ec2iamrole=role)
        """
        return self._values.get("ec2iamrole")

    @builtins.property
    def ec2type(self) -> typing.Optional[str]:
        """Runner default EC2 instance type.

        default
        :default: - t3.micro

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", ec2type="t3.small")
        """
        return self._values.get("ec2type")

    @builtins.property
    def gitlaburl(self) -> typing.Optional[str]:
        """Gitlab Runner register url .

        default
        :default: - gitlaburl='https://gitlab.com/'

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            runner = GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", gitlaburl="https://gitlab.com/")
        """
        return self._values.get("gitlaburl")

    @builtins.property
    def selfvpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC for the Gitlab Runner .

        default
        :default: - new VPC will be created , 1 Vpc , 2 Public Subnet .

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            newvpc = Vpc(stack, "NEWVPC",
                cidr="10.1.0.0/16",
                max_azs=2,
                subnet_configuration=[{
                    "cidr_mask": 26,
                    "name": "RunnerVPC",
                    "subnet_type": SubnetType.PUBLIC
                }],
                nat_gateways=0
            )
            
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", selfvpc=newvpc)
        """
        return self._values.get("selfvpc")

    @builtins.property
    def tag1(self) -> typing.Optional[str]:
        """Gitlab Runner register tag1  .

        default
        :default: - tag1: gitlab .

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", tag1="aa")
        """
        return self._values.get("tag1")

    @builtins.property
    def tag2(self) -> typing.Optional[str]:
        """Gitlab Runner register tag2  .

        default
        :default: - tag2: awscdk .

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", tag2="bb")
        """
        return self._values.get("tag2")

    @builtins.property
    def tag3(self) -> typing.Optional[str]:
        """Gitlab Runner register tag3  .

        default
        :default: - tag3: runner .

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", tag3="cc")
        """
        return self._values.get("tag3")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitlabContainerRunnerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GitlabContainerRunner",
    "GitlabContainerRunnerProps",
]

publication.publish()
