# Implementation Plan: Skillsnap MVP

## Overview

This implementation plan builds the Skillsnap application incrementally, starting with infrastructure and core data models, then building out authentication, API layer, generation logic, and finally the React frontend. Each task builds on previous work to ensure no orphaned code.

## Tasks

- [x] 1. Set up project structure and CDK infrastructure foundation
  - [x] 1.1 Initialize CDK Python project with standard structure
    - Create `infrastructure/` directory with `app.py` and `stacks/` subdirectory
    - Configure CDK for us-west-2 region
    - Set up Python virtual environment and requirements.txt
    - _Requirements: 17.1, 17.2_
  
  - [x] 1.2 Create DynamoDB tables stack
    - Define USER, USER_EMAIL, USER_USERNAME, USER_PREF, JOB, USER_JOB, RESUME, RESUME_URL tables
    - Configure partition keys and sort keys per data model
    - Set up on-demand billing for serverless scaling
    - _Requirements: 15.1, 15.4, 15.5_
  
  - [x] 1.3 Write property tests for DynamoDB key structure
    - **Property 6: Resume CRUD Round-Trip**
    - **Property 40: Email Uniqueness Enforcement**
    - **Property 41: Username Uniqueness Enforcement**
    - **Validates: Requirements 4.1, 15.2, 15.3**

- [x] 2. Implement S3 and CloudFront infrastructure
  - [x] 2.1 Create S3 buckets stack
    - Create skillsnap-landing bucket for static landing page
    - Create skillsnap-webapp bucket for React app
    - Create skillsnap-public-resumes bucket for generated files
    - Configure bucket policies for CloudFront access
    - _Requirements: 2.1, 3.1, 10.6_
  
  - [x] 2.2 Create CloudFront distributions
    - Set up distribution for skillsnap.me (landing page)
    - Set up distribution for app.skillsnap.me (webapp)
    - Set up distribution for *.skillsnap.me (resume URLs)
    - Configure Route53 DNS records and ACM certificates
    - _Requirements: 2.1, 3.1, 11.1, 17.5_
  
  - [x] 2.3 Implement CloudFront Function for URL rewriting
    - Create function to extract username from subdomain
    - Implement passthrough for /assets/*, /_global/*, favicon.ico, robots.txt, sitemap.xml
    - Implement rewriting for /{company}/{job} → /{username}/{company}/{job}/index.html
    - Implement rewriting for deeper paths with username prefix
    - _Requirements: 11.2, 11.3, 11.4_
  
  - [x] 2.4 Write property tests for CloudFront Function
    - **Property 28: CloudFront URL Rewriting**
    - **Property 29: CloudFront Global Asset Passthrough**
    - **Property 30: CloudFront Override CSS Rewriting**
    - **Validates: Requirements 11.2, 11.3, 11.4**

- [x] 3. Checkpoint - Infrastructure foundation
  - Ensure CDK synth succeeds without errors
  - Verify all stacks are properly linked

- [x] 4. Implement Cognito authentication stack
  - [x] 4.1 Create Cognito User Pool and App Client
    - Configure user pool with email/password authentication
    - Set up Google OAuth identity provider
    - Configure hosted UI domain
    - Set up callback URLs for app.skillsnap.me
    - _Requirements: 1.1, 1.2, 1.3_
  
  - [x] 4.2 Implement post-confirmation Lambda trigger
    - Create Lambda to handle new user registration
    - Generate uuid7 for userid
    - Create USER, USER_EMAIL, USER_USERNAME records
    - Handle duplicate email/username errors
    - _Requirements: 1.2, 15.2, 15.3_
  
  - [x] 4.3 Configure Gmail OAuth scope for LinkedIn Job Alerts
    - Add Gmail readonly scope to Google OAuth config
    - Store refresh token securely in USER table
    - _Requirements: 1.6_
  
  - [x] 4.4 Write property tests for authentication
    - **Property 1: OAuth Account Linking Consistency**
    - **Property 3: Unauthenticated Request Rejection**
    - **Validates: Requirements 1.2, 3.2, 14.2**

- [x] 5. Implement API Gateway and core Lambda infrastructure
  - [x] 5.1 Create API Gateway stack
    - Set up REST API at api.skillsnap.me
    - Configure Cognito authorizer for all endpoints
    - Set up CORS for app.skillsnap.me origin
    - _Requirements: 14.1, 14.2_
  
  - [x] 5.2 Create shared Lambda layer
    - Create layer with common dependencies (boto3, uuid7, etc.)
    - Create shared utilities for DynamoDB operations
    - Create shared error handling and response formatting
    - _Requirements: 14.4, 17.3_
  
  - [x] 5.3 Write property tests for API responses
    - **Property 39: API Status Code Accuracy**
    - **Validates: Requirements 14.4, 14.5**

- [x] 6. Implement Resume Lambda functions
  - [x] 6.1 Implement resume-create Lambda
    - Accept resume JSON in request body
    - Validate against ResumeJSON schema
    - Store in RESUME table with userid and resumename
    - Return created resume
    - _Requirements: 4.1, 4.4_
  
  - [x] 6.2 Implement resume-get and resume-list Lambdas
    - Get single resume by userid and resumename
    - List all resumes for authenticated user
    - _Requirements: 4.1_
  
  - [x] 6.3 Implement resume-update Lambda
    - Validate updated JSON against schema
    - Update resumejson and lastupdate fields
    - _Requirements: 4.2_
  
  - [x] 6.4 Implement resume-delete Lambda
    - Delete resume from RESUME table
    - Return confirmation
    - _Requirements: 4.5_
  
  - [x] 6.5 Write property tests for resume operations
    - **Property 6: Resume CRUD Round-Trip**
    - **Property 7: Resume JSON Schema Validation**
    - **Property 8: Resume Deletion Completeness**
    - **Validates: Requirements 4.1, 4.2, 4.4, 4.5**

- [x] 7. Checkpoint - Resume API complete
  - Ensure all resume endpoints work end-to-end
  - Run all property tests

- [x] 8. Implement Job Lambda functions
  - [x] 8.1 Implement job-create-manual Lambda
    - Accept job details in request body
    - Generate uuid7 for jobid
    - Create jobtitlesafe from jobtitle
    - Store in JOB table
    - Create USER_JOB with phase "Search"
    - Apply user's default generation type preferences
    - _Requirements: 5.3, 5.4, 5.5, 13.3_
  
  - [x] 8.2 Implement job-create-url Lambda
    - Accept URL in request body
    - Scrape job posting page
    - Extract jobcompany, jobtitle, jobdesc, joblocation, jobsalary, jobposteddate, jobtags
    - Create JOB and USER_JOB records
    - _Requirements: 5.2, 5.6_
  
  - [x] 8.3 Implement job-create-gmail Lambda
    - Use stored Gmail refresh token
    - Search for LinkedIn Job Alert emails
    - Extract job listings from emails
    - Create JOB and USER_JOB records for each
    - _Requirements: 5.1_
  
  - [x] 8.4 Implement job-get and job-list Lambdas
    - Get single job with USER_JOB data
    - List jobs with optional phase filter
    - Support "All Active" and "All Jobs" aggregations
    - _Requirements: 3.6, 3.7, 3.8_
  
  - [x] 8.5 Implement job-update-phase Lambda
    - Validate phase is one of 11 valid values
    - Update USER_JOB.jobphase
    - _Requirements: 6.5, 12.1, 12.6_
  
  - [x] 8.6 Implement job-delete Lambda
    - Delete USER_JOB record
    - Optionally delete JOB if no other users reference it
    - _Requirements: 5.4_
  
  - [x] 8.7 Write property tests for job operations
    - **Property 4: Phase Filter Accuracy**
    - **Property 5: All Jobs Filter Completeness**
    - **Property 9: Job Creation with UUID7**
    - **Property 10: Job Creation Initial Phase**
    - **Property 11: Job Data Extraction Completeness**
    - **Property 13: Posting Age Calculation**
    - **Property 14: Phase Update Persistence**
    - **Property 32: Valid Phase Values**
    - **Property 38: New Job Preference Application**
    - **Validates: Requirements 3.6, 3.8, 5.4, 5.5, 5.6, 6.3, 6.5, 12.1, 13.3**

- [x] 9. Implement User Preferences Lambda functions
  - [x] 9.1 Implement user-prefs-get Lambda
    - Retrieve all preferences for authenticated user
    - Return as key-value object
    - _Requirements: 13.1_
  
  - [x] 9.2 Implement user-prefs-update Lambda
    - Accept preference updates
    - Validate prefname follows default_gen_{subcomponent} pattern
    - Store in USER_PREF table
    - _Requirements: 13.2, 13.4_
  
  - [x] 9.3 Write property tests for preferences
    - **Property 36: User Preference Storage**
    - **Property 37: Default Generation Type Preference**
    - **Validates: Requirements 13.1, 13.2, 13.4**

- [x] 10. Checkpoint - Job and Preferences API complete
  - Ensure all job and preference endpoints work
  - Run all property tests

- [x] 11. Implement SQS and generation infrastructure
  - [x] 11.1 Create SQS queues
    - Create generation queue for subcomponent tasks
    - Create dead letter queue for failed messages
    - Configure visibility timeout and retry policy
    - _Requirements: 16.1, 16.5_
  
  - [x] 11.2 Implement gen-subcomponent Lambda (SQS triggered)
    - Parse SQS message for userid, jobid, resumeid, component, generationType
    - Fetch resume and job data from DynamoDB
    - Route to AI or manual generation based on type
    - Store result in USER_JOB data field
    - Update generation state to "complete" or "error"
    - _Requirements: 7.5, 8.5, 16.3_
  
  - [x] 11.3 Implement AI generation logic
    - Build prompt combining resume section with job description
    - Call Bedrock Nova Micro model
    - Parse response and extract HTML content
    - Implement retry logic (up to 3 times)
    - _Requirements: 8.1, 8.2, 8.4, 8.6_
  
  - [x] 11.4 Implement manual generation logic
    - Extract corresponding section from resume JSON
    - Convert to lean HTML structure (no inline styles)
    - Return formatted HTML
    - _Requirements: 9.3_
  
  - [x] 11.5 Write property tests for generation
    - **Property 17: Generate All Queue Count**
    - **Property 18: AI Generation Input Composition**
    - **Property 19: Manual Generation Structure**
    - **Property 20: Generation Output HTML Validity**
    - **Property 21: Generation Content Storage**
    - **Property 42: Async Queue Immediate Return**
    - **Property 43: SQS Processing Status Update**
    - **Validates: Requirements 7.5, 7.8, 8.2, 8.4, 8.5, 9.3, 16.1, 16.2, 16.3**

- [x] 12. Implement generation API endpoints
  - [x] 12.1 Implement generate-all endpoint
    - Queue 8 SQS messages (one per subcomponent)
    - Update all generation states to "generating"
    - Return immediately with pending status
    - _Requirements: 7.8, 16.2_
  
  - [x] 12.2 Implement generate-single endpoint
    - Accept component name in path
    - Validate component is one of 8 valid values
    - Check generation state is not "locked"
    - Queue single SQS message
    - Update generation state to "generating"
    - _Requirements: 7.2, 7.3_
  
  - [x] 12.3 Implement generation-status endpoint
    - Return current state for all 8 subcomponents
    - Return current data content if complete
    - _Requirements: 7.4, 7.5_
  
  - [x] 12.4 Implement generation-type-toggle endpoint
    - Accept component name and new type
    - Update USER_JOB type field
    - _Requirements: 7.7_
  
  - [x] 12.5 Write property tests for generation API
    - **Property 15: Generation State Machine**
    - **Property 16: Generation Type Toggle**
    - **Validates: Requirements 7.2, 7.3, 7.7**

- [x] 13. Checkpoint - Generation system complete
  - Test full generation flow end-to-end
  - Verify SQS processing and status updates
  - Run all property tests

- [x] 14. Implement final file generation
  - [x] 14.1 Implement gen-final-html Lambda
    - Aggregate all 8 subcomponents into resume.html
    - Include global CSS links (/assets/resume-base.css)
    - Generate coverletter.html from cover letter subcomponent
    - Include global CSS links (/assets/cover-base.css)
    - _Requirements: 10.2, 10.4, 11.6_
  
  - [x] 14.2 Implement gen-final-pdf Lambda
    - Convert resume.html to resume.pdf
    - Convert coverletter.html to coverletter.pdf
    - Use headless browser or PDF library
    - _Requirements: 10.3, 10.5_
  
  - [x] 14.3 Implement S3 upload and URL registration
    - Upload files to /{username}/{company}/{jobtitlesafe}/
    - Update USER_JOB s3loc fields
    - Create RESUME_URL record for uniqueness
    - _Requirements: 10.6, 10.7, 11.5_
  
  - [x] 14.4 Implement final file API endpoints
    - POST /jobs/{id}/final/resume-html
    - POST /jobs/{id}/final/resume-pdf
    - POST /jobs/{id}/final/cover-html
    - POST /jobs/{id}/final/cover-pdf
    - Check all subcomponents complete before allowing
    - _Requirements: 10.1_
  
  - [x] 14.5 Write property tests for final files
    - **Property 23: Final File Enable Condition**
    - **Property 24: Resume HTML Aggregation**
    - **Property 25: PDF Generation Round-Trip**
    - **Property 26: Final File S3 Path**
    - **Property 27: S3 Location Field Update**
    - **Property 31: Resume URL Uniqueness**
    - **Property 32: Generated HTML Global CSS Links**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.6, 10.7, 11.5, 11.6**

- [x] 15. Implement automatic phase transitions
  - [x] 15.1 Add phase transition logic to job creation
    - Transition to "Queued" when all required data is present
    - _Requirements: 12.3_
  
  - [x] 15.2 Add phase transition logic to generation
    - Transition to "Generating" when first subcomponent starts
    - Transition to "Ready" when all final files complete
    - _Requirements: 12.4, 12.5_
  
  - [x] 15.3 Implement job expiration Lambda (scheduled)
    - Run daily via EventBridge schedule
    - Find jobs older than 30 days not in terminal phases
    - Transition to "Expired"
    - _Requirements: 12.7_
  
  - [x] 15.4 Write property tests for phase transitions
    - **Property 34: Automatic Phase Transitions**
    - **Property 35: Job Expiration**
    - **Validates: Requirements 12.3, 12.4, 12.5, 12.7**

- [x] 16. Checkpoint - Backend complete
  - Verify all API endpoints work
  - Test full job lifecycle from creation to final files
  - Run all property tests

- [x] 17. Implement React WebApp foundation
  - [x] 17.1 Initialize React project with Vite
    - Set up TypeScript configuration
    - Install Tailwind CSS and shadcn/ui
    - Configure build for S3 deployment
    - _Requirements: 3.1_
  
  - [x] 17.2 Implement Cognito authentication integration
    - Set up AWS Amplify Auth
    - Create AuthProvider context
    - Implement login/logout flows
    - Handle token refresh
    - _Requirements: 1.4, 1.7, 3.2_
  
  - [x] 17.3 Create API client service
    - Configure axios/fetch with auth headers
    - Implement request/response interceptors
    - Handle 401 responses with redirect to login
    - _Requirements: 14.2_
  
  - [x] 17.4 Write property tests for auth state
    - **Property 2: Authentication Token Refresh**
    - **Validates: Requirements 1.7**

- [x] 18. Implement WebApp layout components
  - [x] 18.1 Create Header component
    - Logo with link to landing page
    - Navigation links
    - Resume selector dropdown with user's resumes and "Add Resume" option at bottom
    - User profile dropdown (Settings, Logs, Logout)
    - _Requirements: 3.3_
  
  - [x] 18.2 Create Sidebar component
    - Add Job dropdown at top (Gmail, URL, Manual)
    - Phase filters with job counts
    - Phase aggregations (All Active, All Jobs)
    - _Requirements: 3.4, 3.6, 3.7, 3.8_
  
  - [x] 18.3 Create MainContent container
    - Filtered job card list
    - Loading and empty states
    - _Requirements: 3.5_
  
  - [x] 18.4 Write unit tests for layout components
    - Test header renders all elements
    - Test sidebar filter clicks
    - Test phase count display

- [x] 19. Implement Job Card component
  - [x] 19.1 Create JobCardHeader component
    - Company name (link if website known)
    - Job title (link to original posting)
    - Phase indicator/picker
    - Posting age calculation
    - Location, salary, source, tags
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  
  - [x] 19.2 Create SubcomponentGrid component
    - Two-column layout for 8 subcomponents
    - Generation state icon (🔒, ▶️, 💫, ✅, ⚠️)
    - Generation type toggle (⚙️, 🧠)
    - Title link to pop-out editor
    - Generate All button
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8_
  
  - [x] 19.3 Create FinalFileGrid component
    - Two-column layout for 4 final files
    - Generation state icon
    - Title link to pop-out editor
    - _Requirements: 10.1_
  
  - [x] 19.4 Write property tests for job card
    - **Property 12: Job Card Display Completeness**
    - **Validates: Requirements 6.1**

- [x] 20. Implement pop-out editors
  - [x] 20.1 Create SubcomponentEditor modal
    - Rich text editor for HTML content
    - Load current content from USER_JOB
    - Save and Cancel buttons
    - _Requirements: 9.1, 9.2, 9.3, 9.4_
  
  - [x] 20.2 Create JobDescriptionEditor modal
    - Full-text editor for job description
    - Save and Cancel buttons
    - _Requirements: 9.5_
  
  - [x] 20.3 Create FinalFileViewer modal
    - Display generated HTML/PDF
    - Download button
    - Copy URL button for custom resume URL
    - _Requirements: 11.1_
  
  - [x] 20.4 Write property tests for editors
    - **Property 22: Editor Cancel No-Persist**
    - **Validates: Requirements 9.4**

- [x] 21. Implement Add Job flows
  - [x] 21.1 Create AddJobFromURL modal
    - URL input field
    - Submit triggers job-create-url API
    - Display loading and success/error states
    - _Requirements: 5.2_
  
  - [x] 21.2 Create AddJobFromGmail modal
    - Gmail connect button (if not connected)
    - Fetch jobs button
    - Display found jobs with select/deselect
    - Import selected jobs
    - _Requirements: 5.1_
  
  - [x] 21.3 Create AddJobManual modal
    - Form with all job fields
    - Submit triggers job-create-manual API
    - _Requirements: 5.3_

- [x] 22. Implement Resume Management UI
  - [x] 22.1 Create ResumeSelector component
    - Dropdown in header with user's resumes
    - "Add Resume" option at bottom of dropdown opens ResumeEditor
    - Selecting a resume sets it as active for job generation
    - _Requirements: 4.3_
  
  - [x] 22.2 Create ResumeEditor modal
    - Form for all resume sections
    - JSON schema validation on submit
    - Save and Cancel buttons
    - _Requirements: 4.1, 4.2, 4.4_

- [x] 23. Implement User Preferences UI
  - [x] 23.1 Create PreferencesModal
    - Default generation type for each subcomponent
    - Save preferences on change
    - _Requirements: 13.1, 13.2, 13.4_

- [x] 24. Checkpoint - WebApp complete
  - Test full user flow from login to resume generation
  - Verify all UI components render correctly
  - Run all property tests

- [x] 25. Implement Landing Page
  - [x] 25.1 Create static landing page
    - Hero section with value proposition
    - Feature highlights
    - Login/Signup CTA button
    - Responsive design with Tailwind
    - _Requirements: 2.2, 2.3, 2.4_
  
  - [x] 25.2 Configure landing page deployment
    - Build static assets
    - Deploy to skillsnap-landing S3 bucket
    - Invalidate CloudFront cache
    - _Requirements: 2.1_

- [x] 26. Create global CSS assets
  - [x] 26.1 Create resume-base.css
    - Base styling for generated resumes
    - Professional, clean layout
    - Print-friendly styles
    - _Requirements: 11.6_
  
  - [x] 26.2 Create cover-base.css
    - Base styling for cover letters
    - Matching resume aesthetic
    - Print-friendly styles
    - _Requirements: 11.6_
  
  - [x] 26.3 Deploy assets to S3
    - Upload to /assets/ in skillsnap-public-resumes bucket
    - Configure long cache TTL
    - _Requirements: 11.3_

- [x] 27. Final integration and deployment
  - [x] 27.1 Create deployment scripts
    - CDK deploy script for infrastructure
    - Frontend build and deploy script
    - Landing page deploy script
    - _Requirements: 17.1_
  
  - [x] 27.2 Configure CI/CD pipeline
    - GitHub Actions workflow
    - Run tests on PR
    - Deploy to staging on merge to main
    - _Requirements: 17.1_

- [x] 28. Final checkpoint - Full system integration
  - Deploy complete system to AWS
  - Test end-to-end user journey
  - Verify custom resume URLs work
  - Run all property tests

## Notes

- All tasks are required for comprehensive implementation
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Backend uses Python 3.12, Frontend uses TypeScript/React
