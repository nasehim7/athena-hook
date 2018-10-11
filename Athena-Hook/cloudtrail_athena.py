import logging
import pprint
import sys
import boto3
import requests
import time

def actor_usage(name, account, tech, index, errors):
    client = boto3.client('athena')

    # testing to get last (minimum_age) of services used
    query = "SELECT useridentity, eventsource, eventname FROM cloudtrail_logs where eventtime > to_iso8601(current_timestamp - interval '" + str(index) + "' day) order by cloudtrail_logs.eventtime asc limit 100;"
    query_id = athena.start_query_execution(
        QueryString = query,
        QueryExecutionContext = {
            'Database': 'sampledb'
        },
        ResultConfiguration = {
            'OutputLocation': 's3://<OutputBucket>',  # Populate it with the bucket which contains cloudtrail logs
        }
    )['QueryExecutionId']

    query_status = None
    while query_status == 'QUEUED' or query_status == 'RUNNING' or query_status is None:
	query_status = client.get_query_execution(QueryExecutionId=query_id)['QueryExecution']['Status']['State']
	if query_status == 'FAILED' or query_status == 'CANCELLED':
            raise Exception('Athena query with the string "{}" failed or was cancelled'.format(query_string))
	time.sleep(5)

    second_query = athena.get_query_results(
        QueryExecutionId=query_id
    )

    results = {}

    parent_list = second_query['ResultSet']['Rows']
    for i in parent_list[1:]:
        sub_list = i['Data']
        principalid_util = sub_list[1]['VarCharValue']
        principalid = principalid_util.split(',')[1].split('=')[1].split(':')[0]
        if principalid not in results:
        	results[principalid] = {}
        eventSource = sub_list[3]['VarCharValue']
        eventName = sub_list[4]['VarCharValue']
        key_serviceName = eventSource.split('.')[0]
        if key_serviceName not in results[principalid]:
            results[principalid][key_serviceName] = []
            results[principalid][key_serviceName].append(eventName)
        else:
            if eventName not in results[principalid][key_serviceName]:
                results[principalid][key_serviceName].append(eventName)
    return results         
