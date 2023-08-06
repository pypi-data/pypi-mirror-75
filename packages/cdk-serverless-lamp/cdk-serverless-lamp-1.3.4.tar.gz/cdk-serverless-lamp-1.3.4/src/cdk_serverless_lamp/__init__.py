"""
[![NPM version](https://badge.fury.io/js/cdk-serverless-lamp.svg)](https://badge.fury.io/js/cdk-serverless-lamp)
[![PyPI version](https://badge.fury.io/py/cdk-serverless-lamp.svg)](https://badge.fury.io/py/cdk-serverless-lamp)
![Release](https://github.com/pahud/cdk-serverless-lamp/workflows/Release/badge.svg)

# Welcome to cdk-serverless-lamp

`cdk-serverless-lamp` is a JSII construct library for AWS CDK that allows you to deploy the [New Serverless LAMP Stack](https://aws.amazon.com/tw/blogs/compute/introducing-the-new-serverless-lamp-stack/) running PHP Laravel Apps by specifying the local `laravel` directory.

By deploying this stack, it creates the following resources for you:

1. Amazon API Gateway HTTP API
2. AWS Lambda custom runtime with [Bref runtime](https://bref.sh/docs/runtimes/) support
3. Amazon Aurora for MySQL database cluster with RDS proxy enabled

## Usage

Building your serverless Laravel with `ServerlessLaravel` construct:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_serverless_lamp import ServerlessLaravel
from aws_cdk.core import App, Stack
import path as path

app = App()
stack = Stack(app, "ServerlessLaraval")

# the DatabaseCluster sharing the same vpc with the ServerlessLaravel
db = DatabaseCluster(stack, "DatabaseCluster",
    vpc=vpc,
    instance_type=InstanceType("t3.small"),
    rds_proxy=True
)

# the ServerlessLaravel
ServerlessLaravel(stack, "ServerlessLaravel",
    bref_layer_version="arn:aws:lambda:ap-northeast-1:209497400698:layer:php-74-fpm:11",
    laravel_path=path.join(__dirname, "../../composer/laravel58-bref"),
    vpc=vpc,
    database_config={
        "writer_endpoint": db.rds_proxy.endpoint
    }
)
```

On deploy complete, the API Gateway URL will be returned in the Output. Click the URL and you will see the Laravel landing page:

![laravel-welcome](./images/laravel.png)

## Prepare the Laravel and bref

```bash
$ git clone https://github.com/pahud/cdk-serverless-lamp.git
$ cd cdk-serverless-lamp
$ mkdir composer && cd composer
# create a laravel project
$ docker run --rm -ti \
  --volume $PWD:/app \
  composer create-project laravel/laravel laravel58-bref --prefer-dist
# enter this project
$ cd laravel58-bref
# install bref in the vendor
$ docker run --rm -ti \
  --volume $PWD:/app \
  composer require bref/bref
```

## Configure Laravel with Bref for Lambda

According to the Bref [document](https://bref.sh/docs/frameworks/laravel.html), we need configure the environment before it can be deployed on Lambda:

edit the `.env` file

```
VIEW_COMPILED_PATH=/tmp/storage/framework/views

# We cannot store sessions to disk: if you don't need sessions (e.g. API) then use `array`
# If you write a website, use `cookie` or store sessions in database.
SESSION_DRIVER=cookie

# Logging to stderr allows the logs to end up in Cloudwatch
LOG_CHANNEL=stderr
```

edit the `app/Providers/AppServiceProvider.php`

```php
    public function boot()
    {
        // Make sure the directory for compiled views exist
        if (! is_dir(config('view.compiled'))) {
            mkdir(config('view.compiled'), 0755, true);
        }
    }
```

edit `bootstrap/app.php`

```php

$app = new Illuminate\Foundation\Application(
    $_ENV['APP_BASE_PATH'] ?? dirname(__DIR__)
);

// add the following statement
// we will configure APP_STORAGE = '/tmp' in Lambda env var
$app->useStoragePath($_ENV['APP_STORAGE'] ?? $app->storagePath());
```

*(credit to [@azole](https://medium.com/@azole/deploy-serverless-laravel-by-bref-6f28b1e0d53a))*

## Amazon RDS Cluster and Proxy

Use `DatabaseCluster` construct to create your database clusters.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
db = DatabaseCluster(stack, "DatabaseCluster",
    vpc=vpc,
    instance_type=InstanceType("t3.small"),
    # enable rds proxy for this cluster
    rds_proxy=True,
    # one writer and one read replica
    instance_capacity=2
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

import aws_cdk.aws_ec2
import aws_cdk.aws_lambda
import aws_cdk.aws_rds
import aws_cdk.aws_secretsmanager
import aws_cdk.core


class DatabaseCluster(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-serverless-lamp.DatabaseCluster",
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
        vpc: aws_cdk.aws_ec2.IVpc,
        engine: typing.Optional[aws_cdk.aws_rds.IClusterEngine] = None,
        instance_capacity: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        master_user_name: typing.Optional[str] = None,
        rds_proxy: typing.Optional[bool] = None,
        rds_proxy_options: typing.Optional[aws_cdk.aws_rds.DatabaseProxyOptions] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param vpc: The VPC for the DatabaseCluster.
        :param engine: database cluster engine. Default: AURORA_MYSQL
        :param instance_capacity: How many replicas/instances to create. Has to be at least 1. Default: 1
        :param instance_type: instance type of the cluster. Default: - t3.medium (or, more precisely, db.t3.medium)
        :param master_user_name: master username. Default: admin
        :param rds_proxy: enable the Amazon RDS proxy. Default: true
        :param rds_proxy_options: RDS Proxy Options.

        stability
        :stability: experimental
        """
        props = DatabaseProps(
            vpc=vpc,
            engine=engine,
            instance_capacity=instance_capacity,
            instance_type=instance_type,
            master_user_name=master_user_name,
            rds_proxy=rds_proxy,
            rds_proxy_options=rds_proxy_options,
        )

        jsii.create(DatabaseCluster, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="masterPassword")
    def master_password(self) -> aws_cdk.aws_secretsmanager.ISecret:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "masterPassword")

    @builtins.property
    @jsii.member(jsii_name="masterUser")
    def master_user(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "masterUser")

    @builtins.property
    @jsii.member(jsii_name="rdsProxy")
    def rds_proxy(self) -> typing.Optional[aws_cdk.aws_rds.DatabaseProxy]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "rdsProxy")


@jsii.data_type(
    jsii_type="cdk-serverless-lamp.DatabaseConfig",
    jsii_struct_bases=[],
    name_mapping={
        "writer_endpoint": "writerEndpoint",
        "master_user_name": "masterUserName",
        "master_user_password_secret": "masterUserPasswordSecret",
        "reader_endpoint": "readerEndpoint",
    },
)
class DatabaseConfig:
    def __init__(
        self,
        *,
        writer_endpoint: str,
        master_user_name: typing.Optional[str] = None,
        master_user_password_secret: typing.Optional[
            aws_cdk.aws_secretsmanager.ISecret
        ] = None,
        reader_endpoint: typing.Optional[str] = None,
    ) -> None:
        """
        :param writer_endpoint: The DB writer endpoint.
        :param master_user_name: The DB master username.
        :param master_user_password_secret: The DB master password secret.
        :param reader_endpoint: The DB reader endpoint.

        stability
        :stability: experimental
        """
        self._values = {
            "writer_endpoint": writer_endpoint,
        }
        if master_user_name is not None:
            self._values["master_user_name"] = master_user_name
        if master_user_password_secret is not None:
            self._values["master_user_password_secret"] = master_user_password_secret
        if reader_endpoint is not None:
            self._values["reader_endpoint"] = reader_endpoint

    @builtins.property
    def writer_endpoint(self) -> str:
        """The DB writer endpoint.

        stability
        :stability: experimental
        """
        return self._values.get("writer_endpoint")

    @builtins.property
    def master_user_name(self) -> typing.Optional[str]:
        """The DB master username.

        stability
        :stability: experimental
        """
        return self._values.get("master_user_name")

    @builtins.property
    def master_user_password_secret(
        self,
    ) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The DB master password secret.

        stability
        :stability: experimental
        """
        return self._values.get("master_user_password_secret")

    @builtins.property
    def reader_endpoint(self) -> typing.Optional[str]:
        """The DB reader endpoint.

        stability
        :stability: experimental
        """
        return self._values.get("reader_endpoint")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-serverless-lamp.DatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "engine": "engine",
        "instance_capacity": "instanceCapacity",
        "instance_type": "instanceType",
        "master_user_name": "masterUserName",
        "rds_proxy": "rdsProxy",
        "rds_proxy_options": "rdsProxyOptions",
    },
)
class DatabaseProps:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        engine: typing.Optional[aws_cdk.aws_rds.IClusterEngine] = None,
        instance_capacity: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        master_user_name: typing.Optional[str] = None,
        rds_proxy: typing.Optional[bool] = None,
        rds_proxy_options: typing.Optional[aws_cdk.aws_rds.DatabaseProxyOptions] = None,
    ) -> None:
        """
        :param vpc: The VPC for the DatabaseCluster.
        :param engine: database cluster engine. Default: AURORA_MYSQL
        :param instance_capacity: How many replicas/instances to create. Has to be at least 1. Default: 1
        :param instance_type: instance type of the cluster. Default: - t3.medium (or, more precisely, db.t3.medium)
        :param master_user_name: master username. Default: admin
        :param rds_proxy: enable the Amazon RDS proxy. Default: true
        :param rds_proxy_options: RDS Proxy Options.

        stability
        :stability: experimental
        """
        if isinstance(rds_proxy_options, dict):
            rds_proxy_options = aws_cdk.aws_rds.DatabaseProxyOptions(
                **rds_proxy_options
            )
        self._values = {
            "vpc": vpc,
        }
        if engine is not None:
            self._values["engine"] = engine
        if instance_capacity is not None:
            self._values["instance_capacity"] = instance_capacity
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if master_user_name is not None:
            self._values["master_user_name"] = master_user_name
        if rds_proxy is not None:
            self._values["rds_proxy"] = rds_proxy
        if rds_proxy_options is not None:
            self._values["rds_proxy_options"] = rds_proxy_options

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC for the DatabaseCluster.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def engine(self) -> typing.Optional[aws_cdk.aws_rds.IClusterEngine]:
        """database cluster engine.

        default
        :default: AURORA_MYSQL

        stability
        :stability: experimental
        """
        return self._values.get("engine")

    @builtins.property
    def instance_capacity(self) -> typing.Optional[jsii.Number]:
        """How many replicas/instances to create.

        Has to be at least 1.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get("instance_capacity")

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """instance type of the cluster.

        default
        :default: - t3.medium (or, more precisely, db.t3.medium)

        stability
        :stability: experimental
        """
        return self._values.get("instance_type")

    @builtins.property
    def master_user_name(self) -> typing.Optional[str]:
        """master username.

        default
        :default: admin

        stability
        :stability: experimental
        """
        return self._values.get("master_user_name")

    @builtins.property
    def rds_proxy(self) -> typing.Optional[bool]:
        """enable the Amazon RDS proxy.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("rds_proxy")

    @builtins.property
    def rds_proxy_options(
        self,
    ) -> typing.Optional[aws_cdk.aws_rds.DatabaseProxyOptions]:
        """RDS Proxy Options.

        stability
        :stability: experimental
        """
        return self._values.get("rds_proxy_options")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServerlessApi(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-serverless-lamp.ServerlessApi",
):
    """Use ``ServerlessApi`` to create the serverless API resource.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        bref_layer_version: str,
        database_config: typing.Optional["DatabaseConfig"] = None,
        handler: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        lambda_code_path: typing.Optional[str] = None,
        rds_proxy: typing.Optional[aws_cdk.aws_rds.IDatabaseProxy] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param bref_layer_version: AWS Lambda layer version from the Bref runtime. e.g. arn:aws:lambda:us-west-1:209497400698:layer:php-74-fpm:12 check the latest runtime verion arn at https://bref.sh/docs/runtimes/
        :param database_config: Database configurations.
        :param handler: custom lambda function for the API. Default: - A Lambda function with Lavavel and Bref support will be created
        :param lambda_code_path: custom lambda code asset path. Default: - DEFAULT_LAMBDA_ASSET_PATH
        :param rds_proxy: RDS Proxy for the Lambda function. Default: - no db proxy
        :param vpc: The VPC for this stack.

        stability
        :stability: experimental
        """
        props = ServerlessApiProps(
            bref_layer_version=bref_layer_version,
            database_config=database_config,
            handler=handler,
            lambda_code_path=lambda_code_path,
            rds_proxy=rds_proxy,
            vpc=vpc,
        )

        jsii.create(ServerlessApi, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> aws_cdk.aws_lambda.IFunction:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "handler")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "vpc")


@jsii.data_type(
    jsii_type="cdk-serverless-lamp.ServerlessApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "bref_layer_version": "brefLayerVersion",
        "database_config": "databaseConfig",
        "handler": "handler",
        "lambda_code_path": "lambdaCodePath",
        "rds_proxy": "rdsProxy",
        "vpc": "vpc",
    },
)
class ServerlessApiProps:
    def __init__(
        self,
        *,
        bref_layer_version: str,
        database_config: typing.Optional["DatabaseConfig"] = None,
        handler: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        lambda_code_path: typing.Optional[str] = None,
        rds_proxy: typing.Optional[aws_cdk.aws_rds.IDatabaseProxy] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """Construct properties for ``ServerlessApi``.

        :param bref_layer_version: AWS Lambda layer version from the Bref runtime. e.g. arn:aws:lambda:us-west-1:209497400698:layer:php-74-fpm:12 check the latest runtime verion arn at https://bref.sh/docs/runtimes/
        :param database_config: Database configurations.
        :param handler: custom lambda function for the API. Default: - A Lambda function with Lavavel and Bref support will be created
        :param lambda_code_path: custom lambda code asset path. Default: - DEFAULT_LAMBDA_ASSET_PATH
        :param rds_proxy: RDS Proxy for the Lambda function. Default: - no db proxy
        :param vpc: The VPC for this stack.

        stability
        :stability: experimental
        """
        if isinstance(database_config, dict):
            database_config = DatabaseConfig(**database_config)
        self._values = {
            "bref_layer_version": bref_layer_version,
        }
        if database_config is not None:
            self._values["database_config"] = database_config
        if handler is not None:
            self._values["handler"] = handler
        if lambda_code_path is not None:
            self._values["lambda_code_path"] = lambda_code_path
        if rds_proxy is not None:
            self._values["rds_proxy"] = rds_proxy
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def bref_layer_version(self) -> str:
        """AWS Lambda layer version from the Bref runtime.

        e.g. arn:aws:lambda:us-west-1:209497400698:layer:php-74-fpm:12
        check the latest runtime verion arn at https://bref.sh/docs/runtimes/

        stability
        :stability: experimental
        """
        return self._values.get("bref_layer_version")

    @builtins.property
    def database_config(self) -> typing.Optional["DatabaseConfig"]:
        """Database configurations.

        stability
        :stability: experimental
        """
        return self._values.get("database_config")

    @builtins.property
    def handler(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """custom lambda function for the API.

        default
        :default: - A Lambda function with Lavavel and Bref support will be created

        stability
        :stability: experimental
        """
        return self._values.get("handler")

    @builtins.property
    def lambda_code_path(self) -> typing.Optional[str]:
        """custom lambda code asset path.

        default
        :default: - DEFAULT_LAMBDA_ASSET_PATH

        stability
        :stability: experimental
        """
        return self._values.get("lambda_code_path")

    @builtins.property
    def rds_proxy(self) -> typing.Optional[aws_cdk.aws_rds.IDatabaseProxy]:
        """RDS Proxy for the Lambda function.

        default
        :default: - no db proxy

        stability
        :stability: experimental
        """
        return self._values.get("rds_proxy")

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC for this stack.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerlessApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServerlessLaravel(
    ServerlessApi,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-serverless-lamp.ServerlessLaravel",
):
    """Use ``ServerlessLaravel`` to create the serverless Laravel resource.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        laravel_path: str,
        bref_layer_version: str,
        database_config: typing.Optional["DatabaseConfig"] = None,
        handler: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        lambda_code_path: typing.Optional[str] = None,
        rds_proxy: typing.Optional[aws_cdk.aws_rds.IDatabaseProxy] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param laravel_path: path to your local laravel directory with bref.
        :param bref_layer_version: AWS Lambda layer version from the Bref runtime. e.g. arn:aws:lambda:us-west-1:209497400698:layer:php-74-fpm:12 check the latest runtime verion arn at https://bref.sh/docs/runtimes/
        :param database_config: Database configurations.
        :param handler: custom lambda function for the API. Default: - A Lambda function with Lavavel and Bref support will be created
        :param lambda_code_path: custom lambda code asset path. Default: - DEFAULT_LAMBDA_ASSET_PATH
        :param rds_proxy: RDS Proxy for the Lambda function. Default: - no db proxy
        :param vpc: The VPC for this stack.

        stability
        :stability: experimental
        """
        props = ServerlessLaravelProps(
            laravel_path=laravel_path,
            bref_layer_version=bref_layer_version,
            database_config=database_config,
            handler=handler,
            lambda_code_path=lambda_code_path,
            rds_proxy=rds_proxy,
            vpc=vpc,
        )

        jsii.create(ServerlessLaravel, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-serverless-lamp.ServerlessLaravelProps",
    jsii_struct_bases=[ServerlessApiProps],
    name_mapping={
        "bref_layer_version": "brefLayerVersion",
        "database_config": "databaseConfig",
        "handler": "handler",
        "lambda_code_path": "lambdaCodePath",
        "rds_proxy": "rdsProxy",
        "vpc": "vpc",
        "laravel_path": "laravelPath",
    },
)
class ServerlessLaravelProps(ServerlessApiProps):
    def __init__(
        self,
        *,
        bref_layer_version: str,
        database_config: typing.Optional["DatabaseConfig"] = None,
        handler: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        lambda_code_path: typing.Optional[str] = None,
        rds_proxy: typing.Optional[aws_cdk.aws_rds.IDatabaseProxy] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        laravel_path: str,
    ) -> None:
        """Construct properties for ``ServerlessLaravel``.

        :param bref_layer_version: AWS Lambda layer version from the Bref runtime. e.g. arn:aws:lambda:us-west-1:209497400698:layer:php-74-fpm:12 check the latest runtime verion arn at https://bref.sh/docs/runtimes/
        :param database_config: Database configurations.
        :param handler: custom lambda function for the API. Default: - A Lambda function with Lavavel and Bref support will be created
        :param lambda_code_path: custom lambda code asset path. Default: - DEFAULT_LAMBDA_ASSET_PATH
        :param rds_proxy: RDS Proxy for the Lambda function. Default: - no db proxy
        :param vpc: The VPC for this stack.
        :param laravel_path: path to your local laravel directory with bref.

        stability
        :stability: experimental
        """
        if isinstance(database_config, dict):
            database_config = DatabaseConfig(**database_config)
        self._values = {
            "bref_layer_version": bref_layer_version,
            "laravel_path": laravel_path,
        }
        if database_config is not None:
            self._values["database_config"] = database_config
        if handler is not None:
            self._values["handler"] = handler
        if lambda_code_path is not None:
            self._values["lambda_code_path"] = lambda_code_path
        if rds_proxy is not None:
            self._values["rds_proxy"] = rds_proxy
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def bref_layer_version(self) -> str:
        """AWS Lambda layer version from the Bref runtime.

        e.g. arn:aws:lambda:us-west-1:209497400698:layer:php-74-fpm:12
        check the latest runtime verion arn at https://bref.sh/docs/runtimes/

        stability
        :stability: experimental
        """
        return self._values.get("bref_layer_version")

    @builtins.property
    def database_config(self) -> typing.Optional["DatabaseConfig"]:
        """Database configurations.

        stability
        :stability: experimental
        """
        return self._values.get("database_config")

    @builtins.property
    def handler(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """custom lambda function for the API.

        default
        :default: - A Lambda function with Lavavel and Bref support will be created

        stability
        :stability: experimental
        """
        return self._values.get("handler")

    @builtins.property
    def lambda_code_path(self) -> typing.Optional[str]:
        """custom lambda code asset path.

        default
        :default: - DEFAULT_LAMBDA_ASSET_PATH

        stability
        :stability: experimental
        """
        return self._values.get("lambda_code_path")

    @builtins.property
    def rds_proxy(self) -> typing.Optional[aws_cdk.aws_rds.IDatabaseProxy]:
        """RDS Proxy for the Lambda function.

        default
        :default: - no db proxy

        stability
        :stability: experimental
        """
        return self._values.get("rds_proxy")

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC for this stack.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def laravel_path(self) -> str:
        """path to your local laravel directory with bref.

        stability
        :stability: experimental
        """
        return self._values.get("laravel_path")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerlessLaravelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DatabaseCluster",
    "DatabaseConfig",
    "DatabaseProps",
    "ServerlessApi",
    "ServerlessApiProps",
    "ServerlessLaravel",
    "ServerlessLaravelProps",
]

publication.publish()
