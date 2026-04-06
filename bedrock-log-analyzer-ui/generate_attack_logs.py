import boto3
import time

log_group_name = '/aws/lambda/my-function'
log_stream_name = 'security-attack-stream'
region = 'ap-southeast-1'

print("Connecting to CloudWatch Logs in " + region)
client = boto3.client('logs', region_name=region)

try:
    client.create_log_group(logGroupName=log_group_name)
except client.exceptions.ResourceAlreadyExistsException:
    pass

try:
    client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    print("Created Log Stream: " + log_stream_name)
except client.exceptions.ResourceAlreadyExistsException:
    print("Log Stream already exists.")

timestamp = int(round(time.time() * 1000))

# Giả lập 3 vụ tấn công khét lẹt
log_events = [
    {
        'timestamp': timestamp,
        'message': '[SECURITY] Nginx: Possible SQL Injection detected from IP 192.168.45.12 - Request: GET /api/users?id=1%27%20OR%20%271%27%3D%271 HTTP/1.1 403 Forbidden'
    },
    {
        'timestamp': timestamp + 1000,
        'message': '[AUTH_FAILED] SSHd: Failed password for root from 203.0.113.42 port 58492 ssh2'
    },
    {
        'timestamp': timestamp + 2000,
        'message': '[AUTH_FAILED] SSHd: Failed password for root from 203.0.113.42 port 58495 ssh2'
    },
    {
        'timestamp': timestamp + 3000,
        'message': '[AUTH_FAILED] SSHd: Failed password for root from 203.0.113.42 port 58498 ssh2 - Possible Brute Force Attack'
    },
    {
        'timestamp': timestamp + 4000,
        'message': '[SECURITY] WebApp: Path Traversal attempt blocked from IP 10.0.0.99. URI: /../../../etc/passwd'
    }
]

kwargs = {
    'logGroupName': log_group_name,
    'logStreamName': log_stream_name,
    'logEvents': log_events,
}

response = client.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name)
if 'uploadSequenceToken' in response['logStreams'][0]:
    kwargs['sequenceToken'] = response['logStreams'][0]['uploadSequenceToken']

response = client.put_log_events(**kwargs)

print(f"Successfully pushed {len(log_events)} ATTACK log events to CloudWatch!")
