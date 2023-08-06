"""
# Welcome to `cdk-elasticache-monitor`

ElasticacheAutoMonitor allows you to send email, sms, slack, or trigger aws lambda when an alarm occurs.
You will get the following monitoring:

* Cpu Monitor: Should be less than 90%. (See below reference)
* SwapUsage Monitor: Should be less than 50M.
* Evictions Monitor: Should not have evictions value.
* CurrConnections Monitor: According to your business needs, default every 1 vcup is equal to 50 connections.
* FreeableMemory Monitor: Not less than 10%

Reference: https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheMetrics.WhichShouldIMonitor.html

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stack = cdk.Stack()

# sent with email
ElasticacheAutoMonitor.set_up_with_email(stack, "my-elasticache-id",
    emails=["jiale.chan@gmail.com"],
    node_type_class=NodeType.R4_16XLARGE
)

# or sent with sms
ElasticacheAutoMonitor.set_up_with_sms(stack, "my-elasticache-id",
    phones=["+15533728278"],
    node_type_class=NodeType.R4_16XLARGE
)

# or sent with slack
ElasticacheAutoMonitor.set_up_with_slack(stack, "my-elasticache-id",
    web_hook_url="http://xxx.xxx.xxx",
    node_type_class=NodeType.R4_16XLARGE
)

# or trigger lambda
fn = lambda.Function(stack, "MyFunction",
    runtime=lambda.Runtime.NODEJS_10_X,
    handler="index.handler",
    code=lambda.Code.from_inline("exports.handler = function(event, ctx, cb) { return cb(null, \"hi\"); }")
)
ElasticacheAutoMonitor.set_up_with_lambda(stack, "my-elasticache-id", fn,
    node_type_class=NodeType.R4_16XLARGE
)
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

import aws_cdk.aws_lambda
import aws_cdk.core


class ElasticacheAutoMonitor(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-elasticache-monitor.ElasticacheAutoMonitor",
):
    """ElasticacheAutoMonitor allows you to send email, sms, slack, or trigger aws sns topic when an alarm occurs.

    You will get the following monitoring:

    1. Cpu Monitor: Should be less than 90%. (See below reference)
    2. SwapUsage Monitor: Should be less than 50M.
    3. Evictions Monitor: Should not have evictions value.
    4. CurrConnections Monitor: According to your business needs, default every 1 vcup is equal to 50 connections.
    5. FreeableMemory Monitor: Not less than 10%

    Reference: https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheMetrics.WhichShouldIMonitor.html

    stability
    :stability: experimental
    """

    def __init__(self, scope: aws_cdk.core.Construct, id: str) -> None:
        """
        :param scope: -
        :param id: -
        """
        jsii.create(ElasticacheAutoMonitor, self, [scope, id])

    @jsii.member(jsii_name="setUpWithEmail")
    @builtins.classmethod
    def set_up_with_email(
        cls,
        scope: aws_cdk.core.Construct,
        cache_cluster_id: str,
        props: "ISetUpWithEmailProps",
    ) -> None:
        """
        :param scope: -
        :param cache_cluster_id: -
        :param props: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "setUpWithEmail", [scope, cache_cluster_id, props])

    @jsii.member(jsii_name="setUpWithLambda")
    @builtins.classmethod
    def set_up_with_lambda(
        cls,
        scope: aws_cdk.core.Construct,
        cache_cluster_id: str,
        fn: aws_cdk.aws_lambda.Function,
        props: typing.Optional["ISetUpWithLambdaProps"] = None,
    ) -> None:
        """
        :param scope: -
        :param cache_cluster_id: -
        :param fn: -
        :param props: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(
            cls, "setUpWithLambda", [scope, cache_cluster_id, fn, props]
        )

    @jsii.member(jsii_name="setUpWithSlack")
    @builtins.classmethod
    def set_up_with_slack(
        cls,
        scope: aws_cdk.core.Construct,
        cache_cluster_id: str,
        props: "ISetUpWithSlackProps",
    ) -> None:
        """
        :param scope: -
        :param cache_cluster_id: -
        :param props: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "setUpWithSlack", [scope, cache_cluster_id, props])

    @jsii.member(jsii_name="setUpWithSms")
    @builtins.classmethod
    def set_up_with_sms(
        cls,
        scope: aws_cdk.core.Construct,
        cache_cluster_id: str,
        props: "ISetUpWithSmsProps",
    ) -> None:
        """
        :param scope: -
        :param cache_cluster_id: -
        :param props: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "setUpWithSms", [scope, cache_cluster_id, props])


@jsii.interface(jsii_type="cdk-elasticache-monitor.ISetUpWithEmailProps")
class ISetUpWithEmailProps(jsii.compat.Protocol):
    """Elasticache auto monitor set up with email props.

    Note that email subscriptions require confirmation by visiting the link sent to the email address.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISetUpWithEmailPropsProxy

    @builtins.property
    @jsii.member(jsii_name="emails")
    def emails(self) -> typing.List[str]:
        """Mailing list to be sent.

        Note that email subscriptions require confirmation by visiting the link sent to the email address.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="currConnectionsPeriod")
    def curr_connections_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        default
        :default: Duration.minutes(1)

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="currConnectionsThreshold")
    def curr_connections_threshold(self) -> typing.Optional[jsii.Number]:
        """CurrConnections threshold.

        Every 1 vcup is equal to 50 connections

        default
        :default: 100

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional["NodeType"]:
        """Default elasticache node type.

        It is strongly recommended to set according to the actual value.

        default
        :default: NodeType.M5_LARGE

        stability
        :stability: experimental
        """
        ...


class _ISetUpWithEmailPropsProxy:
    """Elasticache auto monitor set up with email props.

    Note that email subscriptions require confirmation by visiting the link sent to the email address.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdk-elasticache-monitor.ISetUpWithEmailProps"

    @builtins.property
    @jsii.member(jsii_name="emails")
    def emails(self) -> typing.List[str]:
        """Mailing list to be sent.

        Note that email subscriptions require confirmation by visiting the link sent to the email address.

        stability
        :stability: experimental
        """
        return jsii.get(self, "emails")

    @builtins.property
    @jsii.member(jsii_name="currConnectionsPeriod")
    def curr_connections_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        default
        :default: Duration.minutes(1)

        stability
        :stability: experimental
        """
        return jsii.get(self, "currConnectionsPeriod")

    @builtins.property
    @jsii.member(jsii_name="currConnectionsThreshold")
    def curr_connections_threshold(self) -> typing.Optional[jsii.Number]:
        """CurrConnections threshold.

        Every 1 vcup is equal to 50 connections

        default
        :default: 100

        stability
        :stability: experimental
        """
        return jsii.get(self, "currConnectionsThreshold")

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional["NodeType"]:
        """Default elasticache node type.

        It is strongly recommended to set according to the actual value.

        default
        :default: NodeType.M5_LARGE

        stability
        :stability: experimental
        """
        return jsii.get(self, "nodeType")


@jsii.interface(jsii_type="cdk-elasticache-monitor.ISetUpWithLambdaProps")
class ISetUpWithLambdaProps(jsii.compat.Protocol):
    """Elasticache auto monitor set up with topic props.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISetUpWithLambdaPropsProxy

    @builtins.property
    @jsii.member(jsii_name="currConnectionsPeriod")
    def curr_connections_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        default
        :default: Duration.minutes(1)

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="currConnectionsThreshold")
    def curr_connections_threshold(self) -> typing.Optional[jsii.Number]:
        """CurrConnections threshold.

        Every 1 vcup is equal to 50 connections

        default
        :default: 100

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional["NodeType"]:
        """Default elasticache node type.

        It is strongly recommended to set according to the actual value.

        default
        :default: NodeType.M5_LARGE

        stability
        :stability: experimental
        """
        ...


class _ISetUpWithLambdaPropsProxy:
    """Elasticache auto monitor set up with topic props.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdk-elasticache-monitor.ISetUpWithLambdaProps"

    @builtins.property
    @jsii.member(jsii_name="currConnectionsPeriod")
    def curr_connections_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        default
        :default: Duration.minutes(1)

        stability
        :stability: experimental
        """
        return jsii.get(self, "currConnectionsPeriod")

    @builtins.property
    @jsii.member(jsii_name="currConnectionsThreshold")
    def curr_connections_threshold(self) -> typing.Optional[jsii.Number]:
        """CurrConnections threshold.

        Every 1 vcup is equal to 50 connections

        default
        :default: 100

        stability
        :stability: experimental
        """
        return jsii.get(self, "currConnectionsThreshold")

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional["NodeType"]:
        """Default elasticache node type.

        It is strongly recommended to set according to the actual value.

        default
        :default: NodeType.M5_LARGE

        stability
        :stability: experimental
        """
        return jsii.get(self, "nodeType")


@jsii.interface(jsii_type="cdk-elasticache-monitor.ISetUpWithSlackProps")
class ISetUpWithSlackProps(jsii.compat.Protocol):
    """Elasticache auto monitor set up with Slack props.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISetUpWithSlackPropsProxy

    @builtins.property
    @jsii.member(jsii_name="webHookUrl")
    def web_hook_url(self) -> str:
        """Go to this(https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) link to apply for webhook.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="channel")
    def channel(self) -> typing.Optional[str]:
        """Setting channel.

        What is a channel: (https://slack.com/intl/en-cn/help/articles/360017938993-What-is-a-channel)

        default
        :default: cloudwatch-alarm

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="currConnectionsPeriod")
    def curr_connections_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        default
        :default: Duration.minutes(1)

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="currConnectionsThreshold")
    def curr_connections_threshold(self) -> typing.Optional[jsii.Number]:
        """CurrConnections threshold.

        Every 1 vcup is equal to 50 connections

        default
        :default: 100

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="iconEmoji")
    def icon_emoji(self) -> typing.Optional[str]:
        """Emoji for bot.

        default
        :default: :scream:

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional["NodeType"]:
        """Default elasticache node type.

        It is strongly recommended to set according to the actual value.

        default
        :default: NodeType.M5_LARGE

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> typing.Optional[str]:
        """Setting Slack bot name.

        default
        :default: Webhookbot

        stability
        :stability: experimental
        """
        ...


class _ISetUpWithSlackPropsProxy:
    """Elasticache auto monitor set up with Slack props.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdk-elasticache-monitor.ISetUpWithSlackProps"

    @builtins.property
    @jsii.member(jsii_name="webHookUrl")
    def web_hook_url(self) -> str:
        """Go to this(https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) link to apply for webhook.

        stability
        :stability: experimental
        """
        return jsii.get(self, "webHookUrl")

    @builtins.property
    @jsii.member(jsii_name="channel")
    def channel(self) -> typing.Optional[str]:
        """Setting channel.

        What is a channel: (https://slack.com/intl/en-cn/help/articles/360017938993-What-is-a-channel)

        default
        :default: cloudwatch-alarm

        stability
        :stability: experimental
        """
        return jsii.get(self, "channel")

    @builtins.property
    @jsii.member(jsii_name="currConnectionsPeriod")
    def curr_connections_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        default
        :default: Duration.minutes(1)

        stability
        :stability: experimental
        """
        return jsii.get(self, "currConnectionsPeriod")

    @builtins.property
    @jsii.member(jsii_name="currConnectionsThreshold")
    def curr_connections_threshold(self) -> typing.Optional[jsii.Number]:
        """CurrConnections threshold.

        Every 1 vcup is equal to 50 connections

        default
        :default: 100

        stability
        :stability: experimental
        """
        return jsii.get(self, "currConnectionsThreshold")

    @builtins.property
    @jsii.member(jsii_name="iconEmoji")
    def icon_emoji(self) -> typing.Optional[str]:
        """Emoji for bot.

        default
        :default: :scream:

        stability
        :stability: experimental
        """
        return jsii.get(self, "iconEmoji")

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional["NodeType"]:
        """Default elasticache node type.

        It is strongly recommended to set according to the actual value.

        default
        :default: NodeType.M5_LARGE

        stability
        :stability: experimental
        """
        return jsii.get(self, "nodeType")

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> typing.Optional[str]:
        """Setting Slack bot name.

        default
        :default: Webhookbot

        stability
        :stability: experimental
        """
        return jsii.get(self, "username")


@jsii.interface(jsii_type="cdk-elasticache-monitor.ISetUpWithSmsProps")
class ISetUpWithSmsProps(jsii.compat.Protocol):
    """Elasticache auto monitor set up with sms props.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISetUpWithSmsPropsProxy

    @builtins.property
    @jsii.member(jsii_name="phones")
    def phones(self) -> typing.List[str]:
        """Include country code and phone number, for example: +15551231234.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="currConnectionsPeriod")
    def curr_connections_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        default
        :default: Duration.minutes(1)

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="currConnectionsThreshold")
    def curr_connections_threshold(self) -> typing.Optional[jsii.Number]:
        """CurrConnections threshold.

        Every 1 vcup is equal to 50 connections

        default
        :default: 100

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional["NodeType"]:
        """Default elasticache node type.

        It is strongly recommended to set according to the actual value.

        default
        :default: NodeType.M5_LARGE

        stability
        :stability: experimental
        """
        ...


class _ISetUpWithSmsPropsProxy:
    """Elasticache auto monitor set up with sms props.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdk-elasticache-monitor.ISetUpWithSmsProps"

    @builtins.property
    @jsii.member(jsii_name="phones")
    def phones(self) -> typing.List[str]:
        """Include country code and phone number, for example: +15551231234.

        stability
        :stability: experimental
        """
        return jsii.get(self, "phones")

    @builtins.property
    @jsii.member(jsii_name="currConnectionsPeriod")
    def curr_connections_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        default
        :default: Duration.minutes(1)

        stability
        :stability: experimental
        """
        return jsii.get(self, "currConnectionsPeriod")

    @builtins.property
    @jsii.member(jsii_name="currConnectionsThreshold")
    def curr_connections_threshold(self) -> typing.Optional[jsii.Number]:
        """CurrConnections threshold.

        Every 1 vcup is equal to 50 connections

        default
        :default: 100

        stability
        :stability: experimental
        """
        return jsii.get(self, "currConnectionsThreshold")

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional["NodeType"]:
        """Default elasticache node type.

        It is strongly recommended to set according to the actual value.

        default
        :default: NodeType.M5_LARGE

        stability
        :stability: experimental
        """
        return jsii.get(self, "nodeType")


class NodeType(metaclass=jsii.JSIIMeta, jsii_type="cdk-elasticache-monitor.NodeType"):
    """
    stability
    :stability: experimental
    """

    @jsii.python.classproperty
    @jsii.member(jsii_name="M4_10XLARGE")
    def M4_10_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "M4_10XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="M4_2XLARGE")
    def M4_2_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "M4_2XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="M4_4XLARGE")
    def M4_4_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "M4_4XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="M4_LARGE")
    def M4_LARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "M4_LARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="M4_XLARGE")
    def M4_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "M4_XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="M5_12XLARGE")
    def M5_12_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "M5_12XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="M5_24XLARGE")
    def M5_24_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "M5_24XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="M5_2XLARGE")
    def M5_2_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "M5_2XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="M5_4XLARGE")
    def M5_4_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "M5_4XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="M5_LARGE")
    def M5_LARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "M5_LARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="M5_XLARGE")
    def M5_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "M5_XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="R4_16XLARGE")
    def R4_16_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "R4_16XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="R4_2XLARGE")
    def R4_2_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "R4_2XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="R4_4XLARGE")
    def R4_4_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "R4_4XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="R4_8XLARGE")
    def R4_8_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "R4_8XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="R4_LARGE")
    def R4_LARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "R4_LARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="R4_XLARGE")
    def R4_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "R4_XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="R5_12XLARGE")
    def R5_12_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "R5_12XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="R5_24LARGE")
    def R5_24_LARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "R5_24LARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="R5_2XLARGE")
    def R5_2_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "R5_2XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="R5_4XLARGE")
    def R5_4_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "R5_4XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="R5_LARGE")
    def R5_LARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "R5_LARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="R5_XLARGE")
    def R5_XLARGE(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "R5_XLARGE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="T2_MEDIUM")
    def T2_MEDIUM(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "T2_MEDIUM")

    @jsii.python.classproperty
    @jsii.member(jsii_name="T2_MIRCO")
    def T2_MIRCO(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "T2_MIRCO")

    @jsii.python.classproperty
    @jsii.member(jsii_name="T2_SMALL")
    def T2_SMALL(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "T2_SMALL")

    @jsii.python.classproperty
    @jsii.member(jsii_name="T3_MEDIUM")
    def T3_MEDIUM(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "T3_MEDIUM")

    @jsii.python.classproperty
    @jsii.member(jsii_name="T3_MICRO")
    def T3_MICRO(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "T3_MICRO")

    @jsii.python.classproperty
    @jsii.member(jsii_name="T3_SMALL")
    def T3_SMALL(cls) -> "NodeType":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "T3_SMALL")

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "memory")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "name")

    @builtins.property
    @jsii.member(jsii_name="vcupCount")
    def vcup_count(self) -> jsii.Number:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "vcupCount")


__all__ = [
    "ElasticacheAutoMonitor",
    "ISetUpWithEmailProps",
    "ISetUpWithLambdaProps",
    "ISetUpWithSlackProps",
    "ISetUpWithSmsProps",
    "NodeType",
]

publication.publish()
