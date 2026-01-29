# Requirements Document

## Introduction

The Resume File Import feature enables users to import resume data from external files (YAML, JSON, or PDF) directly into SkillSnap's Create/Edit Resume screen. This feature reduces manual data entry by allowing users to upload existing resume files, which are then processed by AI to map fields to SkillSnap's internal Resume data structure. Additionally, users can download a YAML template that exactly matches the internal data structure, guaranteeing 100% field mapping when used with the import feature.

## Glossary

- **Resume_Import_System**: The complete file import subsystem including UI components, API endpoints, and Lambda functions
- **File_Picker**: Browser-native file selection dialog for choosing local files
- **Upload_Endpoint**: Secure API endpoint that accepts file uploads and stores them in S3
- **Import_Lambda**: Lambda function that processes uploaded files using AI to map fields to SkillSnap Resume format
- **Temp_Bucket**: S3 bucket/folder for temporarily storing uploaded files before processing
- **Template_File**: A downloadable YAML file that exactly matches the SkillSnap ResumeJSON data structure
- **ResumeJSON**: The internal SkillSnap data structure for storing resume information (contact, summary, skills, highlights, experience, education, awards, keynotes)
- **Nova_Micro**: Amazon Bedrock Nova Micro model used for AI-powered field mapping

## Requirements

### Requirement 1: UI Layout Changes

**User Story:** As a user, I want the Create/Edit Resume screen to have room for import controls, so that I can easily access file import functionality.

#### Acceptance Criteria

1. WHEN the Create/Edit Resume modal opens, THE Resume_Import_System SHALL display a shortened Resume Name text field to accommodate new buttons
2. WHEN the Create/Edit Resume modal opens, THE Resume_Import_System SHALL display a "Load from File" button to the right of the Resume Name field
3. WHEN the Create/Edit Resume modal opens, THE Resume_Import_System SHALL display a "Download Template" button to the right of the "Load from File" button
4. THE Resume_Import_System SHALL maintain visual consistency with existing SkillSnap UI components and styling

### Requirement 2: File Upload Initiation

**User Story:** As a user, I want to select a local file to import, so that I can populate my resume from existing data.

#### Acceptance Criteria

1. WHEN a user clicks the "Load from File" button, THE Resume_Import_System SHALL open the browser's native File_Picker dialog
2. WHEN the File_Picker opens, THE Resume_Import_System SHALL filter to show only supported file types (YAML, JSON, PDF)
3. WHEN a user selects a valid file, THE Resume_Import_System SHALL validate the file size is under 5MB
4. IF a user selects an unsupported file type, THEN THE Resume_Import_System SHALL display an error message and not proceed with upload
5. IF a user selects a file larger than 5MB, THEN THE Resume_Import_System SHALL display an error message and not proceed with upload

### Requirement 3: Upload Progress Indication

**User Story:** As a user, I want to see progress while my file is being processed, so that I know the system is working.

#### Acceptance Criteria

1. WHEN a file upload begins, THE Resume_Import_System SHALL display a spinning indicator
2. WHEN a file upload begins, THE Resume_Import_System SHALL display the text "Analyzing resume file..."
3. WHILE the file is being processed, THE Resume_Import_System SHALL disable the "Load from File" and "Download Template" buttons
4. WHILE the file is being processed, THE Resume_Import_System SHALL prevent the user from closing the modal

### Requirement 4: File Upload to S3

**User Story:** As a system operator, I want uploaded files stored temporarily in S3, so that they can be processed securely.

#### Acceptance Criteria

1. WHEN a file is uploaded, THE Upload_Endpoint SHALL store the file in the Temp_Bucket with a unique key
2. WHEN storing a file, THE Upload_Endpoint SHALL use a path format of `temp-imports/{userid}/{timestamp}-{filename}`
3. THE Temp_Bucket SHALL have a lifecycle policy to delete objects after 60 seconds
4. THE Upload_Endpoint SHALL require valid Cognito authentication before accepting uploads
5. THE Upload_Endpoint SHALL return the S3 key of the uploaded file upon success

### Requirement 5: AI-Powered Field Mapping

**User Story:** As a user, I want my uploaded resume automatically mapped to SkillSnap's format, so that I don't have to manually re-enter data.

#### Acceptance Criteria

1. WHEN the Import_Lambda receives a file location, THE Import_Lambda SHALL retrieve the file from S3
2. WHEN processing a YAML or JSON file, THE Import_Lambda SHALL parse the file content directly
3. WHEN processing a PDF file, THE Import_Lambda SHALL extract text content from the PDF
4. WHEN file content is extracted, THE Import_Lambda SHALL send it to Nova_Micro with the ResumeJSON schema
5. WHEN Nova_Micro returns mapped data, THE Import_Lambda SHALL validate it against the ResumeJSON schema
6. IF the file cannot be parsed, THEN THE Import_Lambda SHALL return an error with a descriptive message
7. IF Nova_Micro fails to map fields, THEN THE Import_Lambda SHALL return a partial result with unmapped fields set to defaults

### Requirement 6: Import Result Display

**User Story:** As a user, I want to see the imported data in the editor, so that I can review and fix any mapping issues before saving.

#### Acceptance Criteria

1. WHEN the Import_Lambda returns successfully, THE Resume_Import_System SHALL populate all form fields with the mapped data
2. WHEN the Import_Lambda returns successfully, THE Resume_Import_System SHALL hide the progress indicator
3. WHEN the Import_Lambda returns successfully, THE Resume_Import_System SHALL re-enable all buttons
4. WHEN data is populated, THE Resume_Import_System SHALL NOT automatically save the resume
5. IF the Import_Lambda returns an error, THEN THE Resume_Import_System SHALL display the error message to the user
6. IF the Import_Lambda returns an error, THEN THE Resume_Import_System SHALL preserve any existing form data

### Requirement 7: Template Download

**User Story:** As a user, I want to download a template file, so that I can create a resume file that will import perfectly.

#### Acceptance Criteria

1. WHEN a user clicks the "Download Template" button, THE Resume_Import_System SHALL trigger a browser download
2. WHEN downloading, THE Resume_Import_System SHALL provide a file named "skillsnap-resume-template.yaml"
3. THE Template_File SHALL contain the complete ResumeJSON structure with example placeholder values
4. THE Template_File SHALL include comments explaining each field's purpose and format
5. WHEN a user imports a file created from the Template_File, THE Import_Lambda SHALL achieve 100% field mapping

### Requirement 8: Error Handling

**User Story:** As a user, I want clear error messages when something goes wrong, so that I can understand and fix the issue.

#### Acceptance Criteria

1. IF the file upload fails due to network error, THEN THE Resume_Import_System SHALL display "Upload failed. Please check your connection and try again."
2. IF the file upload fails due to authentication, THEN THE Resume_Import_System SHALL display "Session expired. Please refresh the page and try again."
3. IF the AI processing times out, THEN THE Resume_Import_System SHALL display "Processing took too long. Please try a smaller file or simpler format."
4. IF the file format is corrupted, THEN THE Resume_Import_System SHALL display "Could not read file. Please ensure it's a valid YAML, JSON, or PDF file."
5. WHEN any error occurs, THE Resume_Import_System SHALL log the error details for debugging

### Requirement 9: Security

**User Story:** As a system operator, I want file uploads to be secure, so that the system is protected from malicious files.

#### Acceptance Criteria

1. THE Upload_Endpoint SHALL validate file MIME types match the declared file extension
2. THE Upload_Endpoint SHALL scan uploaded files for malicious content patterns
3. THE Temp_Bucket SHALL NOT be publicly accessible
4. THE Import_Lambda SHALL process files in an isolated environment
5. THE Import_Lambda SHALL sanitize all extracted text before sending to Nova_Micro

### Requirement 10: Internal Data Structure Alignment

**User Story:** As a developer, I want the internal ResumeJSON format to closely match the input file format, so that field mapping is straightforward and maintainable.

#### Acceptance Criteria

1. THE Resume_Import_System SHALL review the internal ResumeJSON format against the stephen_hilton.yaml structure
2. WHERE field names differ between input format and internal format, THE Resume_Import_System SHALL document the mapping clearly
3. IF refactoring the internal format reduces complexity without breaking existing functionality, THEN THE Resume_Import_System SHALL implement the refactor
4. THE Resume_Import_System SHALL ensure backward compatibility with existing stored resumes during any refactor
5. THE Resume_Import_System SHALL update TypeScript types, Lambda handlers, and UI components if the internal format changes
