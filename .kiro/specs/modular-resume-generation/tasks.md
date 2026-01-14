# Implementation Plan: Modular Resume Generation

## Overview

Transform the monolithic resume generation system into a modular, parallel architecture that generates structured content for each section concurrently, then merges into HTML templates. This approach will significantly reduce timeout issues, improve speed, and provide better user feedback.

## Tasks

- [x] 1. Set up modular architecture foundation
  - Create new folder structure in `src/utils/` for modular components
  - Set up base classes and interfaces for section generators
  - Create configuration system for modular vs legacy generation
  - _Requirements: 8.3, 1.1_

- [x] 1.1 Write property test for modular architecture setup
  - **Property 1: Parallel section generation**
  - **Validates: Requirements 1.1, 2.1, 5.2**

- [x] 2. Implement core section generators
  - [x] 2.1 Create base SectionGenerator class with common interface
    - Define abstract methods for content generation and validation
    - Implement structured content format (YAML/JSON) handling
    - _Requirements: 1.2, 3.1_

  - [x] 2.2 Write property test for structured content format
    - **Property 2: Structured content format**
    - **Validates: Requirements 1.2, 4.2, 5.1**

  - [x] 2.3 Implement SummaryGenerator for professional summaries
    - Generate 580-630 character summaries tailored to job descriptions
    - Return structured YAML content without HTML formatting
    - _Requirements: 1.2, 5.1_

  - [x] 2.4 Implement SkillsGenerator for core skills section
    - Generate 12 relevant skills in 3 columns (20-36 chars each)
    - Return structured format with column organization
    - _Requirements: 1.2, 5.1_

  - [x] 2.5 Implement ExperienceGenerator for work history
    - Generate company descriptions and role bullets (90-115 or 180-240 chars)
    - Maintain factual accuracy while optimizing for job relevance
    - _Requirements: 1.2, 5.1_

  - [x] 2.6 Implement EducationGenerator and AwardsGenerator
    - Generate education entries (course + school only, no dates)
    - Generate awards/keynotes (title only, no dates)
    - _Requirements: 1.2, 5.1_

  - [x] 2.7 Implement CoverLetterGenerator for letter content
    - Generate professional letter body (max 350 words)
    - Structure with opening, body paragraphs, and closing
    - _Requirements: 1.2, 5.1_

- [x] 2.8 Write unit tests for all section generators
  - Test specific examples and edge cases for each generator
  - Validate character limits and content structure
  - _Requirements: 1.2, 5.1_

- [x] 3. Build parallel execution system
  - [x] 3.1 Create ParallelExecutor for concurrent section processing
    - Implement asyncio-based concurrent execution
    - Handle individual section timeouts (30 seconds each)
    - _Requirements: 2.1, 2.3, 6.3_

  - [x] 3.2 Write property test for non-blocking section processing
    - **Property 3: Non-blocking section processing**
    - **Validates: Requirements 1.3, 2.3**

  - [x] 3.3 Implement ContentAggregator for section result combination
    - Combine completed sections into unified data structure
    - Handle missing or failed sections with fallback content
    - _Requirements: 1.4, 6.1_

  - [x] 3.4 Write property test for content validation and fallback
    - **Property 5: Content validation and fallback**
    - **Validates: Requirements 3.2, 3.4, 6.1**

- [x] 4. Create template engine system
  - [x] 4.1 Implement TemplateEngine for HTML rendering
    - Load templates from `src/resources/templates/`
    - Map structured content to template variables
    - Handle missing template variables gracefully
    - _Requirements: 4.1, 4.3, 4.4_

  - [x] 4.2 Write property test for template engine assembly
    - **Property 4: Template engine assembly**
    - **Validates: Requirements 1.4, 3.3, 4.3**

  - [x] 4.3 Create resume and cover letter HTML templates
    - Move existing templates to `src/resources/templates/`
    - Separate content placeholders from formatting
    - Ensure compatibility with existing CSS and icons
    - _Requirements: 4.1, 4.3_

  - [x] 4.4 Write property test for template independence
    - **Property 9: Template independence**
    - **Validates: Requirements 4.1, 4.4**

- [x] 5. Implement comprehensive UI feedback system
  - [x] 5.1 Create UIFeedbackManager for progress tracking
    - Implement 5-second maximum update intervals
    - Track multi-phase progress (queue → generate → PDF)
    - Support both single job and batch operation feedback
    - _Requirements: 9.1, 9.2, 10.1_

  - [x] 5.2 Write property test for UI feedback timing
    - **Property 12: Comprehensive UI feedback**
    - **Validates: Requirements 9.1, 9.2, 9.5, 10.5**

  - [x] 5.3 Update web UI for enhanced progress display
    - Add phase indicators and section-level progress bars
    - Implement batch progress display with individual job details
    - Add real-time error messaging and retry options
    - _Requirements: 9.3, 9.4, 10.2_

  - [x] 5.4 Write property test for multi-phase progress visibility
    - **Property 13: Multi-phase progress visibility**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.4, 10.6**

- [x] 6. Checkpoint - Core modular system functional
  - Ensure all section generators produce valid structured content
  - Verify parallel execution works without blocking
  - Test template engine renders complete HTML
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Integrate with existing systems
  - [x] 7.1 Update step2_generate.py to use modular system
    - Add configuration flag for modular vs legacy generation
    - Integrate ModularResumeGenerator as primary generation method
    - Maintain backward compatibility with existing API
    - _Requirements: 8.1, 8.2_

  - [x] 7.2 Write property test for backward compatibility
    - **Property 11: Backward compatibility**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4**

  - [x] 7.3 Update PDFManager for modular HTML output
    - Ensure PDF generation works with modular HTML structure
    - Add progress reporting for PDF conversion phase
    - Test with both resume and cover letter outputs
    - _Requirements: PDF Integration, 10.3_

  - [x] 7.4 Write property test for PDF generation compatibility
    - **Property 10: PDF generation compatibility**
    - **Validates: Requirements 8.1, PDF Integration**

- [x] 8. Implement error handling and fallbacks
  - [x] 8.1 Create comprehensive error handling system
    - Implement section-level retry logic (up to 2 retries)
    - Add automatic fallback to legacy generation for complete failures
    - Create graceful degradation for partial failures
    - _Requirements: 6.2, 6.4, 8.4_

  - [x] 8.2 Write property test for fault isolation and recovery
    - **Property 7: Fault isolation and recovery**
    - **Validates: Requirements 6.2, 6.3, 6.4**

  - [x] 8.3 Add performance monitoring and optimization
    - Implement timing comparisons between modular and legacy approaches
    - Add token usage tracking for efficiency validation
    - Create performance benchmarks for parallel vs sequential processing
    - _Requirements: 5.4, 2.2_

  - [x] 8.4 Write property test for performance improvement
    - **Property 6: Performance improvement**
    - **Validates: Requirements 2.2, 5.4**

- [x] 9. Final integration and testing
  - [x] 9.1 Create end-to-end integration tests
    - Test complete workflow from job input to PDF output
    - Validate batch processing with multiple jobs
    - Test error scenarios and fallback mechanisms
    - _Requirements: 2.4, 9.3_

  - [x] 9.2 Write property test for batch operation feedback
    - **Property 14: Batch operation feedback**
    - **Validates: Requirements 9.3, 9.4, 10.4**

  - [x] 9.3 Update API endpoints for enhanced progress tracking
    - Modify existing progress endpoints to support multi-phase tracking
    - Add batch progress endpoints for batch operations
    - Ensure WebSocket updates work with new progress structure
    - _Requirements: 9.5, 10.5_

  - [x] 9.4 Write property test for real-time progress tracking
    - **Property 8: Real-time progress tracking**
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4**

- [x] 10. Final checkpoint and deployment preparation
  - Ensure all property tests pass with 100+ iterations each
  - Verify performance improvements meet expectations
  - Test complete system with both single and batch operations
  - Validate UI feedback provides updates every 5 seconds maximum
  - Ensure all tests pass, ask the user if questions arise.
    - Structure with opening, body paragraphs, and closing
    - _Requirements: 1.2, 5.1_

- [ ] 2.8 Write unit tests for all section generators
  - Test specific examples and edge cases for each generator
  - Validate character limits and content structure
  - _Requirements: 1.2, 5.1_

- [ ] 3. Build parallel execution system
  - [ ] 3.1 Create ParallelExecutor for concurrent section processing
    - Implement asyncio-based concurrent execution
    - Handle individual section timeouts (30 seconds each)
    - _Requirements: 2.1, 2.3, 6.3_

  - [ ] 3.2 Write property test for non-blocking section processing
    - **Property 3: Non-blocking section processing**
    - **Validates: Requirements 1.3, 2.3**

  - [ ] 3.3 Implement ContentAggregator for section result combination
    - Combine completed sections into unified data structure
    - Handle missing or failed sections with fallback content
    - _Requirements: 1.4, 6.1_

  - [ ] 3.4 Write property test for content validation and fallback
    - **Property 5: Content validation and fallback**
    - **Validates: Requirements 3.2, 3.4, 6.1**

- [ ] 4. Create template engine system
  - [ ] 4.1 Implement TemplateEngine for HTML rendering
    - Load templates from `src/resources/templates/`
    - Map structured content to template variables
    - Handle missing template variables gracefully
    - _Requirements: 4.1, 4.3, 4.4_

  - [ ] 4.2 Write property test for template engine assembly
    - **Property 4: Template engine assembly**
    - **Validates: Requirements 1.4, 3.3, 4.3**

  - [ ] 4.3 Create resume and cover letter HTML templates
    - Move existing templates to `src/resources/templates/`
    - Separate content placeholders from formatting
    - Ensure compatibility with existing CSS and icons
    - _Requirements: 4.1, 4.3_

  - [ ] 4.4 Write property test for template independence
    - **Property 9: Template independence**
    - **Validates: Requirements 4.1, 4.4**

- [ ] 5. Implement comprehensive UI feedback system
  - [ ] 5.1 Create UIFeedbackManager for progress tracking
    - Implement 5-second maximum update intervals
    - Track multi-phase progress (queue → generate → PDF)
    - Support both single job and batch operation feedback
    - _Requirements: 9.1, 9.2, 10.1_

  - [ ] 5.2 Write property test for UI feedback timing
    - **Property 12: Comprehensive UI feedback**
    - **Validates: Requirements 9.1, 9.2, 9.5, 10.5**

  - [ ] 5.3 Update web UI for enhanced progress display
    - Add phase indicators and section-level progress bars
    - Implement batch progress display with individual job details
    - Add real-time error messaging and retry options
    - _Requirements: 9.3, 9.4, 10.2_

  - [ ] 5.4 Write property test for multi-phase progress visibility
    - **Property 13: Multi-phase progress visibility**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.4, 10.6**

- [ ] 6. Checkpoint - Core modular system functional
  - Ensure all section generators produce valid structured content
  - Verify parallel execution works without blocking
  - Test template engine renders complete HTML
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Integrate with existing systems
  - [ ] 7.1 Update step2_generate.py to use modular system
    - Add configuration flag for modular vs legacy generation
    - Integrate ModularResumeGenerator as primary generation method
    - Maintain backward compatibility with existing API
    - _Requirements: 8.1, 8.2_

  - [ ] 7.2 Write property test for backward compatibility
    - **Property 11: Backward compatibility**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4**

  - [ ] 7.3 Update PDFManager for modular HTML output
    - Ensure PDF generation works with modular HTML structure
    - Add progress reporting for PDF conversion phase
    - Test with both resume and cover letter outputs
    - _Requirements: PDF Integration, 10.3_

  - [ ] 7.4 Write property test for PDF generation compatibility
    - **Property 10: PDF generation compatibility**
    - **Validates: Requirements 8.1, PDF Integration**

- [ ] 8. Implement error handling and fallbacks
  - [ ] 8.1 Create comprehensive error handling system
    - Implement section-level retry logic (up to 2 retries)
    - Add automatic fallback to legacy generation for complete failures
    - Create graceful degradation for partial failures
    - _Requirements: 6.2, 6.4, 8.4_

  - [ ] 8.2 Write property test for fault isolation and recovery
    - **Property 7: Fault isolation and recovery**
    - **Validates: Requirements 6.2, 6.3, 6.4**

  - [ ] 8.3 Add performance monitoring and optimization
    - Implement timing comparisons between modular and legacy approaches
    - Add token usage tracking for efficiency validation
    - Create performance benchmarks for parallel vs sequential processing
    - _Requirements: 5.4, 2.2_

  - [ ] 8.4 Write property test for performance improvement
    - **Property 6: Performance improvement**
    - **Validates: Requirements 2.2, 5.4**

- [ ] 9. Final integration and testing
  - [ ] 9.1 Create end-to-end integration tests
    - Test complete workflow from job input to PDF output
    - Validate batch processing with multiple jobs
    - Test error scenarios and fallback mechanisms
    - _Requirements: 2.4, 9.3_

  - [ ] 9.2 Write property test for batch operation feedback
    - **Property 14: Batch operation feedback**
    - **Validates: Requirements 9.3, 9.4, 10.4**

  - [ ] 9.3 Update API endpoints for enhanced progress tracking
    - Modify existing progress endpoints to support multi-phase tracking
    - Add batch progress endpoints for batch operations
    - Ensure WebSocket updates work with new progress structure
    - _Requirements: 9.5, 10.5_

  - [ ] 9.4 Write property test for real-time progress tracking
    - **Property 8: Real-time progress tracking**
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4**

- [ ] 10. Final checkpoint and deployment preparation
  - Ensure all property tests pass with 100+ iterations each
  - Verify performance improvements meet expectations
  - Test complete system with both single and batch operations
  - Validate UI feedback provides updates every 5 seconds maximum
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Each task references specific requirements for traceability
- Property tests validate universal correctness properties with minimum 100 iterations
- Unit tests validate specific examples and edge cases
- The modular system provides fallback to legacy generation for reliability
- UI feedback ensures users always know the current status of generation processes
- Comprehensive testing from the start ensures system reliability and correctness