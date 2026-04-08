# Implementation Plan: AI Log Analyzer với AWS Bedrock

## Overview

Implement standalone AI log analysis module sử dụng rule-based detection kết hợp AWS Bedrock AI enhancement. Module đọc logs từ local files, phân tích patterns, detect issues phổ biến, và generate enhanced solutions. Implementation được chia thành 10 tasks theo thứ tự logic từ setup đến demo hoàn chỉnh.

**Target Users**: Developers mới học cloud (first cloud project)
**Implementation Language**: Python 3.8+
**Key Technologies**: boto3, AWS Bedrock, hypothesis (property testing)

## Tasks

- [x] 1. Project setup và AWS configuration
  - [x] 1.1 Create project structure và directories
    - Create src/ directory với __init__.py
    - Create tests/ với subdirectories: unit/, property/, integration/, fixtures/
    - Create scripts/, config/, data/logs/, data/output/, docs/ directories
    - Create requirements.txt với dependencies: boto3>=1.34.0, python-dotenv>=1.0.0, hypothesis>=6.92.0, pytest>=7.4.0, pytest-cov>=4.1.0, moto>=4.2.0
    - _Requirements: 8.9, 8.10_
  
  - [x] 1.2 Create configuration files
    - Create .env.example với AWS configuration variables (AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BEDROCK_MODEL, MAX_COST_PER_RUN)
    - Create config/rules.json với detection rules cho 5 issue types (connection, permission, resource, database, security)
    - Create config/bedrock.json với model configurations (claude-3-haiku, claude-3-sonnet) và cost per token
    - _Requirements: 3.10, 7.5, 7.6_
  
  - [x] 1.3 Create setup script
    - Write scripts/setup.sh để check Python version >= 3.8
    - Install dependencies từ requirements.txt
    - Create necessary directories nếu chưa tồn tại
    - Validate AWS credentials configuration
    - Test Bedrock API connectivity
    - _Requirements: 8.7, 8.8, 8.11, 8.12_
  
  - [ ]* 1.4 Write unit tests for setup validation
    - Test directory creation logic
    - Test Python version checking
    - Test AWS credentials validation
    - _Requirements: 8.8, 8.11_

- [ ] 2. Implement Log Parser component
  - [ ] 2.1 Create data models
    - Create src/models.py với dataclasses: LogEntry, Match, ErrorPattern, AnalysisData, Issue, Solution, EnhancedSolution, AnalysisResult
    - Include proper type hints và docstrings
    - _Requirements: 2.1, 2.2, 2.3, 2.4_
  
  - [ ] 2.2 Implement log parsing functions
    - Create src/log_parser.py với LogParser class
    - Implement parse_log_entry() để extract timestamp (ISO 8601 và common formats), severity (ERROR, INFO, WARNING, DEBUG, CRITICAL, WARN, FATAL), component (từ [component] hoặc "component:"), message
    - Implement find_log_files() với recursive directory search và .log extension filtering
    - Implement search_files_for_term() với case-insensitive search và max_matches limit
    - Handle encoding errors gracefully (utf-8 với errors='replace')
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 2.1, 2.2, 2.3, 2.4_
  
  - [ ]* 2.3 Write unit tests for Log Parser
    - Test parse_log_entry() với different timestamp formats
    - Test severity extraction cho all levels
    - Test component extraction từ brackets và colon prefix
    - Test message extraction
    - Test encoding error handling
    - Test file filtering và recursive search
    - _Requirements: 10.1_
  
  - [ ]* 2.4 Write property tests for Log Parser
    - **Property 1: Log file filtering** - Validates: Requirements 1.1, 1.2, 1.3
    - **Property 2: Case-insensitive search** - Validates: Requirements 1.4, 1.5
    - **Property 3: Match structure completeness** - Validates: Requirements 1.7
    - **Property 5: Timestamp extraction** - Validates: Requirements 2.1
    - **Property 6: Severity extraction** - Validates: Requirements 2.2
    - **Property 7: Component extraction** - Validates: Requirements 2.3
    - **Property 8: Message extraction** - Validates: Requirements 2.4
    - _Requirements: 10.1_

- [ ] 3. Implement Pattern Analyzer component
  - [ ] 3.1 Implement pattern analysis functions
    - Create src/pattern_analyzer.py với PatternAnalyzer class
    - Implement analyze_log_entries() để calculate severity distribution, component distribution, time patterns (first/last occurrence, total occurrences)
    - Implement extract_error_patterns() với normalization (UUIDs → <ID>, numbers → <NUM>)
    - Implement pattern grouping và count occurrences
    - Implement top 10 pattern selection sorted by frequency
    - _Requirements: 2.5, 2.6, 2.7, 2.8, 2.9, 2.10_
  
  - [ ]* 3.2 Write unit tests for Pattern Analyzer
    - Test severity distribution calculation
    - Test component distribution calculation
    - Test time pattern analysis
    - Test pattern normalization với UUIDs và numbers
    - Test pattern grouping
    - Test top 10 selection
    - _Requirements: 10.2_
  
  - [ ]* 3.3 Write property tests for Pattern Analyzer
    - **Property 9: Distribution calculations** - Validates: Requirements 2.5, 2.6
    - **Property 10: Time pattern analysis** - Validates: Requirements 2.7
    - **Property 11: Pattern normalization** - Validates: Requirements 2.8
    - **Property 12: Pattern grouping** - Validates: Requirements 2.9
    - **Property 13: Top patterns selection** - Validates: Requirements 2.10
    - **Property 14: Analysis output round trip** - Validates: Requirements 2.11
    - _Requirements: 10.2_

- [ ] 4. Checkpoint - Core parsing và analysis complete
  - Ensure all tests pass cho Log Parser và Pattern Analyzer
  - Verify data models work correctly
  - Ask user if questions arise về parsing logic hoặc pattern analysis

- [ ] 5. Implement Rule-Based Detector component
  - [ ] 5.1 Implement detection logic
    - Create src/rule_detector.py với RuleBasedDetector class
    - Implement detect_issues() với keyword matching cho 5 issue types: connection (keywords: connection, timeout, connect), permission (keywords: permission, access, denied), resource (keywords: memory, cpu, capacity, full), database (keywords: database, db, sql, query), security (keywords: unauthorized, forbidden, authentication failed)
    - Implement classify_issue_type() based on keywords
    - Implement severity calculation (HIGH, MEDIUM, LOW) based on error count và pattern frequency
    - Implement generate_basic_solution() cho mỗi Issue_Type
    - Implement fallback logic: identify component với most errors khi không detect specific issue
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9_
  
  - [ ] 5.2 Implement custom rules support
    - Implement load_custom_rules() để read config/rules.json
    - Apply custom rules trong detection logic
    - _Requirements: 3.10_
  
  - [ ]* 5.3 Write unit tests for Rule-Based Detector
    - Test detection cho mỗi issue type với known patterns
    - Test severity calculation
    - Test basic solution generation
    - Test fallback detection
    - Test custom rules loading và application
    - _Requirements: 10.3_
  
  - [ ]* 5.4 Write property tests for Rule-Based Detector
    - **Property 15: Keyword-based issue detection** - Validates: Requirements 3.1-3.6
    - **Property 16: Severity calculation** - Validates: Requirements 3.7
    - **Property 17: Solution generation** - Validates: Requirements 3.8
    - **Property 18: Fallback detection** - Validates: Requirements 3.9
    - **Property 19: Custom rules application** - Validates: Requirements 3.10
    - **Property 20: Detection output structure** - Validates: Requirements 3.11
    - _Requirements: 10.3_

- [ ] 6. Implement AWS Bedrock integration
  - [ ] 6.1 Implement Bedrock Enhancer core
    - Create src/bedrock_enhancer.py với BedrockEnhancer class
    - Implement __init__() để initialize boto3 Bedrock Runtime client với AWS credentials
    - Implement is_available() để check AWS credentials configuration
    - Implement graceful degradation khi credentials không available
    - _Requirements: 4.1, 4.3, 4.15_
  
  - [ ] 6.2 Implement prompt engineering và API calls
    - Implement enhance_solutions() với prompt template: problem, basic solution, log examples (max 3 patterns)
    - Set API parameters: temperature=0.3-0.5, max_tokens=2000, timeout=30 seconds
    - Implement retry logic với exponential backoff (3 retries)
    - Handle API errors: throttling, quota exceeded, authentication errors, timeout
    - Fallback to basic solution on API failure
    - _Requirements: 4.2, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 4.11, 4.16_
  
  - [ ] 6.3 Implement batching và cost optimization
    - Implement batch_enhance() để process max 5 solutions per API call
    - Implement estimate_cost() based on prompt tokens và completion tokens
    - Implement cost logging sau mỗi API call
    - Mark enhanced solutions với ai_enhanced=true flag
    - Preserve original solution trong output
    - _Requirements: 4.10, 4.12, 4.13, 4.14, 9.1_
  
  - [ ]* 6.4 Write integration tests for Bedrock Enhancer
    - Test Bedrock API integration với mocked AWS (moto)
    - Test prompt construction
    - Test error handling và fallback
    - Test batching logic
    - Test cost estimation
    - _Requirements: 10.4_
  
  - [ ]* 6.5 Write property tests for Bedrock Enhancer
    - **Property 21: AI enhancement quality** - Validates: Requirements 4.4
    - **Property 22: Log examples inclusion** - Validates: Requirements 4.5, 4.6
    - **Property 23: Fallback on AI failure** - Validates: Requirements 4.9
    - **Property 24: Solution batching** - Validates: Requirements 4.10
    - **Property 25: Timeout configuration** - Validates: Requirements 4.11
    - **Property 26: Enhanced solution marking** - Validates: Requirements 4.12
    - **Property 27: Original solution preservation** - Validates: Requirements 4.13
    - **Property 28: API usage logging** - Validates: Requirements 4.14
    - **Property 29: Graceful degradation without credentials** - Validates: Requirements 4.15
    - _Requirements: 10.4_

- [ ] 7. Checkpoint - AI enhancement complete
  - Ensure all tests pass cho Bedrock Enhancer
  - Test với real AWS Bedrock API (nếu credentials available)
  - Verify cost estimation accuracy
  - Ask user if questions arise về AI integration hoặc cost optimization

- [ ] 8. Implement Demo Generator component
  - [ ] 8.1 Implement demo log generation
    - Create src/demo_generator.py với DemoGenerator class
    - Implement generate_attack_logs() cho 4 scenarios: SQL injection, brute force login, DDoS, unauthorized access
    - Implement generate_normal_logs() với realistic traffic patterns
    - Generate logs với proper format: timestamp (ISO 8601), severity (INFO, WARNING, ERROR, CRITICAL), component ([web-server], [database], [auth-service], [api-gateway]), message
    - Implement timestamp patterns: clustered for attacks, distributed for normal traffic
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.11, 5.12_
  
  - [ ] 8.2 Implement log mixing và file creation
    - Implement mix_logs() với configurable ratio (default: 70% normal, 30% attack)
    - Implement write_to_files() để create logs trong data/logs/demo/ directory
    - Support configurable parameters: num_logs, attack_intensity, time_range
    - _Requirements: 5.5, 5.6, 5.7_
  
  - [ ] 8.3 Create demo scripts
    - Create scripts/demo.sh để automate demo flow: generate logs → analyze → show results
    - Create scripts/cleanup.sh để remove demo data
    - Ensure demo completes trong 5 phút
    - _Requirements: 5.8, 5.9, 5.10_
  
  - [ ]* 8.4 Write unit tests for Demo Generator
    - Test log format validity (parseable by Log Parser)
    - Test severity variation
    - Test normal/attack log mixing ratio
    - Test configurable parameters
    - Test file creation
    - _Requirements: 10.10_
  
  - [ ]* 8.5 Write property tests for Demo Generator
    - **Property 30: Demo log format validity** - Validates: Requirements 5.1, 5.3
    - **Property 31: Severity variation in demo logs** - Validates: Requirements 5.4
    - **Property 32: Normal/attack log mixing** - Validates: Requirements 5.5
    - **Property 33: Demo log parameters** - Validates: Requirements 5.6
    - **Property 34: Demo file creation** - Validates: Requirements 5.7
    - **Property 35: Cleanup functionality** - Validates: Requirements 5.10
    - **Property 36: Component variety in demo** - Validates: Requirements 5.11
    - **Property 37: Timestamp patterns in demo** - Validates: Requirements 5.12
    - _Requirements: 10.10_

- [ ] 9. Implement CLI và output formatting
  - [ ] 9.1 Implement main CLI entry point
    - Create analyze_logs.py với argparse CLI: --logs (log directory), --term (search term), --output (output file), --verbose, --disable-ai, --model, --max-cost, --dry-run, --help
    - Implement default values cho all arguments
    - Implement argument validation
    - Implement environment variable support (AWS_REGION, AWS_PROFILE, BEDROCK_MODEL)
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_
  
  - [ ] 9.2 Implement output formatting
    - Implement JSON output với AnalysisResult structure: metadata (timestamp, search_term, log_directory, total_files_searched, total_matches), analysis (severity_distribution, components, time_pattern, error_patterns), solutions (problem, solution, ai_enhanced, original_solution), ai_info (ai_enhancement_used, bedrock_model_used, tokens_used, estimated_cost), schema_version
    - Implement text output mode cho console viewing
    - Implement JSON validation trước khi write
    - Support output to file hoặc stdout
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9_
  
  - [ ] 9.3 Implement progress indicators và logging
    - Show progress indicators khi processing large log files
    - Implement verbose mode với detailed processing steps
    - Show summary statistics: files processed, issues found, time taken
    - Show clear error messages với actionable suggestions
    - _Requirements: 7.7, 7.8, 7.9, 7.10_
  
  - [ ] 9.4 Implement cost control features
    - Implement cost estimation trước khi making API calls
    - Implement cost threshold warning (default: $1.00 per run)
    - Prompt user confirmation khi cost threshold exceeded
    - Implement --max-cost flag để set cost limit
    - Implement cost tracking file (costs.json) với daily/monthly totals
    - Show cost summary trong output
    - _Requirements: 9.5, 9.6, 9.7, 9.8, 9.10, 9.11, 9.12_
  
  - [ ] 9.5 Create wrapper script
    - Create scripts/analyze.sh để simplify common use cases
    - _Requirements: 7.12_
  
  - [ ]* 9.6 Write property tests for CLI và output
    - **Property 38: Analysis result round trip** - Validates: Requirements 6.1
    - **Property 39: Output structure completeness** - Validates: Requirements 6.2-6.5
    - **Property 40: Output mode support** - Validates: Requirements 6.6
    - **Property 41: JSON validation** - Validates: Requirements 6.8
    - **Property 42: Schema versioning** - Validates: Requirements 6.9
    - **Property 43: Default argument values** - Validates: Requirements 7.2
    - **Property 44: Argument validation** - Validates: Requirements 7.3
    - **Property 45: Environment variable support** - Validates: Requirements 7.5
    - **Property 46: Error message clarity** - Validates: Requirements 7.8
    - **Property 47: Verbose mode output** - Validates: Requirements 7.9
    - **Property 48: Summary statistics** - Validates: Requirements 7.10
    - **Property 49: Dry-run mode** - Validates: Requirements 7.11
    - **Property 54: Cost estimation** - Validates: Requirements 9.5
    - **Property 55: Cost logging** - Validates: Requirements 9.6
    - **Property 56: Cost threshold warning** - Validates: Requirements 9.7
    - **Property 57: AI disable flag** - Validates: Requirements 9.9
    - **Property 58: Max cost enforcement** - Validates: Requirements 9.10
    - **Property 59: Cost summary** - Validates: Requirements 9.11
    - **Property 60: Cost tracking persistence** - Validates: Requirements 9.12

- [ ] 10. Checkpoint - Core implementation complete
  - Ensure all tests pass
  - Run end-to-end test với sample logs
  - Verify cost tracking works correctly
  - Ask user if questions arise về CLI hoặc output formatting

- [ ] 11. Testing và validation
  - [ ]* 11.1 Write end-to-end tests
    - Test complete analysis flow: logs → parsing → analysis → detection → enhancement → output
    - Test với different attack scenarios (SQL injection, brute force, DDoS, unauthorized access)
    - Test error handling: missing files, invalid logs, API failures
    - _Requirements: 10.5, 10.8, 10.10_
  
  - [ ]* 11.2 Write performance tests
    - Test processing speed cho 1000 log entries (target: < 30 seconds với AI)
    - Test memory usage với large log files
    - _Requirements: 10.9_
  
  - [ ]* 11.3 Generate test coverage report
    - Run pytest với coverage: pytest --cov=src --cov-report=html tests/
    - Verify coverage >= 80% cho unit tests
    - Verify all properties implemented
    - _Requirements: 10.11_
  
  - [ ] 11.4 Create test script
    - Create scripts/run_tests.sh để run all tests
    - _Requirements: 10.6_

- [ ] 12. Demo scenarios và documentation
  - [ ] 12.1 Create demo scenarios
    - Create 4 demo scenarios với sample logs: SQL injection attack, brute force login attack, DDoS attack, database connection issues
    - Document expected detection results cho mỗi scenario
    - Verify demo flow completes trong 5 phút
    - _Requirements: 5.8, 5.9_
  
  - [ ] 12.2 Write README.md
    - Write clear setup instructions
    - Document prerequisites: Python 3.8+, AWS account, boto3
    - Include step-by-step AWS credentials setup
    - Provide example commands cho common use cases
    - Explain output format và interpretation
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_
  
  - [ ] 12.3 Write USAGE.md
    - Document detailed usage examples
    - Include best practices
    - Document all CLI arguments và options
    - Provide integration examples (Python module usage, callback support, async processing)
    - _Requirements: 8.15, 11.2, 11.3, 11.4_
  
  - [ ] 12.4 Write troubleshooting guide
    - Document common issues và solutions: AWS credentials not found, Bedrock model access denied, API timeout, high costs, out of memory
    - Include example use cases: daily security audit, performance investigation, cost-optimized analysis, batch processing
    - _Requirements: 8.6_
  
  - [ ] 12.5 Add code documentation
    - Add inline comments explaining logic
    - Add docstrings cho all functions và classes
    - _Requirements: 8.13, 8.14_
  
  - [ ] 12.6 Create example output files
    - Generate example JSON output files
    - Include trong docs/ directory
    - _Requirements: 6.10_

- [ ] 13. Cost optimization và final polish
  - [ ] 13.1 Implement additional cost optimizations
    - Implement sampling rate configuration (default: 100%)
    - Verify batching works correctly (max 5 solutions per batch)
    - Verify token limit enforcement (max_tokens=2000)
    - Test với cheaper model (claude-3-haiku) by default
    - _Requirements: 9.1, 9.2, 9.3, 9.4_
  
  - [ ] 13.2 Implement integration interface features
    - Add Python module import capability
    - Implement callback functions cho progress notifications
    - Implement standardized error codes
    - Implement configurable logging levels
    - Implement health check function
    - _Requirements: 11.1, 11.4, 11.5, 11.6, 11.8, 11.9_
  
  - [ ] 13.3 Add security features
    - Implement input validation để prevent directory traversal
    - Add PII masking cho sensitive data (IPs, emails, tokens)
    - Document IAM policy recommendations
    - _Requirements: Security considerations từ design_
  
  - [ ]* 13.4 Write property tests for integration features
    - **Property 61: Callback invocation** - Validates: Requirements 11.4
    - **Property 62: Error code consistency** - Validates: Requirements 11.5
    - **Property 63: Log level configuration** - Validates: Requirements 11.6
    - **Property 65: Output versioning** - Validates: Requirements 11.10
    - **Property 51: Solution batching optimization** - Validates: Requirements 9.1
    - **Property 52: Sampling rate** - Validates: Requirements 9.2
    - **Property 53: Token limit enforcement** - Validates: Requirements 9.3

- [ ] 14. Final validation và demo preparation
  - [ ] 14.1 Run complete test suite
    - Run all unit tests, property tests, integration tests
    - Verify test coverage >= 80%
    - Fix any failing tests
    - _Requirements: 10.12_
  
  - [ ] 14.2 Test demo flow end-to-end
    - Run scripts/setup.sh
    - Run scripts/demo.sh với all 4 scenarios
    - Verify demo completes trong 5 phút
    - Verify output quality và accuracy
    - Test scripts/cleanup.sh
    - _Requirements: 5.9, 10.12_
  
  - [ ] 14.3 Validate cost optimization
    - Test với --disable-ai flag
    - Test với --max-cost flag
    - Verify cost tracking file updates correctly
    - Test cost threshold warnings
    - _Requirements: 9.7, 9.8, 9.9, 9.10_
  
  - [ ] 14.4 Final documentation review
    - Review README.md completeness
    - Review USAGE.md accuracy
    - Verify all example commands work
    - Check troubleshooting guide coverage
    - _Requirements: 8.1-8.15_
  
  - [ ] 14.5 Create release checklist
    - Verify all requirements implemented
    - Verify all tests pass
    - Verify documentation complete
    - Verify demo works end-to-end
    - Create example .env file
    - Tag release version

## Notes

- Tasks marked với `*` are optional testing tasks và có thể skip cho faster MVP
- Mỗi task được design để complete trong 1-2 giờ
- Checkpoints (tasks 4, 7, 10) ensure incremental validation
- Property tests validate universal correctness properties từ design document
- Unit tests validate specific examples và edge cases
- Focus on simplicity và ease of use cho người mới học cloud
- Cost optimization là priority cao để support student budget
- Demo flow phải complete trong 5 phút để easy demonstration
