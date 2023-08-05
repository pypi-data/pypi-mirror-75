import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import Duration as _Duration_5170c158, Construct as _Construct_f50a3f53
from ..aws_cloudfront import (
    HttpOrigin as _HttpOrigin_5c8fb36a,
    HttpOriginProps as _HttpOriginProps_a16ea53e,
    OriginProtocolPolicy as _OriginProtocolPolicy_d2d28ec7,
    Origin as _Origin_539f8e92,
    OriginBindOptions as _OriginBindOptions_5b2ffb69,
    CfnDistribution as _CfnDistribution_3a5e7b5c,
)
from ..aws_elasticloadbalancingv2 import ILoadBalancerV2 as _ILoadBalancerV2_3b69d63d
from ..aws_s3 import IBucket as _IBucket_25bad983


class HttpOrigin(
    _HttpOrigin_5c8fb36a,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_cloudfront_origins.HttpOrigin",
):
    """An Origin for an HTTP server.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        domain_name: str,
        *,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
        keepalive_timeout: typing.Optional[_Duration_5170c158] = None,
        protocol_policy: typing.Optional[_OriginProtocolPolicy_d2d28ec7] = None,
        read_timeout: typing.Optional[_Duration_5170c158] = None,
        connection_attempts: typing.Optional[jsii.Number] = None,
        connection_timeout: typing.Optional[_Duration_5170c158] = None,
        custom_headers: typing.Optional[typing.Mapping[str, str]] = None,
        origin_path: typing.Optional[str] = None,
    ) -> None:
        """
        :param domain_name: -
        :param http_port: The HTTP port that CloudFront uses to connect to the origin. Default: 80
        :param https_port: The HTTPS port that CloudFront uses to connect to the origin. Default: 443
        :param keepalive_timeout: Specifies how long, in seconds, CloudFront persists its connection to the origin. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(5)
        :param protocol_policy: Specifies the protocol (HTTP or HTTPS) that CloudFront uses to connect to the origin. Default: OriginProtocolPolicy.HTTPS_ONLY
        :param read_timeout: Specifies how long, in seconds, CloudFront waits for a response from the origin, also known as the origin response timeout. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(30)
        :param connection_attempts: The number of times that CloudFront attempts to connect to the origin; valid values are 1, 2, or 3 attempts. Default: 3
        :param connection_timeout: The number of seconds that CloudFront waits when trying to establish a connection to the origin. Valid values are 1-10 seconds, inclusive. Default: Duration.seconds(10)
        :param custom_headers: A list of HTTP header names and values that CloudFront adds to requests it sends to the origin. Default: {}
        :param origin_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'

        stability
        :stability: experimental
        """
        props = HttpOriginProps(
            http_port=http_port,
            https_port=https_port,
            keepalive_timeout=keepalive_timeout,
            protocol_policy=protocol_policy,
            read_timeout=read_timeout,
            connection_attempts=connection_attempts,
            connection_timeout=connection_timeout,
            custom_headers=custom_headers,
            origin_path=origin_path,
        )

        jsii.create(HttpOrigin, self, [domain_name, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_cloudfront_origins.HttpOriginProps",
    jsii_struct_bases=[_HttpOriginProps_a16ea53e],
    name_mapping={
        "connection_attempts": "connectionAttempts",
        "connection_timeout": "connectionTimeout",
        "custom_headers": "customHeaders",
        "origin_path": "originPath",
        "http_port": "httpPort",
        "https_port": "httpsPort",
        "keepalive_timeout": "keepaliveTimeout",
        "protocol_policy": "protocolPolicy",
        "read_timeout": "readTimeout",
    },
)
class HttpOriginProps(_HttpOriginProps_a16ea53e):
    def __init__(
        self,
        *,
        connection_attempts: typing.Optional[jsii.Number] = None,
        connection_timeout: typing.Optional[_Duration_5170c158] = None,
        custom_headers: typing.Optional[typing.Mapping[str, str]] = None,
        origin_path: typing.Optional[str] = None,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
        keepalive_timeout: typing.Optional[_Duration_5170c158] = None,
        protocol_policy: typing.Optional[_OriginProtocolPolicy_d2d28ec7] = None,
        read_timeout: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """Properties for an Origin backed by any HTTP server.

        :param connection_attempts: The number of times that CloudFront attempts to connect to the origin; valid values are 1, 2, or 3 attempts. Default: 3
        :param connection_timeout: The number of seconds that CloudFront waits when trying to establish a connection to the origin. Valid values are 1-10 seconds, inclusive. Default: Duration.seconds(10)
        :param custom_headers: A list of HTTP header names and values that CloudFront adds to requests it sends to the origin. Default: {}
        :param origin_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'
        :param http_port: The HTTP port that CloudFront uses to connect to the origin. Default: 80
        :param https_port: The HTTPS port that CloudFront uses to connect to the origin. Default: 443
        :param keepalive_timeout: Specifies how long, in seconds, CloudFront persists its connection to the origin. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(5)
        :param protocol_policy: Specifies the protocol (HTTP or HTTPS) that CloudFront uses to connect to the origin. Default: OriginProtocolPolicy.HTTPS_ONLY
        :param read_timeout: Specifies how long, in seconds, CloudFront waits for a response from the origin, also known as the origin response timeout. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(30)

        stability
        :stability: experimental
        """
        self._values = {}
        if connection_attempts is not None:
            self._values["connection_attempts"] = connection_attempts
        if connection_timeout is not None:
            self._values["connection_timeout"] = connection_timeout
        if custom_headers is not None:
            self._values["custom_headers"] = custom_headers
        if origin_path is not None:
            self._values["origin_path"] = origin_path
        if http_port is not None:
            self._values["http_port"] = http_port
        if https_port is not None:
            self._values["https_port"] = https_port
        if keepalive_timeout is not None:
            self._values["keepalive_timeout"] = keepalive_timeout
        if protocol_policy is not None:
            self._values["protocol_policy"] = protocol_policy
        if read_timeout is not None:
            self._values["read_timeout"] = read_timeout

    @builtins.property
    def connection_attempts(self) -> typing.Optional[jsii.Number]:
        """The number of times that CloudFront attempts to connect to the origin;

        valid values are 1, 2, or 3 attempts.

        default
        :default: 3

        stability
        :stability: experimental
        """
        return self._values.get("connection_attempts")

    @builtins.property
    def connection_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The number of seconds that CloudFront waits when trying to establish a connection to the origin.

        Valid values are 1-10 seconds, inclusive.

        default
        :default: Duration.seconds(10)

        stability
        :stability: experimental
        """
        return self._values.get("connection_timeout")

    @builtins.property
    def custom_headers(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A list of HTTP header names and values that CloudFront adds to requests it sends to the origin.

        default
        :default: {}

        stability
        :stability: experimental
        """
        return self._values.get("custom_headers")

    @builtins.property
    def origin_path(self) -> typing.Optional[str]:
        """An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin.

        Must begin, but not end, with '/' (e.g., '/production/images').

        default
        :default: '/'

        stability
        :stability: experimental
        """
        return self._values.get("origin_path")

    @builtins.property
    def http_port(self) -> typing.Optional[jsii.Number]:
        """The HTTP port that CloudFront uses to connect to the origin.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get("http_port")

    @builtins.property
    def https_port(self) -> typing.Optional[jsii.Number]:
        """The HTTPS port that CloudFront uses to connect to the origin.

        default
        :default: 443

        stability
        :stability: experimental
        """
        return self._values.get("https_port")

    @builtins.property
    def keepalive_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Specifies how long, in seconds, CloudFront persists its connection to the origin.

        The valid range is from 1 to 60 seconds, inclusive.

        default
        :default: Duration.seconds(5)

        stability
        :stability: experimental
        """
        return self._values.get("keepalive_timeout")

    @builtins.property
    def protocol_policy(self) -> typing.Optional[_OriginProtocolPolicy_d2d28ec7]:
        """Specifies the protocol (HTTP or HTTPS) that CloudFront uses to connect to the origin.

        default
        :default: OriginProtocolPolicy.HTTPS_ONLY

        stability
        :stability: experimental
        """
        return self._values.get("protocol_policy")

    @builtins.property
    def read_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Specifies how long, in seconds, CloudFront waits for a response from the origin, also known as the origin response timeout.

        The valid range is from 1 to 60 seconds, inclusive.

        default
        :default: Duration.seconds(30)

        stability
        :stability: experimental
        """
        return self._values.get("read_timeout")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpOriginProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerV2Origin(
    _HttpOrigin_5c8fb36a,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_cloudfront_origins.LoadBalancerV2Origin",
):
    """An Origin for a v2 load balancer.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        load_balancer: _ILoadBalancerV2_3b69d63d,
        *,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
        keepalive_timeout: typing.Optional[_Duration_5170c158] = None,
        protocol_policy: typing.Optional[_OriginProtocolPolicy_d2d28ec7] = None,
        read_timeout: typing.Optional[_Duration_5170c158] = None,
        connection_attempts: typing.Optional[jsii.Number] = None,
        connection_timeout: typing.Optional[_Duration_5170c158] = None,
        custom_headers: typing.Optional[typing.Mapping[str, str]] = None,
        origin_path: typing.Optional[str] = None,
    ) -> None:
        """
        :param load_balancer: -
        :param http_port: The HTTP port that CloudFront uses to connect to the origin. Default: 80
        :param https_port: The HTTPS port that CloudFront uses to connect to the origin. Default: 443
        :param keepalive_timeout: Specifies how long, in seconds, CloudFront persists its connection to the origin. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(5)
        :param protocol_policy: Specifies the protocol (HTTP or HTTPS) that CloudFront uses to connect to the origin. Default: OriginProtocolPolicy.HTTPS_ONLY
        :param read_timeout: Specifies how long, in seconds, CloudFront waits for a response from the origin, also known as the origin response timeout. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(30)
        :param connection_attempts: The number of times that CloudFront attempts to connect to the origin; valid values are 1, 2, or 3 attempts. Default: 3
        :param connection_timeout: The number of seconds that CloudFront waits when trying to establish a connection to the origin. Valid values are 1-10 seconds, inclusive. Default: Duration.seconds(10)
        :param custom_headers: A list of HTTP header names and values that CloudFront adds to requests it sends to the origin. Default: {}
        :param origin_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'

        stability
        :stability: experimental
        """
        props = LoadBalancerV2OriginProps(
            http_port=http_port,
            https_port=https_port,
            keepalive_timeout=keepalive_timeout,
            protocol_policy=protocol_policy,
            read_timeout=read_timeout,
            connection_attempts=connection_attempts,
            connection_timeout=connection_timeout,
            custom_headers=custom_headers,
            origin_path=origin_path,
        )

        jsii.create(LoadBalancerV2Origin, self, [load_balancer, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_cloudfront_origins.LoadBalancerV2OriginProps",
    jsii_struct_bases=[_HttpOriginProps_a16ea53e],
    name_mapping={
        "connection_attempts": "connectionAttempts",
        "connection_timeout": "connectionTimeout",
        "custom_headers": "customHeaders",
        "origin_path": "originPath",
        "http_port": "httpPort",
        "https_port": "httpsPort",
        "keepalive_timeout": "keepaliveTimeout",
        "protocol_policy": "protocolPolicy",
        "read_timeout": "readTimeout",
    },
)
class LoadBalancerV2OriginProps(_HttpOriginProps_a16ea53e):
    def __init__(
        self,
        *,
        connection_attempts: typing.Optional[jsii.Number] = None,
        connection_timeout: typing.Optional[_Duration_5170c158] = None,
        custom_headers: typing.Optional[typing.Mapping[str, str]] = None,
        origin_path: typing.Optional[str] = None,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
        keepalive_timeout: typing.Optional[_Duration_5170c158] = None,
        protocol_policy: typing.Optional[_OriginProtocolPolicy_d2d28ec7] = None,
        read_timeout: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """Properties for an Origin backed by a v2 load balancer.

        :param connection_attempts: The number of times that CloudFront attempts to connect to the origin; valid values are 1, 2, or 3 attempts. Default: 3
        :param connection_timeout: The number of seconds that CloudFront waits when trying to establish a connection to the origin. Valid values are 1-10 seconds, inclusive. Default: Duration.seconds(10)
        :param custom_headers: A list of HTTP header names and values that CloudFront adds to requests it sends to the origin. Default: {}
        :param origin_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'
        :param http_port: The HTTP port that CloudFront uses to connect to the origin. Default: 80
        :param https_port: The HTTPS port that CloudFront uses to connect to the origin. Default: 443
        :param keepalive_timeout: Specifies how long, in seconds, CloudFront persists its connection to the origin. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(5)
        :param protocol_policy: Specifies the protocol (HTTP or HTTPS) that CloudFront uses to connect to the origin. Default: OriginProtocolPolicy.HTTPS_ONLY
        :param read_timeout: Specifies how long, in seconds, CloudFront waits for a response from the origin, also known as the origin response timeout. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(30)

        stability
        :stability: experimental
        """
        self._values = {}
        if connection_attempts is not None:
            self._values["connection_attempts"] = connection_attempts
        if connection_timeout is not None:
            self._values["connection_timeout"] = connection_timeout
        if custom_headers is not None:
            self._values["custom_headers"] = custom_headers
        if origin_path is not None:
            self._values["origin_path"] = origin_path
        if http_port is not None:
            self._values["http_port"] = http_port
        if https_port is not None:
            self._values["https_port"] = https_port
        if keepalive_timeout is not None:
            self._values["keepalive_timeout"] = keepalive_timeout
        if protocol_policy is not None:
            self._values["protocol_policy"] = protocol_policy
        if read_timeout is not None:
            self._values["read_timeout"] = read_timeout

    @builtins.property
    def connection_attempts(self) -> typing.Optional[jsii.Number]:
        """The number of times that CloudFront attempts to connect to the origin;

        valid values are 1, 2, or 3 attempts.

        default
        :default: 3

        stability
        :stability: experimental
        """
        return self._values.get("connection_attempts")

    @builtins.property
    def connection_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The number of seconds that CloudFront waits when trying to establish a connection to the origin.

        Valid values are 1-10 seconds, inclusive.

        default
        :default: Duration.seconds(10)

        stability
        :stability: experimental
        """
        return self._values.get("connection_timeout")

    @builtins.property
    def custom_headers(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A list of HTTP header names and values that CloudFront adds to requests it sends to the origin.

        default
        :default: {}

        stability
        :stability: experimental
        """
        return self._values.get("custom_headers")

    @builtins.property
    def origin_path(self) -> typing.Optional[str]:
        """An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin.

        Must begin, but not end, with '/' (e.g., '/production/images').

        default
        :default: '/'

        stability
        :stability: experimental
        """
        return self._values.get("origin_path")

    @builtins.property
    def http_port(self) -> typing.Optional[jsii.Number]:
        """The HTTP port that CloudFront uses to connect to the origin.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get("http_port")

    @builtins.property
    def https_port(self) -> typing.Optional[jsii.Number]:
        """The HTTPS port that CloudFront uses to connect to the origin.

        default
        :default: 443

        stability
        :stability: experimental
        """
        return self._values.get("https_port")

    @builtins.property
    def keepalive_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Specifies how long, in seconds, CloudFront persists its connection to the origin.

        The valid range is from 1 to 60 seconds, inclusive.

        default
        :default: Duration.seconds(5)

        stability
        :stability: experimental
        """
        return self._values.get("keepalive_timeout")

    @builtins.property
    def protocol_policy(self) -> typing.Optional[_OriginProtocolPolicy_d2d28ec7]:
        """Specifies the protocol (HTTP or HTTPS) that CloudFront uses to connect to the origin.

        default
        :default: OriginProtocolPolicy.HTTPS_ONLY

        stability
        :stability: experimental
        """
        return self._values.get("protocol_policy")

    @builtins.property
    def read_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Specifies how long, in seconds, CloudFront waits for a response from the origin, also known as the origin response timeout.

        The valid range is from 1 to 60 seconds, inclusive.

        default
        :default: Duration.seconds(30)

        stability
        :stability: experimental
        """
        return self._values.get("read_timeout")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerV2OriginProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3Origin(
    _Origin_539f8e92,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_cloudfront_origins.S3Origin",
):
    """An Origin that is backed by an S3 bucket.

    If the bucket is configured for website hosting, this origin will be configured to use the bucket as an
    HTTP server origin and will use the bucket's configured website redirects and error handling. Otherwise,
    the origin is created as a bucket origin and will use CloudFront's redirect and error handling.

    stability
    :stability: experimental
    """

    def __init__(
        self, bucket: _IBucket_25bad983, *, origin_path: typing.Optional[str] = None
    ) -> None:
        """
        :param bucket: -
        :param origin_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'

        stability
        :stability: experimental
        """
        props = S3OriginProps(origin_path=origin_path)

        jsii.create(S3Origin, self, [bucket, props])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, *, origin_index: jsii.Number) -> None:
        """Binds the origin to the associated Distribution.

        Can be used to grant permissions, create dependent resources, etc.

        :param scope: -
        :param origin_index: The positional index of this origin within the distribution. Used for ensuring unique IDs.

        stability
        :stability: experimental
        """
        options = _OriginBindOptions_5b2ffb69(origin_index=origin_index)

        return jsii.invoke(self, "bind", [scope, options])

    @jsii.member(jsii_name="renderOrigin")
    def render_origin(self) -> _CfnDistribution_3a5e7b5c.OriginProperty:
        """Creates and returns the CloudFormation representation of this origin.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderOrigin", [])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        """The unique id for this origin.

        Cannot be accesed until bind() is called.

        stability
        :stability: experimental
        """
        return jsii.get(self, "id")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_cloudfront_origins.S3OriginProps",
    jsii_struct_bases=[],
    name_mapping={"origin_path": "originPath"},
)
class S3OriginProps:
    def __init__(self, *, origin_path: typing.Optional[str] = None) -> None:
        """Properties to use to customize an S3 Origin.

        :param origin_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'

        stability
        :stability: experimental
        """
        self._values = {}
        if origin_path is not None:
            self._values["origin_path"] = origin_path

    @builtins.property
    def origin_path(self) -> typing.Optional[str]:
        """An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin.

        Must begin, but not end, with '/' (e.g., '/production/images').

        default
        :default: '/'

        stability
        :stability: experimental
        """
        return self._values.get("origin_path")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3OriginProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "HttpOrigin",
    "HttpOriginProps",
    "LoadBalancerV2Origin",
    "LoadBalancerV2OriginProps",
    "S3Origin",
    "S3OriginProps",
]

publication.publish()
