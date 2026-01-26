# Business Objective 
Skillsnap goal is to reduce the amount of time required to create bespoke resumes to online job postings from hours to a few minutes.  Users login, create a resume within the application.  They can connect their skillsnap account to their gmail and automatically retrieve "LinkedIn Job Alert" emails, visit each job posting for the job descrption, then decompose that down into structured data that is saved.  Finally, upon request, a user can request a bespoke resume be created by combining one of their resumes with a job description, using AI to select the most relevent parts of their resume and gently modify word choice to be more ATS friendly. 

When asked to Generate Job files, Skillsnap application will create the following content:
- resume.html: bespoke resume for the job posting
- coverletter.html: bespoke cover letter for the job posting
- resume.pdf:  a pdf of resume.html
- coverletter.pdf: a pdf of coverletter.html
- custom online resume url: https://{username}.skillsnap.me/{company}/{jobtitlesafe} 
  - resumes are stored in `S3://skillsnap-public-resumes/{username}/{company}/{jobtitlesafe}/resume.html` or `/coverletter.html` or `/resume.pdf` or `/coverletter.pdf`
  - Use S3 bucket + CloudFront + *.skillsnap.me + CloudFront Function rewrite
  - See `Appendix A: CloudFront Function` for previous AI output / suggestions


This mainly targets more senior professionals who have accumulated a lot of experience and want to quickly generate tailored resumes, rather than sending out a 3 or 4 page complete resume. 

If successful, this allows users to auto-generate dozens of bespoke resumes for dozens of jobs, all in a few minutes, helping them find jobs faster and more efficiently.  Remember, you don't have to outrun the bear, just all other competition. 

Snapskill does NOT apply for the job directly; it only generates resumes and cover letters that are customized for best chance of success. It also helps organize the job search.  However it does not actually apply for positions on behalf of the user (yet).


## Phases of Job Migration
Snapskill will can also help keep applicants organized, building a pipeline of job opportunities and organizing them into phases. These phases apply to all jobs, and the UI should allow for filtering job cards by phase:
- Search:      Job is identified, but information is still being gathered
- Queued:      Jon data is gathered and stored, but resume has not yet been generated
- Generating:  Bespoke AI generated resume is in progress
- Ready:       Bespoke AI resume and cover letter have been generated, both in HTML and PDF, and made available via custom webpage 
- Applied:     User-defined action: they have applied to the job
- Follow-Up:   User-defined action: they have followed-up with the applied company
- Negotiation: User-defined action: they have entered into final negotiations /discussions with the hiring company
- Accepted:    User-defined action: they have accepted a position!  Whoot!
- Skipped :    User-defined action: they have decided not to apply for this job
- Expired:     Automatic action: the job has expired, either being more than 30day old, or marked as "filled"
- Errored:     Some unknown error has occured; the user can address and resubmit if they wish



# Architecture Design
I would like to keep costs 1:1 scalable with user growth, while still leveraging the scalability of AWS.  This means all (or at least most) serverless / hosted projects in AWS.   

Additionally, there are several components that can generate data in parallel, meaning an event-based architecture.  The workflow is not complex, and I'm leaning towards a more simple solution like SQS rather than the more complex EventBridge; however, there may be some time-based activities that require some EventBridge.  

Below are the major components, listed in chronological order in which most users will encounter them:


## Landing Page:
The landing page / main public webpage is https://skillsnap.me  and should look like a fun, edgy but professional website.  The url is registered in AWS Route53 already, and the AWS Cert Manager already setup for https (although not tested yet).

The landing page should feel dynamic and interesting, but ultimately is a static site, so could be hosted in S3 with CloudFront CDN.
The landing page is a single page application, with a login button that redirects to Cognito for authentication to access the webapp component.



## Authentication: 
I need the site to be highly secure, both the API Gateway as well as the landing

Cognito for authentication, with optional GMail integration for "LinkedIn Job Alerts"
Part of the product is connecting to a user's gmail account, searching and returning "LinkedIn Job Alerts" to the engine, so the process will need a "gmail integration" point, ONLY to allow the return of "LinkedIn Job Alerts" emails. 



## Web App:
The webapp should be mostly a React app, hosted in S3, with a CDN in front of it (via CloudFront).  It will communicate with the backend via API Gateway.
The CSS / look and feel should be similar to the landing page, that is: fun, a little edgy, but ultimately professional.
All content and APIs should be protected by Cognito authentication.

The webapp subdomain should be:   
- app.skillsnap.me: the main webapp subdomain
- api.skillsnap.me: the api gateway endpoint

For a full description of the webapp, see "Appendix B: WebApp Requirements"


## API Gateway
API Gateway will driver all major non-UI functionality for the webapp, and will be used to communicate with the backend services.
It will be secured via Cognito authentication.
It will be used to communicate with the backend services, including:
- Lambda functions
- DynamoDB
- S3
- Gmail API


## Lambda Functions
Provide the compute for API requests, and will be triggered by events from EventBridge or SQS.  Also supports internal-only functions.  

Some examples of lambda functions needed(many of which require API endpoints to faciliate web front-end work):

- Create User Resume
- Get User Resume
- Edit User Resume

- Get User Prefs
- Save User Prefs

- Get all jobs
- Get all jobs by status
- Get all jobs by filter

- Generate Contact Manual
- Generate Contact AI
- Generate Summary Manual
- Generate Summary AI
- Generate Skills Manual
- Generate Skills AI
- Generate Highlights Manual
- Generate Highlights AI
- Generate Experience Manual
- Generate Experience AI
- Generate Education Manual
- Generate Education AI
- Generate Awards Manual
- Generate Awards AI
- Generate CoverLetter Manual
- Generate CoverLetter AI
- Generate Bespoke Resume HTML
- Generate Bespoke Resume PDF
- Generate Bespoke CoverLetter HTML
- Generate Bespoke CoverLetter PDF
- Get job all subcontent status
- Get job all finalfile location and status

- Update Job Phase
- Get Job Data 
- Save Job Data
- New Jobs from Gmail
- New Job from URL
- New Job from Manual Entry

...And many more as needed.

 
## Simple Queuing Service (SQS)
Some jobs require async execution, such as generating multiple subcomponents at once.  For these processes, the API can queue up the work to SQS along with needed information or PK to look up information.  


## DynamoDB Tables 
Persistent data store will be performed by DynamoDB, with the following recommended table structure.  Other tables can be created as needed.


### USER 
The main table that joins most all other tables together
- userid (pk): uuid7 for the user
- userhandle: user handle which is displayed
- {other}: other columns required to facilitate IAM auth/authz 
- {other}: other columns required to authorize searching GMail for "LinkedIn Job Alerts" (optional)

### USER_EMAIL
Only exists to enforce email uniqueness.
- useremail (pk): user's unique email address
- userid: points back to USER.userid 

### USER_USERNAME
Only exists to enforce username uniqueness.
- username (pk): user name for logging in 
- userid: points back to USER.userid
 
### USER_PREF 
Preference storage for the web interface and AI generation
- userid (pk): joins with USER.userid 
- prefname (sk): Name part of the name/value pair, representing one of N-number of user preferences
- prefvalue: Value part of the name/value pair, representing one of N-number of user preferences

**Examples of user preferences:** 
- default_gen_contact: default generation state for "contact" data, i.e., other "static" or "ai" 
- default_gen_summary: default generation state for "summary" data, i.e., other "static" or "ai" 
- default_gen_skills: default generation state for "skills" data, i.e., other "static" or "ai" 
- default_gen_highlights: default generation state for "highlights" data, i.e., other "static" or "ai" 
- default_gen_experience: default generation state for "experience" data, i.e., other "static" or "ai" 
- default_gen_education: default generation state for "education" data, i.e., other "static" or "ai" 
- default_gen_awards: default generation state for "awards" data, i.e., other "static" or "ai" 
- default_gen_coverletter: default generation state for "coverletter" data, i.e., other "static" or "ai" 

### JOB
Defines a single job posting, digested down into data that can be used to guide bespoke resume generation
- jobid (pk): uuid7 for the job
- postedts: the posting company or site (linkedin, indeed, mosnster, etc.)
- jobcompany: hiring company name
- joblistid: ID assigned by the posting site (linkedin, indeed, etc.) 
- jobtitle: job title
- jobtitlesafe: job title stripped of all non-alphanum characters (aka url safe / filesystem safe)
- jobdesc: job description
- joblocation: job location
- jobsalary: job salary
- jobposteddate: date the job was posted
- joburl: url to apply for the job
- jobcompanylogo: url to the company logo
- jobtags: [] list of word-or-phrase tags


### USER_JOB
Intersection of the user and what jobs they have entered / want to apply for
- userid (pk): points back to USER.userid
- jobid (sk): points back to JOB.jobid
- jobphase: the phase of the job's development / interest to the user 
- datacontacts: data generated for the "contact" section of the resume, in html format
- datasummary: data generated for the "summary" section of the resume, in html format
- dataskills: data generated for the "skills" section of the resume, in html format
- datahighlights: data generated for the "highlights" section of the resume, in html format
- dataexperience: data generated for the "experience" section of the resume, in html format
- dataeducation: data generated for the "education" section of the resume, in html format
- dataawards: data generated for the "awards" section of the resume, in html format
- datacoverletter: data generated for the "coverletter" section of the resume, in html format
- s3locresumehtml: the S3 location where the resume.html file is stored
- s3locresumepdf: the S3 location where the resume.pdf file is stored
- s3loccoverletterhtml: the S3 location where the coverletter.html file is stored
- s3loccoverletterpdf: the S3 location where the coverletter.pdf file is stored

If the `s3loc*` fields in USER_JOB are missing or empty, the file is assumed to NOT exist.  
When a file is generated, it should be saved to S3 and then update the `s3loc*` field.
See `Appendix A: CloudFront Function` for details.

### RESUME
User resume information in a single json doc, unique per userid / resumename
- userid (pk): points back to USER.userid
- resumename (sk)
- resumejson: json document containing the complete resume information
- lastupdate: timestamp of last update


### RESUME_URL
Maintains a unique list of static hosted URL (in S3), as {username}.skillsnap.me/{company}/{jobtitle}
Each user will always own {username}.skillsnap.me/
- resumeurl (pk): the unique resume url, aka `https://{username}.skillsnap.me/{company}/{jobtitle}`
- userid: points back to USER.userid





# Appendix A: CloudFront Function
Here’s the clean pattern:

## Recommended asset strategy
### Global, shared CSS/JS (cached hard)

Serve these from a fixed path that never gets rewritten:
- https://skillsnap.me/assets/app.css
- https://skillsnap.me/assets/resumebase.css

Then in your resume HTML, include:
```html
<link rel="stylesheet" href="https://skillsnap.me/assets/resume-base.css">
<link rel="stylesheet" href="https://skillsnap.me/assets/cover-base.css">
```

### Per-resume overrides
To support user overrides of the CSS, resume HTML can also include an override stylesheet that lives under the resume path:

```html
<link rel="stylesheet" href="./resume-override.css">
<link rel="stylesheet" href="./cover-override.css">
```


That resolves to:
```html
https://{username}.skillsnap.me/{company}/{jobtitlesafe}/resume-override.css
```

…and you store it in S3 at:
`/{username}/{company}/{jobtitlesafe}/resume-override.css`

and the same with cover-override.css (for cover letters).

This gives you:
- default global styling for everyone
- “just drop an override file” to customize a specific resume
- no API/Lambda required

## What you need to change in the CloudFront Function

You want the function to:

1. Rewrite HTML routes like `/{company}/{job}` → `/{username}/{company}/{job}/index.html`
2. NOT rewrite global assets like `/assets/base.css` (so they stay global)
3. Allow resume-local assets like `/{company}/{job}/override.css` to be rewritten to `/{username}/{company}/{job}/override.css`

So the rule should be:
- passthrough: `/assets/*`, `/static/*`, `/favicon.ico`, etc.
- rewrite everything else by prefixing username
- only force `/index.html` when the path is exactly 2 segments

## Updated CloudFront Function (does exactly that)
```JS
function handler(event) {
  var request = event.request;
  var headers = request.headers;

  // Extract host and username
  var host = headers.host && headers.host.value ? headers.host.value : "";
  host = host.split(":")[0].toLowerCase();

  // Default for apex domain requests
  var username = "www";
  var parts = host.split(".");
  if (parts.length >= 3) username = parts[0];

  var uri = request.uri || "/";
  if (uri === "") uri = "/";

  // 1) Global assets: DO NOT rewrite (keep them shared)
  // Put all shared CSS/JS under /assets/ (or /_global/) and keep it stable.
  if (
    uri.indexOf("/assets/") === 0 ||
    uri.indexOf("/_global/") === 0 ||
    uri === "/favicon.ico" ||
    uri === "/robots.txt" ||
    uri === "/sitemap.xml"
  ) {
    return request;
  }

  // 2) User root -> user homepage
  if (uri === "/") {
    request.uri = "/" + username + "/index.html";
    return request;
  }

  // Normalize trailing slash
  if (uri.length > 1 && uri.charAt(uri.length - 1) === "/") {
    uri = uri.slice(0, -1);
  }

  // Split segments
  var segs = uri.split("/").filter(Boolean);

  // 3) Exactly "/company/job" -> "/username/company/job/index.html"
  if (segs.length === 2) {
    request.uri = "/" + username + "/" + segs[0] + "/" + segs[1] + "/index.html";
    return request;
  }

  // 4) Anything deeper (e.g. "/company/job/override.css") -> prefix username
  request.uri = "/" + username + uri;
  return request;
}
```

## S3 layout that matches this perfectly

Global:
- `s3://bucket/assets/base.css`
- `s3://bucket/assets/app.js` (if needed)

Per resume:
- 's3://bucket/{username}/{company}/{jobtitlesafe}/index.html'
- `s3://bucket/{username}/{company}/{jobtitlesafe}/override.css` (optional)
- `s3://bucket/{username}/{company}/{jobtitlesafe}/photo.jpg` (optional)

### One gotcha to avoid

If you reference global CSS with a relative path like:
```html
<link rel="stylesheet" href="/assets/base.css">
```

that’s fine (it will hit /assets/ and bypass rewriting).

But do not do:
```html
<link rel="stylesheet" href="assets/base.css">
```

because from `/company/job` that becomes `/company/assets/base.css` (not global).

Use absolute `/assets/`... or a full URL.

Cache behavior tip
- Set long TTL on /assets/* (version your filenames if you want instant deploys: base.8f3c.css)
- Set shorter TTL or cache-bust strategy for index.html if users edit it

So: global defaults + per-resume overrides works great with CloudFront Functions and a single bucket.


# Appendix B: WebApp Requirements
The webapp is broken into main page / wrapper functionailty, and job card functionality.   

## Main Page Wrapper
The main page wrapper manages functionality of the entire application, and acts as a container for N-number of job cards.  Functions in the main page wrapper include:
- Header with, left to right:
    - Logo
    - Navigation
    - Add new job button (fetch from email / get from URL / manually enter)
    - User profile picture / settings / view logs
- Sidebar with:
    - Resume select / edit / add
    - Phases with counts, clicking filters
    - Phase Aggregations (All Active // All Jobs)
- Main content area
    - filtererd list of job cards

## Job Cards
Each job card represents a single job that the user is interested in applying to.  Each job card contains several sections (top to bottom):

### Header
- Company name:  links to company website, if known, otherwise shows company name only
- Job title:  links to original public job post URL, i.e., https://www.linkedin.com/jobs/view/4355347055
- Phase indicator / picker:  allows user to move the job to another phase ( aka "Phase", i.e., "Queued",, "Generating", "Ready", "Applied", etc.)
- Posting Age: # days old;  aka today() - posting date, rounded to nearest day
- Location: location of the job
- Salary: salary being offered
- Source of the job location (linkedin, manual, etc.): links to original source
- Job Tags: tags pulled from the job, like "3 contacts", "fast growth", etc.

### Subcomponet Generation 
- "Description": link to pop-out editor for the full job description, with "Save" and "Cancel"
- Generate All: is the same as clicking all "generate" icons of the 8 subcomponents below:
- list of subcontent to generate, in two columns:
    - Column 1
        - Contact: links to Contact editor pop-out
        - Summary: links to Summary editor pop-out
        - Skills: links to Skills editor pop-out
        - Highlights: links to Highlights editor pop-out
    - Column 2
        - Experience:  links to Experience editor pop-out
        - Education:  links to Education editor pop-out
        - Awards:  links to Awards editor pop-out
        - Cover Letter:  links to Cover Letter editor pop-out

### Final File Generation
    - Column 1: 
        - Resume HTML: indicates whether final file generation (aggregation of subcomponents) is complete; click to edit in pop-out window
        - Resume PDF:  indicates whether final file generation (aggregation of subcomponents) is complete; click to edit in pop-out window
    - Column 2: 
        - Cover Letter HTML: indicates whether final file generation (aggregation of subcomponents) is complete; click to edit in pop-out window     
        - Cover Letter PDF:  indicates whether final file generation (aggregation of subcomponents) is complete; click to edit in pop-out window    
 

## Logos on the Job Card

For the two columns in the "**Subcomponet Generation**" section, each item has two icons:
- Icon 1: generation state - clicking the icon generates / regenerates the content based on generation type toggle selected
    - 🔒 locked / cannot be generated at this time (dependencies not met)
    - ▶️ ready to generate
    - 💫 currently generating
    - ✅ generate complete
    - ⚠️ generation error
- Icon 2: generation type toggle - clicking the icon toggles between the two
    - ⚙️ manual
    - 🧠 AI
- Title: clicking on the title opens a pop-out editor window, to allow manual adjustments

For exmaple, `▶️ 🧠 Skills` would mean "ready to generate, using AI".
- clicking ▶️ = generates the Skills section, using AI
- clicking 🧠 = toggles generation type to "manual"
- clicking `Skills` = opens a pop-out view / editing window, with "Save" and "Cancel"


For the two columns in the "**Final File Generation**" section, each item has one icon:
- Icon 1: generation state: clicking the icon generates / regenerates the content based on generation type toggle selected
    - 🔒 locked / cannot be generated at this time (dependencies not met)
    - ▶️ ready to generate
    - 💫 currently generating
    - ✅ generate complete
    - ⚠️ generation error
- Title: clicking on the title opens a pop-out editor window, to allow manual adjustments

For exmaple, 
`🔒 Resume.html` would mean "dependency not met to generate final html resume file"
`✅ Resume.html` would mean "finished generating final html resume file" and save to S3 for private resume URL, and updates DDB with URI to files.



# Appendix C: Initial Kiro Response

Got it! This is a solid foundation. Let me summarize the key decisions and then we'll get building:

Tech Stack Summary:

IaC: AWS CDK (Python) — great fit since you prefer Python and it's more expressive than SAM for complex architectures
Region: us-west-2
Auth: Cognito with Google social login (covers Gmail OAuth too) + email/password option
AI: AWS Bedrock (Nova Lite initially, abstracted for easy model swaps)
Lambda: Python 3.12
Frontend: React with a modern component library (I'll use Tailwind + shadcn/ui for that polished, edgy-but-professional look)
Database: DynamoDB with the schema from requirements.md (I'll fix the RESUME table to use composite key)
Resume JSON Schema: I'll convert your YAML to JSON as the base structure.

Let me create the project structure. Given this is V1 (not MVP), I'll scaffold the full architecture:

skillsnap/
├── infrastructure/          # CDK stacks
│   ├── stacks/
│   │   ├── auth.py         # Cognito + Google OAuth
│   │   ├── api.py          # API Gateway + Lambda
│   │   ├── database.py     # DynamoDB tables
│   │   ├── storage.py      # S3 buckets + CloudFront
│   │   └── frontend.py     # Landing page + webapp hosting
│   └── app.py
├── backend/
│   └── lambdas/            # Python Lambda functions
├── frontend/
│   ├── landing/            # Static landing page
│   └── webapp/             # React app
└── shared/
    └── schemas/            # JSON schemas (resume, job, etc.)