"""
Type annotations for cloudwatch service ServiceResource

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cloudwatch.service_resource import CloudWatchServiceResource
    import mypy_boto3_cloudwatch.service_resource as cloudwatch_resources

    session = Session()
    resource: CloudWatchServiceResource = session.resource("cloudwatch")

    my_alarm: cloudwatch_resources.Alarm = resource.Alarm(...)
    my_metric: cloudwatch_resources.Metric = resource.Metric(...)
```
"""

import sys
from datetime import datetime
from typing import Iterator, List, Sequence

from boto3.resources.base import ResourceMeta, ServiceResource
from boto3.resources.collection import ResourceCollection

from .client import CloudWatchClient
from .literals import (
    AlarmTypeType,
    ComparisonOperatorType,
    HistoryItemTypeType,
    ScanByType,
    StandardUnitType,
    StateValueType,
    StatisticType,
)
from .type_defs import (
    DescribeAlarmHistoryOutputTypeDef,
    DimensionFilterTypeDef,
    DimensionTypeDef,
    GetMetricStatisticsOutputTypeDef,
    MetricDataQueryAlarmTypeDef,
    MetricDataQueryTypeDef,
    TagTypeDef,
    TimestampTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "CloudWatchServiceResource",
    "Alarm",
    "Metric",
    "ServiceResourceAlarmsCollection",
    "ServiceResourceMetricsCollection",
    "MetricAlarmsCollection",
)

class ServiceResourceAlarmsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.alarms)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcealarmscollection)
    """

    def all(self) -> "ServiceResourceAlarmsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.alarms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def filter(  # type: ignore
        self,
        *,
        AlarmNames: Sequence[str] = ...,
        AlarmNamePrefix: str = ...,
        AlarmTypes: Sequence[AlarmTypeType] = ...,
        ChildrenOfAlarmName: str = ...,
        ParentsOfAlarmName: str = ...,
        StateValue: StateValueType = ...,
        ActionPrefix: str = ...,
        MaxRecords: int = ...,
        NextToken: str = ...,
    ) -> "ServiceResourceAlarmsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.alarms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def delete(self) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.alarms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def disable_actions(self) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.alarms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def enable_actions(self) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.alarms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def limit(self, count: int) -> "ServiceResourceAlarmsCollection":
        """
        Return at most this many Alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.alarms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceAlarmsCollection":
        """
        Fetch at most this many Alarms per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.alarms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def pages(self) -> Iterator[List["Alarm"]]:
        """
        A generator which yields pages of Alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.alarms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def __iter__(self) -> Iterator["Alarm"]:
        """
        A generator which yields Alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.alarms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

class ServiceResourceMetricsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.metrics)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcemetricscollection)
    """

    def all(self) -> "ServiceResourceMetricsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.metrics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcemetricscollection)
        """

    def filter(  # type: ignore
        self,
        *,
        Namespace: str = ...,
        MetricName: str = ...,
        Dimensions: Sequence[DimensionFilterTypeDef] = ...,
        NextToken: str = ...,
        RecentlyActive: Literal["PT3H"] = ...,
        IncludeLinkedAccounts: bool = ...,
        OwningAccount: str = ...,
    ) -> "ServiceResourceMetricsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.metrics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcemetricscollection)
        """

    def limit(self, count: int) -> "ServiceResourceMetricsCollection":
        """
        Return at most this many Metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.metrics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcemetricscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceMetricsCollection":
        """
        Fetch at most this many Metrics per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.metrics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcemetricscollection)
        """

    def pages(self) -> Iterator[List["Metric"]]:
        """
        A generator which yields pages of Metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.metrics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcemetricscollection)
        """

    def __iter__(self) -> Iterator["Metric"]:
        """
        A generator which yields Metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.metrics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#serviceresourcemetricscollection)
        """

class MetricAlarmsCollection(ResourceCollection):
    def all(self) -> "MetricAlarmsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        Statistic: StatisticType = ...,
        ExtendedStatistic: str = ...,
        Dimensions: Sequence[DimensionTypeDef] = ...,
        Period: int = ...,
        Unit: StandardUnitType = ...,
    ) -> "MetricAlarmsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def delete(self) -> None:
        """
        Batch method.
        """

    def disable_actions(self) -> None:
        """
        Batch method.
        """

    def enable_actions(self) -> None:
        """
        Batch method.
        """

    def limit(self, count: int) -> "MetricAlarmsCollection":
        """
        Return at most this many Alarms.
        """

    def page_size(self, count: int) -> "MetricAlarmsCollection":
        """
        Fetch at most this many Alarms per service request.
        """

    def pages(self) -> Iterator[List["Alarm"]]:
        """
        A generator which yields pages of Alarms.
        """

    def __iter__(self) -> Iterator["Alarm"]:
        """
        A generator which yields Alarms.
        """

class Alarm(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.Alarm)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#alarm)
    """

    alarm_name: str
    alarm_arn: str
    alarm_description: str
    alarm_configuration_updated_timestamp: datetime
    actions_enabled: bool
    ok_actions: List[str]
    alarm_actions: List[str]
    insufficient_data_actions: List[str]
    state_value: StateValueType
    state_reason: str
    state_reason_data: str
    state_updated_timestamp: datetime
    metric_name: str
    namespace: str
    statistic: StatisticType
    extended_statistic: str
    dimensions: List[DimensionTypeDef]
    period: int
    unit: StandardUnitType
    evaluation_periods: int
    datapoints_to_alarm: int
    threshold: float
    comparison_operator: ComparisonOperatorType
    treat_missing_data: str
    evaluate_low_sample_count_percentile: str
    metrics: List[MetricDataQueryAlarmTypeDef]
    threshold_metric_id: str
    evaluation_state: Literal["PARTIAL_DATA"]
    state_transitioned_timestamp: datetime
    name: str
    metric: "Metric"
    meta: "CloudWatchResourceMeta"

    def delete(self) -> None:
        """
        Deletes the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Alarm.delete)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#alarmdelete-method)
        """

    def describe_history(
        self,
        *,
        AlarmTypes: Sequence[AlarmTypeType] = ...,
        HistoryItemType: HistoryItemTypeType = ...,
        StartDate: TimestampTypeDef = ...,
        EndDate: TimestampTypeDef = ...,
        MaxRecords: int = ...,
        NextToken: str = ...,
        ScanBy: ScanByType = ...,
    ) -> DescribeAlarmHistoryOutputTypeDef:
        """
        Retrieves the history for the specified alarm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Alarm.describe_history)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#alarmdescribe_history-method)
        """

    def disable_actions(self) -> None:
        """
        Disables the actions for the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Alarm.disable_actions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#alarmdisable_actions-method)
        """

    def enable_actions(self) -> None:
        """
        Enables the actions for the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Alarm.enable_actions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#alarmenable_actions-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Alarm.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#alarmget_available_subresources-method)
        """

    def load(self) -> None:
        """
        Calls :py:meth:`CloudWatch.Client.describe_alarms` to update the attributes of
        the Alarm
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Alarm.load)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#alarmload-method)
        """

    def reload(self) -> None:
        """
        Calls :py:meth:`CloudWatch.Client.describe_alarms` to update the attributes of
        the Alarm
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Alarm.reload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#alarmreload-method)
        """

    def set_state(
        self, *, StateValue: StateValueType, StateReason: str, StateReasonData: str = ...
    ) -> None:
        """
        Temporarily sets the state of an alarm for testing purposes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Alarm.set_state)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#alarmset_state-method)
        """

_Alarm = Alarm

class Metric(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.Metric)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#metric)
    """

    metric_name: str
    dimensions: List[DimensionTypeDef]
    namespace: str
    name: str
    alarms: MetricAlarmsCollection
    meta: "CloudWatchResourceMeta"

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Metric.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#metricget_available_subresources-method)
        """

    def get_statistics(
        self,
        *,
        StartTime: TimestampTypeDef,
        EndTime: TimestampTypeDef,
        Period: int,
        Dimensions: Sequence[DimensionTypeDef] = ...,
        Statistics: Sequence[StatisticType] = ...,
        ExtendedStatistics: Sequence[str] = ...,
        Unit: StandardUnitType = ...,
    ) -> GetMetricStatisticsOutputTypeDef:
        """
        Gets statistics for the specified metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Metric.get_statistics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#metricget_statistics-method)
        """

    def load(self) -> None:
        """
        Calls :py:meth:`CloudWatch.Client.list_metrics` to update the attributes of the
        Metric
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Metric.load)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#metricload-method)
        """

    def put_alarm(
        self,
        *,
        AlarmName: str,
        EvaluationPeriods: int,
        ComparisonOperator: ComparisonOperatorType,
        AlarmDescription: str = ...,
        ActionsEnabled: bool = ...,
        OKActions: Sequence[str] = ...,
        AlarmActions: Sequence[str] = ...,
        InsufficientDataActions: Sequence[str] = ...,
        Statistic: StatisticType = ...,
        ExtendedStatistic: str = ...,
        Dimensions: Sequence[DimensionTypeDef] = ...,
        Period: int = ...,
        Unit: StandardUnitType = ...,
        DatapointsToAlarm: int = ...,
        Threshold: float = ...,
        TreatMissingData: str = ...,
        EvaluateLowSampleCountPercentile: str = ...,
        Metrics: Sequence[MetricDataQueryTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ThresholdMetricId: str = ...,
    ) -> "_Alarm":
        """
        Creates or updates an alarm and associates it with the specified metric, metric
        math expression, anomaly detection model, or Metrics Insights
        query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Metric.put_alarm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#metricput_alarm-method)
        """

    def put_data(self) -> None:
        """
        Publishes metric data points to Amazon CloudWatch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Metric.put_data)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#metricput_data-method)
        """

    def reload(self) -> None:
        """
        Calls :py:meth:`CloudWatch.Client.list_metrics` to update the attributes of the
        Metric
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Metric.reload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#metricreload-method)
        """

_Metric = Metric

class CloudWatchResourceMeta(ResourceMeta):
    client: CloudWatchClient

class CloudWatchServiceResource(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/)
    """

    meta: "CloudWatchResourceMeta"
    alarms: ServiceResourceAlarmsCollection
    metrics: ServiceResourceMetricsCollection

    def Alarm(self, name: str) -> "_Alarm":
        """
        Creates a Alarm resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.Alarm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#cloudwatchserviceresourcealarm-method)
        """

    def Metric(self, namespace: str, name: str) -> "_Metric":
        """
        Creates a Metric resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.Metric)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#cloudwatchserviceresourcemetric-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.ServiceResource.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/service_resource/#cloudwatchserviceresourceget_available_subresources-method)
        """
