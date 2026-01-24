# Implementation Plan: Database-Centric File Management

## Overview

This implementation plan transforms ResumAI from filesystem-centric to database-centric file management. Tasks are organized to build foundational components first (database schema, models, repository), then the service layer, followed by event handler updates, and finally API changes.

## Tasks

- [x] 1. Database schema and model updates
  - [x] 1.1 Add job_files table to schema.sql
    - Add CREATE TABLE statement with id, job_id, filename, file_path, file_purpose, file_source, created_at, updated_at
    - Add UNIQUE constraint on (job_id, file_purpose)
    - Add FOREIGN KEY constraint on job_id with CASCADE delete
    - Add indexes on job_id and file_purpose
    - _Requirements: 1.1, 1.2, 1.3, 1.5_
  
  - [x] 1.2 Add JobFile dataclass to models.py
    - Create JobFile dataclass with all fields
    - Add type hints and default values
    - _Requirements: 1.1_
  
  - [x] 1.3 Update schema.py to include job_files in drop_schema
    - Add job_files to the tables list in correct dependency order
    - _Requirements: 1.4_

- [x] 2. Implement JobFileRepository
  - [x] 2.1 Create job_file_repository.py with base structure
    - Create JobFileRepository class extending BaseRepository
    - Implement create() method to insert file records
    - Implement get_by_job_id() method to retrieve all files for a job
    - Implement get_by_job_and_purpose() method for specific file lookup
    - Implement exists() method for existence checks
    - Implement delete() method for single record deletion
    - Implement delete_by_job_id() method for bulk deletion
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_
  
  - [x] 2.2 Write property test for repository round-trip consistency
    - **Property 5: Repository Round-Trip Consistency**
    - **Validates: Requirements 3.1, 3.3**
  
  - [x] 2.3 Write property test for existence check accuracy
    - **Property 6: Repository Existence Check Accuracy**
    - **Validates: Requirements 3.4, 3.6**

- [x] 3. Checkpoint - Verify repository layer
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Implement FileStorageService
  - [x] 4.1 Create file_storage_service.py with core methods
    - Create FileStorageService class with base_path configuration
    - Implement _generate_partition_path() for YYYYMM folder creation
    - Implement _generate_unique_filename() for collision-free names
    - Implement store_file() with atomic file write and database record creation
    - Implement get_file_path() to retrieve path by job_id and purpose
    - Implement get_file_content() to read file content
    - Implement delete_file() with atomic file and record deletion
    - Implement get_files_for_job() to list all files for a job
    - Add logging for all operations
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 7.1, 7.2, 7.3, 7.6_
  
  - [x] 4.2 Implement failure handling and rollback logic
    - Add try/except around file write with database rollback on failure
    - Add file cleanup on database insert failure
    - _Requirements: 7.4, 7.5_
  
  - [x] 4.3 Write property test for file storage location invariant
    - **Property 3: File Storage Location Invariant**
    - **Validates: Requirements 2.1, 2.2, 2.5**
  
  - [x] 4.4 Write property test for unique filename generation
    - **Property 4: Unique Filename Generation**
    - **Validates: Requirements 2.3**
  
  - [x] 4.5 Write property test for atomic store operation
    - **Property 7: Atomic Store Operation**
    - **Validates: Requirements 7.1**
  
  - [x] 4.6 Write property test for atomic delete operation
    - **Property 8: Atomic Delete Operation**
    - **Validates: Requirements 7.3**
  
  - [x] 4.7 Write property test for consistency on failure
    - **Property 9: Consistency on Failure**
    - **Validates: Requirements 7.4, 7.5**

- [x] 5. Checkpoint - Verify service layer
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Update event handlers for new file storage
  - [x] 6.1 Update get_gmail_linkedin.py for database-centric storage
    - Remove job folder creation logic
    - Remove job.yaml file writing
    - Use FileStorageService.store_file() for job posting HTML
    - Set file_purpose to job_posting_html and file_source to url_fetch
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_
  
  - [x] 6.2 Update gen_resume_html.py for database-centric storage
    - Modify to accept job_id parameter
    - Use FileStorageService.store_file() for HTML output
    - Set file_purpose to resume_html and file_source to generated
    - _Requirements: 5.1, 5.2, 5.9_
  
  - [x] 6.3 Update gen_resume_pdf.py for database-centric storage
    - Modify to accept job_id parameter
    - Get HTML path from FileStorageService
    - Use FileStorageService.store_file() for PDF output
    - Set file_purpose to resume_pdf and file_source to generated
    - _Requirements: 5.3, 5.4, 5.9_
  
  - [x] 6.4 Update gen_coverletter_html.py for database-centric storage
    - Modify to accept job_id parameter
    - Use FileStorageService.store_file() for HTML output
    - Set file_purpose to coverletter_html and file_source to generated
    - _Requirements: 5.5, 5.6, 5.9_
  
  - [x] 6.5 Update gen_coverletter_pdf.py for database-centric storage
    - Modify to accept job_id parameter
    - Get HTML path from FileStorageService
    - Use FileStorageService.store_file() for PDF output
    - Set file_purpose to coverletter_pdf and file_source to generated
    - _Requirements: 5.7, 5.8, 5.9_

- [x] 7. Checkpoint - Verify event handlers
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Update API endpoints
  - [x] 8.1 Create new file viewing endpoint with job_id parameter
    - Add route /api/view/<int:job_id>/<file_purpose>
    - Query JobFileRepository for file location
    - Return 404 if record not found
    - Serve file content from database-stored path
    - _Requirements: 6.1, 6.2, 6.3_
  
  - [x] 8.2 Update job detail endpoint to use database for file status
    - Query JobFileRepository for all files associated with job
    - Build doc_status from database records
    - Include files array with purpose, path, source, timestamps
    - Add inconsistency detection for missing files
    - _Requirements: 8.1, 8.2, 8.3, 8.4_
  
  - [x] 8.3 Update file existence check to use database
    - Modify any filesystem-based existence checks to use JobFileRepository.exists()
    - _Requirements: 6.4_
  
  - [x] 8.4 Add file metadata to API responses
    - Include file_path, file_purpose, file_source, timestamps in responses
    - _Requirements: 6.5_
  
  - [x] 8.5 Write property test for API database lookup
    - **Property 10: API Database Lookup**
    - **Validates: Requirements 6.2, 6.4**
  
  - [x] 8.6 Write property test for API 404 on missing records
    - **Property 11: API 404 on Missing Records**
    - **Validates: Requirements 6.3**
  
  - [x] 8.7 Write property test for job detail file completeness
    - **Property 12: Job Detail File Completeness**
    - **Validates: Requirements 8.1, 8.2, 8.3**
  
  - [x] 8.8 Write property test for inconsistency detection
    - **Property 13: Inconsistency Detection**
    - **Validates: Requirements 8.4**

- [x] 9. Database constraint tests
  - [x] 9.1 Write property test for CASCADE delete
    - **Property 1: CASCADE Delete Removes File Records**
    - **Validates: Requirements 1.2, 1.4**
  
  - [x] 9.2 Write property test for unique constraint enforcement
    - **Property 2: Unique Constraint Enforcement**
    - **Validates: Requirements 1.3**

- [x] 10. Final checkpoint - Full integration verification
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- All tasks including property tests are required for comprehensive coverage
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The existing `job_artifacts` table stores file content as BLOBs; the new `job_files` table stores file paths for filesystem-based storage
