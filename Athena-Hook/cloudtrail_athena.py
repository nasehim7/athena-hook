import logging
import pprint
import sys
import boto3
import requests

def actor_usage(name, account, tech, index, errors):
    client = boto3.client('athena')

    # testing to get last (minimum_age) of services used
    query = "SELECT * FROM cloudtrail_logs where eventtime < to_iso8601(current_timestamp - interval '" + str(index) + "' day) order by cloudtrail_logs.eventtime asc limit 100;"
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

    results = {}

    parent_list = second_query['ResultSet']['Rows']
    for i in range(len(parent_list)):
        if i != 0:
            sub_list = parent_list[i]['Data']
            principalid_util = sub_list[1]['VarCharValue']
            start_pos = principalid_util.find(",") + 14
            end_pos = principalid_util.find(",", start_pos)
            principalid = principalid_util[start_pos : end_pos]
            role_from_principalid = principalid[principalid.find(":") + 1 :]

            if role_from_principalid == name:
                key_serviceName = sub_list[3]['VarCharValue'][:-14]
                if key_serviceName not in results:
                    results[key_serviceName] = []
                else:
                    if sub_list[4]['VarCharValue'] not in results[key_serviceName]:
                        results[key_serviceName].append(sub_list[4]['VarCharValue'])
    
    return results         
