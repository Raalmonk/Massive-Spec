"""
Type annotations for dynamodb service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/type_defs/)

Usage::

    ```python
    from mypy_boto3_dynamodb.type_defs import ArchivalSummaryTypeDef

    data: ArchivalSummaryTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Mapping, Sequence, Set, Union

from boto3.dynamodb.conditions import ConditionBase

from .literals import (
    ApproximateCreationDateTimePrecisionType,
    AttributeActionType,
    BackupStatusType,
    BackupTypeFilterType,
    BackupTypeType,
    BatchStatementErrorCodeEnumType,
    BillingModeType,
    ComparisonOperatorType,
    ConditionalOperatorType,
    ContinuousBackupsStatusType,
    ContributorInsightsActionType,
    ContributorInsightsStatusType,
    DestinationStatusType,
    ExportFormatType,
    ExportStatusType,
    ExportTypeType,
    ExportViewTypeType,
    GlobalTableStatusType,
    ImportStatusType,
    IndexStatusType,
    InputCompressionTypeType,
    InputFormatType,
    KeyTypeType,
    PointInTimeRecoveryStatusType,
    ProjectionTypeType,
    ReplicaStatusType,
    ReturnConsumedCapacityType,
    ReturnItemCollectionMetricsType,
    ReturnValuesOnConditionCheckFailureType,
    ReturnValueType,
    S3SseAlgorithmType,
    ScalarAttributeTypeType,
    SelectType,
    SSEStatusType,
    SSETypeType,
    StreamViewTypeType,
    TableClassType,
    TableStatusType,
    TimeToLiveStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ArchivalSummaryTypeDef",
    "AttributeDefinitionTypeDef",
    "AttributeValueTypeDef",
    "TableAttributeValueTypeDef",
    "AutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef",
    "AutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef",
    "BackupDetailsTypeDef",
    "BackupSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "BillingModeSummaryTypeDef",
    "CapacityTypeDef",
    "ConditionBaseImportTypeDef",
    "PointInTimeRecoveryDescriptionTypeDef",
    "ContributorInsightsSummaryTypeDef",
    "CreateBackupInputRequestTypeDef",
    "KeySchemaElementTypeDef",
    "OnDemandThroughputTypeDef",
    "ProjectionTypeDef",
    "ProvisionedThroughputTypeDef",
    "ReplicaTypeDef",
    "CreateReplicaActionTypeDef",
    "OnDemandThroughputOverrideTypeDef",
    "ProvisionedThroughputOverrideTypeDef",
    "SSESpecificationTypeDef",
    "StreamSpecificationTypeDef",
    "TagTypeDef",
    "CsvOptionsOutputTypeDef",
    "CsvOptionsTypeDef",
    "DeleteBackupInputRequestTypeDef",
    "DeleteGlobalSecondaryIndexActionTypeDef",
    "DeleteReplicaActionTypeDef",
    "DeleteReplicationGroupMemberActionTypeDef",
    "DeleteResourcePolicyInputRequestTypeDef",
    "DeleteTableInputRequestTypeDef",
    "DescribeBackupInputRequestTypeDef",
    "DescribeContinuousBackupsInputRequestTypeDef",
    "DescribeContributorInsightsInputRequestTypeDef",
    "FailureExceptionTypeDef",
    "EndpointTypeDef",
    "DescribeExportInputRequestTypeDef",
    "DescribeGlobalTableInputRequestTypeDef",
    "DescribeGlobalTableSettingsInputRequestTypeDef",
    "DescribeImportInputRequestTypeDef",
    "DescribeKinesisStreamingDestinationInputRequestTypeDef",
    "KinesisDataStreamDestinationTypeDef",
    "DescribeTableInputRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeTableReplicaAutoScalingInputRequestTypeDef",
    "DescribeTimeToLiveInputRequestTypeDef",
    "TimeToLiveDescriptionTypeDef",
    "EnableKinesisStreamingConfigurationTypeDef",
    "IncrementalExportSpecificationOutputTypeDef",
    "ExportSummaryTypeDef",
    "TimestampTypeDef",
    "GetResourcePolicyInputRequestTypeDef",
    "ProjectionExtraOutputTypeDef",
    "ProvisionedThroughputDescriptionTypeDef",
    "ProjectionOutputTypeDef",
    "S3BucketSourceTypeDef",
    "PaginatorConfigTypeDef",
    "ListContributorInsightsInputRequestTypeDef",
    "ListExportsInputRequestTypeDef",
    "ListGlobalTablesInputRequestTypeDef",
    "ListImportsInputRequestTypeDef",
    "ListTablesInputRequestTypeDef",
    "ListTagsOfResourceInputRequestTypeDef",
    "PointInTimeRecoverySpecificationTypeDef",
    "PutResourcePolicyInputRequestTypeDef",
    "TableClassSummaryTypeDef",
    "RestoreSummaryTypeDef",
    "SSEDescriptionTypeDef",
    "TableBatchWriterRequestTypeDef",
    "TimeToLiveSpecificationTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateContributorInsightsInputRequestTypeDef",
    "UpdateKinesisStreamingConfigurationTypeDef",
    "BatchStatementErrorTypeDef",
    "DeleteRequestOutputTypeDef",
    "ItemCollectionMetricsTypeDef",
    "ItemResponseTypeDef",
    "KeysAndAttributesOutputTypeDef",
    "PutRequestOutputTypeDef",
    "UniversalAttributeValueTypeDef",
    "AttributeValueUpdateTableTypeDef",
    "ConditionTableTypeDef",
    "DeleteRequestServiceResourceOutputTypeDef",
    "DeleteRequestServiceResourceTypeDef",
    "ExpectedAttributeValueTableTypeDef",
    "GetItemInputTableGetItemTypeDef",
    "ItemCollectionMetricsServiceResourceTypeDef",
    "ItemCollectionMetricsTableTypeDef",
    "KeysAndAttributesServiceResourceOutputTypeDef",
    "KeysAndAttributesServiceResourceTypeDef",
    "PutRequestServiceResourceOutputTypeDef",
    "PutRequestServiceResourceTypeDef",
    "AutoScalingPolicyDescriptionTypeDef",
    "AutoScalingPolicyUpdateTypeDef",
    "CreateBackupOutputTypeDef",
    "DeleteResourcePolicyOutputTypeDef",
    "DescribeLimitsOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetResourcePolicyOutputTypeDef",
    "ListBackupsOutputTypeDef",
    "ListTablesOutputTypeDef",
    "PutResourcePolicyOutputTypeDef",
    "UpdateContributorInsightsOutputTypeDef",
    "ConsumedCapacityTypeDef",
    "ContinuousBackupsDescriptionTypeDef",
    "ListContributorInsightsOutputTypeDef",
    "LocalSecondaryIndexTypeDef",
    "CreateGlobalSecondaryIndexActionTypeDef",
    "GlobalSecondaryIndexTypeDef",
    "SourceTableDetailsTypeDef",
    "UpdateGlobalSecondaryIndexActionTypeDef",
    "CreateGlobalTableInputRequestTypeDef",
    "GlobalTableTypeDef",
    "ReplicaGlobalSecondaryIndexDescriptionTypeDef",
    "ReplicaGlobalSecondaryIndexTypeDef",
    "ListTagsOfResourceOutputTypeDef",
    "TagResourceInputRequestTypeDef",
    "InputFormatOptionsOutputTypeDef",
    "InputFormatOptionsTypeDef",
    "ReplicaUpdateTypeDef",
    "DescribeContributorInsightsOutputTypeDef",
    "DescribeEndpointsResponseTypeDef",
    "DescribeKinesisStreamingDestinationOutputTypeDef",
    "DescribeTableInputTableExistsWaitTypeDef",
    "DescribeTableInputTableNotExistsWaitTypeDef",
    "DescribeTimeToLiveOutputTypeDef",
    "KinesisStreamingDestinationInputRequestTypeDef",
    "KinesisStreamingDestinationOutputTypeDef",
    "ExportDescriptionTypeDef",
    "ListExportsOutputTypeDef",
    "IncrementalExportSpecificationTypeDef",
    "ListBackupsInputRequestTypeDef",
    "LocalSecondaryIndexDescriptionTypeDef",
    "GlobalSecondaryIndexDescriptionTypeDef",
    "GlobalSecondaryIndexInfoTypeDef",
    "GlobalSecondaryIndexOutputTypeDef",
    "LocalSecondaryIndexInfoTypeDef",
    "ImportSummaryTypeDef",
    "ListBackupsInputListBackupsPaginateTypeDef",
    "ListTablesInputListTablesPaginateTypeDef",
    "ListTagsOfResourceInputListTagsOfResourcePaginateTypeDef",
    "UpdateContinuousBackupsInputRequestTypeDef",
    "UpdateTimeToLiveInputRequestTypeDef",
    "UpdateTimeToLiveOutputTypeDef",
    "UpdateKinesisStreamingDestinationInputRequestTypeDef",
    "UpdateKinesisStreamingDestinationOutputTypeDef",
    "BatchStatementResponseTypeDef",
    "WriteRequestOutputTypeDef",
    "AttributeValueUpdateTypeDef",
    "BatchStatementRequestTypeDef",
    "ConditionCheckTypeDef",
    "ConditionTypeDef",
    "DeleteRequestTypeDef",
    "DeleteTypeDef",
    "ExecuteStatementInputRequestTypeDef",
    "ExpectedAttributeValueTypeDef",
    "GetItemInputRequestTypeDef",
    "GetTypeDef",
    "KeysAndAttributesTypeDef",
    "ParameterizedStatementTypeDef",
    "PutRequestTypeDef",
    "PutTypeDef",
    "UpdateTypeDef",
    "QueryInputTableQueryTypeDef",
    "ScanInputTableScanTypeDef",
    "DeleteItemInputTableDeleteItemTypeDef",
    "PutItemInputTablePutItemTypeDef",
    "UpdateItemInputTableUpdateItemTypeDef",
    "KeysAndAttributesServiceResourceUnionTypeDef",
    "WriteRequestServiceResourceOutputTypeDef",
    "WriteRequestServiceResourceTypeDef",
    "AutoScalingSettingsDescriptionTypeDef",
    "AutoScalingSettingsUpdateTypeDef",
    "BatchGetItemOutputServiceResourceTypeDef",
    "BatchGetItemOutputTypeDef",
    "DeleteItemOutputTableTypeDef",
    "DeleteItemOutputTypeDef",
    "ExecuteStatementOutputTypeDef",
    "ExecuteTransactionOutputTypeDef",
    "GetItemOutputTableTypeDef",
    "GetItemOutputTypeDef",
    "PutItemOutputTableTypeDef",
    "PutItemOutputTypeDef",
    "QueryOutputTableTypeDef",
    "QueryOutputTypeDef",
    "ScanOutputTableTypeDef",
    "ScanOutputTypeDef",
    "TransactGetItemsOutputTypeDef",
    "TransactWriteItemsOutputTypeDef",
    "UpdateItemOutputTableTypeDef",
    "UpdateItemOutputTypeDef",
    "DescribeContinuousBackupsOutputTypeDef",
    "UpdateContinuousBackupsOutputTypeDef",
    "TableCreationParametersTypeDef",
    "GlobalSecondaryIndexUpdateTypeDef",
    "ListGlobalTablesOutputTypeDef",
    "ReplicaDescriptionTypeDef",
    "CreateReplicationGroupMemberActionTypeDef",
    "UpdateReplicationGroupMemberActionTypeDef",
    "InputFormatOptionsUnionTypeDef",
    "UpdateGlobalTableInputRequestTypeDef",
    "DescribeExportOutputTypeDef",
    "ExportTableToPointInTimeOutputTypeDef",
    "ExportTableToPointInTimeInputRequestTypeDef",
    "IncrementalExportSpecificationUnionTypeDef",
    "GlobalSecondaryIndexUnionTypeDef",
    "TableCreationParametersOutputTypeDef",
    "SourceTableFeatureDetailsTypeDef",
    "ListImportsOutputTypeDef",
    "BatchExecuteStatementOutputTypeDef",
    "BatchWriteItemOutputTypeDef",
    "BatchExecuteStatementInputRequestTypeDef",
    "QueryInputQueryPaginateTypeDef",
    "QueryInputRequestTypeDef",
    "ScanInputRequestTypeDef",
    "ScanInputScanPaginateTypeDef",
    "DeleteItemInputRequestTypeDef",
    "PutItemInputRequestTypeDef",
    "UpdateItemInputRequestTypeDef",
    "TransactGetItemTypeDef",
    "KeysAndAttributesUnionTypeDef",
    "ExecuteTransactionInputRequestTypeDef",
    "WriteRequestTypeDef",
    "TransactWriteItemTypeDef",
    "BatchGetItemInputServiceResourceBatchGetItemTypeDef",
    "BatchWriteItemOutputServiceResourceTypeDef",
    "WriteRequestServiceResourceUnionTypeDef",
    "ReplicaGlobalSecondaryIndexAutoScalingDescriptionTypeDef",
    "ReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef",
    "GlobalSecondaryIndexAutoScalingUpdateTypeDef",
    "GlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef",
    "ReplicaGlobalSecondaryIndexAutoScalingUpdateTypeDef",
    "ReplicaGlobalSecondaryIndexSettingsUpdateTypeDef",
    "ImportTableInputRequestTypeDef",
    "GlobalTableDescriptionTypeDef",
    "TableDescriptionTypeDef",
    "ReplicationGroupUpdateTypeDef",
    "CreateTableInputRequestTypeDef",
    "CreateTableInputServiceResourceCreateTableTypeDef",
    "RestoreTableFromBackupInputRequestTypeDef",
    "RestoreTableToPointInTimeInputRequestTypeDef",
    "ImportTableDescriptionTypeDef",
    "TableCreationParametersUnionTypeDef",
    "BackupDescriptionTypeDef",
    "TransactGetItemsInputRequestTypeDef",
    "BatchGetItemInputRequestTypeDef",
    "WriteRequestUnionTypeDef",
    "TransactWriteItemsInputRequestTypeDef",
    "BatchWriteItemInputServiceResourceBatchWriteItemTypeDef",
    "ReplicaAutoScalingDescriptionTypeDef",
    "ReplicaSettingsDescriptionTypeDef",
    "ReplicaAutoScalingUpdateTypeDef",
    "ReplicaSettingsUpdateTypeDef",
    "CreateGlobalTableOutputTypeDef",
    "DescribeGlobalTableOutputTypeDef",
    "UpdateGlobalTableOutputTypeDef",
    "CreateTableOutputTypeDef",
    "DeleteTableOutputTypeDef",
    "DescribeTableOutputTypeDef",
    "RestoreTableFromBackupOutputTypeDef",
    "RestoreTableToPointInTimeOutputTypeDef",
    "UpdateTableOutputTypeDef",
    "UpdateTableInputRequestTypeDef",
    "UpdateTableInputTableUpdateTypeDef",
    "DescribeImportOutputTypeDef",
    "ImportTableOutputTypeDef",
    "DeleteBackupOutputTypeDef",
    "DescribeBackupOutputTypeDef",
    "BatchWriteItemInputRequestTypeDef",
    "TableAutoScalingDescriptionTypeDef",
    "DescribeGlobalTableSettingsOutputTypeDef",
    "UpdateGlobalTableSettingsOutputTypeDef",
    "UpdateTableReplicaAutoScalingInputRequestTypeDef",
    "UpdateGlobalTableSettingsInputRequestTypeDef",
    "DescribeTableReplicaAutoScalingOutputTypeDef",
    "UpdateTableReplicaAutoScalingOutputTypeDef",
)

ArchivalSummaryTypeDef = TypedDict(
    "ArchivalSummaryTypeDef",
    {
        "ArchivalDateTime": NotRequired[datetime],
        "ArchivalReason": NotRequired[str],
        "ArchivalBackupArn": NotRequired[str],
    },
)
AttributeDefinitionTypeDef = TypedDict(
    "AttributeDefinitionTypeDef",
    {
        "AttributeName": str,
        "AttributeType": ScalarAttributeTypeType,
    },
)
AttributeValueTypeDef = TypedDict(
    "AttributeValueTypeDef",
    {
        "S": NotRequired[str],
        "N": NotRequired[str],
        "B": NotRequired[bytes],
        "SS": NotRequired[Sequence[str]],
        "NS": NotRequired[Sequence[str]],
        "BS": NotRequired[Sequence[bytes]],
        "M": NotRequired[Mapping[str, Any]],
        "L": NotRequired[Sequence[Any]],
        "NULL": NotRequired[bool],
        "BOOL": NotRequired[bool],
    },
)
TableAttributeValueTypeDef = Union[
    bytes,
    bytearray,
    str,
    int,
    Decimal,
    bool,
    Set[int],
    Set[Decimal],
    Set[str],
    Set[bytes],
    Set[bytearray],
    Sequence[Any],
    Mapping[str, Any],
    None,
]
AutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef = TypedDict(
    "AutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef",
    {
        "TargetValue": float,
        "DisableScaleIn": NotRequired[bool],
        "ScaleInCooldown": NotRequired[int],
        "ScaleOutCooldown": NotRequired[int],
    },
)
AutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef = TypedDict(
    "AutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef",
    {
        "TargetValue": float,
        "DisableScaleIn": NotRequired[bool],
        "ScaleInCooldown": NotRequired[int],
        "ScaleOutCooldown": NotRequired[int],
    },
)
BackupDetailsTypeDef = TypedDict(
    "BackupDetailsTypeDef",
    {
        "BackupArn": str,
        "BackupName": str,
        "BackupStatus": BackupStatusType,
        "BackupType": BackupTypeType,
        "BackupCreationDateTime": datetime,
        "BackupSizeBytes": NotRequired[int],
        "BackupExpiryDateTime": NotRequired[datetime],
    },
)
BackupSummaryTypeDef = TypedDict(
    "BackupSummaryTypeDef",
    {
        "TableName": NotRequired[str],
        "TableId": NotRequired[str],
        "TableArn": NotRequired[str],
        "BackupArn": NotRequired[str],
        "BackupName": NotRequired[str],
        "BackupCreationDateTime": NotRequired[datetime],
        "BackupExpiryDateTime": NotRequired[datetime],
        "BackupStatus": NotRequired[BackupStatusType],
        "BackupType": NotRequired[BackupTypeType],
        "BackupSizeBytes": NotRequired[int],
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
BillingModeSummaryTypeDef = TypedDict(
    "BillingModeSummaryTypeDef",
    {
        "BillingMode": NotRequired[BillingModeType],
        "LastUpdateToPayPerRequestDateTime": NotRequired[datetime],
    },
)
CapacityTypeDef = TypedDict(
    "CapacityTypeDef",
    {
        "ReadCapacityUnits": NotRequired[float],
        "WriteCapacityUnits": NotRequired[float],
        "CapacityUnits": NotRequired[float],
    },
)
ConditionBaseImportTypeDef = Union[str, ConditionBase]
PointInTimeRecoveryDescriptionTypeDef = TypedDict(
    "PointInTimeRecoveryDescriptionTypeDef",
    {
        "PointInTimeRecoveryStatus": NotRequired[PointInTimeRecoveryStatusType],
        "EarliestRestorableDateTime": NotRequired[datetime],
        "LatestRestorableDateTime": NotRequired[datetime],
    },
)
ContributorInsightsSummaryTypeDef = TypedDict(
    "ContributorInsightsSummaryTypeDef",
    {
        "TableName": NotRequired[str],
        "IndexName": NotRequired[str],
        "ContributorInsightsStatus": NotRequired[ContributorInsightsStatusType],
    },
)
CreateBackupInputRequestTypeDef = TypedDict(
    "CreateBackupInputRequestTypeDef",
    {
        "TableName": str,
        "BackupName": str,
    },
)
KeySchemaElementTypeDef = TypedDict(
    "KeySchemaElementTypeDef",
    {
        "AttributeName": str,
        "KeyType": KeyTypeType,
    },
)
OnDemandThroughputTypeDef = TypedDict(
    "OnDemandThroughputTypeDef",
    {
        "MaxReadRequestUnits": NotRequired[int],
        "MaxWriteRequestUnits": NotRequired[int],
    },
)
ProjectionTypeDef = TypedDict(
    "ProjectionTypeDef",
    {
        "ProjectionType": NotRequired[ProjectionTypeType],
        "NonKeyAttributes": NotRequired[Sequence[str]],
    },
)
ProvisionedThroughputTypeDef = TypedDict(
    "ProvisionedThroughputTypeDef",
    {
        "ReadCapacityUnits": int,
        "WriteCapacityUnits": int,
    },
)
ReplicaTypeDef = TypedDict(
    "ReplicaTypeDef",
    {
        "RegionName": NotRequired[str],
    },
)
CreateReplicaActionTypeDef = TypedDict(
    "CreateReplicaActionTypeDef",
    {
        "RegionName": str,
    },
)
OnDemandThroughputOverrideTypeDef = TypedDict(
    "OnDemandThroughputOverrideTypeDef",
    {
        "MaxReadRequestUnits": NotRequired[int],
    },
)
ProvisionedThroughputOverrideTypeDef = TypedDict(
    "ProvisionedThroughputOverrideTypeDef",
    {
        "ReadCapacityUnits": NotRequired[int],
    },
)
SSESpecificationTypeDef = TypedDict(
    "SSESpecificationTypeDef",
    {
        "Enabled": NotRequired[bool],
        "SSEType": NotRequired[SSETypeType],
        "KMSMasterKeyId": NotRequired[str],
    },
)
StreamSpecificationTypeDef = TypedDict(
    "StreamSpecificationTypeDef",
    {
        "StreamEnabled": bool,
        "StreamViewType": NotRequired[StreamViewTypeType],
    },
)
TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)
CsvOptionsOutputTypeDef = TypedDict(
    "CsvOptionsOutputTypeDef",
    {
        "Delimiter": NotRequired[str],
        "HeaderList": NotRequired[List[str]],
    },
)
CsvOptionsTypeDef = TypedDict(
    "CsvOptionsTypeDef",
    {
        "Delimiter": NotRequired[str],
        "HeaderList": NotRequired[Sequence[str]],
    },
)
DeleteBackupInputRequestTypeDef = TypedDict(
    "DeleteBackupInputRequestTypeDef",
    {
        "BackupArn": str,
    },
)
DeleteGlobalSecondaryIndexActionTypeDef = TypedDict(
    "DeleteGlobalSecondaryIndexActionTypeDef",
    {
        "IndexName": str,
    },
)
DeleteReplicaActionTypeDef = TypedDict(
    "DeleteReplicaActionTypeDef",
    {
        "RegionName": str,
    },
)
DeleteReplicationGroupMemberActionTypeDef = TypedDict(
    "DeleteReplicationGroupMemberActionTypeDef",
    {
        "RegionName": str,
    },
)
DeleteResourcePolicyInputRequestTypeDef = TypedDict(
    "DeleteResourcePolicyInputRequestTypeDef",
    {
        "ResourceArn": str,
        "ExpectedRevisionId": NotRequired[str],
    },
)
DeleteTableInputRequestTypeDef = TypedDict(
    "DeleteTableInputRequestTypeDef",
    {
        "TableName": str,
    },
)
DescribeBackupInputRequestTypeDef = TypedDict(
    "DescribeBackupInputRequestTypeDef",
    {
        "BackupArn": str,
    },
)
DescribeContinuousBackupsInputRequestTypeDef = TypedDict(
    "DescribeContinuousBackupsInputRequestTypeDef",
    {
        "TableName": str,
    },
)
DescribeContributorInsightsInputRequestTypeDef = TypedDict(
    "DescribeContributorInsightsInputRequestTypeDef",
    {
        "TableName": str,
        "IndexName": NotRequired[str],
    },
)
FailureExceptionTypeDef = TypedDict(
    "FailureExceptionTypeDef",
    {
        "ExceptionName": NotRequired[str],
        "ExceptionDescription": NotRequired[str],
    },
)
EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "Address": str,
        "CachePeriodInMinutes": int,
    },
)
DescribeExportInputRequestTypeDef = TypedDict(
    "DescribeExportInputRequestTypeDef",
    {
        "ExportArn": str,
    },
)
DescribeGlobalTableInputRequestTypeDef = TypedDict(
    "DescribeGlobalTableInputRequestTypeDef",
    {
        "GlobalTableName": str,
    },
)
DescribeGlobalTableSettingsInputRequestTypeDef = TypedDict(
    "DescribeGlobalTableSettingsInputRequestTypeDef",
    {
        "GlobalTableName": str,
    },
)
DescribeImportInputRequestTypeDef = TypedDict(
    "DescribeImportInputRequestTypeDef",
    {
        "ImportArn": str,
    },
)
DescribeKinesisStreamingDestinationInputRequestTypeDef = TypedDict(
    "DescribeKinesisStreamingDestinationInputRequestTypeDef",
    {
        "TableName": str,
    },
)
KinesisDataStreamDestinationTypeDef = TypedDict(
    "KinesisDataStreamDestinationTypeDef",
    {
        "StreamArn": NotRequired[str],
        "DestinationStatus": NotRequired[DestinationStatusType],
        "DestinationStatusDescription": NotRequired[str],
        "ApproximateCreationDateTimePrecision": NotRequired[
            ApproximateCreationDateTimePrecisionType
        ],
    },
)
DescribeTableInputRequestTypeDef = TypedDict(
    "DescribeTableInputRequestTypeDef",
    {
        "TableName": str,
    },
)
WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": NotRequired[int],
        "MaxAttempts": NotRequired[int],
    },
)
DescribeTableReplicaAutoScalingInputRequestTypeDef = TypedDict(
    "DescribeTableReplicaAutoScalingInputRequestTypeDef",
    {
        "TableName": str,
    },
)
DescribeTimeToLiveInputRequestTypeDef = TypedDict(
    "DescribeTimeToLiveInputRequestTypeDef",
    {
        "TableName": str,
    },
)
TimeToLiveDescriptionTypeDef = TypedDict(
    "TimeToLiveDescriptionTypeDef",
    {
        "TimeToLiveStatus": NotRequired[TimeToLiveStatusType],
        "AttributeName": NotRequired[str],
    },
)
EnableKinesisStreamingConfigurationTypeDef = TypedDict(
    "EnableKinesisStreamingConfigurationTypeDef",
    {
        "ApproximateCreationDateTimePrecision": NotRequired[
            ApproximateCreationDateTimePrecisionType
        ],
    },
)
IncrementalExportSpecificationOutputTypeDef = TypedDict(
    "IncrementalExportSpecificationOutputTypeDef",
    {
        "ExportFromTime": NotRequired[datetime],
        "ExportToTime": NotRequired[datetime],
        "ExportViewType": NotRequired[ExportViewTypeType],
    },
)
ExportSummaryTypeDef = TypedDict(
    "ExportSummaryTypeDef",
    {
        "ExportArn": NotRequired[str],
        "ExportStatus": NotRequired[ExportStatusType],
        "ExportType": NotRequired[ExportTypeType],
    },
)
TimestampTypeDef = Union[datetime, str]
GetResourcePolicyInputRequestTypeDef = TypedDict(
    "GetResourcePolicyInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
ProjectionExtraOutputTypeDef = TypedDict(
    "ProjectionExtraOutputTypeDef",
    {
        "ProjectionType": NotRequired[ProjectionTypeType],
        "NonKeyAttributes": NotRequired[List[str]],
    },
)
ProvisionedThroughputDescriptionTypeDef = TypedDict(
    "ProvisionedThroughputDescriptionTypeDef",
    {
        "LastIncreaseDateTime": NotRequired[datetime],
        "LastDecreaseDateTime": NotRequired[datetime],
        "NumberOfDecreasesToday": NotRequired[int],
        "ReadCapacityUnits": NotRequired[int],
        "WriteCapacityUnits": NotRequired[int],
    },
)
ProjectionOutputTypeDef = TypedDict(
    "ProjectionOutputTypeDef",
    {
        "ProjectionType": NotRequired[ProjectionTypeType],
        "NonKeyAttributes": NotRequired[List[str]],
    },
)
S3BucketSourceTypeDef = TypedDict(
    "S3BucketSourceTypeDef",
    {
        "S3Bucket": str,
        "S3BucketOwner": NotRequired[str],
        "S3KeyPrefix": NotRequired[str],
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
ListContributorInsightsInputRequestTypeDef = TypedDict(
    "ListContributorInsightsInputRequestTypeDef",
    {
        "TableName": NotRequired[str],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListExportsInputRequestTypeDef = TypedDict(
    "ListExportsInputRequestTypeDef",
    {
        "TableArn": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
ListGlobalTablesInputRequestTypeDef = TypedDict(
    "ListGlobalTablesInputRequestTypeDef",
    {
        "ExclusiveStartGlobalTableName": NotRequired[str],
        "Limit": NotRequired[int],
        "RegionName": NotRequired[str],
    },
)
ListImportsInputRequestTypeDef = TypedDict(
    "ListImportsInputRequestTypeDef",
    {
        "TableArn": NotRequired[str],
        "PageSize": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
ListTablesInputRequestTypeDef = TypedDict(
    "ListTablesInputRequestTypeDef",
    {
        "ExclusiveStartTableName": NotRequired[str],
        "Limit": NotRequired[int],
    },
)
ListTagsOfResourceInputRequestTypeDef = TypedDict(
    "ListTagsOfResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "NextToken": NotRequired[str],
    },
)
PointInTimeRecoverySpecificationTypeDef = TypedDict(
    "PointInTimeRecoverySpecificationTypeDef",
    {
        "PointInTimeRecoveryEnabled": bool,
    },
)
PutResourcePolicyInputRequestTypeDef = TypedDict(
    "PutResourcePolicyInputRequestTypeDef",
    {
        "ResourceArn": str,
        "Policy": str,
        "ExpectedRevisionId": NotRequired[str],
        "ConfirmRemoveSelfResourceAccess": NotRequired[bool],
    },
)
TableClassSummaryTypeDef = TypedDict(
    "TableClassSummaryTypeDef",
    {
        "TableClass": NotRequired[TableClassType],
        "LastUpdateDateTime": NotRequired[datetime],
    },
)
RestoreSummaryTypeDef = TypedDict(
    "RestoreSummaryTypeDef",
    {
        "RestoreDateTime": datetime,
        "RestoreInProgress": bool,
        "SourceBackupArn": NotRequired[str],
        "SourceTableArn": NotRequired[str],
    },
)
SSEDescriptionTypeDef = TypedDict(
    "SSEDescriptionTypeDef",
    {
        "Status": NotRequired[SSEStatusType],
        "SSEType": NotRequired[SSETypeType],
        "KMSMasterKeyArn": NotRequired[str],
        "InaccessibleEncryptionDateTime": NotRequired[datetime],
    },
)
TableBatchWriterRequestTypeDef = TypedDict(
    "TableBatchWriterRequestTypeDef",
    {
        "overwrite_by_pkeys": NotRequired[List[str]],
    },
)
TimeToLiveSpecificationTypeDef = TypedDict(
    "TimeToLiveSpecificationTypeDef",
    {
        "Enabled": bool,
        "AttributeName": str,
    },
)
UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)
UpdateContributorInsightsInputRequestTypeDef = TypedDict(
    "UpdateContributorInsightsInputRequestTypeDef",
    {
        "TableName": str,
        "ContributorInsightsAction": ContributorInsightsActionType,
        "IndexName": NotRequired[str],
    },
)
UpdateKinesisStreamingConfigurationTypeDef = TypedDict(
    "UpdateKinesisStreamingConfigurationTypeDef",
    {
        "ApproximateCreationDateTimePrecision": NotRequired[
            ApproximateCreationDateTimePrecisionType
        ],
    },
)
BatchStatementErrorTypeDef = TypedDict(
    "BatchStatementErrorTypeDef",
    {
        "Code": NotRequired[BatchStatementErrorCodeEnumType],
        "Message": NotRequired[str],
        "Item": NotRequired[Dict[str, AttributeValueTypeDef]],
    },
)
DeleteRequestOutputTypeDef = TypedDict(
    "DeleteRequestOutputTypeDef",
    {
        "Key": Dict[str, AttributeValueTypeDef],
    },
)
ItemCollectionMetricsTypeDef = TypedDict(
    "ItemCollectionMetricsTypeDef",
    {
        "ItemCollectionKey": NotRequired[Dict[str, AttributeValueTypeDef]],
        "SizeEstimateRangeGB": NotRequired[List[float]],
    },
)
ItemResponseTypeDef = TypedDict(
    "ItemResponseTypeDef",
    {
        "Item": NotRequired[Dict[str, AttributeValueTypeDef]],
    },
)
KeysAndAttributesOutputTypeDef = TypedDict(
    "KeysAndAttributesOutputTypeDef",
    {
        "Keys": List[Dict[str, AttributeValueTypeDef]],
        "AttributesToGet": NotRequired[List[str]],
        "ConsistentRead": NotRequired[bool],
        "ProjectionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Dict[str, str]],
    },
)
PutRequestOutputTypeDef = TypedDict(
    "PutRequestOutputTypeDef",
    {
        "Item": Dict[str, AttributeValueTypeDef],
    },
)
UniversalAttributeValueTypeDef = Union[
    AttributeValueTypeDef,
    bytes,
    bytearray,
    str,
    int,
    Decimal,
    bool,
    Set[int],
    Set[Decimal],
    Set[str],
    Set[bytes],
    Set[bytearray],
    Sequence[Any],
    Mapping[str, Any],
    None,
]
AttributeValueUpdateTableTypeDef = TypedDict(
    "AttributeValueUpdateTableTypeDef",
    {
        "Value": NotRequired[TableAttributeValueTypeDef],
        "Action": NotRequired[AttributeActionType],
    },
)
ConditionTableTypeDef = TypedDict(
    "ConditionTableTypeDef",
    {
        "ComparisonOperator": ComparisonOperatorType,
        "AttributeValueList": NotRequired[Sequence[TableAttributeValueTypeDef]],
    },
)
DeleteRequestServiceResourceOutputTypeDef = TypedDict(
    "DeleteRequestServiceResourceOutputTypeDef",
    {
        "Key": Dict[str, TableAttributeValueTypeDef],
    },
)
DeleteRequestServiceResourceTypeDef = TypedDict(
    "DeleteRequestServiceResourceTypeDef",
    {
        "Key": Mapping[str, TableAttributeValueTypeDef],
    },
)
ExpectedAttributeValueTableTypeDef = TypedDict(
    "ExpectedAttributeValueTableTypeDef",
    {
        "Value": NotRequired[TableAttributeValueTypeDef],
        "Exists": NotRequired[bool],
        "ComparisonOperator": NotRequired[ComparisonOperatorType],
        "AttributeValueList": NotRequired[Sequence[TableAttributeValueTypeDef]],
    },
)
GetItemInputTableGetItemTypeDef = TypedDict(
    "GetItemInputTableGetItemTypeDef",
    {
        "Key": Mapping[str, TableAttributeValueTypeDef],
        "AttributesToGet": NotRequired[Sequence[str]],
        "ConsistentRead": NotRequired[bool],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ProjectionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
    },
)
ItemCollectionMetricsServiceResourceTypeDef = TypedDict(
    "ItemCollectionMetricsServiceResourceTypeDef",
    {
        "ItemCollectionKey": NotRequired[Dict[str, TableAttributeValueTypeDef]],
        "SizeEstimateRangeGB": NotRequired[List[float]],
    },
)
ItemCollectionMetricsTableTypeDef = TypedDict(
    "ItemCollectionMetricsTableTypeDef",
    {
        "ItemCollectionKey": NotRequired[Dict[str, TableAttributeValueTypeDef]],
        "SizeEstimateRangeGB": NotRequired[List[float]],
    },
)
KeysAndAttributesServiceResourceOutputTypeDef = TypedDict(
    "KeysAndAttributesServiceResourceOutputTypeDef",
    {
        "Keys": List[Dict[str, TableAttributeValueTypeDef]],
        "AttributesToGet": NotRequired[List[str]],
        "ConsistentRead": NotRequired[bool],
        "ProjectionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Dict[str, str]],
    },
)
KeysAndAttributesServiceResourceTypeDef = TypedDict(
    "KeysAndAttributesServiceResourceTypeDef",
    {
        "Keys": Sequence[Mapping[str, TableAttributeValueTypeDef]],
        "AttributesToGet": NotRequired[Sequence[str]],
        "ConsistentRead": NotRequired[bool],
        "ProjectionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
    },
)
PutRequestServiceResourceOutputTypeDef = TypedDict(
    "PutRequestServiceResourceOutputTypeDef",
    {
        "Item": Dict[str, TableAttributeValueTypeDef],
    },
)
PutRequestServiceResourceTypeDef = TypedDict(
    "PutRequestServiceResourceTypeDef",
    {
        "Item": Mapping[str, TableAttributeValueTypeDef],
    },
)
AutoScalingPolicyDescriptionTypeDef = TypedDict(
    "AutoScalingPolicyDescriptionTypeDef",
    {
        "PolicyName": NotRequired[str],
        "TargetTrackingScalingPolicyConfiguration": NotRequired[
            AutoScalingTargetTrackingScalingPolicyConfigurationDescriptionTypeDef
        ],
    },
)
AutoScalingPolicyUpdateTypeDef = TypedDict(
    "AutoScalingPolicyUpdateTypeDef",
    {
        "TargetTrackingScalingPolicyConfiguration": AutoScalingTargetTrackingScalingPolicyConfigurationUpdateTypeDef,
        "PolicyName": NotRequired[str],
    },
)
CreateBackupOutputTypeDef = TypedDict(
    "CreateBackupOutputTypeDef",
    {
        "BackupDetails": BackupDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteResourcePolicyOutputTypeDef = TypedDict(
    "DeleteResourcePolicyOutputTypeDef",
    {
        "RevisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeLimitsOutputTypeDef = TypedDict(
    "DescribeLimitsOutputTypeDef",
    {
        "AccountMaxReadCapacityUnits": int,
        "AccountMaxWriteCapacityUnits": int,
        "TableMaxReadCapacityUnits": int,
        "TableMaxWriteCapacityUnits": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetResourcePolicyOutputTypeDef = TypedDict(
    "GetResourcePolicyOutputTypeDef",
    {
        "Policy": str,
        "RevisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListBackupsOutputTypeDef = TypedDict(
    "ListBackupsOutputTypeDef",
    {
        "BackupSummaries": List[BackupSummaryTypeDef],
        "LastEvaluatedBackupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTablesOutputTypeDef = TypedDict(
    "ListTablesOutputTypeDef",
    {
        "TableNames": List[str],
        "LastEvaluatedTableName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutResourcePolicyOutputTypeDef = TypedDict(
    "PutResourcePolicyOutputTypeDef",
    {
        "RevisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateContributorInsightsOutputTypeDef = TypedDict(
    "UpdateContributorInsightsOutputTypeDef",
    {
        "TableName": str,
        "IndexName": str,
        "ContributorInsightsStatus": ContributorInsightsStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ConsumedCapacityTypeDef = TypedDict(
    "ConsumedCapacityTypeDef",
    {
        "TableName": NotRequired[str],
        "CapacityUnits": NotRequired[float],
        "ReadCapacityUnits": NotRequired[float],
        "WriteCapacityUnits": NotRequired[float],
        "Table": NotRequired[CapacityTypeDef],
        "LocalSecondaryIndexes": NotRequired[Dict[str, CapacityTypeDef]],
        "GlobalSecondaryIndexes": NotRequired[Dict[str, CapacityTypeDef]],
    },
)
ContinuousBackupsDescriptionTypeDef = TypedDict(
    "ContinuousBackupsDescriptionTypeDef",
    {
        "ContinuousBackupsStatus": ContinuousBackupsStatusType,
        "PointInTimeRecoveryDescription": NotRequired[PointInTimeRecoveryDescriptionTypeDef],
    },
)
ListContributorInsightsOutputTypeDef = TypedDict(
    "ListContributorInsightsOutputTypeDef",
    {
        "ContributorInsightsSummaries": List[ContributorInsightsSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
LocalSecondaryIndexTypeDef = TypedDict(
    "LocalSecondaryIndexTypeDef",
    {
        "IndexName": str,
        "KeySchema": Sequence[KeySchemaElementTypeDef],
        "Projection": ProjectionTypeDef,
    },
)
CreateGlobalSecondaryIndexActionTypeDef = TypedDict(
    "CreateGlobalSecondaryIndexActionTypeDef",
    {
        "IndexName": str,
        "KeySchema": Sequence[KeySchemaElementTypeDef],
        "Projection": ProjectionTypeDef,
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
    },
)
GlobalSecondaryIndexTypeDef = TypedDict(
    "GlobalSecondaryIndexTypeDef",
    {
        "IndexName": str,
        "KeySchema": Sequence[KeySchemaElementTypeDef],
        "Projection": ProjectionTypeDef,
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
    },
)
SourceTableDetailsTypeDef = TypedDict(
    "SourceTableDetailsTypeDef",
    {
        "TableName": str,
        "TableId": str,
        "KeySchema": List[KeySchemaElementTypeDef],
        "TableCreationDateTime": datetime,
        "ProvisionedThroughput": ProvisionedThroughputTypeDef,
        "TableArn": NotRequired[str],
        "TableSizeBytes": NotRequired[int],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
        "ItemCount": NotRequired[int],
        "BillingMode": NotRequired[BillingModeType],
    },
)
UpdateGlobalSecondaryIndexActionTypeDef = TypedDict(
    "UpdateGlobalSecondaryIndexActionTypeDef",
    {
        "IndexName": str,
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
    },
)
CreateGlobalTableInputRequestTypeDef = TypedDict(
    "CreateGlobalTableInputRequestTypeDef",
    {
        "GlobalTableName": str,
        "ReplicationGroup": Sequence[ReplicaTypeDef],
    },
)
GlobalTableTypeDef = TypedDict(
    "GlobalTableTypeDef",
    {
        "GlobalTableName": NotRequired[str],
        "ReplicationGroup": NotRequired[List[ReplicaTypeDef]],
    },
)
ReplicaGlobalSecondaryIndexDescriptionTypeDef = TypedDict(
    "ReplicaGlobalSecondaryIndexDescriptionTypeDef",
    {
        "IndexName": NotRequired[str],
        "ProvisionedThroughputOverride": NotRequired[ProvisionedThroughputOverrideTypeDef],
        "OnDemandThroughputOverride": NotRequired[OnDemandThroughputOverrideTypeDef],
    },
)
ReplicaGlobalSecondaryIndexTypeDef = TypedDict(
    "ReplicaGlobalSecondaryIndexTypeDef",
    {
        "IndexName": str,
        "ProvisionedThroughputOverride": NotRequired[ProvisionedThroughputOverrideTypeDef],
        "OnDemandThroughputOverride": NotRequired[OnDemandThroughputOverrideTypeDef],
    },
)
ListTagsOfResourceOutputTypeDef = TypedDict(
    "ListTagsOfResourceOutputTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)
InputFormatOptionsOutputTypeDef = TypedDict(
    "InputFormatOptionsOutputTypeDef",
    {
        "Csv": NotRequired[CsvOptionsOutputTypeDef],
    },
)
InputFormatOptionsTypeDef = TypedDict(
    "InputFormatOptionsTypeDef",
    {
        "Csv": NotRequired[CsvOptionsTypeDef],
    },
)
ReplicaUpdateTypeDef = TypedDict(
    "ReplicaUpdateTypeDef",
    {
        "Create": NotRequired[CreateReplicaActionTypeDef],
        "Delete": NotRequired[DeleteReplicaActionTypeDef],
    },
)
DescribeContributorInsightsOutputTypeDef = TypedDict(
    "DescribeContributorInsightsOutputTypeDef",
    {
        "TableName": str,
        "IndexName": str,
        "ContributorInsightsRuleList": List[str],
        "ContributorInsightsStatus": ContributorInsightsStatusType,
        "LastUpdateDateTime": datetime,
        "FailureException": FailureExceptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeEndpointsResponseTypeDef = TypedDict(
    "DescribeEndpointsResponseTypeDef",
    {
        "Endpoints": List[EndpointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeKinesisStreamingDestinationOutputTypeDef = TypedDict(
    "DescribeKinesisStreamingDestinationOutputTypeDef",
    {
        "TableName": str,
        "KinesisDataStreamDestinations": List[KinesisDataStreamDestinationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeTableInputTableExistsWaitTypeDef = TypedDict(
    "DescribeTableInputTableExistsWaitTypeDef",
    {
        "TableName": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
DescribeTableInputTableNotExistsWaitTypeDef = TypedDict(
    "DescribeTableInputTableNotExistsWaitTypeDef",
    {
        "TableName": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
DescribeTimeToLiveOutputTypeDef = TypedDict(
    "DescribeTimeToLiveOutputTypeDef",
    {
        "TimeToLiveDescription": TimeToLiveDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
KinesisStreamingDestinationInputRequestTypeDef = TypedDict(
    "KinesisStreamingDestinationInputRequestTypeDef",
    {
        "TableName": str,
        "StreamArn": str,
        "EnableKinesisStreamingConfiguration": NotRequired[
            EnableKinesisStreamingConfigurationTypeDef
        ],
    },
)
KinesisStreamingDestinationOutputTypeDef = TypedDict(
    "KinesisStreamingDestinationOutputTypeDef",
    {
        "TableName": str,
        "StreamArn": str,
        "DestinationStatus": DestinationStatusType,
        "EnableKinesisStreamingConfiguration": EnableKinesisStreamingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ExportDescriptionTypeDef = TypedDict(
    "ExportDescriptionTypeDef",
    {
        "ExportArn": NotRequired[str],
        "ExportStatus": NotRequired[ExportStatusType],
        "StartTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
        "ExportManifest": NotRequired[str],
        "TableArn": NotRequired[str],
        "TableId": NotRequired[str],
        "ExportTime": NotRequired[datetime],
        "ClientToken": NotRequired[str],
        "S3Bucket": NotRequired[str],
        "S3BucketOwner": NotRequired[str],
        "S3Prefix": NotRequired[str],
        "S3SseAlgorithm": NotRequired[S3SseAlgorithmType],
        "S3SseKmsKeyId": NotRequired[str],
        "FailureCode": NotRequired[str],
        "FailureMessage": NotRequired[str],
        "ExportFormat": NotRequired[ExportFormatType],
        "BilledSizeBytes": NotRequired[int],
        "ItemCount": NotRequired[int],
        "ExportType": NotRequired[ExportTypeType],
        "IncrementalExportSpecification": NotRequired[IncrementalExportSpecificationOutputTypeDef],
    },
)
ListExportsOutputTypeDef = TypedDict(
    "ListExportsOutputTypeDef",
    {
        "ExportSummaries": List[ExportSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
IncrementalExportSpecificationTypeDef = TypedDict(
    "IncrementalExportSpecificationTypeDef",
    {
        "ExportFromTime": NotRequired[TimestampTypeDef],
        "ExportToTime": NotRequired[TimestampTypeDef],
        "ExportViewType": NotRequired[ExportViewTypeType],
    },
)
ListBackupsInputRequestTypeDef = TypedDict(
    "ListBackupsInputRequestTypeDef",
    {
        "TableName": NotRequired[str],
        "Limit": NotRequired[int],
        "TimeRangeLowerBound": NotRequired[TimestampTypeDef],
        "TimeRangeUpperBound": NotRequired[TimestampTypeDef],
        "ExclusiveStartBackupArn": NotRequired[str],
        "BackupType": NotRequired[BackupTypeFilterType],
    },
)
LocalSecondaryIndexDescriptionTypeDef = TypedDict(
    "LocalSecondaryIndexDescriptionTypeDef",
    {
        "IndexName": NotRequired[str],
        "KeySchema": NotRequired[List[KeySchemaElementTypeDef]],
        "Projection": NotRequired[ProjectionExtraOutputTypeDef],
        "IndexSizeBytes": NotRequired[int],
        "ItemCount": NotRequired[int],
        "IndexArn": NotRequired[str],
    },
)
GlobalSecondaryIndexDescriptionTypeDef = TypedDict(
    "GlobalSecondaryIndexDescriptionTypeDef",
    {
        "IndexName": NotRequired[str],
        "KeySchema": NotRequired[List[KeySchemaElementTypeDef]],
        "Projection": NotRequired[ProjectionExtraOutputTypeDef],
        "IndexStatus": NotRequired[IndexStatusType],
        "Backfilling": NotRequired[bool],
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputDescriptionTypeDef],
        "IndexSizeBytes": NotRequired[int],
        "ItemCount": NotRequired[int],
        "IndexArn": NotRequired[str],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
    },
)
GlobalSecondaryIndexInfoTypeDef = TypedDict(
    "GlobalSecondaryIndexInfoTypeDef",
    {
        "IndexName": NotRequired[str],
        "KeySchema": NotRequired[List[KeySchemaElementTypeDef]],
        "Projection": NotRequired[ProjectionOutputTypeDef],
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
    },
)
GlobalSecondaryIndexOutputTypeDef = TypedDict(
    "GlobalSecondaryIndexOutputTypeDef",
    {
        "IndexName": str,
        "KeySchema": List[KeySchemaElementTypeDef],
        "Projection": ProjectionOutputTypeDef,
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
    },
)
LocalSecondaryIndexInfoTypeDef = TypedDict(
    "LocalSecondaryIndexInfoTypeDef",
    {
        "IndexName": NotRequired[str],
        "KeySchema": NotRequired[List[KeySchemaElementTypeDef]],
        "Projection": NotRequired[ProjectionOutputTypeDef],
    },
)
ImportSummaryTypeDef = TypedDict(
    "ImportSummaryTypeDef",
    {
        "ImportArn": NotRequired[str],
        "ImportStatus": NotRequired[ImportStatusType],
        "TableArn": NotRequired[str],
        "S3BucketSource": NotRequired[S3BucketSourceTypeDef],
        "CloudWatchLogGroupArn": NotRequired[str],
        "InputFormat": NotRequired[InputFormatType],
        "StartTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
    },
)
ListBackupsInputListBackupsPaginateTypeDef = TypedDict(
    "ListBackupsInputListBackupsPaginateTypeDef",
    {
        "TableName": NotRequired[str],
        "TimeRangeLowerBound": NotRequired[TimestampTypeDef],
        "TimeRangeUpperBound": NotRequired[TimestampTypeDef],
        "BackupType": NotRequired[BackupTypeFilterType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTablesInputListTablesPaginateTypeDef = TypedDict(
    "ListTablesInputListTablesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTagsOfResourceInputListTagsOfResourcePaginateTypeDef = TypedDict(
    "ListTagsOfResourceInputListTagsOfResourcePaginateTypeDef",
    {
        "ResourceArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
UpdateContinuousBackupsInputRequestTypeDef = TypedDict(
    "UpdateContinuousBackupsInputRequestTypeDef",
    {
        "TableName": str,
        "PointInTimeRecoverySpecification": PointInTimeRecoverySpecificationTypeDef,
    },
)
UpdateTimeToLiveInputRequestTypeDef = TypedDict(
    "UpdateTimeToLiveInputRequestTypeDef",
    {
        "TableName": str,
        "TimeToLiveSpecification": TimeToLiveSpecificationTypeDef,
    },
)
UpdateTimeToLiveOutputTypeDef = TypedDict(
    "UpdateTimeToLiveOutputTypeDef",
    {
        "TimeToLiveSpecification": TimeToLiveSpecificationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateKinesisStreamingDestinationInputRequestTypeDef = TypedDict(
    "UpdateKinesisStreamingDestinationInputRequestTypeDef",
    {
        "TableName": str,
        "StreamArn": str,
        "UpdateKinesisStreamingConfiguration": NotRequired[
            UpdateKinesisStreamingConfigurationTypeDef
        ],
    },
)
UpdateKinesisStreamingDestinationOutputTypeDef = TypedDict(
    "UpdateKinesisStreamingDestinationOutputTypeDef",
    {
        "TableName": str,
        "StreamArn": str,
        "DestinationStatus": DestinationStatusType,
        "UpdateKinesisStreamingConfiguration": UpdateKinesisStreamingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchStatementResponseTypeDef = TypedDict(
    "BatchStatementResponseTypeDef",
    {
        "Error": NotRequired[BatchStatementErrorTypeDef],
        "TableName": NotRequired[str],
        "Item": NotRequired[Dict[str, AttributeValueTypeDef]],
    },
)
WriteRequestOutputTypeDef = TypedDict(
    "WriteRequestOutputTypeDef",
    {
        "PutRequest": NotRequired[PutRequestOutputTypeDef],
        "DeleteRequest": NotRequired[DeleteRequestOutputTypeDef],
    },
)
AttributeValueUpdateTypeDef = TypedDict(
    "AttributeValueUpdateTypeDef",
    {
        "Value": NotRequired[UniversalAttributeValueTypeDef],
        "Action": NotRequired[AttributeActionType],
    },
)
BatchStatementRequestTypeDef = TypedDict(
    "BatchStatementRequestTypeDef",
    {
        "Statement": str,
        "Parameters": NotRequired[Sequence[UniversalAttributeValueTypeDef]],
        "ConsistentRead": NotRequired[bool],
        "ReturnValuesOnConditionCheckFailure": NotRequired[ReturnValuesOnConditionCheckFailureType],
    },
)
ConditionCheckTypeDef = TypedDict(
    "ConditionCheckTypeDef",
    {
        "Key": Mapping[str, UniversalAttributeValueTypeDef],
        "TableName": str,
        "ConditionExpression": str,
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, UniversalAttributeValueTypeDef]],
        "ReturnValuesOnConditionCheckFailure": NotRequired[ReturnValuesOnConditionCheckFailureType],
    },
)
ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {
        "ComparisonOperator": ComparisonOperatorType,
        "AttributeValueList": NotRequired[Sequence[UniversalAttributeValueTypeDef]],
    },
)
DeleteRequestTypeDef = TypedDict(
    "DeleteRequestTypeDef",
    {
        "Key": Mapping[str, UniversalAttributeValueTypeDef],
    },
)
DeleteTypeDef = TypedDict(
    "DeleteTypeDef",
    {
        "Key": Mapping[str, UniversalAttributeValueTypeDef],
        "TableName": str,
        "ConditionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, UniversalAttributeValueTypeDef]],
        "ReturnValuesOnConditionCheckFailure": NotRequired[ReturnValuesOnConditionCheckFailureType],
    },
)
ExecuteStatementInputRequestTypeDef = TypedDict(
    "ExecuteStatementInputRequestTypeDef",
    {
        "Statement": str,
        "Parameters": NotRequired[Sequence[UniversalAttributeValueTypeDef]],
        "ConsistentRead": NotRequired[bool],
        "NextToken": NotRequired[str],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "Limit": NotRequired[int],
        "ReturnValuesOnConditionCheckFailure": NotRequired[ReturnValuesOnConditionCheckFailureType],
    },
)
ExpectedAttributeValueTypeDef = TypedDict(
    "ExpectedAttributeValueTypeDef",
    {
        "Value": NotRequired[UniversalAttributeValueTypeDef],
        "Exists": NotRequired[bool],
        "ComparisonOperator": NotRequired[ComparisonOperatorType],
        "AttributeValueList": NotRequired[Sequence[UniversalAttributeValueTypeDef]],
    },
)
GetItemInputRequestTypeDef = TypedDict(
    "GetItemInputRequestTypeDef",
    {
        "TableName": str,
        "Key": Mapping[str, UniversalAttributeValueTypeDef],
        "AttributesToGet": NotRequired[Sequence[str]],
        "ConsistentRead": NotRequired[bool],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ProjectionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
    },
)
GetTypeDef = TypedDict(
    "GetTypeDef",
    {
        "Key": Mapping[str, UniversalAttributeValueTypeDef],
        "TableName": str,
        "ProjectionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
    },
)
KeysAndAttributesTypeDef = TypedDict(
    "KeysAndAttributesTypeDef",
    {
        "Keys": Sequence[Mapping[str, UniversalAttributeValueTypeDef]],
        "AttributesToGet": NotRequired[Sequence[str]],
        "ConsistentRead": NotRequired[bool],
        "ProjectionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
    },
)
ParameterizedStatementTypeDef = TypedDict(
    "ParameterizedStatementTypeDef",
    {
        "Statement": str,
        "Parameters": NotRequired[Sequence[UniversalAttributeValueTypeDef]],
        "ReturnValuesOnConditionCheckFailure": NotRequired[ReturnValuesOnConditionCheckFailureType],
    },
)
PutRequestTypeDef = TypedDict(
    "PutRequestTypeDef",
    {
        "Item": Mapping[str, UniversalAttributeValueTypeDef],
    },
)
PutTypeDef = TypedDict(
    "PutTypeDef",
    {
        "Item": Mapping[str, UniversalAttributeValueTypeDef],
        "TableName": str,
        "ConditionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, UniversalAttributeValueTypeDef]],
        "ReturnValuesOnConditionCheckFailure": NotRequired[ReturnValuesOnConditionCheckFailureType],
    },
)
UpdateTypeDef = TypedDict(
    "UpdateTypeDef",
    {
        "Key": Mapping[str, UniversalAttributeValueTypeDef],
        "UpdateExpression": str,
        "TableName": str,
        "ConditionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, UniversalAttributeValueTypeDef]],
        "ReturnValuesOnConditionCheckFailure": NotRequired[ReturnValuesOnConditionCheckFailureType],
    },
)
QueryInputTableQueryTypeDef = TypedDict(
    "QueryInputTableQueryTypeDef",
    {
        "IndexName": NotRequired[str],
        "Select": NotRequired[SelectType],
        "AttributesToGet": NotRequired[Sequence[str]],
        "Limit": NotRequired[int],
        "ConsistentRead": NotRequired[bool],
        "KeyConditions": NotRequired[Mapping[str, ConditionTableTypeDef]],
        "QueryFilter": NotRequired[Mapping[str, ConditionTableTypeDef]],
        "ConditionalOperator": NotRequired[ConditionalOperatorType],
        "ScanIndexForward": NotRequired[bool],
        "ExclusiveStartKey": NotRequired[Mapping[str, TableAttributeValueTypeDef]],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ProjectionExpression": NotRequired[str],
        "FilterExpression": NotRequired[ConditionBaseImportTypeDef],
        "KeyConditionExpression": NotRequired[ConditionBaseImportTypeDef],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, TableAttributeValueTypeDef]],
    },
)
ScanInputTableScanTypeDef = TypedDict(
    "ScanInputTableScanTypeDef",
    {
        "IndexName": NotRequired[str],
        "AttributesToGet": NotRequired[Sequence[str]],
        "Limit": NotRequired[int],
        "Select": NotRequired[SelectType],
        "ScanFilter": NotRequired[Mapping[str, ConditionTableTypeDef]],
        "ConditionalOperator": NotRequired[ConditionalOperatorType],
        "ExclusiveStartKey": NotRequired[Mapping[str, TableAttributeValueTypeDef]],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "TotalSegments": NotRequired[int],
        "Segment": NotRequired[int],
        "ProjectionExpression": NotRequired[str],
        "FilterExpression": NotRequired[ConditionBaseImportTypeDef],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, TableAttributeValueTypeDef]],
        "ConsistentRead": NotRequired[bool],
    },
)
DeleteItemInputTableDeleteItemTypeDef = TypedDict(
    "DeleteItemInputTableDeleteItemTypeDef",
    {
        "Key": Mapping[str, TableAttributeValueTypeDef],
        "Expected": NotRequired[Mapping[str, ExpectedAttributeValueTableTypeDef]],
        "ConditionalOperator": NotRequired[ConditionalOperatorType],
        "ReturnValues": NotRequired[ReturnValueType],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ReturnItemCollectionMetrics": NotRequired[ReturnItemCollectionMetricsType],
        "ConditionExpression": NotRequired[ConditionBaseImportTypeDef],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, TableAttributeValueTypeDef]],
        "ReturnValuesOnConditionCheckFailure": NotRequired[ReturnValuesOnConditionCheckFailureType],
    },
)
PutItemInputTablePutItemTypeDef = TypedDict(
    "PutItemInputTablePutItemTypeDef",
    {
        "Item": Mapping[str, TableAttributeValueTypeDef],
        "Expected": NotRequired[Mapping[str, ExpectedAttributeValueTableTypeDef]],
        "ReturnValues": NotRequired[ReturnValueType],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ReturnItemCollectionMetrics": NotRequired[ReturnItemCollectionMetricsType],
        "ConditionalOperator": NotRequired[ConditionalOperatorType],
        "ConditionExpression": NotRequired[ConditionBaseImportTypeDef],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, TableAttributeValueTypeDef]],
        "ReturnValuesOnConditionCheckFailure": NotRequired[ReturnValuesOnConditionCheckFailureType],
    },
)
UpdateItemInputTableUpdateItemTypeDef = TypedDict(
    "UpdateItemInputTableUpdateItemTypeDef",
    {
        "Key": Mapping[str, TableAttributeValueTypeDef],
        "AttributeUpdates": NotRequired[Mapping[str, AttributeValueUpdateTableTypeDef]],
        "Expected": NotRequired[Mapping[str, ExpectedAttributeValueTableTypeDef]],
        "ConditionalOperator": NotRequired[ConditionalOperatorType],
        "ReturnValues": NotRequired[ReturnValueType],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ReturnItemCollectionMetrics": NotRequired[ReturnItemCollectionMetricsType],
        "UpdateExpression": NotRequired[str],
        "ConditionExpression": NotRequired[ConditionBaseImportTypeDef],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, TableAttributeValueTypeDef]],
        "ReturnValuesOnConditionCheckFailure": NotRequired[ReturnValuesOnConditionCheckFailureType],
    },
)
KeysAndAttributesServiceResourceUnionTypeDef = Union[
    KeysAndAttributesServiceResourceTypeDef, KeysAndAttributesServiceResourceOutputTypeDef
]
WriteRequestServiceResourceOutputTypeDef = TypedDict(
    "WriteRequestServiceResourceOutputTypeDef",
    {
        "PutRequest": NotRequired[PutRequestServiceResourceOutputTypeDef],
        "DeleteRequest": NotRequired[DeleteRequestServiceResourceOutputTypeDef],
    },
)
WriteRequestServiceResourceTypeDef = TypedDict(
    "WriteRequestServiceResourceTypeDef",
    {
        "PutRequest": NotRequired[PutRequestServiceResourceTypeDef],
        "DeleteRequest": NotRequired[DeleteRequestServiceResourceTypeDef],
    },
)
AutoScalingSettingsDescriptionTypeDef = TypedDict(
    "AutoScalingSettingsDescriptionTypeDef",
    {
        "MinimumUnits": NotRequired[int],
        "MaximumUnits": NotRequired[int],
        "AutoScalingDisabled": NotRequired[bool],
        "AutoScalingRoleArn": NotRequired[str],
        "ScalingPolicies": NotRequired[List[AutoScalingPolicyDescriptionTypeDef]],
    },
)
AutoScalingSettingsUpdateTypeDef = TypedDict(
    "AutoScalingSettingsUpdateTypeDef",
    {
        "MinimumUnits": NotRequired[int],
        "MaximumUnits": NotRequired[int],
        "AutoScalingDisabled": NotRequired[bool],
        "AutoScalingRoleArn": NotRequired[str],
        "ScalingPolicyUpdate": NotRequired[AutoScalingPolicyUpdateTypeDef],
    },
)
BatchGetItemOutputServiceResourceTypeDef = TypedDict(
    "BatchGetItemOutputServiceResourceTypeDef",
    {
        "Responses": Dict[str, List[Dict[str, TableAttributeValueTypeDef]]],
        "UnprocessedKeys": Dict[str, KeysAndAttributesServiceResourceOutputTypeDef],
        "ConsumedCapacity": List[ConsumedCapacityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchGetItemOutputTypeDef = TypedDict(
    "BatchGetItemOutputTypeDef",
    {
        "Responses": Dict[str, List[Dict[str, AttributeValueTypeDef]]],
        "UnprocessedKeys": Dict[str, KeysAndAttributesOutputTypeDef],
        "ConsumedCapacity": List[ConsumedCapacityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteItemOutputTableTypeDef = TypedDict(
    "DeleteItemOutputTableTypeDef",
    {
        "Attributes": Dict[str, TableAttributeValueTypeDef],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ItemCollectionMetrics": ItemCollectionMetricsTableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteItemOutputTypeDef = TypedDict(
    "DeleteItemOutputTypeDef",
    {
        "Attributes": Dict[str, AttributeValueTypeDef],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ItemCollectionMetrics": ItemCollectionMetricsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ExecuteStatementOutputTypeDef = TypedDict(
    "ExecuteStatementOutputTypeDef",
    {
        "Items": List[Dict[str, AttributeValueTypeDef]],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "LastEvaluatedKey": Dict[str, AttributeValueTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ExecuteTransactionOutputTypeDef = TypedDict(
    "ExecuteTransactionOutputTypeDef",
    {
        "Responses": List[ItemResponseTypeDef],
        "ConsumedCapacity": List[ConsumedCapacityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetItemOutputTableTypeDef = TypedDict(
    "GetItemOutputTableTypeDef",
    {
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
        "Item": NotRequired[Dict[str, TableAttributeValueTypeDef]],
    },
)
GetItemOutputTypeDef = TypedDict(
    "GetItemOutputTypeDef",
    {
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
        "Item": NotRequired[Dict[str, AttributeValueTypeDef]],
    },
)
PutItemOutputTableTypeDef = TypedDict(
    "PutItemOutputTableTypeDef",
    {
        "Attributes": Dict[str, TableAttributeValueTypeDef],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ItemCollectionMetrics": ItemCollectionMetricsTableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutItemOutputTypeDef = TypedDict(
    "PutItemOutputTypeDef",
    {
        "Attributes": Dict[str, AttributeValueTypeDef],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ItemCollectionMetrics": ItemCollectionMetricsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
QueryOutputTableTypeDef = TypedDict(
    "QueryOutputTableTypeDef",
    {
        "Items": List[Dict[str, TableAttributeValueTypeDef]],
        "Count": int,
        "ScannedCount": int,
        "LastEvaluatedKey": Dict[str, TableAttributeValueTypeDef],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
QueryOutputTypeDef = TypedDict(
    "QueryOutputTypeDef",
    {
        "Items": List[Dict[str, AttributeValueTypeDef]],
        "Count": int,
        "ScannedCount": int,
        "LastEvaluatedKey": Dict[str, AttributeValueTypeDef],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ScanOutputTableTypeDef = TypedDict(
    "ScanOutputTableTypeDef",
    {
        "Items": List[Dict[str, TableAttributeValueTypeDef]],
        "Count": int,
        "ScannedCount": int,
        "LastEvaluatedKey": Dict[str, TableAttributeValueTypeDef],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ScanOutputTypeDef = TypedDict(
    "ScanOutputTypeDef",
    {
        "Items": List[Dict[str, AttributeValueTypeDef]],
        "Count": int,
        "ScannedCount": int,
        "LastEvaluatedKey": Dict[str, AttributeValueTypeDef],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
TransactGetItemsOutputTypeDef = TypedDict(
    "TransactGetItemsOutputTypeDef",
    {
        "ConsumedCapacity": List[ConsumedCapacityTypeDef],
        "Responses": List[ItemResponseTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
TransactWriteItemsOutputTypeDef = TypedDict(
    "TransactWriteItemsOutputTypeDef",
    {
        "ConsumedCapacity": List[ConsumedCapacityTypeDef],
        "ItemCollectionMetrics": Dict[str, List[ItemCollectionMetricsTypeDef]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateItemOutputTableTypeDef = TypedDict(
    "UpdateItemOutputTableTypeDef",
    {
        "Attributes": Dict[str, TableAttributeValueTypeDef],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ItemCollectionMetrics": ItemCollectionMetricsTableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateItemOutputTypeDef = TypedDict(
    "UpdateItemOutputTypeDef",
    {
        "Attributes": Dict[str, AttributeValueTypeDef],
        "ConsumedCapacity": ConsumedCapacityTypeDef,
        "ItemCollectionMetrics": ItemCollectionMetricsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeContinuousBackupsOutputTypeDef = TypedDict(
    "DescribeContinuousBackupsOutputTypeDef",
    {
        "ContinuousBackupsDescription": ContinuousBackupsDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateContinuousBackupsOutputTypeDef = TypedDict(
    "UpdateContinuousBackupsOutputTypeDef",
    {
        "ContinuousBackupsDescription": ContinuousBackupsDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
TableCreationParametersTypeDef = TypedDict(
    "TableCreationParametersTypeDef",
    {
        "TableName": str,
        "AttributeDefinitions": Sequence[AttributeDefinitionTypeDef],
        "KeySchema": Sequence[KeySchemaElementTypeDef],
        "BillingMode": NotRequired[BillingModeType],
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
        "SSESpecification": NotRequired[SSESpecificationTypeDef],
        "GlobalSecondaryIndexes": NotRequired[Sequence[GlobalSecondaryIndexTypeDef]],
    },
)
GlobalSecondaryIndexUpdateTypeDef = TypedDict(
    "GlobalSecondaryIndexUpdateTypeDef",
    {
        "Update": NotRequired[UpdateGlobalSecondaryIndexActionTypeDef],
        "Create": NotRequired[CreateGlobalSecondaryIndexActionTypeDef],
        "Delete": NotRequired[DeleteGlobalSecondaryIndexActionTypeDef],
    },
)
ListGlobalTablesOutputTypeDef = TypedDict(
    "ListGlobalTablesOutputTypeDef",
    {
        "GlobalTables": List[GlobalTableTypeDef],
        "LastEvaluatedGlobalTableName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ReplicaDescriptionTypeDef = TypedDict(
    "ReplicaDescriptionTypeDef",
    {
        "RegionName": NotRequired[str],
        "ReplicaStatus": NotRequired[ReplicaStatusType],
        "ReplicaStatusDescription": NotRequired[str],
        "ReplicaStatusPercentProgress": NotRequired[str],
        "KMSMasterKeyId": NotRequired[str],
        "ProvisionedThroughputOverride": NotRequired[ProvisionedThroughputOverrideTypeDef],
        "OnDemandThroughputOverride": NotRequired[OnDemandThroughputOverrideTypeDef],
        "GlobalSecondaryIndexes": NotRequired[List[ReplicaGlobalSecondaryIndexDescriptionTypeDef]],
        "ReplicaInaccessibleDateTime": NotRequired[datetime],
        "ReplicaTableClassSummary": NotRequired[TableClassSummaryTypeDef],
    },
)
CreateReplicationGroupMemberActionTypeDef = TypedDict(
    "CreateReplicationGroupMemberActionTypeDef",
    {
        "RegionName": str,
        "KMSMasterKeyId": NotRequired[str],
        "ProvisionedThroughputOverride": NotRequired[ProvisionedThroughputOverrideTypeDef],
        "OnDemandThroughputOverride": NotRequired[OnDemandThroughputOverrideTypeDef],
        "GlobalSecondaryIndexes": NotRequired[Sequence[ReplicaGlobalSecondaryIndexTypeDef]],
        "TableClassOverride": NotRequired[TableClassType],
    },
)
UpdateReplicationGroupMemberActionTypeDef = TypedDict(
    "UpdateReplicationGroupMemberActionTypeDef",
    {
        "RegionName": str,
        "KMSMasterKeyId": NotRequired[str],
        "ProvisionedThroughputOverride": NotRequired[ProvisionedThroughputOverrideTypeDef],
        "OnDemandThroughputOverride": NotRequired[OnDemandThroughputOverrideTypeDef],
        "GlobalSecondaryIndexes": NotRequired[Sequence[ReplicaGlobalSecondaryIndexTypeDef]],
        "TableClassOverride": NotRequired[TableClassType],
    },
)
InputFormatOptionsUnionTypeDef = Union[InputFormatOptionsTypeDef, InputFormatOptionsOutputTypeDef]
UpdateGlobalTableInputRequestTypeDef = TypedDict(
    "UpdateGlobalTableInputRequestTypeDef",
    {
        "GlobalTableName": str,
        "ReplicaUpdates": Sequence[ReplicaUpdateTypeDef],
    },
)
DescribeExportOutputTypeDef = TypedDict(
    "DescribeExportOutputTypeDef",
    {
        "ExportDescription": ExportDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ExportTableToPointInTimeOutputTypeDef = TypedDict(
    "ExportTableToPointInTimeOutputTypeDef",
    {
        "ExportDescription": ExportDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ExportTableToPointInTimeInputRequestTypeDef = TypedDict(
    "ExportTableToPointInTimeInputRequestTypeDef",
    {
        "TableArn": str,
        "S3Bucket": str,
        "ExportTime": NotRequired[TimestampTypeDef],
        "ClientToken": NotRequired[str],
        "S3BucketOwner": NotRequired[str],
        "S3Prefix": NotRequired[str],
        "S3SseAlgorithm": NotRequired[S3SseAlgorithmType],
        "S3SseKmsKeyId": NotRequired[str],
        "ExportFormat": NotRequired[ExportFormatType],
        "ExportType": NotRequired[ExportTypeType],
        "IncrementalExportSpecification": NotRequired[IncrementalExportSpecificationTypeDef],
    },
)
IncrementalExportSpecificationUnionTypeDef = Union[
    IncrementalExportSpecificationTypeDef, IncrementalExportSpecificationOutputTypeDef
]
GlobalSecondaryIndexUnionTypeDef = Union[
    GlobalSecondaryIndexTypeDef, GlobalSecondaryIndexOutputTypeDef
]
TableCreationParametersOutputTypeDef = TypedDict(
    "TableCreationParametersOutputTypeDef",
    {
        "TableName": str,
        "AttributeDefinitions": List[AttributeDefinitionTypeDef],
        "KeySchema": List[KeySchemaElementTypeDef],
        "BillingMode": NotRequired[BillingModeType],
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
        "SSESpecification": NotRequired[SSESpecificationTypeDef],
        "GlobalSecondaryIndexes": NotRequired[List[GlobalSecondaryIndexOutputTypeDef]],
    },
)
SourceTableFeatureDetailsTypeDef = TypedDict(
    "SourceTableFeatureDetailsTypeDef",
    {
        "LocalSecondaryIndexes": NotRequired[List[LocalSecondaryIndexInfoTypeDef]],
        "GlobalSecondaryIndexes": NotRequired[List[GlobalSecondaryIndexInfoTypeDef]],
        "StreamDescription": NotRequired[StreamSpecificationTypeDef],
        "TimeToLiveDescription": NotRequired[TimeToLiveDescriptionTypeDef],
        "SSEDescription": NotRequired[SSEDescriptionTypeDef],
    },
)
ListImportsOutputTypeDef = TypedDict(
    "ListImportsOutputTypeDef",
    {
        "ImportSummaryList": List[ImportSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
BatchExecuteStatementOutputTypeDef = TypedDict(
    "BatchExecuteStatementOutputTypeDef",
    {
        "Responses": List[BatchStatementResponseTypeDef],
        "ConsumedCapacity": List[ConsumedCapacityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchWriteItemOutputTypeDef = TypedDict(
    "BatchWriteItemOutputTypeDef",
    {
        "UnprocessedItems": Dict[str, List[WriteRequestOutputTypeDef]],
        "ItemCollectionMetrics": Dict[str, List[ItemCollectionMetricsTypeDef]],
        "ConsumedCapacity": List[ConsumedCapacityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchExecuteStatementInputRequestTypeDef = TypedDict(
    "BatchExecuteStatementInputRequestTypeDef",
    {
        "Statements": Sequence[BatchStatementRequestTypeDef],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
    },
)
QueryInputQueryPaginateTypeDef = TypedDict(
    "QueryInputQueryPaginateTypeDef",
    {
        "TableName": str,
        "IndexName": NotRequired[str],
        "Select": NotRequired[SelectType],
        "AttributesToGet": NotRequired[Sequence[str]],
        "ConsistentRead": NotRequired[bool],
        "KeyConditions": NotRequired[Mapping[str, ConditionTypeDef]],
        "QueryFilter": NotRequired[Mapping[str, ConditionTypeDef]],
        "ConditionalOperator": NotRequired[ConditionalOperatorType],
        "ScanIndexForward": NotRequired[bool],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ProjectionExpression": NotRequired[str],
        "FilterExpression": NotRequired[str],
        "KeyConditionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, UniversalAttributeValueTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
QueryInputRequestTypeDef = TypedDict(
    "QueryInputRequestTypeDef",
    {
        "TableName": str,
        "IndexName": NotRequired[str],
        "Select": NotRequired[SelectType],
        "AttributesToGet": NotRequired[Sequence[str]],
        "Limit": NotRequired[int],
        "ConsistentRead": NotRequired[bool],
        "KeyConditions": NotRequired[Mapping[str, ConditionTypeDef]],
        "QueryFilter": NotRequired[Mapping[str, ConditionTypeDef]],
        "ConditionalOperator": NotRequired[ConditionalOperatorType],
        "ScanIndexForward": NotRequired[bool],
        "ExclusiveStartKey": NotRequired[Mapping[str, UniversalAttributeValueTypeDef]],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ProjectionExpression": NotRequired[str],
        "FilterExpression": NotRequired[str],
        "KeyConditionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, UniversalAttributeValueTypeDef]],
    },
)
ScanInputRequestTypeDef = TypedDict(
    "ScanInputRequestTypeDef",
    {
        "TableName": str,
        "IndexName": NotRequired[str],
        "AttributesToGet": NotRequired[Sequence[str]],
        "Limit": NotRequired[int],
        "Select": NotRequired[SelectType],
        "ScanFilter": NotRequired[Mapping[str, ConditionTypeDef]],
        "ConditionalOperator": NotRequired[ConditionalOperatorType],
        "ExclusiveStartKey": NotRequired[Mapping[str, UniversalAttributeValueTypeDef]],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "TotalSegments": NotRequired[int],
        "Segment": NotRequired[int],
        "ProjectionExpression": NotRequired[str],
        "FilterExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, UniversalAttributeValueTypeDef]],
        "ConsistentRead": NotRequired[bool],
    },
)
ScanInputScanPaginateTypeDef = TypedDict(
    "ScanInputScanPaginateTypeDef",
    {
        "TableName": str,
        "IndexName": NotRequired[str],
        "AttributesToGet": NotRequired[Sequence[str]],
        "Select": NotRequired[SelectType],
        "ScanFilter": NotRequired[Mapping[str, ConditionTypeDef]],
        "ConditionalOperator": NotRequired[ConditionalOperatorType],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "TotalSegments": NotRequired[int],
        "Segment": NotRequired[int],
        "ProjectionExpression": NotRequired[str],
        "FilterExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, UniversalAttributeValueTypeDef]],
        "ConsistentRead": NotRequired[bool],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
DeleteItemInputRequestTypeDef = TypedDict(
    "DeleteItemInputRequestTypeDef",
    {
        "TableName": str,
        "Key": Mapping[str, UniversalAttributeValueTypeDef],
        "Expected": NotRequired[Mapping[str, ExpectedAttributeValueTypeDef]],
        "ConditionalOperator": NotRequired[ConditionalOperatorType],
        "ReturnValues": NotRequired[ReturnValueType],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ReturnItemCollectionMetrics": NotRequired[ReturnItemCollectionMetricsType],
        "ConditionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, UniversalAttributeValueTypeDef]],
        "ReturnValuesOnConditionCheckFailure": NotRequired[ReturnValuesOnConditionCheckFailureType],
    },
)
PutItemInputRequestTypeDef = TypedDict(
    "PutItemInputRequestTypeDef",
    {
        "TableName": str,
        "Item": Mapping[str, UniversalAttributeValueTypeDef],
        "Expected": NotRequired[Mapping[str, ExpectedAttributeValueTypeDef]],
        "ReturnValues": NotRequired[ReturnValueType],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ReturnItemCollectionMetrics": NotRequired[ReturnItemCollectionMetricsType],
        "ConditionalOperator": NotRequired[ConditionalOperatorType],
        "ConditionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, UniversalAttributeValueTypeDef]],
        "ReturnValuesOnConditionCheckFailure": NotRequired[ReturnValuesOnConditionCheckFailureType],
    },
)
UpdateItemInputRequestTypeDef = TypedDict(
    "UpdateItemInputRequestTypeDef",
    {
        "TableName": str,
        "Key": Mapping[str, UniversalAttributeValueTypeDef],
        "AttributeUpdates": NotRequired[Mapping[str, AttributeValueUpdateTypeDef]],
        "Expected": NotRequired[Mapping[str, ExpectedAttributeValueTypeDef]],
        "ConditionalOperator": NotRequired[ConditionalOperatorType],
        "ReturnValues": NotRequired[ReturnValueType],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ReturnItemCollectionMetrics": NotRequired[ReturnItemCollectionMetricsType],
        "UpdateExpression": NotRequired[str],
        "ConditionExpression": NotRequired[str],
        "ExpressionAttributeNames": NotRequired[Mapping[str, str]],
        "ExpressionAttributeValues": NotRequired[Mapping[str, UniversalAttributeValueTypeDef]],
        "ReturnValuesOnConditionCheckFailure": NotRequired[ReturnValuesOnConditionCheckFailureType],
    },
)
TransactGetItemTypeDef = TypedDict(
    "TransactGetItemTypeDef",
    {
        "Get": GetTypeDef,
    },
)
KeysAndAttributesUnionTypeDef = Union[KeysAndAttributesTypeDef, KeysAndAttributesOutputTypeDef]
ExecuteTransactionInputRequestTypeDef = TypedDict(
    "ExecuteTransactionInputRequestTypeDef",
    {
        "TransactStatements": Sequence[ParameterizedStatementTypeDef],
        "ClientRequestToken": NotRequired[str],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
    },
)
WriteRequestTypeDef = TypedDict(
    "WriteRequestTypeDef",
    {
        "PutRequest": NotRequired[PutRequestTypeDef],
        "DeleteRequest": NotRequired[DeleteRequestTypeDef],
    },
)
TransactWriteItemTypeDef = TypedDict(
    "TransactWriteItemTypeDef",
    {
        "ConditionCheck": NotRequired[ConditionCheckTypeDef],
        "Put": NotRequired[PutTypeDef],
        "Delete": NotRequired[DeleteTypeDef],
        "Update": NotRequired[UpdateTypeDef],
    },
)
BatchGetItemInputServiceResourceBatchGetItemTypeDef = TypedDict(
    "BatchGetItemInputServiceResourceBatchGetItemTypeDef",
    {
        "RequestItems": Mapping[str, KeysAndAttributesServiceResourceUnionTypeDef],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
    },
)
BatchWriteItemOutputServiceResourceTypeDef = TypedDict(
    "BatchWriteItemOutputServiceResourceTypeDef",
    {
        "UnprocessedItems": Dict[str, List[WriteRequestServiceResourceOutputTypeDef]],
        "ItemCollectionMetrics": Dict[str, List[ItemCollectionMetricsServiceResourceTypeDef]],
        "ConsumedCapacity": List[ConsumedCapacityTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
WriteRequestServiceResourceUnionTypeDef = Union[
    WriteRequestServiceResourceTypeDef, WriteRequestServiceResourceOutputTypeDef
]
ReplicaGlobalSecondaryIndexAutoScalingDescriptionTypeDef = TypedDict(
    "ReplicaGlobalSecondaryIndexAutoScalingDescriptionTypeDef",
    {
        "IndexName": NotRequired[str],
        "IndexStatus": NotRequired[IndexStatusType],
        "ProvisionedReadCapacityAutoScalingSettings": NotRequired[
            AutoScalingSettingsDescriptionTypeDef
        ],
        "ProvisionedWriteCapacityAutoScalingSettings": NotRequired[
            AutoScalingSettingsDescriptionTypeDef
        ],
    },
)
ReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef = TypedDict(
    "ReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef",
    {
        "IndexName": str,
        "IndexStatus": NotRequired[IndexStatusType],
        "ProvisionedReadCapacityUnits": NotRequired[int],
        "ProvisionedReadCapacityAutoScalingSettings": NotRequired[
            AutoScalingSettingsDescriptionTypeDef
        ],
        "ProvisionedWriteCapacityUnits": NotRequired[int],
        "ProvisionedWriteCapacityAutoScalingSettings": NotRequired[
            AutoScalingSettingsDescriptionTypeDef
        ],
    },
)
GlobalSecondaryIndexAutoScalingUpdateTypeDef = TypedDict(
    "GlobalSecondaryIndexAutoScalingUpdateTypeDef",
    {
        "IndexName": NotRequired[str],
        "ProvisionedWriteCapacityAutoScalingUpdate": NotRequired[AutoScalingSettingsUpdateTypeDef],
    },
)
GlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef = TypedDict(
    "GlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef",
    {
        "IndexName": str,
        "ProvisionedWriteCapacityUnits": NotRequired[int],
        "ProvisionedWriteCapacityAutoScalingSettingsUpdate": NotRequired[
            AutoScalingSettingsUpdateTypeDef
        ],
    },
)
ReplicaGlobalSecondaryIndexAutoScalingUpdateTypeDef = TypedDict(
    "ReplicaGlobalSecondaryIndexAutoScalingUpdateTypeDef",
    {
        "IndexName": NotRequired[str],
        "ProvisionedReadCapacityAutoScalingUpdate": NotRequired[AutoScalingSettingsUpdateTypeDef],
    },
)
ReplicaGlobalSecondaryIndexSettingsUpdateTypeDef = TypedDict(
    "ReplicaGlobalSecondaryIndexSettingsUpdateTypeDef",
    {
        "IndexName": str,
        "ProvisionedReadCapacityUnits": NotRequired[int],
        "ProvisionedReadCapacityAutoScalingSettingsUpdate": NotRequired[
            AutoScalingSettingsUpdateTypeDef
        ],
    },
)
ImportTableInputRequestTypeDef = TypedDict(
    "ImportTableInputRequestTypeDef",
    {
        "S3BucketSource": S3BucketSourceTypeDef,
        "InputFormat": InputFormatType,
        "TableCreationParameters": TableCreationParametersTypeDef,
        "ClientToken": NotRequired[str],
        "InputFormatOptions": NotRequired[InputFormatOptionsTypeDef],
        "InputCompressionType": NotRequired[InputCompressionTypeType],
    },
)
GlobalTableDescriptionTypeDef = TypedDict(
    "GlobalTableDescriptionTypeDef",
    {
        "ReplicationGroup": NotRequired[List[ReplicaDescriptionTypeDef]],
        "GlobalTableArn": NotRequired[str],
        "CreationDateTime": NotRequired[datetime],
        "GlobalTableStatus": NotRequired[GlobalTableStatusType],
        "GlobalTableName": NotRequired[str],
    },
)
TableDescriptionTypeDef = TypedDict(
    "TableDescriptionTypeDef",
    {
        "AttributeDefinitions": NotRequired[List[AttributeDefinitionTypeDef]],
        "TableName": NotRequired[str],
        "KeySchema": NotRequired[List[KeySchemaElementTypeDef]],
        "TableStatus": NotRequired[TableStatusType],
        "CreationDateTime": NotRequired[datetime],
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputDescriptionTypeDef],
        "TableSizeBytes": NotRequired[int],
        "ItemCount": NotRequired[int],
        "TableArn": NotRequired[str],
        "TableId": NotRequired[str],
        "BillingModeSummary": NotRequired[BillingModeSummaryTypeDef],
        "LocalSecondaryIndexes": NotRequired[List[LocalSecondaryIndexDescriptionTypeDef]],
        "GlobalSecondaryIndexes": NotRequired[List[GlobalSecondaryIndexDescriptionTypeDef]],
        "StreamSpecification": NotRequired[StreamSpecificationTypeDef],
        "LatestStreamLabel": NotRequired[str],
        "LatestStreamArn": NotRequired[str],
        "GlobalTableVersion": NotRequired[str],
        "Replicas": NotRequired[List[ReplicaDescriptionTypeDef]],
        "RestoreSummary": NotRequired[RestoreSummaryTypeDef],
        "SSEDescription": NotRequired[SSEDescriptionTypeDef],
        "ArchivalSummary": NotRequired[ArchivalSummaryTypeDef],
        "TableClassSummary": NotRequired[TableClassSummaryTypeDef],
        "DeletionProtectionEnabled": NotRequired[bool],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
    },
)
ReplicationGroupUpdateTypeDef = TypedDict(
    "ReplicationGroupUpdateTypeDef",
    {
        "Create": NotRequired[CreateReplicationGroupMemberActionTypeDef],
        "Update": NotRequired[UpdateReplicationGroupMemberActionTypeDef],
        "Delete": NotRequired[DeleteReplicationGroupMemberActionTypeDef],
    },
)
CreateTableInputRequestTypeDef = TypedDict(
    "CreateTableInputRequestTypeDef",
    {
        "AttributeDefinitions": Sequence[AttributeDefinitionTypeDef],
        "TableName": str,
        "KeySchema": Sequence[KeySchemaElementTypeDef],
        "LocalSecondaryIndexes": NotRequired[Sequence[LocalSecondaryIndexTypeDef]],
        "GlobalSecondaryIndexes": NotRequired[Sequence[GlobalSecondaryIndexUnionTypeDef]],
        "BillingMode": NotRequired[BillingModeType],
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "StreamSpecification": NotRequired[StreamSpecificationTypeDef],
        "SSESpecification": NotRequired[SSESpecificationTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "TableClass": NotRequired[TableClassType],
        "DeletionProtectionEnabled": NotRequired[bool],
        "ResourcePolicy": NotRequired[str],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
    },
)
CreateTableInputServiceResourceCreateTableTypeDef = TypedDict(
    "CreateTableInputServiceResourceCreateTableTypeDef",
    {
        "AttributeDefinitions": Sequence[AttributeDefinitionTypeDef],
        "TableName": str,
        "KeySchema": Sequence[KeySchemaElementTypeDef],
        "LocalSecondaryIndexes": NotRequired[Sequence[LocalSecondaryIndexTypeDef]],
        "GlobalSecondaryIndexes": NotRequired[Sequence[GlobalSecondaryIndexUnionTypeDef]],
        "BillingMode": NotRequired[BillingModeType],
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "StreamSpecification": NotRequired[StreamSpecificationTypeDef],
        "SSESpecification": NotRequired[SSESpecificationTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "TableClass": NotRequired[TableClassType],
        "DeletionProtectionEnabled": NotRequired[bool],
        "ResourcePolicy": NotRequired[str],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
    },
)
RestoreTableFromBackupInputRequestTypeDef = TypedDict(
    "RestoreTableFromBackupInputRequestTypeDef",
    {
        "TargetTableName": str,
        "BackupArn": str,
        "BillingModeOverride": NotRequired[BillingModeType],
        "GlobalSecondaryIndexOverride": NotRequired[Sequence[GlobalSecondaryIndexUnionTypeDef]],
        "LocalSecondaryIndexOverride": NotRequired[Sequence[LocalSecondaryIndexTypeDef]],
        "ProvisionedThroughputOverride": NotRequired[ProvisionedThroughputTypeDef],
        "OnDemandThroughputOverride": NotRequired[OnDemandThroughputTypeDef],
        "SSESpecificationOverride": NotRequired[SSESpecificationTypeDef],
    },
)
RestoreTableToPointInTimeInputRequestTypeDef = TypedDict(
    "RestoreTableToPointInTimeInputRequestTypeDef",
    {
        "TargetTableName": str,
        "SourceTableArn": NotRequired[str],
        "SourceTableName": NotRequired[str],
        "UseLatestRestorableTime": NotRequired[bool],
        "RestoreDateTime": NotRequired[TimestampTypeDef],
        "BillingModeOverride": NotRequired[BillingModeType],
        "GlobalSecondaryIndexOverride": NotRequired[Sequence[GlobalSecondaryIndexUnionTypeDef]],
        "LocalSecondaryIndexOverride": NotRequired[Sequence[LocalSecondaryIndexTypeDef]],
        "ProvisionedThroughputOverride": NotRequired[ProvisionedThroughputTypeDef],
        "OnDemandThroughputOverride": NotRequired[OnDemandThroughputTypeDef],
        "SSESpecificationOverride": NotRequired[SSESpecificationTypeDef],
    },
)
ImportTableDescriptionTypeDef = TypedDict(
    "ImportTableDescriptionTypeDef",
    {
        "ImportArn": NotRequired[str],
        "ImportStatus": NotRequired[ImportStatusType],
        "TableArn": NotRequired[str],
        "TableId": NotRequired[str],
        "ClientToken": NotRequired[str],
        "S3BucketSource": NotRequired[S3BucketSourceTypeDef],
        "ErrorCount": NotRequired[int],
        "CloudWatchLogGroupArn": NotRequired[str],
        "InputFormat": NotRequired[InputFormatType],
        "InputFormatOptions": NotRequired[InputFormatOptionsOutputTypeDef],
        "InputCompressionType": NotRequired[InputCompressionTypeType],
        "TableCreationParameters": NotRequired[TableCreationParametersOutputTypeDef],
        "StartTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
        "ProcessedSizeBytes": NotRequired[int],
        "ProcessedItemCount": NotRequired[int],
        "ImportedItemCount": NotRequired[int],
        "FailureCode": NotRequired[str],
        "FailureMessage": NotRequired[str],
    },
)
TableCreationParametersUnionTypeDef = Union[
    TableCreationParametersTypeDef, TableCreationParametersOutputTypeDef
]
BackupDescriptionTypeDef = TypedDict(
    "BackupDescriptionTypeDef",
    {
        "BackupDetails": NotRequired[BackupDetailsTypeDef],
        "SourceTableDetails": NotRequired[SourceTableDetailsTypeDef],
        "SourceTableFeatureDetails": NotRequired[SourceTableFeatureDetailsTypeDef],
    },
)
TransactGetItemsInputRequestTypeDef = TypedDict(
    "TransactGetItemsInputRequestTypeDef",
    {
        "TransactItems": Sequence[TransactGetItemTypeDef],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
    },
)
BatchGetItemInputRequestTypeDef = TypedDict(
    "BatchGetItemInputRequestTypeDef",
    {
        "RequestItems": Mapping[str, KeysAndAttributesUnionTypeDef],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
    },
)
WriteRequestUnionTypeDef = Union[WriteRequestTypeDef, WriteRequestOutputTypeDef]
TransactWriteItemsInputRequestTypeDef = TypedDict(
    "TransactWriteItemsInputRequestTypeDef",
    {
        "TransactItems": Sequence[TransactWriteItemTypeDef],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ReturnItemCollectionMetrics": NotRequired[ReturnItemCollectionMetricsType],
        "ClientRequestToken": NotRequired[str],
    },
)
BatchWriteItemInputServiceResourceBatchWriteItemTypeDef = TypedDict(
    "BatchWriteItemInputServiceResourceBatchWriteItemTypeDef",
    {
        "RequestItems": Mapping[str, Sequence[WriteRequestServiceResourceUnionTypeDef]],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ReturnItemCollectionMetrics": NotRequired[ReturnItemCollectionMetricsType],
    },
)
ReplicaAutoScalingDescriptionTypeDef = TypedDict(
    "ReplicaAutoScalingDescriptionTypeDef",
    {
        "RegionName": NotRequired[str],
        "GlobalSecondaryIndexes": NotRequired[
            List[ReplicaGlobalSecondaryIndexAutoScalingDescriptionTypeDef]
        ],
        "ReplicaProvisionedReadCapacityAutoScalingSettings": NotRequired[
            AutoScalingSettingsDescriptionTypeDef
        ],
        "ReplicaProvisionedWriteCapacityAutoScalingSettings": NotRequired[
            AutoScalingSettingsDescriptionTypeDef
        ],
        "ReplicaStatus": NotRequired[ReplicaStatusType],
    },
)
ReplicaSettingsDescriptionTypeDef = TypedDict(
    "ReplicaSettingsDescriptionTypeDef",
    {
        "RegionName": str,
        "ReplicaStatus": NotRequired[ReplicaStatusType],
        "ReplicaBillingModeSummary": NotRequired[BillingModeSummaryTypeDef],
        "ReplicaProvisionedReadCapacityUnits": NotRequired[int],
        "ReplicaProvisionedReadCapacityAutoScalingSettings": NotRequired[
            AutoScalingSettingsDescriptionTypeDef
        ],
        "ReplicaProvisionedWriteCapacityUnits": NotRequired[int],
        "ReplicaProvisionedWriteCapacityAutoScalingSettings": NotRequired[
            AutoScalingSettingsDescriptionTypeDef
        ],
        "ReplicaGlobalSecondaryIndexSettings": NotRequired[
            List[ReplicaGlobalSecondaryIndexSettingsDescriptionTypeDef]
        ],
        "ReplicaTableClassSummary": NotRequired[TableClassSummaryTypeDef],
    },
)
ReplicaAutoScalingUpdateTypeDef = TypedDict(
    "ReplicaAutoScalingUpdateTypeDef",
    {
        "RegionName": str,
        "ReplicaGlobalSecondaryIndexUpdates": NotRequired[
            Sequence[ReplicaGlobalSecondaryIndexAutoScalingUpdateTypeDef]
        ],
        "ReplicaProvisionedReadCapacityAutoScalingUpdate": NotRequired[
            AutoScalingSettingsUpdateTypeDef
        ],
    },
)
ReplicaSettingsUpdateTypeDef = TypedDict(
    "ReplicaSettingsUpdateTypeDef",
    {
        "RegionName": str,
        "ReplicaProvisionedReadCapacityUnits": NotRequired[int],
        "ReplicaProvisionedReadCapacityAutoScalingSettingsUpdate": NotRequired[
            AutoScalingSettingsUpdateTypeDef
        ],
        "ReplicaGlobalSecondaryIndexSettingsUpdate": NotRequired[
            Sequence[ReplicaGlobalSecondaryIndexSettingsUpdateTypeDef]
        ],
        "ReplicaTableClass": NotRequired[TableClassType],
    },
)
CreateGlobalTableOutputTypeDef = TypedDict(
    "CreateGlobalTableOutputTypeDef",
    {
        "GlobalTableDescription": GlobalTableDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeGlobalTableOutputTypeDef = TypedDict(
    "DescribeGlobalTableOutputTypeDef",
    {
        "GlobalTableDescription": GlobalTableDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateGlobalTableOutputTypeDef = TypedDict(
    "UpdateGlobalTableOutputTypeDef",
    {
        "GlobalTableDescription": GlobalTableDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateTableOutputTypeDef = TypedDict(
    "CreateTableOutputTypeDef",
    {
        "TableDescription": TableDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteTableOutputTypeDef = TypedDict(
    "DeleteTableOutputTypeDef",
    {
        "TableDescription": TableDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeTableOutputTypeDef = TypedDict(
    "DescribeTableOutputTypeDef",
    {
        "Table": TableDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RestoreTableFromBackupOutputTypeDef = TypedDict(
    "RestoreTableFromBackupOutputTypeDef",
    {
        "TableDescription": TableDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RestoreTableToPointInTimeOutputTypeDef = TypedDict(
    "RestoreTableToPointInTimeOutputTypeDef",
    {
        "TableDescription": TableDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateTableOutputTypeDef = TypedDict(
    "UpdateTableOutputTypeDef",
    {
        "TableDescription": TableDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateTableInputRequestTypeDef = TypedDict(
    "UpdateTableInputRequestTypeDef",
    {
        "TableName": str,
        "AttributeDefinitions": NotRequired[Sequence[AttributeDefinitionTypeDef]],
        "BillingMode": NotRequired[BillingModeType],
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "GlobalSecondaryIndexUpdates": NotRequired[Sequence[GlobalSecondaryIndexUpdateTypeDef]],
        "StreamSpecification": NotRequired[StreamSpecificationTypeDef],
        "SSESpecification": NotRequired[SSESpecificationTypeDef],
        "ReplicaUpdates": NotRequired[Sequence[ReplicationGroupUpdateTypeDef]],
        "TableClass": NotRequired[TableClassType],
        "DeletionProtectionEnabled": NotRequired[bool],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
    },
)
UpdateTableInputTableUpdateTypeDef = TypedDict(
    "UpdateTableInputTableUpdateTypeDef",
    {
        "AttributeDefinitions": NotRequired[Sequence[AttributeDefinitionTypeDef]],
        "BillingMode": NotRequired[BillingModeType],
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "GlobalSecondaryIndexUpdates": NotRequired[Sequence[GlobalSecondaryIndexUpdateTypeDef]],
        "StreamSpecification": NotRequired[StreamSpecificationTypeDef],
        "SSESpecification": NotRequired[SSESpecificationTypeDef],
        "ReplicaUpdates": NotRequired[Sequence[ReplicationGroupUpdateTypeDef]],
        "TableClass": NotRequired[TableClassType],
        "DeletionProtectionEnabled": NotRequired[bool],
        "OnDemandThroughput": NotRequired[OnDemandThroughputTypeDef],
    },
)
DescribeImportOutputTypeDef = TypedDict(
    "DescribeImportOutputTypeDef",
    {
        "ImportTableDescription": ImportTableDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ImportTableOutputTypeDef = TypedDict(
    "ImportTableOutputTypeDef",
    {
        "ImportTableDescription": ImportTableDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteBackupOutputTypeDef = TypedDict(
    "DeleteBackupOutputTypeDef",
    {
        "BackupDescription": BackupDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeBackupOutputTypeDef = TypedDict(
    "DescribeBackupOutputTypeDef",
    {
        "BackupDescription": BackupDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchWriteItemInputRequestTypeDef = TypedDict(
    "BatchWriteItemInputRequestTypeDef",
    {
        "RequestItems": Mapping[str, Sequence[WriteRequestUnionTypeDef]],
        "ReturnConsumedCapacity": NotRequired[ReturnConsumedCapacityType],
        "ReturnItemCollectionMetrics": NotRequired[ReturnItemCollectionMetricsType],
    },
)
TableAutoScalingDescriptionTypeDef = TypedDict(
    "TableAutoScalingDescriptionTypeDef",
    {
        "TableName": NotRequired[str],
        "TableStatus": NotRequired[TableStatusType],
        "Replicas": NotRequired[List[ReplicaAutoScalingDescriptionTypeDef]],
    },
)
DescribeGlobalTableSettingsOutputTypeDef = TypedDict(
    "DescribeGlobalTableSettingsOutputTypeDef",
    {
        "GlobalTableName": str,
        "ReplicaSettings": List[ReplicaSettingsDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateGlobalTableSettingsOutputTypeDef = TypedDict(
    "UpdateGlobalTableSettingsOutputTypeDef",
    {
        "GlobalTableName": str,
        "ReplicaSettings": List[ReplicaSettingsDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateTableReplicaAutoScalingInputRequestTypeDef = TypedDict(
    "UpdateTableReplicaAutoScalingInputRequestTypeDef",
    {
        "TableName": str,
        "GlobalSecondaryIndexUpdates": NotRequired[
            Sequence[GlobalSecondaryIndexAutoScalingUpdateTypeDef]
        ],
        "ProvisionedWriteCapacityAutoScalingUpdate": NotRequired[AutoScalingSettingsUpdateTypeDef],
        "ReplicaUpdates": NotRequired[Sequence[ReplicaAutoScalingUpdateTypeDef]],
    },
)
UpdateGlobalTableSettingsInputRequestTypeDef = TypedDict(
    "UpdateGlobalTableSettingsInputRequestTypeDef",
    {
        "GlobalTableName": str,
        "GlobalTableBillingMode": NotRequired[BillingModeType],
        "GlobalTableProvisionedWriteCapacityUnits": NotRequired[int],
        "GlobalTableProvisionedWriteCapacityAutoScalingSettingsUpdate": NotRequired[
            AutoScalingSettingsUpdateTypeDef
        ],
        "GlobalTableGlobalSecondaryIndexSettingsUpdate": NotRequired[
            Sequence[GlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef]
        ],
        "ReplicaSettingsUpdate": NotRequired[Sequence[ReplicaSettingsUpdateTypeDef]],
    },
)
DescribeTableReplicaAutoScalingOutputTypeDef = TypedDict(
    "DescribeTableReplicaAutoScalingOutputTypeDef",
    {
        "TableAutoScalingDescription": TableAutoScalingDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateTableReplicaAutoScalingOutputTypeDef = TypedDict(
    "UpdateTableReplicaAutoScalingOutputTypeDef",
    {
        "TableAutoScalingDescription": TableAutoScalingDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
