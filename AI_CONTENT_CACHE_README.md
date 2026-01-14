# AI Content Cache System

## Overview

The AI Content Cache system saves AI-generated content to files for future use, enabling:

1. **Fast HTML/PDF regeneration** without re-running expensive AI calls
2. **Future user editing capability** of AI-generated content
3. **Consistent content reuse** across multiple regenerations
4. **Debugging and inspection** of AI-generated content

## How It Works

### Content Storage

When AI generates content for resume sections (Summary, Skills, Experience, Cover Letter), the system:

1. **Saves each section** to a separate YAML file in `{job_directory}/ai_content/`
2. **Includes metadata** like generation timestamp, generator used, job info
3. **Preserves structure** for easy editing and reuse

### File Structure

```
src/jobs/2_generated/JobName.ID.Timestamp/
├── ai_content/                    # New cache directory
│   ├── summary.yaml              # AI-generated summary
│   ├── skills.yaml               # AI-generated skills
│   ├── experience.yaml           # AI-generated experience
│   ├── education.yaml            # AI-generated education (if applicable)
│   └── cover_letter.yaml         # AI-generated cover letter
├── JobName.yaml                  # Original job data
├── resume.html                   # Generated resume
├── coverletter.html              # Generated cover letter
└── *.pdf                         # Generated PDFs
```

### Cache File Format

Each cached section file contains:

```yaml
section_name: "summary"
generated_at: "2026-01-10T12:25:36.714482"
content:
  summary: "Professional summary tailored to the job..."
  character_count: 605
metadata:
  cache_version: "1.0"
  generator_type: "ai_generated"
  editable: true
  generator_class: "SummaryGenerator"
  uses_llm: true
  job_title: "Senior Vice President"
  company: "Tech Company"
```

## Usage

### Automatic Caching

The system automatically caches AI content during normal resume generation:

```python
# In step2_generate.py
result = generator.generate_resume(
    resume_data, 
    job_data, 
    job_id, 
    job_directory="/path/to/job/dir",  # Enables caching
    use_cache=True                     # Uses cache when available
)
```

### Regenerate HTML from Cache

Use the "Regenerate HTML Only" button in the web interface, or call:

```python
from step2_generate import regenerate_html_from_cached_content

result = regenerate_html_from_cached_content(
    job_directory="/path/to/job/dir",
    job_data=job_info
)
```

### Manual Cache Management

```python
from utils.ai_content_cache import AIContentCache

# Initialize cache for a job
cache = AIContentCache("/path/to/job/directory")

# Check what's cached
cached_sections = cache.get_cached_sections()
print(f"Cached sections: {cached_sections}")

# Load specific section
summary_content = cache.load_section_content("summary")

# Get cache information
cache_info = cache.get_cache_info()

# Clear cache (optional)
cache.clear_cache("summary")  # Clear specific section
cache.clear_cache()           # Clear all sections
```

## Benefits

### 1. Performance
- **Fast regeneration**: HTML/PDF regeneration takes seconds instead of minutes
- **No API costs**: Reuses existing AI content without new LLM calls
- **Reliable output**: Consistent results every time

### 2. User Experience
- **Quick iterations**: Test template changes rapidly
- **Predictable results**: Same content every regeneration
- **Error recovery**: Regenerate if files are accidentally deleted

### 3. Future Capabilities
- **User editing**: Foundation for allowing users to edit AI content directly
- **Version control**: Track changes to AI-generated content
- **A/B testing**: Compare different AI-generated versions

## Implementation Details

### Cache Integration Points

1. **Section Generators**: Each generator can save/load from cache
2. **Modular Generator**: Orchestrates caching across all sections
3. **Template Engine**: Uses cached content for HTML generation
4. **Web Interface**: "Regenerate HTML Only" uses cached content

### Backward Compatibility

- **Legacy fallback**: If no cache exists, falls back to original YAML parsing
- **Optional caching**: System works with or without cache directory
- **Graceful degradation**: Missing cache files don't break generation

### Error Handling

- **Cache validation**: Verifies cache file structure before use
- **Fallback mechanisms**: Uses original content if cache is corrupted
- **Logging**: Comprehensive logging for debugging cache issues

## Testing

Run the test suite to verify caching functionality:

```bash
python test_ai_content_cache.py
```

Tests cover:
- Basic save/load functionality
- Job directory discovery
- Real job directory integration
- Error handling and edge cases

## Future Enhancements

### Phase 1 (Current)
- ✅ Automatic content caching during generation
- ✅ Fast HTML/PDF regeneration from cache
- ✅ Cache management utilities

### Phase 2 (Planned)
- 🔄 Web interface for viewing cached content
- 🔄 User editing of cached AI content
- 🔄 Cache versioning and history

### Phase 3 (Future)
- 📋 A/B testing of different AI outputs
- 📋 Content approval workflows
- 📋 Collaborative editing features

## Troubleshooting

### Cache Not Working
1. Check if job directory is passed to generation functions
2. Verify `ai_content` directory exists and is writable
3. Check logs for cache-related errors

### Regeneration Issues
1. Ensure cached content files exist and are valid YAML
2. Check that job data is available for template rendering
3. Verify template engine can access cached content structure

### Performance Issues
1. Cache directory should be on fast storage
2. Large cache files may slow down loading
3. Consider cache cleanup for old jobs

## Version History

- **v1.5.20260110.60**: Initial AI Content Cache implementation
- **v1.5.20260110.59**: Cache integration with modular generation
- **v1.5.20260110.58**: Section generator cache support
- **v1.5.20260110.57**: Base cache infrastructure