# UI Fix Plan: Data Generated Card

## Differences Identified

Comparing the Design Mockup with the Actual Implementation:

### 1. Missing Subcontent Generation State Grid
- **Design**: Shows 8 subcontent items with checkmarks (like Queued phase)
- **Actual**: Missing entirely - only shows document status

### 2. Missing File Links Row (job.yaml, job.log, Error.md)
- **Design**: Shows clickable links with checkmarks: ✅ job.yaml, ✅ job.log, ⚠️ Error.md
- **Actual**: Only shows "Edit job.yaml" and "View job.log" at bottom

### 3. Document Status Icons Wrong
- **Design**: Uses ✅ (complete), ▶️ (ready to generate), 🔒 (locked/waiting)
- **Actual**: Uses ❌ instead of ▶️

### 4. Document Names Don't Match Design
- **Design**: "resume.html", "coverletter.html", "resume.pdf", "coverletter.pdf"
- **Actual**: "Resume HTML", "Cover Letter HTML", etc.

### 5. Section Title Wrong
- **Design**: "Next Steps: Generate Final Documents:"
- **Actual**: Just "Next Steps"

## Implementation Plan (Revised)

### Fix 1: Add Subcontent Grid to Data Generated Phase ✅ DONE
- Reuse the same subcontent grid from Queued phase
- Show checkmarks (✅) for generated sections, ▶️ for missing
- Section names clickable to view/edit the subcontent file

### Fix 2: Add File Links Row ✅ DONE
- Add row with: ✅ job.yaml, ✅ job.log
- ⚠️ Error.md shown only if error.md exists
- Make them clickable links

### Fix 3: Fix Document Status Section ✅ DONE
- Changed section title to "Next Steps: Generate Final Documents"
- Use ▶️ for ready-to-generate (not ❌)
- Use lowercase filenames: resume.html, coverletter.html, resume.pdf, coverletter.pdf
- Keep 🔒 for locked PDFs

### Fix 4: Document grid layout ✅ DONE
- Changed from vertical list to 2-column grid
- Added hover states for clickable items

## Files Modified
- `src/ui/static/js/main.js` - Updated createDataGeneratedPhaseContent() and createDocStatus()
- `src/ui/static/css/main.css` - Added styles for file-links-row and improved doc-status-grid
