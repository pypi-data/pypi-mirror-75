from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.models import BaseOperator, SkipMixin
from airflow.utils.decorators import apply_defaults

from awehflow.operators.flow import EventEmittingOperator
from awehflow.utils import utc_now


class BigQueryJobOperator(BigQueryOperator):
    """Exactly like BigQueryOperator, except that it pushes the job_id to xcom"""
    def execute(self, context):
        if self.bq_cursor is None:
            self.log.info('Executing: %s', self.sql)
            hook = BigQueryHook(
                bigquery_conn_id=self.bigquery_conn_id,
                use_legacy_sql=self.use_legacy_sql,
                delegate_to=self.delegate_to,
                location=self.location,
            )
            conn = hook.get_conn()
            self.bq_cursor = conn.cursor()

        job_id = self.bq_cursor.run_query(
            sql=self.sql,
            destination_dataset_table=self.destination_dataset_table,
            write_disposition=self.write_disposition,
            allow_large_results=self.allow_large_results,
            flatten_results=self.flatten_results,
            udf_config=self.udf_config,
            maximum_billing_tier=self.maximum_billing_tier,
            maximum_bytes_billed=self.maximum_bytes_billed,
            create_disposition=self.create_disposition,
            query_params=self.query_params,
            labels=self.labels,
            schema_update_options=self.schema_update_options,
            priority=self.priority,
            time_partitioning=self.time_partitioning,
            api_resource_configs=self.api_resource_configs,
            cluster_fields=self.cluster_fields,
        )
        self.log.info('BigQuery job: {}'.format(job_id))
        return job_id


class BigQueryJobTaskMetricOperator(EventEmittingOperator):
    """
    Neeeds help
    """

    @apply_defaults
    def __init__(
            self,
            task_ids=None,
            bigquery_conn_id='bigquery_default',
            *args, **kwargs):
        """
        :param task_ids: List of task_ids saying which tasks to sink their job_metrics for
        """

        super(BigQueryJobTaskMetricOperator, self).__init__(*args, **kwargs)
        if task_ids is None:
            task_ids = []
        self.task_ids = task_ids
        self.bigquery_conn_id = bigquery_conn_id

    def execute(self, context):
        hook = BigQueryHook(
            bigquery_conn_id=self.bigquery_conn_id
        )
        jobs = hook.get_service().jobs()

        for task_id in self.task_ids:
            job_id = context['task_instance'].xcom_pull(task_ids=task_id)
            if job_id:
                job = jobs.get(
                    projectId=hook.project_id,
                    jobId=job_id
                ).execute()
                self.emit_event('task_metric', {
                    'run_id': context['dag_run'].run_id,
                    'dag_id': self.dag.dag_id,
                    'job_name': context['task'].params.get('job_name', ''),
                    'task_id': task_id,
                    'value': job,
                    'created_time': utc_now(),
                    'reference_time': context['next_execution_date']
                })


class BigQueryShortCircuitOperator(BaseOperator, SkipMixin):
    """
    A "short circuit" operator that can be used a a "pre check" system.  The supplied sql statement should turn a single BOOL column.

    If the BOOL value is TRUE then downstream processors will execute as normal.
    If the BOOL value is FALSE then any downstream processors will be skipped.

    """

    template_fields = ('sql',)
    template_ext = ('.sql',)

    @apply_defaults
    def __init__(
            self,
            sql,
            bigquery_conn_id='bigquery_default',
            use_legacy_sql=True,
            *args, **kwargs):
        super(BigQueryShortCircuitOperator, self).__init__(*args, **kwargs)
        self.sql = sql
        self.bigquery_conn_id = bigquery_conn_id
        self.use_legacy_sql = use_legacy_sql

    def execute(self, context):
        records = self.db_hook.get_first(self.sql)
        success = records and all([bool(r) for r in records])

        if success:
            return

        self.log.info('Skipping downstream tasks...')

        downstream_tasks = context['task'].get_flat_relatives(upstream=False)
        self.log.debug("Downstream task_ids %s", downstream_tasks)

        if downstream_tasks:
            self.skip(context['dag_run'], context['ti'].execution_date, downstream_tasks)

        self.log.info("Done.")

    @property
    def db_hook(self):
        return BigQueryHook(bigquery_conn_id=self.bigquery_conn_id, use_legacy_sql=self.use_legacy_sql)