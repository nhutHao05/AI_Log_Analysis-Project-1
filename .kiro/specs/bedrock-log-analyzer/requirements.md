# Requirements Document

## Introduction

Module AI phân tích logs sử dụng AWS Bedrock để enhance rule-based detection. Module này là standalone component đọc logs từ local files (giả lập logs từ CloudWatch), phân tích patterns, detect issues, và generate enhanced solutions. Output của module sẽ được team khác integrate vào hệ thống monitoring lớn hơn.

**SCOPE CỦA MODULE NÀY (User đảm nhận):**
- Đọc và parse logs từ local files
- Rule-based detection cho các vấn đề phổ biến
- AI enhancement với AWS Bedrock
- Demo scenarios và testing
- Documentation và usage examples

**OUT OF SCOPE (Team khác đảm nhận):**
- CloudWatch integration và log collection
- Telegram alerts và notifications
- Auto-remediation actions
- Terraform infrastructure setup
- EC2 deployment và Ansible configuration

## Glossary

- **AI_Log_Analyzer**: Module phân tích logs với rule-based detection và AWS Bedrock AI enhancement
- **Log_Parser**: Component parse log entries thành structured data (timestamp, severity, component, message)
- **Pattern_Analyzer**: Component phân tích patterns và trends từ parsed logs
- **Rule_Based_Detector**: Component phát hiện vấn đề dựa trên predefined rules và keywords
- **Bedrock_Enhancer**: Component sử dụng AWS Bedrock để enhance solutions với detailed explanations
- **Demo_Generator**: Component tạo sample logs mô phỏng attack scenarios
- **Log_Entry**: Một dòng log với structured data: timestamp, severity, component, message
- **Error_Pattern**: Pattern được extract từ logs bằng cách normalize UUIDs và numbers
- **Issue_Type**: Loại vấn đề được phát hiện (connection, permission, resource, database issues)
- **Solution**: Đề xuất khắc phục vấn đề (basic từ rules, enhanced từ AI)
- **Analysis_Result**: Output JSON/text format chứa detected issues và solutions

## Requirements

### Requirement 1: Đọc logs từ local files

**User Story:** Là một developer, tôi muốn module đọc logs từ local files (giả lập logs từ CloudWatch), để có thể phân tích logs mà không cần AWS infrastructure.

#### Acceptance Criteria

1. THE AI_Log_Analyzer SHALL đọc log files từ local directory với recursive search
2. THE AI_Log_Analyzer SHALL filter log files theo extension (.log)
3. THE AI_Log_Analyzer SHALL support configurable max_files limit để control số lượng files processed
4. THE AI_Log_Analyzer SHALL search log files cho specific search term (case-insensitive)
5. THE AI_Log_Analyzer SHALL support configurable max_matches limit để control memory usage
6. THE AI_Log_Analyzer SHALL handle file encoding errors gracefully (utf-8 với errors='replace')
7. THE AI_Log_Analyzer SHALL collect matching log entries với file path, line number, và content
8. THE AI_Log_Analyzer SHALL accept log directory path qua command-line argument hoặc config file
9. THE AI_Log_Analyzer SHALL validate log directory exists trước khi processing
10. WHEN log directory không tồn tại, THE AI_Log_Analyzer SHALL return clear error message

### Requirement 2: Parse và phân tích logs

**User Story:** Là một developer, tôi muốn module tự động parse và phân tích logs, để có thể hiểu được patterns và trends trong logs một cách có cấu trúc.

#### Acceptance Criteria

1. WHEN nhận được Log_Entry, THE Log_Parser SHALL extract timestamp theo format ISO 8601 hoặc common log formats
2. WHEN nhận được Log_Entry, THE Log_Parser SHALL extract severity level (ERROR, INFO, WARNING, DEBUG, CRITICAL, WARN, FATAL)
3. WHEN nhận được Log_Entry, THE Log_Parser SHALL extract component name từ brackets [component] hoặc prefix "component:"
4. WHEN nhận được Log_Entry, THE Log_Parser SHALL extract message content sau khi remove timestamp, severity, và component
5. THE Pattern_Analyzer SHALL tính severity distribution (count của mỗi severity level)
6. THE Pattern_Analyzer SHALL tính component distribution (count của logs từ mỗi component)
7. THE Pattern_Analyzer SHALL analyze time patterns (first occurrence, last occurrence, total occurrences)
8. THE Pattern_Analyzer SHALL extract common error patterns bằng cách normalize UUIDs thành <ID> và numbers thành <NUM>
9. THE Pattern_Analyzer SHALL group similar error patterns và count occurrences
10. THE Pattern_Analyzer SHALL identify top 10 most common error patterns
11. THE Pattern_Analyzer SHALL output structured analysis data (JSON format) để dễ integrate với other systems

### Requirement 3: Rule-based detection cho các vấn đề phổ biến

**User Story:** Là một developer, tôi muốn module tự động phát hiện các vấn đề phổ biến bằng rules, để có thể nhanh chóng identify issues mà không cần AI.

#### Acceptance Criteria

1. THE Rule_Based_Detector SHALL detect connection issues bằng keywords: "connection", "timeout", "connect"
2. THE Rule_Based_Detector SHALL detect permission issues bằng keywords: "permission", "access", "denied"
3. THE Rule_Based_Detector SHALL detect resource issues bằng keywords: "memory", "cpu", "capacity", "full"
4. THE Rule_Based_Detector SHALL detect database issues bằng keywords: "database", "db", "sql", "query"
5. THE Rule_Based_Detector SHALL detect security issues bằng keywords: "unauthorized", "forbidden", "authentication failed"
6. WHEN detect issue, THE Rule_Based_Detector SHALL classify Issue_Type (connection, permission, resource, database, security)
7. WHEN detect issue, THE Rule_Based_Detector SHALL calculate severity level dựa trên error count và patterns
8. THE Rule_Based_Detector SHALL generate basic Solution cho mỗi Issue_Type
9. WHEN không detect specific issue, THE Rule_Based_Detector SHALL identify component với most errors và suggest general solution
10. THE Rule_Based_Detector SHALL support custom rules configuration qua config file (JSON format)
11. THE Rule_Based_Detector SHALL output detection results với issue type, severity, affected components, và basic solutions

### Requirement 4: AWS Bedrock AI Enhancement

**User Story:** Là một developer, tôi muốn sử dụng AWS Bedrock để enhance solutions từ rule-based detection, để có detailed explanations và specific steps cho từng vấn đề.

#### Acceptance Criteria

1. THE Bedrock_Enhancer SHALL connect đến AWS Bedrock API sử dụng boto3 và AWS credentials
2. THE Bedrock_Enhancer SHALL support Claude models (claude-3-sonnet, claude-3-haiku) từ AWS Bedrock
3. THE Bedrock_Enhancer SHALL authenticate với AWS sử dụng IAM credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
4. WHEN nhận basic Solution từ Rule_Based_Detector, THE Bedrock_Enhancer SHALL enhance với detailed explanation
5. THE Bedrock_Enhancer SHALL include log examples trong prompt để AI có context (max 3 patterns)
6. THE Bedrock_Enhancer SHALL optimize token usage bằng cách limit log examples và prompt length
7. THE Bedrock_Enhancer SHALL set temperature=0.3-0.5 để có focused và deterministic responses
8. THE Bedrock_Enhancer SHALL set max_tokens=2000 để control response length và cost
9. WHEN AI enhancement fails hoặc timeout, THE Bedrock_Enhancer SHALL fallback về basic Solution
10. THE Bedrock_Enhancer SHALL batch process multiple solutions để optimize API calls (max 5 solutions per batch)
11. THE Bedrock_Enhancer SHALL có configurable timeout (default: 30 seconds per request)
12. THE Bedrock_Enhancer SHALL mark enhanced solutions với flag "ai_enhanced": true
13. THE Bedrock_Enhancer SHALL preserve original solution khi enhance để có thể compare
14. THE Bedrock_Enhancer SHALL log API usage (tokens used, cost estimate) cho mỗi request
15. WHEN AWS credentials không available, THE Bedrock_Enhancer SHALL disable AI enhancement và log warning
16. THE Bedrock_Enhancer SHALL handle AWS API errors gracefully (throttling, quota exceeded, authentication errors)

### Requirement 5: Demo scenarios và sample log generation

**User Story:** Là một developer, tôi muốn có demo scenarios với sample logs, để có thể test module và demo cho stakeholders trong 5 phút.

#### Acceptance Criteria

1. THE Demo_Generator SHALL tạo sample log files mô phỏng realistic attack scenarios
2. THE Demo_Generator SHALL support multiple attack scenarios: SQL injection, brute force login, DDoS, unauthorized access
3. THE Demo_Generator SHALL generate logs với proper format (timestamp, severity, component, message)
4. THE Demo_Generator SHALL tạo logs với varying severity levels (INFO, WARNING, ERROR, CRITICAL)
5. THE Demo_Generator SHALL include normal traffic logs mixed với attack logs để realistic
6. THE Demo_Generator SHALL có configurable parameters: số lượng logs, attack intensity, time range
7. THE Demo_Generator SHALL tạo logs trong directory structure: data/logs/demo/
8. THE Demo_Generator SHALL có script run_demo.sh để automate demo flow
9. THE Demo_Generator SHALL complete demo flow trong vòng 5 phút (generate logs → analyze → show results)
10. THE Demo_Generator SHALL có cleanup script để xóa demo data sau khi test
11. THE Demo_Generator SHALL generate logs cho multiple components (web-server, database, auth-service, api-gateway)
12. THE Demo_Generator SHALL include timestamp patterns để simulate time-based attacks

### Requirement 6: Output format và integration interface

**User Story:** Là một developer, tôi muốn module output results trong format dễ integrate, để team khác có thể sử dụng output trong hệ thống lớn hơn.

#### Acceptance Criteria

1. THE AI_Log_Analyzer SHALL output Analysis_Result trong JSON format
2. THE Analysis_Result SHALL bao gồm metadata: timestamp, search_term, log_directory, total_files_searched, total_matches
3. THE Analysis_Result SHALL bao gồm analysis: severity_distribution, components, time_pattern, error_patterns
4. THE Analysis_Result SHALL bao gồm solutions: problem, solution, ai_enhanced flag, original_solution
5. THE Analysis_Result SHALL bao gồm AI usage info: ai_enhancement_used, bedrock_model_used, tokens_used, estimated_cost
6. THE AI_Log_Analyzer SHALL support output to file (--output flag) hoặc stdout
7. THE AI_Log_Analyzer SHALL có simple text output mode cho console viewing
8. THE AI_Log_Analyzer SHALL validate JSON output structure trước khi write
9. THE AI_Log_Analyzer SHALL include schema version trong output để support future changes
10. THE AI_Log_Analyzer SHALL có example output files trong documentation

### Requirement 7: Command-line interface và usability

**User Story:** Là một developer, tôi muốn có command-line interface dễ sử dụng, để có thể chạy analysis nhanh chóng với different configurations.

#### Acceptance Criteria

1. THE AI_Log_Analyzer SHALL có CLI với arguments: --logs, --term, --output, --verbose, --disable-ai, --model
2. THE AI_Log_Analyzer SHALL có default values cho tất cả arguments
3. THE AI_Log_Analyzer SHALL validate arguments trước khi processing
4. THE AI_Log_Analyzer SHALL show help message với --help flag
5. THE AI_Log_Analyzer SHALL support environment variables cho configuration (AWS_REGION, AWS_PROFILE, BEDROCK_MODEL)
6. THE AI_Log_Analyzer SHALL có .env.example file với configuration examples
7. THE AI_Log_Analyzer SHALL show progress indicators khi processing large log files
8. THE AI_Log_Analyzer SHALL show clear error messages với actionable suggestions
9. THE AI_Log_Analyzer SHALL có verbose mode để show detailed processing steps
10. THE AI_Log_Analyzer SHALL show summary statistics sau khi complete (files processed, issues found, time taken)
11. THE AI_Log_Analyzer SHALL support --dry-run mode để preview actions without executing
12. THE AI_Log_Analyzer SHALL có wrapper script (analyze.sh) để simplify common use cases

### Requirement 8: Documentation và setup instructions

**User Story:** Là một developer mới học cloud, tôi muốn có documentation rõ ràng, để có thể setup và sử dụng module dễ dàng.

#### Acceptance Criteria

1. THE AI_Log_Analyzer SHALL có README.md với clear setup instructions
2. THE README SHALL bao gồm prerequisites: Python version, AWS account, boto3
3. THE README SHALL có step-by-step AWS credentials setup instructions
4. THE README SHALL có example commands cho common use cases
5. THE README SHALL explain output format và how to interpret results
6. THE README SHALL có troubleshooting section cho common issues
7. THE AI_Log_Analyzer SHALL có setup.sh script để automate installation
8. THE Setup_Script SHALL check Python version (>= 3.8)
9. THE Setup_Script SHALL install Python dependencies từ requirements.txt
10. THE Setup_Script SHALL create necessary directories (data/logs, output)
11. THE Setup_Script SHALL validate AWS credentials configuration
12. THE Setup_Script SHALL test Bedrock API connectivity
13. THE AI_Log_Analyzer SHALL có inline code comments explaining logic
14. THE AI_Log_Analyzer SHALL có docstrings cho all functions và classes
15. THE AI_Log_Analyzer SHALL có USAGE.md với detailed usage examples và best practices

### Requirement 9: Cost optimization cho AWS Bedrock

**User Story:** Là một student với budget hạn chế, tôi muốn module optimize chi phí khi sử dụng AWS Bedrock, để không vượt quá budget.

#### Acceptance Criteria

1. THE Bedrock_Enhancer SHALL batch multiple solutions trong single API call khi có thể
2. THE Bedrock_Enhancer SHALL có configurable sampling rate để analyze subset của logs (default: 100%)
3. THE Bedrock_Enhancer SHALL có max_tokens limit để control response length và cost
4. THE Bedrock_Enhancer SHALL use cheaper model (claude-3-haiku) by default, với option upgrade to claude-3-sonnet
5. THE Bedrock_Enhancer SHALL estimate cost trước khi making API calls
6. THE Bedrock_Enhancer SHALL log actual cost sau mỗi API call
7. THE Bedrock_Enhancer SHALL có cost threshold warning (default: $1.00 per run)
8. WHEN cost threshold exceeded, THE Bedrock_Enhancer SHALL prompt user confirmation trước khi continue
9. THE AI_Log_Analyzer SHALL có --disable-ai flag để skip AI enhancement và save cost
10. THE AI_Log_Analyzer SHALL có --max-cost flag để set cost limit per run
11. THE AI_Log_Analyzer SHALL show cost summary trong output (tokens used, estimated cost)
12. THE AI_Log_Analyzer SHALL có cost tracking file (costs.json) để track spending over time

### Requirement 10: Testing và validation

**User Story:** Là một developer, tôi muốn có comprehensive testing, để đảm bảo module hoạt động đúng trước khi demo.

#### Acceptance Criteria

1. THE AI_Log_Analyzer SHALL có unit tests cho Log_Parser với different log formats
2. THE AI_Log_Analyzer SHALL có unit tests cho Pattern_Analyzer với sample data
3. THE AI_Log_Analyzer SHALL có unit tests cho Rule_Based_Detector với known patterns
4. THE AI_Log_Analyzer SHALL có integration tests cho Bedrock_Enhancer với mock API
5. THE AI_Log_Analyzer SHALL có end-to-end tests với sample log files
6. THE AI_Log_Analyzer SHALL có test script (run_tests.sh) để run all tests
7. THE AI_Log_Analyzer SHALL validate output JSON schema trong tests
8. THE AI_Log_Analyzer SHALL test error handling (missing files, invalid logs, API failures)
9. THE AI_Log_Analyzer SHALL có performance tests để ensure processing speed
10. THE AI_Log_Analyzer SHALL test với different attack scenarios (SQL injection, brute force, DDoS)
11. THE AI_Log_Analyzer SHALL có test coverage report
12. THE AI_Log_Analyzer SHALL pass all tests trước khi demo

### Requirement 11: Integration interface cho team khác

**User Story:** Là một team member khác, tôi muốn dễ dàng integrate AI module vào hệ thống lớn hơn, để có thể sử dụng AI analysis trong production system.

#### Acceptance Criteria

1. THE AI_Log_Analyzer SHALL có clear API interface (input/output contract)
2. THE AI_Log_Analyzer SHALL có Python module import capability để use as library
3. THE AI_Log_Analyzer SHALL có example integration code trong documentation
4. THE AI_Log_Analyzer SHALL support callback functions để notify về analysis progress
5. THE AI_Log_Analyzer SHALL có error codes và error messages standardized
6. THE AI_Log_Analyzer SHALL có logging với configurable log levels
7. THE AI_Log_Analyzer SHALL support async processing cho large log files
8. THE AI_Log_Analyzer SHALL có health check endpoint để verify module status
9. THE AI_Log_Analyzer SHALL document all configuration options
10. THE AI_Log_Analyzer SHALL có versioning trong output để support backward compatibility
