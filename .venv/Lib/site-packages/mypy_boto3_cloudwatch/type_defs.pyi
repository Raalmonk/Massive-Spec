"""
Type annotations for cloudwatch service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudwatch.type_defs import AlarmHistoryItemTypeDef

    data: AlarmHistoryItemTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ActionsSuppressedByType,
    AlarmTypeType,
    AnomalyDetectorStateValueType,
    AnomalyDetectorTypeType,
    ComparisonOperatorType,
    HistoryItemTypeType,
    MetricStreamOutputFormatType,
    ScanByType,
    StandardUnitType,
    StateValueType,
    StatisticType,
    StatusCodeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AlarmHistoryItemTypeDef",
    "RangeExtraOutputTypeDef",
    "RangeOutputTypeDef",
    "DimensionTypeDef",
    "MetricCharacteristicsTypeDef",
    "CloudwatchEventStateTypeDef",
    "CloudwatchEventMetricStatsMetricTypeDef",
    "CompositeAlarmTypeDef",
    "DashboardEntryTypeDef",
    "DashboardValidationMessageTypeDef",
    "DatapointTypeDef",
    "DeleteAlarmsInputRequestTypeDef",
    "DeleteDashboardsInputRequestTypeDef",
    "DeleteInsightRulesInputRequestTypeDef",
    "PartialFailureTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteMetricStreamInputRequestTypeDef",
    "TimestampTypeDef",
    "PaginatorConfigTypeDef",
    "WaiterConfigTypeDef",
    "DescribeAlarmsInputRequestTypeDef",
    "DescribeInsightRulesInputRequestTypeDef",
    "InsightRuleTypeDef",
    "DimensionFilterTypeDef",
    "DisableAlarmActionsInputRequestTypeDef",
    "DisableInsightRulesInputRequestTypeDef",
    "EnableAlarmActionsInputRequestTypeDef",
    "EnableInsightRulesInputRequestTypeDef",
    "GetDashboardInputRequestTypeDef",
    "InsightRuleMetricDatapointTypeDef",
    "LabelOptionsTypeDef",
    "MessageDataTypeDef",
    "GetMetricStreamInputRequestTypeDef",
    "MetricStreamFilterOutputTypeDef",
    "GetMetricWidgetImageInputRequestTypeDef",
    "InsightRuleContributorDatapointTypeDef",
    "ListDashboardsInputRequestTypeDef",
    "ListManagedInsightRulesInputRequestTypeDef",
    "ListMetricStreamsInputRequestTypeDef",
    "MetricStreamEntryTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "TagTypeDef",
    "ManagedRuleStateTypeDef",
    "StatisticSetTypeDef",
    "MetricStreamFilterTypeDef",
    "MetricStreamStatisticsMetricTypeDef",
    "PutDashboardInputRequestTypeDef",
    "SetAlarmStateInputAlarmSetStateTypeDef",
    "SetAlarmStateInputRequestTypeDef",
    "StartMetricStreamsInputRequestTypeDef",
    "StopMetricStreamsInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "AnomalyDetectorConfigurationExtraOutputTypeDef",
    "AnomalyDetectorConfigurationOutputTypeDef",
    "DescribeAlarmsForMetricInputRequestTypeDef",
    "DescribeAnomalyDetectorsInputRequestTypeDef",
    "MetricExtraOutputTypeDef",
    "MetricOutputTypeDef",
    "MetricTypeDef",
    "SingleMetricAnomalyDetectorExtraOutputTypeDef",
    "SingleMetricAnomalyDetectorOutputTypeDef",
    "SingleMetricAnomalyDetectorTypeDef",
    "CloudwatchEventMetricStatsTypeDef",
    "DeleteInsightRulesOutputTypeDef",
    "DescribeAlarmHistoryOutputTypeDef",
    "DisableInsightRulesOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableInsightRulesOutputTypeDef",
    "GetDashboardOutputTypeDef",
    "GetMetricStatisticsOutputTypeDef",
    "GetMetricWidgetImageOutputTypeDef",
    "ListDashboardsOutputTypeDef",
    "PutDashboardOutputTypeDef",
    "PutManagedInsightRulesOutputTypeDef",
    "PutMetricStreamOutputTypeDef",
    "DescribeAlarmHistoryInputAlarmDescribeHistoryTypeDef",
    "DescribeAlarmHistoryInputRequestTypeDef",
    "GetInsightRuleReportInputRequestTypeDef",
    "GetMetricStatisticsInputMetricGetStatisticsTypeDef",
    "GetMetricStatisticsInputRequestTypeDef",
    "RangeTypeDef",
    "DescribeAlarmHistoryInputDescribeAlarmHistoryPaginateTypeDef",
    "DescribeAlarmsInputDescribeAlarmsPaginateTypeDef",
    "DescribeAnomalyDetectorsInputDescribeAnomalyDetectorsPaginateTypeDef",
    "ListDashboardsInputListDashboardsPaginateTypeDef",
    "DescribeAlarmsInputAlarmExistsWaitTypeDef",
    "DescribeAlarmsInputCompositeAlarmExistsWaitTypeDef",
    "DescribeInsightRulesOutputTypeDef",
    "ListMetricsInputListMetricsPaginateTypeDef",
    "ListMetricsInputRequestTypeDef",
    "MetricDataResultTypeDef",
    "InsightRuleContributorTypeDef",
    "ListMetricStreamsOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ManagedRuleTypeDef",
    "PutCompositeAlarmInputRequestTypeDef",
    "PutInsightRuleInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "ManagedRuleDescriptionTypeDef",
    "MetricDatumTypeDef",
    "MetricStreamFilterUnionTypeDef",
    "MetricStreamStatisticsConfigurationOutputTypeDef",
    "MetricStreamStatisticsConfigurationTypeDef",
    "ListMetricsOutputTypeDef",
    "MetricStatExtraOutputTypeDef",
    "MetricStatOutputTypeDef",
    "MetricStatTypeDef",
    "SingleMetricAnomalyDetectorUnionTypeDef",
    "CloudwatchEventMetricTypeDef",
    "AnomalyDetectorConfigurationTypeDef",
    "GetMetricDataOutputTypeDef",
    "GetInsightRuleReportOutputTypeDef",
    "PutManagedInsightRulesInputRequestTypeDef",
    "ListManagedInsightRulesOutputTypeDef",
    "PutMetricDataInputRequestTypeDef",
    "GetMetricStreamOutputTypeDef",
    "MetricStreamStatisticsConfigurationUnionTypeDef",
    "MetricDataQueryExtraOutputTypeDef",
    "MetricDataQueryOutputTypeDef",
    "MetricDataQueryTypeDef",
    "CloudwatchEventDetailConfigurationTypeDef",
    "AnomalyDetectorConfigurationUnionTypeDef",
    "PutMetricStreamInputRequestTypeDef",
    "MetricMathAnomalyDetectorExtraOutputTypeDef",
    "MetricAlarmTypeDef",
    "MetricMathAnomalyDetectorOutputTypeDef",
    "MetricDataQueryUnionTypeDef",
    "MetricMathAnomalyDetectorTypeDef",
    "PutMetricAlarmInputMetricPutAlarmTypeDef",
    "CloudwatchEventDetailTypeDef",
    "DescribeAlarmsForMetricOutputTypeDef",
    "DescribeAlarmsOutputTypeDef",
    "MetricStatAlarmTypeDef",
    "AnomalyDetectorTypeDef",
    "GetMetricDataInputGetMetricDataPaginateTypeDef",
    "GetMetricDataInputRequestTypeDef",
    "PutMetricAlarmInputRequestTypeDef",
    "DeleteAnomalyDetectorInputRequestTypeDef",
    "MetricMathAnomalyDetectorUnionTypeDef",
    "PutAnomalyDetectorInputRequestTypeDef",
    "CloudwatchEventTypeDef",
    "MetricDataQueryAlarmTypeDef",
    "DescribeAnomalyDetectorsOutputTypeDef",
)

AlarmHistoryItemTypeDef = TypedDict(
    "AlarmHistoryItemTypeDef",
    {
        "AlarmName": NotRequired[str],
        "AlarmType": NotRequired[AlarmTypeType],
        "Timestamp": NotRequired[datetime],
        "HistoryItemType": NotRequired[HistoryItemTypeType],
        "HistorySummary": NotRequired[str],
        "HistoryData": NotRequired[str],
    },
)
RangeExtraOutputTypeDef = TypedDict(
    "RangeExtraOutputTypeDef",
    {
        "StartTime": datetime,
        "EndTime": datetime,
    },
)
RangeOutputTypeDef = TypedDict(
    "RangeOutputTypeDef",
    {
        "StartTime": datetime,
        "EndTime": datetime,
    },
)
DimensionTypeDef = TypedDict(
    "DimensionTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)
MetricCharacteristicsTypeDef = TypedDict(
    "MetricCharacteristicsTypeDef",
    {
        "PeriodicSpikes": NotRequired[bool],
    },
)
CloudwatchEventStateTypeDef = TypedDict(
    "CloudwatchEventStateTypeDef",
    {
        "timestamp": str,
        "value": str,
        "reason": NotRequired[str],
        "reasonData": NotRequired[str],
        "actionsSuppressedBy": NotRequired[str],
        "actionsSuppressedReason": NotRequired[str],
    },
)
CloudwatchEventMetricStatsMetricTypeDef = TypedDict(
    "CloudwatchEventMetricStatsMetricTypeDef",
    {
        "metricName": str,
        "namespace": str,
        "dimensions": Dict[str, str],
    },
)
CompositeAlarmTypeDef = TypedDict(
    "CompositeAlarmTypeDef",
    {
        "ActionsEnabled": NotRequired[bool],
        "AlarmActions": NotRequired[List[str]],
        "AlarmArn": NotRequired[str],
        "AlarmConfigurationUpdatedTimestamp": NotRequired[datetime],
        "AlarmDescription": NotRequired[str],
        "AlarmName": NotRequired[str],
        "AlarmRule": NotRequired[str],
        "InsufficientDataActions": NotRequired[List[str]],
        "OKActions": NotRequired[List[str]],
        "StateReason": NotRequired[str],
        "StateReasonData": NotRequired[str],
        "StateUpdatedTimestamp": NotRequired[datetime],
        "StateValue": NotRequired[StateValueType],
        "StateTransitionedTimestamp": NotRequired[datetime],
        "ActionsSuppressedBy": NotRequired[ActionsSuppressedByType],
        "ActionsSuppressedReason": NotRequired[str],
        "ActionsSuppressor": NotRequired[str],
        "ActionsSuppressorWaitPeriod": NotRequired[int],
        "ActionsSuppressorExtensionPeriod": NotRequired[int],
    },
)
DashboardEntryTypeDef = TypedDict(
    "DashboardEntryTypeDef",
    {
        "DashboardName": NotRequired[str],
        "DashboardArn": NotRequired[str],
        "LastModified": NotRequired[datetime],
        "Size": NotRequired[int],
    },
)
DashboardValidationMessageTypeDef = TypedDict(
    "DashboardValidationMessageTypeDef",
    {
        "DataPath": NotRequired[str],
        "Message": NotRequired[str],
    },
)
DatapointTypeDef = TypedDict(
    "DatapointTypeDef",
    {
        "Timestamp": NotRequired[datetime],
        "SampleCount": NotRequired[float],
        "Average": NotRequired[float],
        "Sum": NotRequired[float],
        "Minimum": NotRequired[float],
        "Maximum": NotRequired[float],
        "Unit": NotRequired[StandardUnitType],
        "ExtendedStatistics": NotRequired[Dict[str, float]],
    },
)
DeleteAlarmsInputRequestTypeDef = TypedDict(
    "DeleteAlarmsInputRequestTypeDef",
    {
        "AlarmNames": Sequence[str],
    },
)
DeleteDashboardsInputRequestTypeDef = TypedDict(
    "DeleteDashboardsInputRequestTypeDef",
    {
        "DashboardNames": Sequence[str],
    },
)
DeleteInsightRulesInputRequestTypeDef = TypedDict(
    "DeleteInsightRulesInputRequestTypeDef",
    {
        "RuleNames": Sequence[str],
    },
)
PartialFailureTypeDef = TypedDict(
    "PartialFailureTypeDef",
    {
        "FailureResource": NotRequired[str],
        "ExceptionType": NotRequired[str],
        "FailureCode": NotRequired[str],
        "FailureDescription": NotRequired[str],
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
DeleteMetricStreamInputRequestTypeDef = TypedDict(
    "DeleteMetricStreamInputRequestTypeDef",
    {
        "Name": str,
    },
)
TimestampTypeDef = Union[datetime, str]
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": NotRequired[int],
        "MaxAttempts": NotRequired[int],
    },
)
DescribeAlarmsInputRequestTypeDef = TypedDict(
    "DescribeAlarmsInputRequestTypeDef",
    {
        "AlarmNames": NotRequired[Sequence[str]],
        "AlarmNamePrefix": NotRequired[str],
        "AlarmTypes": NotRequired[Sequence[AlarmTypeType]],
        "ChildrenOfAlarmName": NotRequired[str],
        "ParentsOfAlarmName": NotRequired[str],
        "StateValue": NotRequired[StateValueType],
        "ActionPrefix": NotRequired[str],
        "MaxRecords": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
DescribeInsightRulesInputRequestTypeDef = TypedDict(
    "DescribeInsightRulesInputRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
InsightRuleTypeDef = TypedDict(
    "InsightRuleTypeDef",
    {
        "Name": str,
        "State": str,
        "Schema": str,
        "Definition": str,
        "ManagedRule": NotRequired[bool],
    },
)
DimensionFilterTypeDef = TypedDict(
    "DimensionFilterTypeDef",
    {
        "Name": str,
        "Value": NotRequired[str],
    },
)
DisableAlarmActionsInputRequestTypeDef = TypedDict(
    "DisableAlarmActionsInputRequestTypeDef",
    {
        "AlarmNames": Sequence[str],
    },
)
DisableInsightRulesInputRequestTypeDef = TypedDict(
    "DisableInsightRulesInputRequestTypeDef",
    {
        "RuleNames": Sequence[str],
    },
)
EnableAlarmActionsInputRequestTypeDef = TypedDict(
    "EnableAlarmActionsInputRequestTypeDef",
    {
        "AlarmNames": Sequence[str],
    },
)
EnableInsightRulesInputRequestTypeDef = TypedDict(
    "EnableInsightRulesInputRequestTypeDef",
    {
        "RuleNames": Sequence[str],
    },
)
GetDashboardInputRequestTypeDef = TypedDict(
    "GetDashboardInputRequestTypeDef",
    {
        "DashboardName": str,
    },
)
InsightRuleMetricDatapointTypeDef = TypedDict(
    "InsightRuleMetricDatapointTypeDef",
    {
        "Timestamp": datetime,
        "UniqueContributors": NotRequired[float],
        "MaxContributorValue": NotRequired[float],
        "SampleCount": NotRequired[float],
        "Average": NotRequired[float],
        "Sum": NotRequired[float],
        "Minimum": NotRequired[float],
        "Maximum": NotRequired[float],
    },
)
LabelOptionsTypeDef = TypedDict(
    "LabelOptionsTypeDef",
    {
        "Timezone": NotRequired[str],
    },
)
MessageDataTypeDef = TypedDict(
    "MessageDataTypeDef",
    {
        "Code": NotRequired[str],
        "Value": NotRequired[str],
    },
)
GetMetricStreamInputRequestTypeDef = TypedDict(
    "GetMetricStreamInputRequestTypeDef",
    {
        "Name": str,
    },
)
MetricStreamFilterOutputTypeDef = TypedDict(
    "MetricStreamFilterOutputTypeDef",
    {
        "Namespace": NotRequired[str],
        "MetricNames": NotRequired[List[str]],
    },
)
GetMetricWidgetImageInputRequestTypeDef = TypedDict(
    "GetMetricWidgetImageInputRequestTypeDef",
    {
        "MetricWidget": str,
        "OutputFormat": NotRequired[str],
    },
)
InsightRuleContributorDatapointTypeDef = TypedDict(
    "InsightRuleContributorDatapointTypeDef",
    {
        "Timestamp": datetime,
        "ApproximateValue": float,
    },
)
ListDashboardsInputRequestTypeDef = TypedDict(
    "ListDashboardsInputRequestTypeDef",
    {
        "DashboardNamePrefix": NotRequired[str],
        "NextToken": NotRequired[str],
    },
)
ListManagedInsightRulesInputRequestTypeDef = TypedDict(
    "ListManagedInsightRulesInputRequestTypeDef",
    {
        "ResourceARN": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListMetricStreamsInputRequestTypeDef = TypedDict(
    "ListMetricStreamsInputRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
MetricStreamEntryTypeDef = TypedDict(
    "MetricStreamEntryTypeDef",
    {
        "Arn": NotRequired[str],
        "CreationDate": NotRequired[datetime],
        "LastUpdateDate": NotRequired[datetime],
        "Name": NotRequired[str],
        "FirehoseArn": NotRequired[str],
        "State": NotRequired[str],
        "OutputFormat": NotRequired[MetricStreamOutputFormatType],
    },
)
ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
    },
)
TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)
ManagedRuleStateTypeDef = TypedDict(
    "ManagedRuleStateTypeDef",
    {
        "RuleName": str,
        "State": str,
    },
)
StatisticSetTypeDef = TypedDict(
    "StatisticSetTypeDef",
    {
        "SampleCount": float,
        "Sum": float,
        "Minimum": float,
        "Maximum": float,
    },
)
MetricStreamFilterTypeDef = TypedDict(
    "MetricStreamFilterTypeDef",
    {
        "Namespace": NotRequired[str],
        "MetricNames": NotRequired[Sequence[str]],
    },
)
MetricStreamStatisticsMetricTypeDef = TypedDict(
    "MetricStreamStatisticsMetricTypeDef",
    {
        "Namespace": str,
        "MetricName": str,
    },
)
PutDashboardInputRequestTypeDef = TypedDict(
    "PutDashboardInputRequestTypeDef",
    {
        "DashboardName": str,
        "DashboardBody": str,
    },
)
SetAlarmStateInputAlarmSetStateTypeDef = TypedDict(
    "SetAlarmStateInputAlarmSetStateTypeDef",
    {
        "StateValue": StateValueType,
        "StateReason": str,
        "StateReasonData": NotRequired[str],
    },
)
SetAlarmStateInputRequestTypeDef = TypedDict(
    "SetAlarmStateInputRequestTypeDef",
    {
        "AlarmName": str,
        "StateValue": StateValueType,
        "StateReason": str,
        "StateReasonData": NotRequired[str],
    },
)
StartMetricStreamsInputRequestTypeDef = TypedDict(
    "StartMetricStreamsInputRequestTypeDef",
    {
        "Names": Sequence[str],
    },
)
StopMetricStreamsInputRequestTypeDef = TypedDict(
    "StopMetricStreamsInputRequestTypeDef",
    {
        "Names": Sequence[str],
    },
)
UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)
AnomalyDetectorConfigurationExtraOutputTypeDef = TypedDict(
    "AnomalyDetectorConfigurationExtraOutputTypeDef",
    {
        "ExcludedTimeRanges": NotRequired[List[RangeExtraOutputTypeDef]],
        "MetricTimezone": NotRequired[str],
    },
)
AnomalyDetectorConfigurationOutputTypeDef = TypedDict(
    "AnomalyDetectorConfigurationOutputTypeDef",
    {
        "ExcludedTimeRanges": NotRequired[List[RangeOutputTypeDef]],
        "MetricTimezone": NotRequired[str],
    },
)
DescribeAlarmsForMetricInputRequestTypeDef = TypedDict(
    "DescribeAlarmsForMetricInputRequestTypeDef",
    {
        "MetricName": str,
        "Namespace": str,
        "Statistic": NotRequired[StatisticType],
        "ExtendedStatistic": NotRequired[str],
        "Dimensions": NotRequired[Sequence[DimensionTypeDef]],
        "Period": NotRequired[int],
        "Unit": NotRequired[StandardUnitType],
    },
)
DescribeAnomalyDetectorsInputRequestTypeDef = TypedDict(
    "DescribeAnomalyDetectorsInputRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Namespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Dimensions": NotRequired[Sequence[DimensionTypeDef]],
        "AnomalyDetectorTypes": NotRequired[Sequence[AnomalyDetectorTypeType]],
    },
)
MetricExtraOutputTypeDef = TypedDict(
    "MetricExtraOutputTypeDef",
    {
        "Namespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Dimensions": NotRequired[List[DimensionTypeDef]],
    },
)
MetricOutputTypeDef = TypedDict(
    "MetricOutputTypeDef",
    {
        "Namespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Dimensions": NotRequired[List[DimensionTypeDef]],
    },
)
MetricTypeDef = TypedDict(
    "MetricTypeDef",
    {
        "Namespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Dimensions": NotRequired[Sequence[DimensionTypeDef]],
    },
)
SingleMetricAnomalyDetectorExtraOutputTypeDef = TypedDict(
    "SingleMetricAnomalyDetectorExtraOutputTypeDef",
    {
        "AccountId": NotRequired[str],
        "Namespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Dimensions": NotRequired[List[DimensionTypeDef]],
        "Stat": NotRequired[str],
    },
)
SingleMetricAnomalyDetectorOutputTypeDef = TypedDict(
    "SingleMetricAnomalyDetectorOutputTypeDef",
    {
        "AccountId": NotRequired[str],
        "Namespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Dimensions": NotRequired[List[DimensionTypeDef]],
        "Stat": NotRequired[str],
    },
)
SingleMetricAnomalyDetectorTypeDef = TypedDict(
    "SingleMetricAnomalyDetectorTypeDef",
    {
        "AccountId": NotRequired[str],
        "Namespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Dimensions": NotRequired[Sequence[DimensionTypeDef]],
        "Stat": NotRequired[str],
    },
)
CloudwatchEventMetricStatsTypeDef = TypedDict(
    "CloudwatchEventMetricStatsTypeDef",
    {
        "period": str,
        "stat": str,
        "metric": NotRequired[CloudwatchEventMetricStatsMetricTypeDef],
    },
)
DeleteInsightRulesOutputTypeDef = TypedDict(
    "DeleteInsightRulesOutputTypeDef",
    {
        "Failures": List[PartialFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeAlarmHistoryOutputTypeDef = TypedDict(
    "DescribeAlarmHistoryOutputTypeDef",
    {
        "AlarmHistoryItems": List[AlarmHistoryItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
DisableInsightRulesOutputTypeDef = TypedDict(
    "DisableInsightRulesOutputTypeDef",
    {
        "Failures": List[PartialFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnableInsightRulesOutputTypeDef = TypedDict(
    "EnableInsightRulesOutputTypeDef",
    {
        "Failures": List[PartialFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDashboardOutputTypeDef = TypedDict(
    "GetDashboardOutputTypeDef",
    {
        "DashboardArn": str,
        "DashboardBody": str,
        "DashboardName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetMetricStatisticsOutputTypeDef = TypedDict(
    "GetMetricStatisticsOutputTypeDef",
    {
        "Label": str,
        "Datapoints": List[DatapointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetMetricWidgetImageOutputTypeDef = TypedDict(
    "GetMetricWidgetImageOutputTypeDef",
    {
        "MetricWidgetImage": bytes,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDashboardsOutputTypeDef = TypedDict(
    "ListDashboardsOutputTypeDef",
    {
        "DashboardEntries": List[DashboardEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
PutDashboardOutputTypeDef = TypedDict(
    "PutDashboardOutputTypeDef",
    {
        "DashboardValidationMessages": List[DashboardValidationMessageTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutManagedInsightRulesOutputTypeDef = TypedDict(
    "PutManagedInsightRulesOutputTypeDef",
    {
        "Failures": List[PartialFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutMetricStreamOutputTypeDef = TypedDict(
    "PutMetricStreamOutputTypeDef",
    {
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeAlarmHistoryInputAlarmDescribeHistoryTypeDef = TypedDict(
    "DescribeAlarmHistoryInputAlarmDescribeHistoryTypeDef",
    {
        "AlarmTypes": NotRequired[Sequence[AlarmTypeType]],
        "HistoryItemType": NotRequired[HistoryItemTypeType],
        "StartDate": NotRequired[TimestampTypeDef],
        "EndDate": NotRequired[TimestampTypeDef],
        "MaxRecords": NotRequired[int],
        "NextToken": NotRequired[str],
        "ScanBy": NotRequired[ScanByType],
    },
)
DescribeAlarmHistoryInputRequestTypeDef = TypedDict(
    "DescribeAlarmHistoryInputRequestTypeDef",
    {
        "AlarmName": NotRequired[str],
        "AlarmTypes": NotRequired[Sequence[AlarmTypeType]],
        "HistoryItemType": NotRequired[HistoryItemTypeType],
        "StartDate": NotRequired[TimestampTypeDef],
        "EndDate": NotRequired[TimestampTypeDef],
        "MaxRecords": NotRequired[int],
        "NextToken": NotRequired[str],
        "ScanBy": NotRequired[ScanByType],
    },
)
GetInsightRuleReportInputRequestTypeDef = TypedDict(
    "GetInsightRuleReportInputRequestTypeDef",
    {
        "RuleName": str,
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
        "Period": int,
        "MaxContributorCount": NotRequired[int],
        "Metrics": NotRequired[Sequence[str]],
        "OrderBy": NotRequired[str],
    },
)
GetMetricStatisticsInputMetricGetStatisticsTypeDef = TypedDict(
    "GetMetricStatisticsInputMetricGetStatisticsTypeDef",
    {
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
        "Period": int,
        "Dimensions": NotRequired[Sequence[DimensionTypeDef]],
        "Statistics": NotRequired[Sequence[StatisticType]],
        "ExtendedStatistics": NotRequired[Sequence[str]],
        "Unit": NotRequired[StandardUnitType],
    },
)
GetMetricStatisticsInputRequestTypeDef = TypedDict(
    "GetMetricStatisticsInputRequestTypeDef",
    {
        "Namespace": str,
        "MetricName": str,
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
        "Period": int,
        "Dimensions": NotRequired[Sequence[DimensionTypeDef]],
        "Statistics": NotRequired[Sequence[StatisticType]],
        "ExtendedStatistics": NotRequired[Sequence[str]],
        "Unit": NotRequired[StandardUnitType],
    },
)
RangeTypeDef = TypedDict(
    "RangeTypeDef",
    {
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
    },
)
DescribeAlarmHistoryInputDescribeAlarmHistoryPaginateTypeDef = TypedDict(
    "DescribeAlarmHistoryInputDescribeAlarmHistoryPaginateTypeDef",
    {
        "AlarmName": NotRequired[str],
        "AlarmTypes": NotRequired[Sequence[AlarmTypeType]],
        "HistoryItemType": NotRequired[HistoryItemTypeType],
        "StartDate": NotRequired[TimestampTypeDef],
        "EndDate": NotRequired[TimestampTypeDef],
        "ScanBy": NotRequired[ScanByType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
DescribeAlarmsInputDescribeAlarmsPaginateTypeDef = TypedDict(
    "DescribeAlarmsInputDescribeAlarmsPaginateTypeDef",
    {
        "AlarmNames": NotRequired[Sequence[str]],
        "AlarmNamePrefix": NotRequired[str],
        "AlarmTypes": NotRequired[Sequence[AlarmTypeType]],
        "ChildrenOfAlarmName": NotRequired[str],
        "ParentsOfAlarmName": NotRequired[str],
        "StateValue": NotRequired[StateValueType],
        "ActionPrefix": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
DescribeAnomalyDetectorsInputDescribeAnomalyDetectorsPaginateTypeDef = TypedDict(
    "DescribeAnomalyDetectorsInputDescribeAnomalyDetectorsPaginateTypeDef",
    {
        "Namespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Dimensions": NotRequired[Sequence[DimensionTypeDef]],
        "AnomalyDetectorTypes": NotRequired[Sequence[AnomalyDetectorTypeType]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListDashboardsInputListDashboardsPaginateTypeDef = TypedDict(
    "ListDashboardsInputListDashboardsPaginateTypeDef",
    {
        "DashboardNamePrefix": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
DescribeAlarmsInputAlarmExistsWaitTypeDef = TypedDict(
    "DescribeAlarmsInputAlarmExistsWaitTypeDef",
    {
        "AlarmNames": NotRequired[Sequence[str]],
        "AlarmNamePrefix": NotRequired[str],
        "AlarmTypes": NotRequired[Sequence[AlarmTypeType]],
        "ChildrenOfAlarmName": NotRequired[str],
        "ParentsOfAlarmName": NotRequired[str],
        "StateValue": NotRequired[StateValueType],
        "ActionPrefix": NotRequired[str],
        "MaxRecords": NotRequired[int],
        "NextToken": NotRequired[str],
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
DescribeAlarmsInputCompositeAlarmExistsWaitTypeDef = TypedDict(
    "DescribeAlarmsInputCompositeAlarmExistsWaitTypeDef",
    {
        "AlarmNames": NotRequired[Sequence[str]],
        "AlarmNamePrefix": NotRequired[str],
        "AlarmTypes": NotRequired[Sequence[AlarmTypeType]],
        "ChildrenOfAlarmName": NotRequired[str],
        "ParentsOfAlarmName": NotRequired[str],
        "StateValue": NotRequired[StateValueType],
        "ActionPrefix": NotRequired[str],
        "MaxRecords": NotRequired[int],
        "NextToken": NotRequired[str],
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
DescribeInsightRulesOutputTypeDef = TypedDict(
    "DescribeInsightRulesOutputTypeDef",
    {
        "InsightRules": List[InsightRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListMetricsInputListMetricsPaginateTypeDef = TypedDict(
    "ListMetricsInputListMetricsPaginateTypeDef",
    {
        "Namespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Dimensions": NotRequired[Sequence[DimensionFilterTypeDef]],
        "RecentlyActive": NotRequired[Literal["PT3H"]],
        "IncludeLinkedAccounts": NotRequired[bool],
        "OwningAccount": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListMetricsInputRequestTypeDef = TypedDict(
    "ListMetricsInputRequestTypeDef",
    {
        "Namespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Dimensions": NotRequired[Sequence[DimensionFilterTypeDef]],
        "NextToken": NotRequired[str],
        "RecentlyActive": NotRequired[Literal["PT3H"]],
        "IncludeLinkedAccounts": NotRequired[bool],
        "OwningAccount": NotRequired[str],
    },
)
MetricDataResultTypeDef = TypedDict(
    "MetricDataResultTypeDef",
    {
        "Id": NotRequired[str],
        "Label": NotRequired[str],
        "Timestamps": NotRequired[List[datetime]],
        "Values": NotRequired[List[float]],
        "StatusCode": NotRequired[StatusCodeType],
        "Messages": NotRequired[List[MessageDataTypeDef]],
    },
)
InsightRuleContributorTypeDef = TypedDict(
    "InsightRuleContributorTypeDef",
    {
        "Keys": List[str],
        "ApproximateAggregateValue": float,
        "Datapoints": List[InsightRuleContributorDatapointTypeDef],
    },
)
ListMetricStreamsOutputTypeDef = TypedDict(
    "ListMetricStreamsOutputTypeDef",
    {
        "Entries": List[MetricStreamEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ManagedRuleTypeDef = TypedDict(
    "ManagedRuleTypeDef",
    {
        "TemplateName": str,
        "ResourceARN": str,
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
PutCompositeAlarmInputRequestTypeDef = TypedDict(
    "PutCompositeAlarmInputRequestTypeDef",
    {
        "AlarmName": str,
        "AlarmRule": str,
        "ActionsEnabled": NotRequired[bool],
        "AlarmActions": NotRequired[Sequence[str]],
        "AlarmDescription": NotRequired[str],
        "InsufficientDataActions": NotRequired[Sequence[str]],
        "OKActions": NotRequired[Sequence[str]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "ActionsSuppressor": NotRequired[str],
        "ActionsSuppressorWaitPeriod": NotRequired[int],
        "ActionsSuppressorExtensionPeriod": NotRequired[int],
    },
)
PutInsightRuleInputRequestTypeDef = TypedDict(
    "PutInsightRuleInputRequestTypeDef",
    {
        "RuleName": str,
        "RuleDefinition": str,
        "RuleState": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)
ManagedRuleDescriptionTypeDef = TypedDict(
    "ManagedRuleDescriptionTypeDef",
    {
        "TemplateName": NotRequired[str],
        "ResourceARN": NotRequired[str],
        "RuleState": NotRequired[ManagedRuleStateTypeDef],
    },
)
MetricDatumTypeDef = TypedDict(
    "MetricDatumTypeDef",
    {
        "MetricName": str,
        "Dimensions": NotRequired[Sequence[DimensionTypeDef]],
        "Timestamp": NotRequired[TimestampTypeDef],
        "Value": NotRequired[float],
        "StatisticValues": NotRequired[StatisticSetTypeDef],
        "Values": NotRequired[Sequence[float]],
        "Counts": NotRequired[Sequence[float]],
        "Unit": NotRequired[StandardUnitType],
        "StorageResolution": NotRequired[int],
    },
)
MetricStreamFilterUnionTypeDef = Union[MetricStreamFilterTypeDef, MetricStreamFilterOutputTypeDef]
MetricStreamStatisticsConfigurationOutputTypeDef = TypedDict(
    "MetricStreamStatisticsConfigurationOutputTypeDef",
    {
        "IncludeMetrics": List[MetricStreamStatisticsMetricTypeDef],
        "AdditionalStatistics": List[str],
    },
)
MetricStreamStatisticsConfigurationTypeDef = TypedDict(
    "MetricStreamStatisticsConfigurationTypeDef",
    {
        "IncludeMetrics": Sequence[MetricStreamStatisticsMetricTypeDef],
        "AdditionalStatistics": Sequence[str],
    },
)
ListMetricsOutputTypeDef = TypedDict(
    "ListMetricsOutputTypeDef",
    {
        "Metrics": List[MetricExtraOutputTypeDef],
        "OwningAccounts": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
MetricStatExtraOutputTypeDef = TypedDict(
    "MetricStatExtraOutputTypeDef",
    {
        "Metric": MetricExtraOutputTypeDef,
        "Period": int,
        "Stat": str,
        "Unit": NotRequired[StandardUnitType],
    },
)
MetricStatOutputTypeDef = TypedDict(
    "MetricStatOutputTypeDef",
    {
        "Metric": MetricOutputTypeDef,
        "Period": int,
        "Stat": str,
        "Unit": NotRequired[StandardUnitType],
    },
)
MetricStatTypeDef = TypedDict(
    "MetricStatTypeDef",
    {
        "Metric": MetricTypeDef,
        "Period": int,
        "Stat": str,
        "Unit": NotRequired[StandardUnitType],
    },
)
SingleMetricAnomalyDetectorUnionTypeDef = Union[
    SingleMetricAnomalyDetectorTypeDef, SingleMetricAnomalyDetectorExtraOutputTypeDef
]
CloudwatchEventMetricTypeDef = TypedDict(
    "CloudwatchEventMetricTypeDef",
    {
        "id": str,
        "returnData": bool,
        "metricStat": NotRequired[CloudwatchEventMetricStatsTypeDef],
        "expression": NotRequired[str],
        "label": NotRequired[str],
        "period": NotRequired[int],
    },
)
AnomalyDetectorConfigurationTypeDef = TypedDict(
    "AnomalyDetectorConfigurationTypeDef",
    {
        "ExcludedTimeRanges": NotRequired[Sequence[RangeTypeDef]],
        "MetricTimezone": NotRequired[str],
    },
)
GetMetricDataOutputTypeDef = TypedDict(
    "GetMetricDataOutputTypeDef",
    {
        "MetricDataResults": List[MetricDataResultTypeDef],
        "Messages": List[MessageDataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetInsightRuleReportOutputTypeDef = TypedDict(
    "GetInsightRuleReportOutputTypeDef",
    {
        "KeyLabels": List[str],
        "AggregationStatistic": str,
        "AggregateValue": float,
        "ApproximateUniqueCount": int,
        "Contributors": List[InsightRuleContributorTypeDef],
        "MetricDatapoints": List[InsightRuleMetricDatapointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutManagedInsightRulesInputRequestTypeDef = TypedDict(
    "PutManagedInsightRulesInputRequestTypeDef",
    {
        "ManagedRules": Sequence[ManagedRuleTypeDef],
    },
)
ListManagedInsightRulesOutputTypeDef = TypedDict(
    "ListManagedInsightRulesOutputTypeDef",
    {
        "ManagedRules": List[ManagedRuleDescriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
PutMetricDataInputRequestTypeDef = TypedDict(
    "PutMetricDataInputRequestTypeDef",
    {
        "Namespace": str,
        "MetricData": Sequence[MetricDatumTypeDef],
    },
)
GetMetricStreamOutputTypeDef = TypedDict(
    "GetMetricStreamOutputTypeDef",
    {
        "Arn": str,
        "Name": str,
        "IncludeFilters": List[MetricStreamFilterOutputTypeDef],
        "ExcludeFilters": List[MetricStreamFilterOutputTypeDef],
        "FirehoseArn": str,
        "RoleArn": str,
        "State": str,
        "CreationDate": datetime,
        "LastUpdateDate": datetime,
        "OutputFormat": MetricStreamOutputFormatType,
        "StatisticsConfigurations": List[MetricStreamStatisticsConfigurationOutputTypeDef],
        "IncludeLinkedAccountsMetrics": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
MetricStreamStatisticsConfigurationUnionTypeDef = Union[
    MetricStreamStatisticsConfigurationTypeDef, MetricStreamStatisticsConfigurationOutputTypeDef
]
MetricDataQueryExtraOutputTypeDef = TypedDict(
    "MetricDataQueryExtraOutputTypeDef",
    {
        "Id": str,
        "MetricStat": NotRequired[MetricStatExtraOutputTypeDef],
        "Expression": NotRequired[str],
        "Label": NotRequired[str],
        "ReturnData": NotRequired[bool],
        "Period": NotRequired[int],
        "AccountId": NotRequired[str],
    },
)
MetricDataQueryOutputTypeDef = TypedDict(
    "MetricDataQueryOutputTypeDef",
    {
        "Id": str,
        "MetricStat": NotRequired[MetricStatOutputTypeDef],
        "Expression": NotRequired[str],
        "Label": NotRequired[str],
        "ReturnData": NotRequired[bool],
        "Period": NotRequired[int],
        "AccountId": NotRequired[str],
    },
)
MetricDataQueryTypeDef = TypedDict(
    "MetricDataQueryTypeDef",
    {
        "Id": str,
        "MetricStat": NotRequired[MetricStatTypeDef],
        "Expression": NotRequired[str],
        "Label": NotRequired[str],
        "ReturnData": NotRequired[bool],
        "Period": NotRequired[int],
        "AccountId": NotRequired[str],
    },
)
CloudwatchEventDetailConfigurationTypeDef = TypedDict(
    "CloudwatchEventDetailConfigurationTypeDef",
    {
        "id": NotRequired[str],
        "description": NotRequired[str],
        "metrics": NotRequired[List[CloudwatchEventMetricTypeDef]],
        "actionsSuppressor": NotRequired[str],
        "actionsSuppressorWaitPeriod": NotRequired[int],
        "actionsSuppressorExtensionPeriod": NotRequired[int],
        "threshold": NotRequired[int],
        "evaluationPeriods": NotRequired[int],
        "alarmRule": NotRequired[str],
        "alarmName": NotRequired[str],
        "treatMissingData": NotRequired[str],
        "comparisonOperator": NotRequired[str],
        "timestamp": NotRequired[str],
        "actionsEnabled": NotRequired[bool],
        "okActions": NotRequired[List[str]],
        "alarmActions": NotRequired[List[str]],
        "insufficientDataActions": NotRequired[List[str]],
    },
)
AnomalyDetectorConfigurationUnionTypeDef = Union[
    AnomalyDetectorConfigurationTypeDef, AnomalyDetectorConfigurationExtraOutputTypeDef
]
PutMetricStreamInputRequestTypeDef = TypedDict(
    "PutMetricStreamInputRequestTypeDef",
    {
        "Name": str,
        "FirehoseArn": str,
        "RoleArn": str,
        "OutputFormat": MetricStreamOutputFormatType,
        "IncludeFilters": NotRequired[Sequence[MetricStreamFilterUnionTypeDef]],
        "ExcludeFilters": NotRequired[Sequence[MetricStreamFilterUnionTypeDef]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "StatisticsConfigurations": NotRequired[
            Sequence[MetricStreamStatisticsConfigurationUnionTypeDef]
        ],
        "IncludeLinkedAccountsMetrics": NotRequired[bool],
    },
)
MetricMathAnomalyDetectorExtraOutputTypeDef = TypedDict(
    "MetricMathAnomalyDetectorExtraOutputTypeDef",
    {
        "MetricDataQueries": NotRequired[List[MetricDataQueryExtraOutputTypeDef]],
    },
)
MetricAlarmTypeDef = TypedDict(
    "MetricAlarmTypeDef",
    {
        "AlarmName": NotRequired[str],
        "AlarmArn": NotRequired[str],
        "AlarmDescription": NotRequired[str],
        "AlarmConfigurationUpdatedTimestamp": NotRequired[datetime],
        "ActionsEnabled": NotRequired[bool],
        "OKActions": NotRequired[List[str]],
        "AlarmActions": NotRequired[List[str]],
        "InsufficientDataActions": NotRequired[List[str]],
        "StateValue": NotRequired[StateValueType],
        "StateReason": NotRequired[str],
        "StateReasonData": NotRequired[str],
        "StateUpdatedTimestamp": NotRequired[datetime],
        "MetricName": NotRequired[str],
        "Namespace": NotRequired[str],
        "Statistic": NotRequired[StatisticType],
        "ExtendedStatistic": NotRequired[str],
        "Dimensions": NotRequired[List[DimensionTypeDef]],
        "Period": NotRequired[int],
        "Unit": NotRequired[StandardUnitType],
        "EvaluationPeriods": NotRequired[int],
        "DatapointsToAlarm": NotRequired[int],
        "Threshold": NotRequired[float],
        "ComparisonOperator": NotRequired[ComparisonOperatorType],
        "TreatMissingData": NotRequired[str],
        "EvaluateLowSampleCountPercentile": NotRequired[str],
        "Metrics": NotRequired[List[MetricDataQueryOutputTypeDef]],
        "ThresholdMetricId": NotRequired[str],
        "EvaluationState": NotRequired[Literal["PARTIAL_DATA"]],
        "StateTransitionedTimestamp": NotRequired[datetime],
    },
)
MetricMathAnomalyDetectorOutputTypeDef = TypedDict(
    "MetricMathAnomalyDetectorOutputTypeDef",
    {
        "MetricDataQueries": NotRequired[List[MetricDataQueryOutputTypeDef]],
    },
)
MetricDataQueryUnionTypeDef = Union[MetricDataQueryTypeDef, MetricDataQueryExtraOutputTypeDef]
MetricMathAnomalyDetectorTypeDef = TypedDict(
    "MetricMathAnomalyDetectorTypeDef",
    {
        "MetricDataQueries": NotRequired[Sequence[MetricDataQueryTypeDef]],
    },
)
PutMetricAlarmInputMetricPutAlarmTypeDef = TypedDict(
    "PutMetricAlarmInputMetricPutAlarmTypeDef",
    {
        "AlarmName": str,
        "EvaluationPeriods": int,
        "ComparisonOperator": ComparisonOperatorType,
        "AlarmDescription": NotRequired[str],
        "ActionsEnabled": NotRequired[bool],
        "OKActions": NotRequired[Sequence[str]],
        "AlarmActions": NotRequired[Sequence[str]],
        "InsufficientDataActions": NotRequired[Sequence[str]],
        "Statistic": NotRequired[StatisticType],
        "ExtendedStatistic": NotRequired[str],
        "Dimensions": NotRequired[Sequence[DimensionTypeDef]],
        "Period": NotRequired[int],
        "Unit": NotRequired[StandardUnitType],
        "DatapointsToAlarm": NotRequired[int],
        "Threshold": NotRequired[float],
        "TreatMissingData": NotRequired[str],
        "EvaluateLowSampleCountPercentile": NotRequired[str],
        "Metrics": NotRequired[Sequence[MetricDataQueryTypeDef]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "ThresholdMetricId": NotRequired[str],
    },
)
CloudwatchEventDetailTypeDef = TypedDict(
    "CloudwatchEventDetailTypeDef",
    {
        "alarmName": str,
        "state": CloudwatchEventStateTypeDef,
        "operation": NotRequired[str],
        "configuration": NotRequired[CloudwatchEventDetailConfigurationTypeDef],
        "previousConfiguration": NotRequired[CloudwatchEventDetailConfigurationTypeDef],
        "previousState": NotRequired[CloudwatchEventStateTypeDef],
    },
)
DescribeAlarmsForMetricOutputTypeDef = TypedDict(
    "DescribeAlarmsForMetricOutputTypeDef",
    {
        "MetricAlarms": List[MetricAlarmTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeAlarmsOutputTypeDef = TypedDict(
    "DescribeAlarmsOutputTypeDef",
    {
        "CompositeAlarms": List[CompositeAlarmTypeDef],
        "MetricAlarms": List[MetricAlarmTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
MetricStatAlarmTypeDef = TypedDict(
    "MetricStatAlarmTypeDef",
    {
        "Metric": MetricAlarmTypeDef,
        "Period": int,
        "Stat": str,
        "Unit": NotRequired[StandardUnitType],
    },
)
AnomalyDetectorTypeDef = TypedDict(
    "AnomalyDetectorTypeDef",
    {
        "Namespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Dimensions": NotRequired[List[DimensionTypeDef]],
        "Stat": NotRequired[str],
        "Configuration": NotRequired[AnomalyDetectorConfigurationOutputTypeDef],
        "StateValue": NotRequired[AnomalyDetectorStateValueType],
        "MetricCharacteristics": NotRequired[MetricCharacteristicsTypeDef],
        "SingleMetricAnomalyDetector": NotRequired[SingleMetricAnomalyDetectorOutputTypeDef],
        "MetricMathAnomalyDetector": NotRequired[MetricMathAnomalyDetectorOutputTypeDef],
    },
)
GetMetricDataInputGetMetricDataPaginateTypeDef = TypedDict(
    "GetMetricDataInputGetMetricDataPaginateTypeDef",
    {
        "MetricDataQueries": Sequence[MetricDataQueryUnionTypeDef],
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
        "ScanBy": NotRequired[ScanByType],
        "LabelOptions": NotRequired[LabelOptionsTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetMetricDataInputRequestTypeDef = TypedDict(
    "GetMetricDataInputRequestTypeDef",
    {
        "MetricDataQueries": Sequence[MetricDataQueryUnionTypeDef],
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
        "NextToken": NotRequired[str],
        "ScanBy": NotRequired[ScanByType],
        "MaxDatapoints": NotRequired[int],
        "LabelOptions": NotRequired[LabelOptionsTypeDef],
    },
)
PutMetricAlarmInputRequestTypeDef = TypedDict(
    "PutMetricAlarmInputRequestTypeDef",
    {
        "AlarmName": str,
        "EvaluationPeriods": int,
        "ComparisonOperator": ComparisonOperatorType,
        "AlarmDescription": NotRequired[str],
        "ActionsEnabled": NotRequired[bool],
        "OKActions": NotRequired[Sequence[str]],
        "AlarmActions": NotRequired[Sequence[str]],
        "InsufficientDataActions": NotRequired[Sequence[str]],
        "MetricName": NotRequired[str],
        "Namespace": NotRequired[str],
        "Statistic": NotRequired[StatisticType],
        "ExtendedStatistic": NotRequired[str],
        "Dimensions": NotRequired[Sequence[DimensionTypeDef]],
        "Period": NotRequired[int],
        "Unit": NotRequired[StandardUnitType],
        "DatapointsToAlarm": NotRequired[int],
        "Threshold": NotRequired[float],
        "TreatMissingData": NotRequired[str],
        "EvaluateLowSampleCountPercentile": NotRequired[str],
        "Metrics": NotRequired[Sequence[MetricDataQueryUnionTypeDef]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "ThresholdMetricId": NotRequired[str],
    },
)
DeleteAnomalyDetectorInputRequestTypeDef = TypedDict(
    "DeleteAnomalyDetectorInputRequestTypeDef",
    {
        "Namespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Dimensions": NotRequired[Sequence[DimensionTypeDef]],
        "Stat": NotRequired[str],
        "SingleMetricAnomalyDetector": NotRequired[SingleMetricAnomalyDetectorTypeDef],
        "MetricMathAnomalyDetector": NotRequired[MetricMathAnomalyDetectorTypeDef],
    },
)
MetricMathAnomalyDetectorUnionTypeDef = Union[
    MetricMathAnomalyDetectorTypeDef, MetricMathAnomalyDetectorExtraOutputTypeDef
]
PutAnomalyDetectorInputRequestTypeDef = TypedDict(
    "PutAnomalyDetectorInputRequestTypeDef",
    {
        "Namespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Dimensions": NotRequired[Sequence[DimensionTypeDef]],
        "Stat": NotRequired[str],
        "Configuration": NotRequired[AnomalyDetectorConfigurationTypeDef],
        "MetricCharacteristics": NotRequired[MetricCharacteristicsTypeDef],
        "SingleMetricAnomalyDetector": NotRequired[SingleMetricAnomalyDetectorTypeDef],
        "MetricMathAnomalyDetector": NotRequired[MetricMathAnomalyDetectorTypeDef],
    },
)
CloudwatchEventTypeDef = TypedDict(
    "CloudwatchEventTypeDef",
    {
        "version": str,
        "id": str,
        "detail-type": str,
        "source": str,
        "account": str,
        "time": str,
        "region": str,
        "resources": List[str],
        "detail": CloudwatchEventDetailTypeDef,
    },
)
MetricDataQueryAlarmTypeDef = TypedDict(
    "MetricDataQueryAlarmTypeDef",
    {
        "Id": str,
        "MetricStat": NotRequired[MetricStatAlarmTypeDef],
        "Expression": NotRequired[str],
        "Label": NotRequired[str],
        "ReturnData": NotRequired[bool],
        "Period": NotRequired[int],
        "AccountId": NotRequired[str],
    },
)
DescribeAnomalyDetectorsOutputTypeDef = TypedDict(
    "DescribeAnomalyDetectorsOutputTypeDef",
    {
        "AnomalyDetectors": List[AnomalyDetectorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
