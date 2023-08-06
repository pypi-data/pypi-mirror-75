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
