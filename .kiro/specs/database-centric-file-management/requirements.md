# Requirements Document

## Introduction

This feature transitions the ResumAI application from a filesystem-centric architecture to a database-centric file management approach. Currently, the UI experiences "job.yaml not found" errors because file APIs accept folder/file locations directly instead of querying the database. With job data now stored in SQLite, all UI behavior and file operations should use the database as the single source of truth for file locations, eliminating sync issues between the database and filesystem.

## Glossary

- **Job_Files_Table**: A new database table that tracks all files associated with jobs, including their locations, purposes, and metadata.
- **File_Storage_Service**: A service component responsible for managing file storage operations using YYYYMM partitioned folders.
- **Job_File_Repository**: A repository component that provides data access methods for the Job_Files_Table.
- **File_Purpose**: An enumeration of valid file uses including job_posting_html, resume_html, resume_pdf, coverletter_html, coverletter_pdf, and subcontent.
- **File_Source**: An enumeration indicating how a file was obtained, such as url_fetch or generated.
- **Partition_Folder**: A folder named with YYYYMM format (e.g., 202601) used to organize files by month.
- **Job_ID**: The database primary key identifier for a job record.

## Requirements

### Requirement 1: Job_Files Database Table

**User Story:** As a developer, I want a dedicated database table to track all job-related files, so that file locations are always consistent with the database state.

#### Acceptance Criteria

1. THE Job_Files_Table SHALL contain columns for id, job_id, filename, file_path, file_purpose, file_source, and timestamps (created_at, updated_at).
2. THE Job_Files_Table SHALL enforce a foreign key constraint on job_id referencing the jobs table with CASCADE delete.
3. THE Job_Files_Table SHALL enforce a unique constraint on the combination of job_id and file_purpose to prevent duplicate file entries for the same purpose.
4. WHEN a job is deleted, THEN THE Job_Files_Table SHALL automatically delete all associated file records via CASCADE.
5. THE Job_Files_Table SHALL include an index on job_id for efficient lookups.

### Requirement 2: File Storage Strategy

**User Story:** As a developer, I want files stored in partitioned folders by month, so that no single folder becomes too large and file organization is predictable.

#### Acceptance Criteria

1. THE File_Storage_Service SHALL store all job-related files in the src/files/ directory.
2. THE File_Storage_Service SHALL organize files into YYYYMM subdirectories based on the current date when the file is created.
3. THE File_Storage_Service SHALL generate unique filenames to prevent collisions within partition folders.
4. WHEN storing a file, THE File_Storage_Service SHALL create the partition folder if it does not exist.
5. THE File_Storage_Service SHALL NOT create per-job folders or use job-specific naming conventions in the folder structure.

### Requirement 3: Job_File_Repository

**User Story:** As a developer, I want a repository layer for file metadata operations, so that all file lookups go through a consistent data access pattern.

#### Acceptance Criteria

1. THE Job_File_Repository SHALL provide a method to create a file record given job_id, filename, file_path, file_purpose, and file_source.
2. THE Job_File_Repository SHALL provide a method to retrieve all file records for a given job_id.
3. THE Job_File_Repository SHALL provide a method to retrieve a specific file record by job_id and file_purpose.
4. THE Job_File_Repository SHALL provide a method to check if a file exists for a given job_id and file_purpose.
5. THE Job_File_Repository SHALL provide a method to delete a file record by id.
6. WHEN retrieving file records, THE Job_File_Repository SHALL return None or empty list if no records exist rather than raising exceptions.

### Requirement 4: Email Fetch Workflow Changes

**User Story:** As a user, I want the email fetch workflow to store job posting HTML files in the new partitioned structure, so that file locations are tracked in the database.

#### Acceptance Criteria

1. WHEN fetching jobs from email, THE System SHALL parse email data and create job records in the SQLite jobs table.
2. WHEN fetching jobs from email, THE System SHALL NOT create per-job folders in the jobs/ directory.
3. WHEN fetching jobs from email, THE System SHALL NOT save job.yaml files to the filesystem.
4. WHEN fetching job posting HTML from URLs, THE System SHALL save HTML files to src/files/YYYYMM/ partitioned folders.
5. WHEN saving job posting HTML, THE System SHALL create a record in the Job_Files_Table with file_purpose set to job_posting_html.
6. WHEN saving job posting HTML, THE System SHALL set file_source to url_fetch in the Job_Files_Table record.

### Requirement 5: Document Generation Workflow Changes

**User Story:** As a user, I want generated documents stored in the partitioned file structure with database tracking, so that document locations are always queryable.

#### Acceptance Criteria

1. WHEN generating resume HTML, THE System SHALL save the file to src/files/YYYYMM/ partitioned folders.
2. WHEN generating resume HTML, THE System SHALL create a record in the Job_Files_Table with file_purpose set to resume_html.
3. WHEN generating resume PDF, THE System SHALL save the file to src/files/YYYYMM/ partitioned folders.
4. WHEN generating resume PDF, THE System SHALL create a record in the Job_Files_Table with file_purpose set to resume_pdf.
5. WHEN generating cover letter HTML, THE System SHALL save the file to src/files/YYYYMM/ partitioned folders.
6. WHEN generating cover letter HTML, THE System SHALL create a record in the Job_Files_Table with file_purpose set to coverletter_html.
7. WHEN generating cover letter PDF, THE System SHALL save the file to src/files/YYYYMM/ partitioned folders.
8. WHEN generating cover letter PDF, THE System SHALL create a record in the Job_Files_Table with file_purpose set to coverletter_pdf.
9. WHEN generating any document, THE System SHALL set file_source to generated in the Job_Files_Table record.

### Requirement 6: API Changes for File Access

**User Story:** As a developer, I want all file-related APIs to accept job_id instead of folder paths, so that file lookups always go through the database.

#### Acceptance Criteria

1. THE file viewing API SHALL accept job_id and file_purpose as parameters instead of folder_name and filename.
2. WHEN a file is requested, THE API SHALL query the Job_Files_Table to find the file location.
3. IF a file record does not exist in the Job_Files_Table, THEN THE API SHALL return a 404 error with a descriptive message.
4. THE file existence check API SHALL query the Job_Files_Table rather than checking the filesystem directly.
5. WHEN returning file metadata, THE API SHALL include the file_path, file_purpose, file_source, and timestamps from the Job_Files_Table.

### Requirement 7: File Service Integration

**User Story:** As a developer, I want a unified file service that coordinates storage and database operations, so that file operations are atomic and consistent.

#### Acceptance Criteria

1. THE File_Storage_Service SHALL provide a method to store a file that both writes to disk and creates a database record.
2. THE File_Storage_Service SHALL provide a method to retrieve a file path by job_id and file_purpose.
3. THE File_Storage_Service SHALL provide a method to delete a file that both removes from disk and deletes the database record.
4. IF a file write fails, THEN THE File_Storage_Service SHALL NOT create a database record.
5. IF a database record creation fails after file write, THEN THE File_Storage_Service SHALL delete the written file to maintain consistency.
6. THE File_Storage_Service SHALL log all file operations for debugging purposes.

### Requirement 8: Job Detail API Updates

**User Story:** As a user, I want the job detail view to show file information from the database, so that I see accurate file status regardless of filesystem state.

#### Acceptance Criteria

1. WHEN retrieving job details, THE API SHALL query the Job_Files_Table for all files associated with the job.
2. THE job detail response SHALL include a files array with each file's purpose, path, source, and timestamps.
3. THE doc_status in the job detail response SHALL be derived from Job_Files_Table records rather than filesystem checks.
4. IF a file record exists in the database but the file is missing from disk, THEN THE API SHALL indicate this inconsistency in the response.
