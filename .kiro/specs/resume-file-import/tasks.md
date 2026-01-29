# Implementation Plan: Resume File Import

## Overview

This implementation plan covers adding file import functionality to the Create/Edit Resume screen, including S3 temp storage, presigned URL uploads, AI-powered field mapping via Nova Micro, and a downloadable YAML template.

## Tasks

- [x] 1. Infrastructure Setup
  - [x] 1.1 Create S3 temp bucket for file uploads
    - Add `skillsnap-imports-temp` bucket to `infrastructure/stacks/s3_stack.py`
    - Configure CORS for browser uploads
    - Add lifecycle policy for cleanup (1 day expiration)
    - _Requirements: 4.1, 4.3_
  
  - [x] 1.2 Create Lambda for presigned URL generation
    - Create `infrastructure/lambdas/resume/import_url.py`
    - Generate presigned PUT URL with 60-second expiry
    - Validate filename and content type
    - Return S3 key in format `temp-imports/{userid}/{timestamp}-{filename}`
    - _Requirements: 4.2, 4.4, 4.5_
  
  - [x] 1.3 Create Lambda for file processing
    - Create `infrastructure/lambdas/resume/import_process.py`
    - Retrieve file from S3
    - Parse YAML/JSON directly, extract text from PDF
    - Send to Nova Micro with ResumeJSON schema
    - Validate response and apply defaults for missing fields
    - Delete temp file after processing
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_
  
  - [x] 1.4 Add Lambda functions to Lambda stack
    - Add `resume-import-url` and `resume-import-process` to `infrastructure/stacks/lambda_stack.py`
    - Grant S3 read/write permissions for temp bucket
    - Grant Bedrock invoke permissions
    - _Requirements: 4.4_
  
  - [x] 1.5 Add API Gateway endpoints
    - Add `POST /resumes/import/url` endpoint
    - Add `POST /resumes/import/process` endpoint
    - Configure Cognito authorization
    - _Requirements: 4.4_

- [x] 2. Checkpoint - Deploy and test infrastructure
  - Deploy CDK stack
  - Test presigned URL generation via API
  - Test file upload to S3
  - Test file processing Lambda
  - Ensure all tests pass, ask the user if questions arise.

- [x] 3. Frontend - API Integration
  - [x] 3.1 Add API methods for import
    - Add `getImportUrl(filename, contentType)` to `webapp/src/services/api.ts`
    - Add `processImport(s3Key)` to `webapp/src/services/api.ts`
    - _Requirements: 4.5, 6.1_
  
  - [x] 3.2 Create import service module
    - Create `webapp/src/services/importService.ts`
    - Implement file validation (size, type)
    - Implement presigned URL upload flow
    - Implement process request and response handling
    - _Requirements: 2.3, 2.4, 2.5_

- [x] 4. Frontend - UI Components
  - [x] 4.1 Update ResumeEditor layout
    - Shorten Resume Name input field width
    - Add "Load from File" button with upload icon
    - Add "Download Template" button with download icon
    - Style buttons to match existing UI
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  
  - [x] 4.2 Implement file picker functionality
    - Add hidden file input with accept filter for YAML, JSON, PDF
    - Wire "Load from File" button to trigger file input
    - Validate selected file before upload
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  
  - [x] 4.3 Implement progress overlay
    - Create loading overlay with spinner
    - Display "Analyzing resume file..." text
    - Disable buttons during processing
    - Prevent modal close during processing
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  
  - [x] 4.4 Implement import result handling
    - Populate form fields with mapped data on success
    - Display error message on failure
    - Preserve existing form data on error
    - Re-enable buttons after completion
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_
  
  - [x] 4.5 Implement template download
    - Create `webapp/public/skillsnap-resume-template.yaml` with full template
    - Wire "Download Template" button to trigger download
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 5. Checkpoint - Test frontend integration
  - Test file selection and validation
  - Test upload progress indication
  - Test successful import populates form
  - Test error handling preserves form data
  - Test template download
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Security and Error Handling
  - [x] 6.1 Add MIME type validation
    - Validate content type matches file extension in Lambda
    - Return 400 error for mismatched types
    - _Requirements: 9.1_
  
  - [x] 6.2 Add input sanitization
    - Sanitize extracted text before sending to Nova Micro
    - Remove potential script tags and injection patterns
    - _Requirements: 9.5_
  
  - [x] 6.3 Implement comprehensive error messages
    - Add user-friendly error messages for all failure scenarios
    - Log detailed errors for debugging
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 7. Final Checkpoint
  - End-to-end test: upload YAML file, verify form populated
  - End-to-end test: upload JSON file, verify form populated
  - End-to-end test: upload PDF file, verify form populated
  - Test template round-trip: download template, fill, import
  - Test error scenarios: oversized file, invalid format, network error
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Property-Based Tests
  - [x] 8.1 Write property test for file validation
    - **Property 1: File Validation Rejects Invalid Inputs**
    - **Validates: Requirements 2.3, 2.4, 2.5**
  
  - [x] 8.2 Write property test for S3 key generation
    - **Property 2: Upload Produces Valid Unique S3 Key**
    - **Validates: Requirements 4.1, 4.2, 4.5**
  
  - [x] 8.3 Write property test for AI response validation
    - **Property 5: AI Response Produces Valid ResumeJSON**
    - **Validates: Requirements 5.5, 5.7**
  
  - [x] 8.4 Write property test for template round-trip
    - **Property 9: Template Round-Trip Mapping**
    - **Validates: Requirements 7.3, 7.5**

## Notes

- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Deploy to AWS after each checkpoint per project guidelines
