# Instructions for AI generated resume/cover letter 
(for now - webUI coming soon).

1. Find a job description for which you want to apply.
   <br> For example, [this snowflake job](https://careers.snowflake.com/us/en/job/SNCOUSA6DCE1C77384481D9382BAF72018F745EXTERNALENUS7AB43CEB3E174E9F94ED9263664CE36E/Director-Sales-Operations-Go-to-Market-Planning).
2. Open up the web page, highlight all the relevent information, and COPY (cmd-c) to your clipboard.
3. Open up this webpage in your browser:<br>
https://www.pastetomarkdown.com/
4. PASTE the job description from your clipboard into the above webpage - it will convert it to Markdown (a simplified web syntax).  Then COPY the output markdown to your clipboard.
5. Create a new job file in the "jobs" folder in this project, following the format: "{company}_{Job Title}.md" and PASTE in the markdown content, and save. 
6. Make sure you have defined a yaml file with your information in the "people" folder.  If you haven't, use template.yaml as a starting point.  
7. In a terminal, execute the python program: <br>
`python3 ./src/build_resume.py <person.yaml> <job.md>`<br>
The process will pause and ask you for any optional prompts you want to add before submission to the AI.  This is completely optional, but is a good place to add nuance. For example, if applying to a startup, you could add `be sure to highlight experience at early-stage product start-ups`, or `make sure this fits on two pages, drop earlier experience if needed.`

## Output:
This will generate 2 files, both in the `output` directory: 
- `<person>_<job>_resume.docx`
- `<person>_<job>_letter.docx` 

That's it!  Rinse / Repeat as needed!

## Warning: 
Please always double-check your resume before sending!  While GenAI is an awesome tool and the system prompts are very clear to NOT FABRICATE INFORMATION, it is instructed to adjust wordings to align phrasing and prioritization of the resume to fit the job.  For Sr. level jobs, this "adjusted wording" can sometimes change the nuance communicated to be subtly incorrect.  AKA always double-check the AI's work, and adjust as needed (hence it's .docx not pdf).
