"""
## Kinesis Firehose Transformer
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

import aws_cdk.aws_glue
import aws_cdk.aws_kinesisfirehose
import aws_cdk.aws_logs
import aws_cdk.core


class KinesisFirehoseTransformer(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-7layer-constructs/kinesis-firehose-transformer.KinesisFirehoseTransformer",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        create_encryption_key: bool,
        delivery_stream_name: str,
        enable_cloudwatch_logging: bool,
        target_table_config: "TargetGlueTableConfig",
        logs_config: typing.Optional["LogsConfig"] = None,
        processing_config: typing.Optional[
            aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ProcessingConfigurationProperty
        ] = None,
        source_backup_config: typing.Optional["SourceBackupConfig"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param create_encryption_key: -
        :param delivery_stream_name: -
        :param enable_cloudwatch_logging: -
        :param target_table_config: -
        :param logs_config: -
        :param processing_config: -
        :param source_backup_config: -
        """
        props = KinesisFirehoseTransformerProps(
            create_encryption_key=create_encryption_key,
            delivery_stream_name=delivery_stream_name,
            enable_cloudwatch_logging=enable_cloudwatch_logging,
            target_table_config=target_table_config,
            logs_config=logs_config,
            processing_config=processing_config,
            source_backup_config=source_backup_config,
        )

        jsii.create(KinesisFirehoseTransformer, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseArn")
    def kinesis_firehose_arn(self) -> str:
        return jsii.get(self, "kinesisFirehoseArn")


@jsii.data_type(
    jsii_type="@cdk-7layer-constructs/kinesis-firehose-transformer.KinesisFirehoseTransformerProps",
    jsii_struct_bases=[],
    name_mapping={
        "create_encryption_key": "createEncryptionKey",
        "delivery_stream_name": "deliveryStreamName",
        "enable_cloudwatch_logging": "enableCloudwatchLogging",
        "target_table_config": "targetTableConfig",
        "logs_config": "logsConfig",
        "processing_config": "processingConfig",
        "source_backup_config": "sourceBackupConfig",
    },
)
class KinesisFirehoseTransformerProps:
    def __init__(
        self,
        *,
        create_encryption_key: bool,
        delivery_stream_name: str,
        enable_cloudwatch_logging: bool,
        target_table_config: "TargetGlueTableConfig",
        logs_config: typing.Optional["LogsConfig"] = None,
        processing_config: typing.Optional[
            aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ProcessingConfigurationProperty
        ] = None,
        source_backup_config: typing.Optional["SourceBackupConfig"] = None,
    ) -> None:
        """
        :param create_encryption_key: -
        :param delivery_stream_name: -
        :param enable_cloudwatch_logging: -
        :param target_table_config: -
        :param logs_config: -
        :param processing_config: -
        :param source_backup_config: -
        """
        if isinstance(target_table_config, dict):
            target_table_config = TargetGlueTableConfig(**target_table_config)
        if isinstance(logs_config, dict):
            logs_config = LogsConfig(**logs_config)
        if isinstance(processing_config, dict):
            processing_config = aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ProcessingConfigurationProperty(
                **processing_config
            )
        if isinstance(source_backup_config, dict):
            source_backup_config = SourceBackupConfig(**source_backup_config)
        self._values = {
            "create_encryption_key": create_encryption_key,
            "delivery_stream_name": delivery_stream_name,
            "enable_cloudwatch_logging": enable_cloudwatch_logging,
            "target_table_config": target_table_config,
        }
        if logs_config is not None:
            self._values["logs_config"] = logs_config
        if processing_config is not None:
            self._values["processing_config"] = processing_config
        if source_backup_config is not None:
            self._values["source_backup_config"] = source_backup_config

    @builtins.property
    def create_encryption_key(self) -> bool:
        return self._values.get("create_encryption_key")

    @builtins.property
    def delivery_stream_name(self) -> str:
        return self._values.get("delivery_stream_name")

    @builtins.property
    def enable_cloudwatch_logging(self) -> bool:
        return self._values.get("enable_cloudwatch_logging")

    @builtins.property
    def target_table_config(self) -> "TargetGlueTableConfig":
        return self._values.get("target_table_config")

    @builtins.property
    def logs_config(self) -> typing.Optional["LogsConfig"]:
        return self._values.get("logs_config")

    @builtins.property
    def processing_config(
        self,
    ) -> typing.Optional[
        aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ProcessingConfigurationProperty
    ]:
        return self._values.get("processing_config")

    @builtins.property
    def source_backup_config(self) -> typing.Optional["SourceBackupConfig"]:
        return self._values.get("source_backup_config")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseTransformerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-7layer-constructs/kinesis-firehose-transformer.LogsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "logs_group_name": "logsGroupName",
        "logs_removal_policy": "logsRemovalPolicy",
        "logs_retention_days": "logsRetentionDays",
    },
)
class LogsConfig:
    def __init__(
        self,
        *,
        logs_group_name: str,
        logs_removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        logs_retention_days: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
    ) -> None:
        """
        :param logs_group_name: -
        :param logs_removal_policy: -
        :param logs_retention_days: -
        """
        self._values = {
            "logs_group_name": logs_group_name,
        }
        if logs_removal_policy is not None:
            self._values["logs_removal_policy"] = logs_removal_policy
        if logs_retention_days is not None:
            self._values["logs_retention_days"] = logs_retention_days

    @builtins.property
    def logs_group_name(self) -> str:
        return self._values.get("logs_group_name")

    @builtins.property
    def logs_removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        return self._values.get("logs_removal_policy")

    @builtins.property
    def logs_retention_days(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        return self._values.get("logs_retention_days")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-7layer-constructs/kinesis-firehose-transformer.SourceBackupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "columns": "columns",
        "glue_database_arn": "glueDatabaseArn",
        "table_name": "tableName",
        "target_s3_bucket_arn": "targetS3BucketArn",
        "target_s3prefix": "targetS3prefix",
    },
)
class SourceBackupConfig:
    def __init__(
        self,
        *,
        columns: typing.List[aws_cdk.aws_glue.Column],
        glue_database_arn: str,
        table_name: str,
        target_s3_bucket_arn: typing.Optional[str] = None,
        target_s3prefix: typing.Optional[str] = None,
    ) -> None:
        """
        :param columns: -
        :param glue_database_arn: -
        :param table_name: -
        :param target_s3_bucket_arn: -
        :param target_s3prefix: -
        """
        self._values = {
            "columns": columns,
            "glue_database_arn": glue_database_arn,
            "table_name": table_name,
        }
        if target_s3_bucket_arn is not None:
            self._values["target_s3_bucket_arn"] = target_s3_bucket_arn
        if target_s3prefix is not None:
            self._values["target_s3prefix"] = target_s3prefix

    @builtins.property
    def columns(self) -> typing.List[aws_cdk.aws_glue.Column]:
        return self._values.get("columns")

    @builtins.property
    def glue_database_arn(self) -> str:
        return self._values.get("glue_database_arn")

    @builtins.property
    def table_name(self) -> str:
        return self._values.get("table_name")

    @builtins.property
    def target_s3_bucket_arn(self) -> typing.Optional[str]:
        return self._values.get("target_s3_bucket_arn")

    @builtins.property
    def target_s3prefix(self) -> typing.Optional[str]:
        return self._values.get("target_s3prefix")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceBackupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-7layer-constructs/kinesis-firehose-transformer.TargetGlueTableConfig",
    jsii_struct_bases=[],
    name_mapping={
        "columns": "columns",
        "glue_database_arn": "glueDatabaseArn",
        "table_name": "tableName",
        "target_s3_bucket_arn": "targetS3BucketArn",
        "target_s3prefix": "targetS3prefix",
    },
)
class TargetGlueTableConfig:
    def __init__(
        self,
        *,
        columns: typing.List[aws_cdk.aws_glue.Column],
        glue_database_arn: str,
        table_name: str,
        target_s3_bucket_arn: typing.Optional[str] = None,
        target_s3prefix: typing.Optional[str] = None,
    ) -> None:
        """
        :param columns: -
        :param glue_database_arn: -
        :param table_name: -
        :param target_s3_bucket_arn: -
        :param target_s3prefix: -
        """
        self._values = {
            "columns": columns,
            "glue_database_arn": glue_database_arn,
            "table_name": table_name,
        }
        if target_s3_bucket_arn is not None:
            self._values["target_s3_bucket_arn"] = target_s3_bucket_arn
        if target_s3prefix is not None:
            self._values["target_s3prefix"] = target_s3prefix

    @builtins.property
    def columns(self) -> typing.List[aws_cdk.aws_glue.Column]:
        return self._values.get("columns")

    @builtins.property
    def glue_database_arn(self) -> str:
        return self._values.get("glue_database_arn")

    @builtins.property
    def table_name(self) -> str:
        return self._values.get("table_name")

    @builtins.property
    def target_s3_bucket_arn(self) -> typing.Optional[str]:
        return self._values.get("target_s3_bucket_arn")

    @builtins.property
    def target_s3prefix(self) -> typing.Optional[str]:
        return self._values.get("target_s3prefix")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetGlueTableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "KinesisFirehoseTransformer",
    "KinesisFirehoseTransformerProps",
    "LogsConfig",
    "SourceBackupConfig",
    "TargetGlueTableConfig",
]

publication.publish()
