# Requirements Document

## Introduction

Skillsnap is a web application that reduces the time required to create bespoke resumes for job postings from hours to minutes. Users create resumes within the application, optionally connect their Gmail to retrieve LinkedIn Job Alerts, and use AI to generate tailored resumes and cover letters optimized for ATS systems. The application targets senior professionals with extensive experience who want to quickly generate customized resumes rather than sending generic multi-page documents.

## Glossary

- **Skillsnap_System**: The complete Skillsnap application including frontend, backend, and infrastructure
- **Landing_Page**: The static public website at skillsnap.me that introduces the product
- **WebApp**: The React-based authenticated application at app.skillsnap.me
- **API_Gateway**: The REST API endpoint at api.skillsnap.me
- **Auth_Service**: AWS Cognito-based authentication with Google OAuth integration
- **Job_Card**: A UI component representing a single job opportunity with generation controls
- **Resume_Generator**: The AI-powered service that creates bespoke resume content
- **Subcomponent**: One of eight resume sections (Contact, Summary, Skills, Highlights, Experience, Education, Awards, Cover Letter)
- **Final_File**: Generated output files (resume.html, resume.pdf, coverletter.html, coverletter.pdf)
- **Job_Phase**: The current status of a job in the user's pipeline (Search, Queued, Generating, Ready, Applied, Follow-Up, Negotiation, Accepted, Skipped, Expired, Errored)
- **CloudFront_Function**: Edge function that rewrites URLs for custom resume hosting
- **DynamoDB**: The NoSQL database storing all persistent data
- **S3_Bucket**: Object storage for static assets and generated resume files

## Requirements

### Requirement 1: User Authentication

**User Story:** As a user, I want to securely authenticate to Skillsnap, so that I can access my resumes and job data.

#### Acceptance Criteria

1. WHEN a user visits the landing page and clicks login, THE Auth_Service SHALL redirect them to Cognito authentication
2. WHEN a user authenticates via Google OAuth, THE Auth_Service SHALL create or link their Skillsnap account
3. WHEN a user authenticates via email/password, THE Auth_Service SHALL validate credentials and issue tokens
4. WHEN authentication succeeds, THE Auth_Service SHALL redirect the user to the WebApp
5. IF authentication fails, THEN THE Auth_Service SHALL display an error message and allow retry
6. WHEN a user requests Gmail integration, THE Auth_Service SHALL request only the scope needed to read LinkedIn Job Alert emails
7. THE Auth_Service SHALL store authentication tokens securely and refresh them before expiration

### Requirement 2: Landing Page

**User Story:** As a visitor, I want to view an engaging landing page, so that I can understand Skillsnap's value and sign up.

#### Acceptance Criteria

1. THE Landing_Page SHALL be hosted as a static site on S3 with CloudFront CDN at skillsnap.me
2. THE Landing_Page SHALL display product information with a professional yet edgy design
3. THE Landing_Page SHALL include a prominent login/signup button that redirects to Auth_Service
4. THE Landing_Page SHALL be responsive and accessible on mobile and desktop devices
5. THE Landing_Page SHALL load within 3 seconds on standard broadband connections

### Requirement 3: WebApp Main Interface

**User Story:** As an authenticated user, I want a well-organized interface, so that I can efficiently manage my job search.

#### Acceptance Criteria

1. THE WebApp SHALL be hosted at app.skillsnap.me as a React application on S3 with CloudFront
2. THE WebApp SHALL require authentication via Auth_Service before displaying content
3. WHEN the WebApp loads, THE WebApp SHALL display a header with logo, navigation, resume selector dropdown, and user profile
4. WHEN the WebApp loads, THE WebApp SHALL display a sidebar with add job button, phase filters with counts, and phase aggregations
5. WHEN the WebApp loads, THE WebApp SHALL display a main content area with filtered job cards
6. WHEN a user clicks a phase filter, THE WebApp SHALL display only job cards matching that phase
7. WHEN a user clicks "All Active", THE WebApp SHALL display jobs in phases: Search, Queued, Generating, Ready, Applied, Follow-Up, Negotiation
8. WHEN a user clicks "All Jobs", THE WebApp SHALL display all jobs regardless of phase

### Requirement 4: Resume Management

**User Story:** As a user, I want to create and manage multiple resumes, so that I can use different base resumes for different job types.

#### Acceptance Criteria

1. WHEN a user creates a new resume, THE Skillsnap_System SHALL store it in DynamoDB with userid and resumename as keys
2. WHEN a user edits a resume, THE Skillsnap_System SHALL update the resumejson field and lastupdate timestamp
3. WHEN a user selects a resume in the sidebar, THE WebApp SHALL use that resume as the base for job generation
4. THE Skillsnap_System SHALL validate resume JSON against the defined schema before saving
5. WHEN a user deletes a resume, THE Skillsnap_System SHALL remove it from DynamoDB and confirm deletion

### Requirement 5: Job Creation

**User Story:** As a user, I want to add jobs from multiple sources, so that I can build my job pipeline efficiently.

#### Acceptance Criteria

1. WHEN a user clicks "Add Job" and selects "From Gmail", THE Skillsnap_System SHALL fetch LinkedIn Job Alert emails and extract job listings
2. WHEN a user clicks "Add Job" and selects "From URL", THE Skillsnap_System SHALL scrape the job posting and extract structured data
3. WHEN a user clicks "Add Job" and selects "Manual Entry", THE WebApp SHALL display a form for entering job details
4. WHEN a job is created, THE Skillsnap_System SHALL generate a uuid7 jobid and store it in the JOB table
5. WHEN a job is created, THE Skillsnap_System SHALL create a USER_JOB record linking the user to the job with initial phase "Search"
6. THE Skillsnap_System SHALL extract and store: jobcompany, jobtitle, jobtitlesafe, jobdesc, joblocation, jobsalary, jobposteddate, joburl, jobtags

### Requirement 6: Job Card Display

**User Story:** As a user, I want to see comprehensive job information on each card, so that I can make informed decisions.

#### Acceptance Criteria

1. WHEN displaying a job card, THE WebApp SHALL show the header with company name, job title, phase indicator, posting age, location, salary, source, and tags
2. WHEN the company website is known, THE WebApp SHALL make the company name a clickable link
3. WHEN displaying posting age, THE WebApp SHALL calculate days since jobposteddate rounded to nearest day
4. WHEN a user clicks the phase indicator, THE WebApp SHALL display a picker to change the job phase
5. WHEN a user changes the job phase, THE Skillsnap_System SHALL update USER_JOB.jobphase in DynamoDB

### Requirement 7: Subcomponent Generation

**User Story:** As a user, I want to generate resume subcomponents individually, so that I can customize each section.

#### Acceptance Criteria

1. WHEN displaying subcomponent controls, THE WebApp SHALL show generation state icon, generation type toggle, and title for each of: Contact, Summary, Skills, Highlights, Experience, Education, Awards, Cover Letter
2. WHEN generation state is locked (🔒), THE WebApp SHALL prevent generation until dependencies are met
3. WHEN generation state is ready (▶️), THE WebApp SHALL allow the user to trigger generation
4. WHEN generation is in progress (💫), THE WebApp SHALL display a loading indicator
5. WHEN generation completes (✅), THE WebApp SHALL display success and store content in USER_JOB
6. IF generation fails (⚠️), THEN THE WebApp SHALL display an error indicator and allow retry
7. WHEN a user clicks the generation type toggle, THE WebApp SHALL switch between manual (⚙️) and AI (🧠) modes
8. WHEN a user clicks "Generate All", THE Skillsnap_System SHALL queue generation for all eight subcomponents

### Requirement 8: AI Content Generation

**User Story:** As a user, I want AI to generate tailored resume content, so that my resume is optimized for each job.

#### Acceptance Criteria

1. WHEN AI generation is triggered for a subcomponent, THE Resume_Generator SHALL use AWS Bedrock Nova Micro model
2. WHEN generating content, THE Resume_Generator SHALL combine the user's base resume with the job description
3. WHEN generating content, THE Resume_Generator SHALL select relevant experience and optimize word choice for ATS
4. THE Resume_Generator SHALL return content in HTML format suitable for the subcomponent
5. WHEN generation completes, THE Skillsnap_System SHALL store the content in the appropriate USER_JOB data field
6. IF Bedrock returns an error, THEN THE Resume_Generator SHALL retry up to 3 times before marking as errored

### Requirement 9: Manual Content Entry

**User Story:** As a user, I want to manually enter or edit subcomponent content, so that I have full control over my resume.

#### Acceptance Criteria

1. WHEN a user clicks a subcomponent title, THE WebApp SHALL open a pop-out editor with current content
2. THE WebApp SHALL provide a rich text editor for HTML content editing
3. WHEN a user clicks "Save", THE Skillsnap_System SHALL validate and store the content in USER_JOB
4. WHEN a user clicks "Cancel", THE WebApp SHALL close the editor without saving changes
5. WHEN editing the job description, THE WebApp SHALL open a dedicated editor for the full description text

### Requirement 10: Final File Generation

**User Story:** As a user, I want to generate final resume and cover letter files, so that I can apply to jobs.

#### Acceptance Criteria

1. WHEN all required subcomponents are complete, THE WebApp SHALL enable final file generation buttons
2. WHEN a user triggers Resume HTML generation, THE Skillsnap_System SHALL aggregate subcomponents into resume.html
3. WHEN a user triggers Resume PDF generation, THE Skillsnap_System SHALL convert resume.html to resume.pdf
4. WHEN a user triggers Cover Letter HTML generation, THE Skillsnap_System SHALL generate coverletter.html from the Cover Letter subcomponent
5. WHEN a user triggers Cover Letter PDF generation, THE Skillsnap_System SHALL convert coverletter.html to coverletter.pdf
6. WHEN final files are generated, THE Skillsnap_System SHALL upload them to S3 at /{username}/{company}/{jobtitlesafe}/
7. WHEN files are uploaded, THE Skillsnap_System SHALL update USER_JOB s3loc fields with the file locations

### Requirement 11: Custom Resume URLs

**User Story:** As a user, I want custom URLs for my resumes, so that I can share professional links with employers.

#### Acceptance Criteria

1. THE Skillsnap_System SHALL serve resumes at https://{username}.skillsnap.me/{company}/{jobtitlesafe}
2. WHEN a request arrives at a custom URL, THE CloudFront_Function SHALL rewrite the path to the S3 location
3. THE CloudFront_Function SHALL preserve global assets at /assets/* without rewriting
4. THE CloudFront_Function SHALL support per-resume override CSS at /{company}/{jobtitlesafe}/resume-override.css
5. WHEN a resume URL is created, THE Skillsnap_System SHALL store it in RESUME_URL table for uniqueness
6. THE Skillsnap_System SHALL include global CSS from /assets/resume-base.css and /assets/cover-base.css

### Requirement 12: Job Phase Management

**User Story:** As a user, I want to track jobs through phases, so that I can organize my job search pipeline.

#### Acceptance Criteria

1. THE Skillsnap_System SHALL support phases: Search, Queued, Generating, Ready, Applied, Follow-Up, Negotiation, Accepted, Skipped, Expired, Errored
2. WHEN a job is first created, THE Skillsnap_System SHALL set phase to "Search"
3. WHEN job data gathering completes, THE Skillsnap_System SHALL transition phase to "Queued"
4. WHEN resume generation starts, THE Skillsnap_System SHALL transition phase to "Generating"
5. WHEN all final files are ready, THE Skillsnap_System SHALL transition phase to "Ready"
6. WHEN a user manually changes phase, THE Skillsnap_System SHALL update USER_JOB.jobphase
7. WHEN a job is older than 30 days or marked as filled, THE Skillsnap_System SHALL transition phase to "Expired"

### Requirement 13: User Preferences

**User Story:** As a user, I want to set default preferences, so that my workflow is streamlined.

#### Acceptance Criteria

1. THE Skillsnap_System SHALL store user preferences in USER_PREF table with userid and prefname as keys
2. WHEN a user sets a default generation type for a subcomponent, THE Skillsnap_System SHALL store it as default_gen_{subcomponent}
3. WHEN creating a new job, THE WebApp SHALL apply user's default generation type preferences
4. WHEN a user updates preferences, THE Skillsnap_System SHALL persist changes immediately

### Requirement 14: API Gateway

**User Story:** As a developer, I want a secure API, so that the frontend can communicate with backend services.

#### Acceptance Criteria

1. THE API_Gateway SHALL be hosted at api.skillsnap.me
2. THE API_Gateway SHALL require valid Cognito tokens for all endpoints
3. THE API_Gateway SHALL route requests to appropriate Lambda functions
4. THE API_Gateway SHALL return appropriate HTTP status codes and error messages
5. IF a request lacks valid authentication, THEN THE API_Gateway SHALL return 401 Unauthorized

### Requirement 15: Data Persistence

**User Story:** As a user, I want my data persisted reliably, so that I don't lose my work.

#### Acceptance Criteria

1. THE Skillsnap_System SHALL store user data in DynamoDB tables: USER, USER_EMAIL, USER_USERNAME, USER_PREF, JOB, USER_JOB, RESUME, RESUME_URL
2. THE Skillsnap_System SHALL enforce email uniqueness via USER_EMAIL table
3. THE Skillsnap_System SHALL enforce username uniqueness via USER_USERNAME table
4. WHEN storing a resume, THE Skillsnap_System SHALL use userid as partition key and resumename as sort key
5. WHEN storing a user-job relationship, THE Skillsnap_System SHALL use userid as partition key and jobid as sort key

### Requirement 16: Asynchronous Processing

**User Story:** As a user, I want background processing for long operations, so that the UI remains responsive.

#### Acceptance Criteria

1. WHEN "Generate All" is triggered, THE Skillsnap_System SHALL queue subcomponent generation tasks to SQS
2. WHEN a task is queued, THE Skillsnap_System SHALL return immediately with a pending status
3. WHEN a Lambda processes an SQS message, THE Skillsnap_System SHALL update the job status in DynamoDB
4. THE WebApp SHALL poll or use WebSocket to display real-time generation progress
5. IF an SQS message fails processing, THEN THE Skillsnap_System SHALL retry according to queue configuration

### Requirement 17: Infrastructure

**User Story:** As an operator, I want infrastructure as code, so that deployments are repeatable and scalable.

#### Acceptance Criteria

1. THE Skillsnap_System SHALL be deployed using AWS CDK with Python
2. THE Skillsnap_System SHALL deploy to us-west-2 region
3. THE Skillsnap_System SHALL use Lambda with Python 3.12 runtime
4. THE Skillsnap_System SHALL scale costs proportionally with user growth (serverless architecture)
5. THE Skillsnap_System SHALL use Route53 for DNS and ACM for SSL certificates
