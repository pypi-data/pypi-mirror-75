"""
[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-contentful-webhook

[![Build Status](https://travis-ci.org/cloudcomponents/cdk-constructs.svg?branch=master)](https://travis-ci.org/cloudcomponents/cdk-constructs)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-contentful-webhook)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-contentful-webhook/)

> Create, update and delete contentful webhooks with your app deployment

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-contentful-webhook
```

Python:

```bash
pip install cloudcomponents.cdk-contentful-webhook
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps
from aws_cdk.aws_apigateway import RestApi
from cloudcomponents.cdk_contentful_webhook import ContentfulWebhook

class ContentfulWebhookStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection)

        api = RestApi(self, "Endpoint")
        api.root.add_method("POST")

        access_token = process.env.ACCESS_TOKEN

        space_id = process.env.SPACE_ID

        topics = ["Entry.create"]

        ContentfulWebhook(self, "ContentfulWebhook",
            access_token=access_token,
            space_id=space_id,
            name="ExampleWebhook",
            url=api.url,
            topics=topics,
            log_level="debug"
        )
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-contentful-webhook/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-contentful-webhook/LICENSE)
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


class ContentfulWebhook(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-contentful-webhook.ContentfulWebhook",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        access_token: str,
        name: str,
        space_id: str,
        topics: typing.List[str],
        url: str,
        log_level: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param access_token: -
        :param name: -
        :param space_id: -
        :param topics: -
        :param url: -
        :param log_level: -
        """
        props = ContentfulWebhookProps(
            access_token=access_token,
            name=name,
            space_id=space_id,
            topics=topics,
            url=url,
            log_level=log_level,
        )

        jsii.create(ContentfulWebhook, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-contentful-webhook.ContentfulWebhookProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "name": "name",
        "space_id": "spaceId",
        "topics": "topics",
        "url": "url",
        "log_level": "logLevel",
    },
)
class ContentfulWebhookProps:
    def __init__(
        self,
        *,
        access_token: str,
        name: str,
        space_id: str,
        topics: typing.List[str],
        url: str,
        log_level: typing.Optional[str] = None,
    ) -> None:
        """
        :param access_token: -
        :param name: -
        :param space_id: -
        :param topics: -
        :param url: -
        :param log_level: -
        """
        self._values = {
            "access_token": access_token,
            "name": name,
            "space_id": space_id,
            "topics": topics,
            "url": url,
        }
        if log_level is not None:
            self._values["log_level"] = log_level

    @builtins.property
    def access_token(self) -> str:
        return self._values.get("access_token")

    @builtins.property
    def name(self) -> str:
        return self._values.get("name")

    @builtins.property
    def space_id(self) -> str:
        return self._values.get("space_id")

    @builtins.property
    def topics(self) -> typing.List[str]:
        return self._values.get("topics")

    @builtins.property
    def url(self) -> str:
        return self._values.get("url")

    @builtins.property
    def log_level(self) -> typing.Optional[str]:
        return self._values.get("log_level")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContentfulWebhookProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ContentfulWebhook",
    "ContentfulWebhookProps",
]

publication.publish()
