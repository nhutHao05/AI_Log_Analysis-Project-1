# Bedrock Log Analyzer UI

Web interface for analyzing CloudWatch logs with AWS Bedrock AI enhancement.

## Features

- Pull logs from AWS CloudWatch
- Analyze patterns and detect issues
- AI-enhanced solutions using AWS Bedrock (Nova Micro)
- Interactive web interface with Streamlit
- Export results as JSON/CSV

## Quick Start

### 1. Setup

```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

### 2. Configure AWS

```bash
aws configure
# Or use IAM role on EC2
```

### 3. Update .env

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run

```bash
streamlit run streamlit_app.py
```

Open http://localhost:8501

## Configuration

Edit `.env` file:

```bash
AWS_REGION=ap-southeast-1
AWS_PROFILE=default
BEDROCK_MODEL=us.amazon.nova-micro-v1:0
STREAMLIT_SERVER_PORT=8501
```

## IAM Permissions Required

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "logs:GetLogEvents"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": "*"
    }
  ]
}
```

## Supported Models

- `us.amazon.nova-micro-v1:0` (default, fastest & cheapest)
- `amazon.nova-micro-v1:0` (in-region)
- `claude-3-haiku`
- `claude-3-sonnet`

## Supported Regions

Nova Micro is available in:
- ap-southeast-1 (Singapore)
- ap-southeast-2 (Sydney)
- ap-northeast-1 (Tokyo)
- us-east-1, us-east-2, us-west-2
- eu-central-1, eu-west-1, eu-west-3

## Cost Estimation

- Nova Micro: ~$0.001 per analysis
- Claude Haiku: ~$0.005 per analysis
- Claude Sonnet: ~$0.025 per analysis

## Docker Deployment

```bash
docker build -t bedrock-analyzer .
docker run -p 8501:8501 \
  -e AWS_REGION=ap-southeast-1 \
  -v ~/.aws:/root/.aws \
  bedrock-analyzer
```

## Troubleshooting

### AWS Credentials Error
```bash
aws sts get-caller-identity
```

### Port Already in Use
```bash
streamlit run streamlit_app.py --server.port=8502
```

### Bedrock Access Denied
Check IAM permissions and model availability in your region.

## Project Structure

```
bedrock-log-analyzer-ui/
├── streamlit_app.py          # Main Streamlit UI
├── cloudwatch_client.py      # CloudWatch integration
├── src/                      # Analysis modules
│   ├── models.py            # Data models
│   ├── log_parser.py        # Log parsing
│   ├── pattern_analyzer.py  # Pattern analysis
│   ├── rule_detector.py     # Issue detection
│   └── bedrock_enhancer.py  # AI enhancement
├── requirements.txt          # Dependencies
├── .env.example             # Environment template
├── setup.sh                 # Setup script
└── Dockerfile               # Docker image
```

## License

MIT
