import boto3
import time
import json
import random

log_group_name = '/aws/lambda/my-function'
log_stream_name = 'omni-log-stream'
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

cloudtrail_log = {
    "eventVersion": "1.08",
    "userIdentity": {
        "type": "IAMUser",
        "principalId": "AIDA123456789",
        "arn": "arn:aws:iam::123456789012:user/dev-intern",
        "accountId": "123456789012"
    },
    "eventTime": "2026-04-06T21:44:22Z",
    "eventSource": "ec2.amazonaws.com",
    "eventName": "DeleteVpc",
    "awsRegion": "ap-southeast-1",
    "sourceIPAddress": "203.0.113.42",
    "errorCode": "AccessDenied",
    "errorMessage": "User: arn:aws:iam::123456789012:user/dev-intern is not authorized to perform: ec2:DeleteVpc on resource"
}

def generate_random_log(timestamp):
    rand = random.random()
    if rand < 0.7:
        # 70% VPC Flow Log REJECT (Mô phỏng rà quét port)
        ip = f"{random.randint(10, 203)}.{random.randint(0, 255)}.{random.randint(0, 20)}.{random.randint(1, 20)}"
        return {
            'timestamp': timestamp,
            'message': f'2 123456789012 eni-abc123def456 {ip} 10.0.1.55 {random.randint(10000, 60000)} 22 6 20 1800 1620140600 1620140660 REJECT OK'
        }
    elif rand < 0.9:
        # 20% App Logs ERROR
        return {
            'timestamp': timestamp,
            'message': f'[ERROR] App: Nginx Reverse Proxy returned 502 Bad Gateway to the Load Balancer. Node worker #{random.randint(1, 5)} unreachable.'
        }
    else:
        # 10% CloudTrail AccessDenied
        ct = dict(cloudtrail_log)
        ct['eventTime'] = f"2026-04-06T{random.randint(10,23)}:{random.randint(10,59)}:22Z"
        return {
            'timestamp': timestamp,
            'message': json.dumps(ct)
        }

print("Generating 1000 logs...")
all_logs = []
current_time = int(round(time.time() * 1000))
# Tạo dữ liệu lùi về quá khứ 1 tiếng trước cho đa dạng
start_time = current_time - (3600 * 1000)

for i in range(1000):
    all_logs.append(generate_random_log(start_time + i * 1000))

# Định sẵn Token
response = client.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name)
seq_token = response['logStreams'][0].get('uploadSequenceToken')

# Bơm theo từng Batch (Max CloudWatch là 10.000, nén batch 500 là an toàn)
BATCH_SIZE = 500
total_pushed = 0

for i in range(0, len(all_logs), BATCH_SIZE):
    batch = all_logs[i:i + BATCH_SIZE]
    kwargs = {
        'logGroupName': log_group_name,
        'logStreamName': log_stream_name,
        'logEvents': batch,
    }
    if seq_token:
        kwargs['sequenceToken'] = seq_token

    response = client.put_log_events(**kwargs)
    seq_token = response.get('nextSequenceToken')
    total_pushed += len(batch)
    print(f"Pushed batch of {len(batch)} logs. Sequence token updated.")
    time.sleep(1) # delay nhẹ tránh Rate Limit

print(f"✅ Successfully pushed {total_pushed} Omni Logs (VPC Flow + CloudTrail + App) to CloudWatch!")
