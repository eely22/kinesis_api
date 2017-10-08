[![Deployment status from DeployBot](https://bluz.deploybot.com/badge/66802254036135/98581.svg)](http://deploybot.com)

Kinesis API
==========
AWS Kinesis is a stream based delivery system where large amounts of data can be processed. Producers create events
which are then put into the stream, and consumers read the events in order and process them. One stream can be broken
into many shards, where each shard has guaranteed ordering.

Kinesis does not have a REST API front-end that can be used by producers to insert data into a stream. This project uses
API Gateway and Lambda functions to do just that. Data can be sent to the REST API and it will be inserted into the
requested kinesis stream.

## Endpoint
All functions use the common endpoint https://api.banc.io

## Kinesis
/kinesis/{stream name}

### POST
Post a new event to the specified kinesis stream

#### Arguments

The following arguments must be passed in the data body:
- event: data to be passed to the kinesis stream

The following arguments can optionally be passed in the data body:
- region: region the stream will be loacted within (default 'us-west-2')
- partition_key: string value used to determine which shard the data is placed. passing the same value guarantees the
events would be in the same shard.

#### Response:
Returning http code can be as follows:

Code | Description 
--- | --- 
200| Success
400| Bad Request
500| Server Error

#### Example:
```
curl --header 'Content-Type:application/json; charset=UTF-8' -d '{"event": {"hello": "world"}' https://api.banc.io/kinesis/test-stream
```
