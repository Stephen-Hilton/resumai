# Implementation Plan: Job Application Automation

## Overview

This implementation plan breaks down the job application automation system into discrete, manageable tasks. The system will be built incrementally, starting with core infrastructure, then adding data collection, content generation, document generation, and finally the web UI. Each task builds on previous work, with checkpoints to ensure quality and correctness.

## Tasks

- [x] 1. Set up core infrastructure and data models
  - Create directory structure for events, lib, ui, templates, tests
  - Define EventContext, EventResult, EventError data classes
  - Define JobIdentity, JobModel, JobSource Pydantic models
  - Set up logging utilities (append_app_log, append_job_log)
  - _Requirements: 3.4, 3.5, 14.1_

- [x]* 1.1 Write property test for EventContext immutability
  - **Property 24: Event Context Immutability**
  - **Validates: Requirements 3.7**

- [x] 2. Implement event bus and discovery
  - [x] 2.1 Create event bus with dynamic event discovery
    - Implement discover_events() to scan src/events/ directory
    - Implement run_event() with async execution
    - Implement run_events_parallel() for concurrent execution
    - Add error handling and exception catching
    - _Requirements: 3.1, 3.2, 3.6, 3.7_

  - [x]* 2.2 Write property test for event discovery
    - **Property 7: Event Discovery Completeness**
    - **Validates: Requirements 3.1**

  - [x]* 2.3 Write property test for event error handling
    - **Property 8: Event Execution Error Handling**
    - **Validates: Requirements 3.6**

- [x] 3. Implement job folder management
  - [x] 3.1 Create job folder utilities
    - Implement folder_name() to generate folder names from JobIdentity
    - Implement parse_job_folder_name() to parse folder names
    - Implement slug_part() for sanitization
    - Implement phase_path() for phase directory paths
    - _Requirements: 1.1, 1.2, 1.4_

  - [x]* 3.2 Write property test for folder name round trip
    - **Property 1: Folder Name Round Trip**
    - **Validates: Requirements 1.1, 1.4**

  - [x]* 3.3 Write property test for folder name sanitization
    - **Property 2: Folder Name Sanitization**
    - **Validates: Requirements 1.2**

- [x] 4. Implement create_jobfolder event
  - [x] 4.1 Create create_jobfolder event module
    - Implement execute() to create job folder in 1_Queued
    - Generate unique job ID if not provided
    - Write job.yaml to folder
    - Append to job.log
    - Return EventResult with success status
    - _Requirements: 1.1, 1.3, 1.6_

  - [x]* 4.2 Write property test for unique ID generation
    - **Property 3: Unique ID Generation**
    - **Validates: Requirements 1.3**

  - [x]* 4.3 Write property test for folder creation idempotence
    - **Property 4: Folder Creation Idempotence**
    - **Validates: Requirements 1.6**

- [-] 5. Implement phase transition events
  - [x] 5.1 Create move_* event modules for all phases
    - Implement move_queue, move_data_gen, move_docs_gen
    - Implement move_applied, move_followup, move_interviewing, move_negotiating, move_accepted
    - Implement move_skipped, move_expired, move_errored
    - Preserve all files during moves
    - Append log entry for each transition
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [x]* 5.2 Write property test for phase transition file preservation
    - **Property 5: Phase Transition File Preservation**
    - **Validates: Requirements 2.3, 2.4**

  - [ ]* 5.3 Write property test for phase transition logging
    - **Property 6: Phase Transition Logging**
    - **Validates: Requirements 2.5**

- [ ] 6. Checkpoint - Ensure core infrastructure tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Implement data validation
  - [ ] 7.1 Create validation utilities
    - Implement validate_job_yaml() using Pydantic
    - Implement validate_resume_yaml() with basic checks
    - Return specific error messages for validation failures
    - _Requirements: 4.7, 4.8, 14.1, 14.2, 14.3, 14.5_

  - [ ]* 7.2 Write property test for job YAML validation
    - **Property 9: Job YAML Validation**
    - **Validates: Requirements 4.7, 14.1, 14.2**

- [ ] 8. Implement log_message and notify_user events
  - [ ] 8.1 Create log_message event
    - Implement execute() to append to job.log
    - Format: {YYYY-MM-DD HH:MM:SS} - {context} - {message}
    - _Requirements: 8.1, 8.2_

  - [ ] 8.2 Create notify_user event
    - Implement execute() to send WebSocket message
    - Also call log_message
    - Include job_folder_name in notification
    - _Requirements: 9.1, 9.2, 9.3_

  - [ ]* 8.3 Write property test for log entry format
    - **Property 14: Log Entry Format**
    - **Validates: Requirements 8.2, 8.3**

- [ ] 9. Implement job data collection events
  - [ ] 9.1 Create get_gmail_linkedin event
    - Connect to Gmail via IMAP
    - Search for "LinkedIn Job Alert" emails from last 2 weeks
    - Parse email HTML to extract job listings
    - Create job folders for each listing
    - _Requirements: 4.1, 4.2_

  - [ ] 9.2 Create get_url event
    - Fetch HTML from job.yaml url field
    - Save to job.html
    - Parse HTML based on domain (linkedin.com support)
    - Create or augment job.yaml
    - _Requirements: 4.3, 4.4, 4.5_

- [ ] 10. Implement LLM interface
  - [ ] 10.1 Create LLM abstraction layer
    - Implement generate_content() with OpenAI API
    - Add 5-minute timeout
    - Add retry logic (3 attempts)
    - Track API costs
    - Support configuration via environment variables
    - _Requirements: 5.1, 5.7, 5.8, 5.9_

- [ ] 11. Implement content generation events
  - [ ] 11.1 Create gen_llm_subcontent_* events
    - Implement for: summary, skills, highlights, experience, education, awards, coverletter
    - Read job.yaml and resume.yaml
    - Call LLM interface
    - Write to subcontent.{section}.yaml
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [ ] 11.2 Create gen_static_subcontent_* events
    - Implement for: contacts, summary, skills, highlights, experience, education, awards, coverletter
    - Copy from resume.yaml verbatim
    - Write to subcontent.{section}.yaml
    - Create template for sections that don't exist in resume.yaml
    - _Requirements: 6.1, 6.2, 6.3_

  - [ ]* 11.3 Write property test for static content round trip
    - **Property 10: Static Content Round Trip**
    - **Validates: Requirements 6.1, 6.2**

  - [ ]* 11.4 Write property test for subcontent event configuration
    - **Property 25: Subcontent Event Configuration**
    - **Validates: Requirements 5.3, 6.5**

- [ ] 12. Implement batch_gen_data event
  - [ ] 12.1 Create batch_gen_data event
    - Read subcontent_events from job.yaml
    - Execute all subcontent events serially
    - Move to 2_Data_Generated on success
    - Move to Errored on failure after 3 retries
    - _Requirements: 5.5, 5.6, 5.7_

  - [ ]* 12.2 Write property test for subcontent file completeness
    - **Property 11: Subcontent File Completeness**
    - **Validates: Requirements 7.1, 22.1**

- [ ] 13. Checkpoint - Ensure content generation tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. Implement document generation utilities
  - [ ] 14.1 Create CSS generation
    - Generate main.css with universal styles
    - Generate per-section CSS files (contacts, summary, skills, highlights, experience, education, awards)
    - _Requirements: 7.4, 7.5, 7.6_

  - [ ] 14.2 Create HTML generation
    - Implement generate_resume_html() to combine subcontent files
    - Maintain separate sections with distinct CSS classes
    - Reference all CSS files
    - Implement generate_coverletter_html() from subcontent.coverletter.yaml
    - _Requirements: 7.2, 7.3, 7.8_

  - [ ] 14.3 Create PDF generation
    - Implement generate_pdf() using Playwright
    - Launch headless Chromium
    - Render HTML with print CSS
    - Save PDF
    - _Requirements: 7.7, 7.9_

  - [ ]* 14.4 Write property test for CSS file generation
    - **Property 12: CSS File Generation**
    - **Validates: Requirements 7.4, 7.5**

  - [ ]* 14.5 Write property test for HTML to PDF dependency
    - **Property 13: HTML to PDF Dependency**
    - **Validates: Requirements 22.2**

- [ ] 15. Implement document generation events
  - [ ] 15.1 Create gen_resume_html event
    - Validate all subcontent files exist
    - Call generate_resume_html()
    - Overwrite existing file
    - _Requirements: 7.1, 7.2, 7.10_

  - [ ] 15.2 Create gen_coverletter_html event
    - Validate subcontent.coverletter.yaml exists
    - Call generate_coverletter_html()
    - Overwrite existing file
    - _Requirements: 7.8, 7.10_

  - [ ] 15.3 Create gen_resume_pdf event
    - Validate resume.html exists
    - Call generate_pdf()
    - Overwrite existing file
    - _Requirements: 7.7, 7.10_

  - [ ] 15.4 Create gen_coverletter_pdf event
    - Validate coverletter.html exists
    - Call generate_pdf()
    - Overwrite existing file
    - _Requirements: 7.9, 7.10_

- [ ] 16. Implement batch_gen_docs event
  - [ ] 16.1 Create batch_gen_docs event
    - Execute in sequence: gen_resume_html, gen_coverletter_html, gen_resume_pdf, gen_coverletter_pdf
    - Move to 3_Docs_Generated on success
    - _Requirements: 7.11, 7.12, 22.4_

  - [ ]* 16.2 Write property test for file dependency enforcement
    - **Property 18: File Dependency Enforcement**
    - **Validates: Requirements 22.7**

- [ ] 17. Implement error handling and recovery
  - [ ] 17.1 Add retry logic to event bus
    - Retry failed events up to 3 times
    - Wait for other events to complete before retrying
    - _Requirements: 10.1, 10.2_

  - [ ] 17.2 Create error.md generation
    - Include error details, context, originating phase
    - Include recommended next steps
    - _Requirements: 10.3, 8.7_

  - [ ]* 17.3 Write property test for error file creation
    - **Property 15: Error File Creation**
    - **Validates: Requirements 10.3, 8.7**

  - [ ]* 17.4 Write property test for retry logic
    - **Property 16: Retry Logic**
    - **Validates: Requirements 10.1, 10.2**

- [ ] 18. Implement S3 upload event
  - [ ] 18.1 Create upload_s3 event
    - Read S3_RESUME_BUCKET from .env
    - Upload resume.pdf as resume.{id}.pdf
    - Upload coverletter.pdf as coverletter.{id}.pdf
    - Log S3 URLs to job.log
    - Don't move to Errored on failure
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [ ] 19. Checkpoint - Ensure document generation tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 20. Implement Flask web server
  - [ ] 20.1 Create Flask app structure
    - Set up Flask app with routes
    - Configure static files and templates
    - Add CORS support
    - _Requirements: 12.1_

  - [ ] 20.2 Create WebSocket manager
    - Implement broadcast_toast()
    - Implement broadcast_job_update()
    - Implement broadcast_phase_update()
    - _Requirements: 21.9_

- [ ] 21. Implement dashboard UI
  - [ ] 21.1 Create base HTML template
    - Add ResumAI Dohickey header with rocket icon
    - Add version number
    - Add resume selector dropdown with refresh button
    - Add action buttons: Fetch Jobs from Email, Add Job by URL, Manually Enter Job
    - _Requirements: 12.2, 12.3, 12.4_

  - [ ] 21.2 Create phases sidebar
    - Display all phase names with counts
    - Calculate All Active and All Jobs counts
    - Make phase names clickable for filtering
    - Highlight selected phase
    - _Requirements: 12.5, 12.6, 12.7, 26.1, 26.2, 26.3, 26.4_

  - [ ] 21.3 Create job cards grid
    - Display 2-3 cards per row
    - Show company, title, date, location, salary, source, tags
    - Show phase and Move to dropdown
    - Show total file count
    - _Requirements: 12.8, 12.13, 16.1, 16.2, 16.3_

  - [ ] 21.4 Create app logs panel
    - Display on right side
    - Read from src/logs/{YYYYMMDD}.applog.txt every 1 second
    - Display most recent 100 entries
    - Auto-scroll to bottom
    - Use monospace 6pt font
    - Handle log rotation at midnight
    - _Requirements: 12.10, 12.11, 12.12, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7, 23.8, 23.9, 23.10, 23.11_

- [ ] 22. Implement job card UI variations
  - [ ] 22.1 Create Queued phase job card
    - Display subcontent state section
    - Show file state icon (☑️ or ✅) and generation type icon (⚙️ or 🧠)
    - Make generation type icons clickable to toggle
    - Add "Generate Resume Data" button
    - Add "Or, skip this Job" button
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5, 17.6, 17.7, 17.8, 17.9, 17.10_

  - [ ] 22.2 Create Data Generated phase job card
    - Display subcontent file status (✅ or ❌)
    - Display Next Steps section
    - Show HTML/PDF status with 🔒 for locked PDFs
    - Add "Generate All Resume Docs" button
    - Add links to job.yaml editor, job.log viewer, Error.md viewer
    - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5, 18.6, 18.7, 18.8_

  - [ ] 22.3 Create Docs Generated and higher phase job card
    - Display all file statuses
    - Show ⚠️ icon for Error.md if exists
    - No generation buttons
    - Allow viewing all files through clickable links
    - _Requirements: 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7, 19.8_

- [ ] 23. Implement interactive UI elements
  - [ ] 23.1 Add click handlers for navigation
    - Company/title → job detail page
    - Source → open URL in new tab
    - Subcontent names → open yaml file for editing
    - File names → open file for viewing
    - _Requirements: 20.1, 20.2, 20.3, 20.4, 20.5, 20.6, 20.7_

  - [ ] 23.2 Add click handlers for actions
    - Generation type icons → toggle LLM/static
    - Move to dropdown → trigger move_* event
    - Generate buttons → trigger batch events
    - _Requirements: 20.8, 20.9_

  - [ ] 23.3 Add visual feedback
    - Hover effects for clickable elements
    - Cursor changes
    - Loading indicators
    - _Requirements: 20.10_

- [ ] 24. Implement dynamic UI updates
  - [ ] 24.1 Add WebSocket client
    - Connect to WebSocket server
    - Handle toast notifications
    - Handle job updates
    - Handle phase updates
    - _Requirements: 21.1, 21.2, 21.3, 21.4_

  - [ ] 24.2 Implement real-time icon updates
    - Update file status icons as events complete
    - Change 🔒 to ▶️ when dependencies met
    - Update total file count
    - _Requirements: 21.5, 21.6, 21.7, 21.8, 21.10_

  - [ ]* 24.3 Write property test for WebSocket message delivery
    - **Property 21: WebSocket Message Delivery**
    - **Validates: Requirements 21.1, 21.2, 21.3, 21.4**

- [ ] 25. Implement API endpoints
  - [ ] 25.1 Create job management endpoints
    - POST /api/toggle_generation
    - POST /api/generate_data
    - POST /api/generate_docs
    - POST /api/move_phase
    - _Requirements: 17.6, 17.7, 17.8, 18.6, 20.9_

  - [ ] 25.2 Create data collection endpoints
    - POST /api/fetch_email
    - POST /api/add_url
    - POST /api/manual_entry
    - _Requirements: 24.1, 24.2, 24.3, 24.4, 24.5, 24.6_

  - [ ] 25.3 Create utility endpoints
    - GET /api/logs
    - GET /api/job_stats
    - GET /api/resumes
    - POST /api/refresh_resumes
    - _Requirements: 23.2, 26.2, 25.2, 25.6_

- [ ] 26. Implement resume selection
  - [ ] 26.1 Create resume discovery
    - Scan resumes/ directory for .yaml files
    - Populate dropdown
    - _Requirements: 25.1, 25.2_

  - [ ] 26.2 Implement resume persistence
    - Save selected resume to configuration
    - Load on page load
    - Use for all content generation
    - _Requirements: 25.5, 25.7, 25.8_

  - [ ]* 26.3 Write property test for resume selection persistence
    - **Property 20: Resume Selection Persistence**
    - **Validates: Requirements 25.5, 25.7, 25.8**

- [ ] 27. Implement phase filtering
  - [ ] 27.1 Create filtering logic
    - Filter jobs by selected phase
    - Calculate phase counts
    - Update "Jobs in <phase name>" header
    - _Requirements: 26.5, 26.6, 26.7, 26.8_

  - [ ]* 27.2 Write property test for phase count accuracy
    - **Property 17: Phase Count Accuracy**
    - **Validates: Requirements 26.2, 26.4**

- [ ] 28. Implement batch processing
  - [ ] 28.1 Create batch processing button
    - Add "Process All Jobs in Queue" button
    - Trigger batch_gen_data for all queued jobs
    - Trigger batch_gen_docs for all data-generated jobs
    - Process serially to avoid concurrency limits
    - _Requirements: 27.1, 27.2, 27.3_

  - [ ] 28.2 Add batch processing feedback
    - Update icons in real-time
    - Display toast for each completion
    - Show summary notification at end
    - _Requirements: 27.4, 27.5, 27.6, 27.7_

  - [ ]* 28.3 Write property test for batch processing completeness
    - **Property 19: Batch Processing Completeness**
    - **Validates: Requirements 27.4, 27.9**

- [ ] 29. Implement log file rotation
  - [ ] 29.1 Add daily log rotation
    - Close current log at midnight
    - Create new log with next day's date
    - Compress old logs
    - _Requirements: 8.6, 23.8_

  - [ ]* 29.2 Write property test for log file rotation
    - **Property 22: Log File Rotation**
    - **Validates: Requirements 8.6, 23.8**

- [ ] 30. Implement folder name correction
  - [ ] 30.1 Add folder validation and correction
    - Check folder name matches job.yaml
    - Rename if mismatch found
    - _Requirements: 1.4, 1.5_

  - [ ]* 30.2 Write property test for folder name correction
    - **Property 23: Folder Name Correction**
    - **Validates: Requirements 1.5**

- [ ] 31. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 32. Integration testing and polish
  - [ ] 32.1 Test end-to-end workflows
    - Create job → Generate data → Generate docs → Move to Applied
    - Test error recovery and retry logic
    - Test batch processing
    - _Requirements: All_

  - [ ] 32.2 Add error handling polish
    - Improve error messages
    - Add user-friendly error displays
    - Test all error paths
    - _Requirements: 10.1-10.7_

  - [ ] 32.3 Performance optimization
    - Optimize file I/O
    - Cache frequently accessed data
    - Test with large job queues
    - _Requirements: Performance considerations_

  - [ ] 32.4 Security review
    - Validate all file paths
    - Sanitize all user inputs
    - Review API key handling
    - _Requirements: Security considerations_

## Notes

- Tasks marked with `*` are optional property-based tests and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The implementation follows the event-driven architecture specified in the design
- All events are async and support parallel execution
- The UI updates in real-time via WebSocket
- The system is local-first with optional cloud storage (S3)
