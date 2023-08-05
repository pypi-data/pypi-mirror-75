"""
[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-github-webhook

[![Build Status](https://travis-ci.org/cloudcomponents/cdk-constructs.svg?branch=master)](https://travis-ci.org/cloudcomponents/cdk-constructs)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-github-webhook)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-github-webhook/)

> Create, update and delete github webhooks with your app deployment

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-github-webhook
```

Python:

```bash
pip install cloudcomponents.cdk-github-webhook
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps
from aws_cdk.aws_apigateway import RestApi
from cloudcomponents.cdk_github_webhook import GithubWebhook

class GithubWebhookStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection)

        api = RestApi(self, "github-webhook")
        api.root.add_method("POST")

        github_api_token = process.env.API_TOKEN

        # @example https://github.com/cloudcomponents/cdk-constructs
        github_repo_url = process.env.REPO_URL

        # @see https://developer.github.com/v3/activity/events/types/
        events = ["*"]

        GithubWebhook(self, "GithubWebhook",
            github_api_token=github_api_token,
            github_repo_url=github_repo_url,
            payload_url=api.url,
            events=events,
            log_level="debug"
        )
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-github-webhook/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-github-webhook/LICENSE)
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

import aws_cdk.core


class GithubWebhook(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-github-webhook.GithubWebhook",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        events: typing.List[str],
        github_api_token: str,
        github_repo_url: str,
        payload_url: str,
        log_level: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param events: Determines what events the hook is triggered for.
        :param github_api_token: The OAuth access token.
        :param github_repo_url: The Github repo url.
        :param payload_url: The URL to which the payloads will be delivered.
        :param log_level: -
        """
        props = GithubWebhookProps(
            events=events,
            github_api_token=github_api_token,
            github_repo_url=github_repo_url,
            payload_url=payload_url,
            log_level=log_level,
        )

        jsii.create(GithubWebhook, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-github-webhook.GithubWebhookProps",
    jsii_struct_bases=[],
    name_mapping={
        "events": "events",
        "github_api_token": "githubApiToken",
        "github_repo_url": "githubRepoUrl",
        "payload_url": "payloadUrl",
        "log_level": "logLevel",
    },
)
class GithubWebhookProps:
    def __init__(
        self,
        *,
        events: typing.List[str],
        github_api_token: str,
        github_repo_url: str,
        payload_url: str,
        log_level: typing.Optional[str] = None,
    ) -> None:
        """
        :param events: Determines what events the hook is triggered for.
        :param github_api_token: The OAuth access token.
        :param github_repo_url: The Github repo url.
        :param payload_url: The URL to which the payloads will be delivered.
        :param log_level: -
        """
        self._values = {
            "events": events,
            "github_api_token": github_api_token,
            "github_repo_url": github_repo_url,
            "payload_url": payload_url,
        }
        if log_level is not None:
            self._values["log_level"] = log_level

    @builtins.property
    def events(self) -> typing.List[str]:
        """Determines what events the hook is triggered for.

        see
        :see: https://developer.github.com/v3/activity/events/types/
        """
        return self._values.get("events")

    @builtins.property
    def github_api_token(self) -> str:
        """The OAuth access token."""
        return self._values.get("github_api_token")

    @builtins.property
    def github_repo_url(self) -> str:
        """The Github repo url."""
        return self._values.get("github_repo_url")

    @builtins.property
    def payload_url(self) -> str:
        """The URL to which the payloads will be delivered."""
        return self._values.get("payload_url")

    @builtins.property
    def log_level(self) -> typing.Optional[str]:
        return self._values.get("log_level")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubWebhookProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GithubWebhook",
    "GithubWebhookProps",
]

publication.publish()
