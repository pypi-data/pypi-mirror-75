"""
# cdk-sqlserver-seeder [![Mentioned in Awesome CDK](https://awesome.re/mentioned-badge.svg)](https://github.com/eladb/awesome-cdk)

![build](https://github.com/kolomied/cdk-sqlserver-seeder/workflows/build/badge.svg)
![jsii-publish](https://github.com/kolomied/cdk-sqlserver-seeder/workflows/jsii-publish/badge.svg)
![downloads](https://img.shields.io/npm/dt/cdk-sqlserver-seeder)

[![npm version](https://badge.fury.io/js/cdk-sqlserver-seeder.svg)](https://badge.fury.io/js/cdk-sqlserver-seeder)
[![PyPI version](https://badge.fury.io/py/cdk-sqlserver-seeder.svg)](https://badge.fury.io/py/cdk-sqlserver-seeder)
[![NuGet version](https://badge.fury.io/nu/Talnakh.SqlServerSeeder.svg)](https://badge.fury.io/nu/Talnakh.SqlServerSeeder)
[![Maven Central](https://img.shields.io/maven-central/v/xyz.talnakh/SqlServerSeeder?color=brightgreen)](https://repo1.maven.org/maven2/xyz/talnakh/SqlServerSeeder/)

A simple CDK seeder for SQL Server RDS databases.

When you create an RDS SQL Server instance using CloudFormation template, there is no way to provide initial
schema definition as part of CloudFormation stack deployment. Custom schema deployment scripts can be executed
only after the database deployment is complete.

*cdk-sqlserver-seeder* library is a [AWS CDK](https://aws.amazon.com/cdk/) construct that provides a way to automate
this process and eliminate manual steps involved in the process of preparing new RDS SQL Server environment by
executing custom SQL scripts on RDS SQL Server instance creation/deletion.

The construct relies on [Invoke-SqlCmd](https://docs.microsoft.com/en-us/powershell/module/sqlserver/invoke-sqlcmd) cmdlet
to run the scripts and provides a way to handle transient errors during stack provisioning.

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds
from cdk_sqlserver_seeder import SqlServerSeeder

class DatabaseStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection)

        sql_server = rds.DatabaseInstance(self, "Instance",
            engine=rds.DatabaseInstanceEngine.SQL_SERVER_WEB
        )

        seeder = SqlServerSeeder(self, "SqlSeeder",
            database=sql_server,
            port=1433,
            vpc=vpc,
            create_script_path="./SQL/v1.0.0.sql", # script to be executed on resource creation
            delete_script_path="./SQL/cleanup.sql"
        )
```

## Configuration properties

SqlServerSeeder construct accepts the following configuration properties:

| Parameter  | Required  | Default | Description |
|---|---|---|---|
| `vpc`              | yes |       | VPC for Lambda function deployment      |
| `database`         | yes |       | RDS SQL Server database instance        |
| `createScriptPath` | yes |       | SQL scripts to run on resource creation |
| `deleteScriptPath` | no  |       | SQL script to run on resource deletion  |
| `port`             | no  | 1433  | RSD SQL Server database port            |
| `memorySize`       | no  | 512   | Lambda function memory size             |
| `ignoreSqlErrors`  | no  | false | Whether to ignore SQL error or not      |

## Architecture

![Architecture](/doc/architecture.png)

`cdk-sqlserver-seeder` deploys a custom resource backed by PowerShell lambda to connect to SQL Server instance. Lambda function is deployed in private subnets of your VPC where RDS instance resides.

Lambda function retrieves database credentials from [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) and uses them to construct connection string to the database.

SQL scripts are uploaded into S3 bucket during CDK application deployment.
Lambda function downloads these scripts during execution.

## Security considerations

Lambda function has the following permissions:

* Managed policies

  * `AWSLambdaBasicExecutionRole` for CloudWatch logs
  * `AWSLambdaVPCAccessExecutionRole` for VPC access
* Inline policy

  * `secretsmanager:GetSecretValue` for RDS credentials secret
  * `s3:GetObject*`, `s3:GetBucket*`, `s3:List*` for S3 bucket with SQL scripts

## Acknowledgements

The whole project inspired by [aws-cdk-dynamodb-seeder](https://github.com/elegantdevelopment/aws-cdk-dynamodb-seeder).
I though it would be very helpful to have a similar way to seed initial schema to more traditional SQL Server databases.
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
import aws_cdk.aws_rds
import aws_cdk.core


class SqlServerSeeder(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-sqlserver-seeder.SqlServerSeeder",
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
        create_script_path: str,
        database: aws_cdk.aws_rds.DatabaseInstance,
        port: jsii.Number,
        vpc: aws_cdk.aws_ec2.IVpc,
        delete_script_path: typing.Optional[str] = None,
        ignore_sql_errors: typing.Optional[bool] = None,
        memory_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param create_script_path: 
        :param database: 
        :param port: 
        :param vpc: 
        :param delete_script_path: 
        :param ignore_sql_errors: Flag that allows to ignore SQL errors. May be helpful during troubleshooting. Default: false
        :param memory_size: The amount of memory, in MB, that is allocated to custom resource's Lambda function. May require some tweaking for "hunger" SQL scripts. Default: 512

        stability
        :stability: experimental
        """
        props = SqlServerSeederProps(
            create_script_path=create_script_path,
            database=database,
            port=port,
            vpc=vpc,
            delete_script_path=delete_script_path,
            ignore_sql_errors=ignore_sql_errors,
            memory_size=memory_size,
        )

        jsii.create(SqlServerSeeder, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-sqlserver-seeder.SqlServerSeederProps",
    jsii_struct_bases=[],
    name_mapping={
        "create_script_path": "createScriptPath",
        "database": "database",
        "port": "port",
        "vpc": "vpc",
        "delete_script_path": "deleteScriptPath",
        "ignore_sql_errors": "ignoreSqlErrors",
        "memory_size": "memorySize",
    },
)
class SqlServerSeederProps:
    def __init__(
        self,
        *,
        create_script_path: str,
        database: aws_cdk.aws_rds.DatabaseInstance,
        port: jsii.Number,
        vpc: aws_cdk.aws_ec2.IVpc,
        delete_script_path: typing.Optional[str] = None,
        ignore_sql_errors: typing.Optional[bool] = None,
        memory_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param create_script_path: 
        :param database: 
        :param port: 
        :param vpc: 
        :param delete_script_path: 
        :param ignore_sql_errors: Flag that allows to ignore SQL errors. May be helpful during troubleshooting. Default: false
        :param memory_size: The amount of memory, in MB, that is allocated to custom resource's Lambda function. May require some tweaking for "hunger" SQL scripts. Default: 512

        stability
        :stability: experimental
        """
        self._values = {
            "create_script_path": create_script_path,
            "database": database,
            "port": port,
            "vpc": vpc,
        }
        if delete_script_path is not None:
            self._values["delete_script_path"] = delete_script_path
        if ignore_sql_errors is not None:
            self._values["ignore_sql_errors"] = ignore_sql_errors
        if memory_size is not None:
            self._values["memory_size"] = memory_size

    @builtins.property
    def create_script_path(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("create_script_path")

    @builtins.property
    def database(self) -> aws_cdk.aws_rds.DatabaseInstance:
        """
        stability
        :stability: experimental
        """
        return self._values.get("database")

    @builtins.property
    def port(self) -> jsii.Number:
        """
        stability
        :stability: experimental
        """
        return self._values.get("port")

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """
        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def delete_script_path(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("delete_script_path")

    @builtins.property
    def ignore_sql_errors(self) -> typing.Optional[bool]:
        """Flag that allows to ignore SQL errors.

        May be helpful during troubleshooting.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("ignore_sql_errors")

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        """The amount of memory, in MB, that is allocated to custom resource's Lambda function.

        May require some tweaking for "hunger" SQL scripts.

        default
        :default: 512

        stability
        :stability: experimental
        """
        return self._values.get("memory_size")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlServerSeederProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SqlServerSeeder",
    "SqlServerSeederProps",
]

publication.publish()
