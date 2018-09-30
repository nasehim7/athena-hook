import logging
import pprint
import sys
import boto3
import requests

def actor_usage(name, account, tech, index, errors):
    client = boto3.client('athena')

    # testing to get last 20 days data
    query = "SELECT * FROM cloudtrail_logs where eventtime > to_iso8601(current_timestamp - interval '20' day) order by cloudtrail_logs.eventtime asc limit 100;"
    first_query = athena.start_query_execution(
        QueryString = query,
        QueryExecutionContext = {
            'Database': 'sampledb'
        },
        ResultConfiguration = {
            'OutputLocation': 's3://<OutputBucket>',  # Populate it with the bucket which contains cloudtrail logs
        }
    )
    logging.info(pprint.pformat(result))
    QueryId = result['QueryExecutionId']

    second_query = athena.get_query_results(
        QueryExecutionId=QueryId
    )

    print result

    """results = {}
    for event_source in response.aggregations.group_by_eventSource.buckets:
        for event_name in event_source.group_by_eventName.buckets:
            event_source_short = event_source.key.split('.amazonaws.com')[0]
            key = "{es}:{en}".format(es=event_source_short, en=event_name.key)
            if key in results:
                results[key] += event_name.doc_count
            else:
                results[key] = event_name.doc_count

    return [k for k in results.keys()]"""
