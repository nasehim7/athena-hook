import logging
import pprint
import sys
import boto3
import requests
import time

def actor_usage(name, account, tech, index, errors):
    client = boto3.client('athena')

    # testing to get last (minimum_age) of services used
    query = "SELECT useridentity, eventsource, eventname FROM cloudtrail_logs where eventtime < to_iso8601(current_timestamp - interval '" + str(index) + "' day) order by cloudtrail_logs.eventtime;"
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
    for i in range(len(parent_list)):
        if i != 0:
            sub_list = parent_list[i]['Data']
            principalid_util = sub_list[1]['VarCharValue']
            start_pos = principalid_util.find(",") + 14
            end_pos = principalid_util.find(",", start_pos)
            principalid = principalid_util[start_pos : end_pos]
            util = principalid.find(":")
            role_from_principalid = ""
            if util != -1:
            	role_from_principalid = principalid[util + 1:]
            if role_from_principalid == name:
                key_serviceName = sub_list[3]['VarCharValue'][:-14]
                if key_serviceName not in results:
                    results[key_serviceName] = []
                    results[key_serviceName].append(sub_list[4]['VarCharValue'])
                else:
                    if sub_list[3]['VarCharValue'] not in results[key_serviceName]:
                        results[key_serviceName].append(sub_list[4]['VarCharValue'])
    return results         
