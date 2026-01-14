# Requirements Document

## Introduction

Transform the current monolithic resume generation system into a modular, parallel content generation system that separates content creation from HTML formatting. This will improve speed, reliability, and maintainability while reducing token usage and timeout issues.

## Glossary

- **Content_Generator**: Component that generates structured content (YAML/JSON) for resume sections
- **Template_Engine**: Component that merges structured content into HTML templates
- **Section_Processor**: Individual processor for each resume section (summary, experience, skills, etc.)
- **Parallel_Executor**: Component that runs multiple content generation requests simultaneously
- **Structured_Content**: Resume content in YAML or JSON format without HTML formatting

## Requirements

### Requirement 1: Modular Content Generation

**User Story:** As a system architect, I want to generate resume content in separate, focused requests, so that each request is faster and more reliable.

#### Acceptance Criteria

1. WHEN generating a resume, THE Content_Generator SHALL create separate requests for each major section
2. WHEN processing sections, THE Section_Processor SHALL return structured content in YAML or JSON format
3. WHEN a section request completes, THE System SHALL not wait for other sections to continue processing
4. WHEN all sections complete, THE Template_Engine SHALL merge the structured content into HTML
5. WHERE section generation fails, THE System SHALL use fallback content or retry individual sections

### Requirement 2: Parallel Processing

**User Story:** As a user, I want resume generation to be faster, so that I don't experience long wait times or timeouts.

#### Acceptance Criteria

1. WHEN generating resume content, THE Parallel_Executor SHALL run multiple section requests simultaneously
2. WHEN sections are processed in parallel, THE System SHALL complete in significantly less time than sequential processing
3. WHEN one section fails, THE System SHALL continue processing other sections without blocking
4. WHEN all parallel requests complete, THE System SHALL aggregate results and proceed to template rendering

### Requirement 3: Structured Content Format

**User Story:** As a developer, I want content returned in structured format, so that it's easier to process and template.

#### Acceptance Criteria

1. WHEN requesting content generation, THE Content_Generator SHALL specify YAML or JSON output format
2. WHEN content is returned, THE System SHALL validate the structured format before processing
3. WHEN structured content is valid, THE Template_Engine SHALL map fields to HTML template variables
4. WHERE structured content is invalid, THE System SHALL log errors and use fallback content

### Requirement 4: Template Separation

**User Story:** As a maintainer, I want HTML formatting separated from content generation, so that template changes don't require LLM prompt updates.

#### Acceptance Criteria

1. WHEN updating HTML templates, THE System SHALL not require changes to LLM prompts
2. WHEN generating content, THE Content_Generator SHALL focus only on content quality and relevance
3. WHEN rendering HTML, THE Template_Engine SHALL handle all formatting, styling, and structure
4. WHERE template variables are missing, THE System SHALL provide sensible defaults or skip optional sections

### Requirement 5: Token Efficiency

**User Story:** As a system operator, I want to minimize token usage, so that generation is cost-effective and faster.

#### Acceptance Criteria

1. WHEN generating content, THE Content_Generator SHALL return only content without HTML markup
2. WHEN making LLM requests, THE System SHALL use focused prompts for each section type
3. WHEN content is structured, THE System SHALL avoid repeating formatting instructions in responses
4. WHEN calculating token usage, THE System SHALL demonstrate significant reduction compared to monolithic approach

### Requirement 6: Error Handling and Fallbacks

**User Story:** As a user, I want the system to handle failures gracefully, so that partial failures don't prevent resume generation.

#### Acceptance Criteria

1. WHEN a section generation fails, THE System SHALL use existing content from the original resume
2. WHEN multiple sections fail, THE System SHALL still produce a complete resume with available content
3. WHEN timeout occurs, THE System SHALL cancel individual requests rather than the entire process
4. WHERE all sections fail, THE System SHALL fall back to the original monolithic generation method

### Requirement 7: Progress Tracking

**User Story:** As a user, I want to see detailed progress of section generation, so that I understand what's happening during the process.

#### Acceptance Criteria

1. WHEN sections are being processed, THE System SHALL report progress for each individual section
2. WHEN sections complete, THE System SHALL update progress indicators in real-time
3. WHEN template rendering begins, THE System SHALL indicate the final assembly phase
4. WHERE sections are running in parallel, THE System SHALL show concurrent progress for multiple sections

### Requirement 9: Comprehensive UI Feedback

**User Story:** As a user, I want detailed, real-time feedback on all generation processes, so that I always know the current status and progress.

#### Acceptance Criteria

1. WHEN any generation process starts, THE System SHALL display initial status within 1 second
2. WHEN processes are running, THE System SHALL update status at least every 5 seconds
3. WHEN running batch operations, THE System SHALL show progress for each individual job in the batch
4. WHEN running single job operations, THE System SHALL show detailed phase-by-phase progress
5. WHERE processes span multiple phases (queue → generate → PDF), THE System SHALL indicate current phase and overall progress
6. WHEN errors occur, THE System SHALL immediately display error status with clear messaging
7. WHEN processes complete, THE System SHALL show completion status and provide next action options

### Requirement 8: Backward Compatibility

**User Story:** As a system maintainer, I want the new system to be backward compatible, so that existing functionality continues to work during transition.

#### Acceptance Criteria

1. WHEN the modular system is deployed, THE System SHALL maintain existing API endpoints
2. WHEN legacy generation is needed, THE System SHALL provide fallback to the original monolithic method
3. WHEN configuration is set, THE System SHALL allow switching between modular and monolithic generation
4. WHERE new system fails, THE System SHALL automatically fall back to the proven legacy approach

**User Story:** As a user, I want to see progress across all phases of job processing, so that I understand the complete workflow status.

#### Acceptance Criteria

1. WHEN jobs are queued (1_queued phase), THE System SHALL show "Preparing job data" status
2. WHEN content generation starts (2_generated phase), THE System SHALL show detailed section progress
3. WHEN PDF generation begins, THE System SHALL show "Converting to PDF" status with file-by-file progress
4. WHEN batch processing multiple jobs, THE System SHALL show overall batch progress plus individual job progress
5. WHERE phase transitions occur, THE System SHALL clearly indicate the phase change
6. WHEN estimating completion time, THE System SHALL provide realistic time estimates based on current progress

**User Story:** As a system maintainer, I want the new system to be backward compatible, so that existing functionality continues to work during transition.

#### Acceptance Criteria

1. WHEN the modular system is deployed, THE System SHALL maintain existing API endpoints
2. WHEN legacy generation is needed, THE System SHALL provide fallback to the original monolithic method
3. WHEN configuration is set, THE System SHALL allow switching between modular and monolithic generation
4. WHERE new system fails, THE System SHALL automatically fall back to the proven legacy approach