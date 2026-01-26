/**
 * Skillsnap TypeScript Types
 * Requirements: Data Models from design.md
 */

// Job Phases
export type JobPhase = 
  | 'Queued' | 'Generating' | 'Ready'
  | 'Applied' | 'Follow-Up' | 'Negotiation' | 'Accepted'
  | 'Skipped' | 'Expired' | 'Errored' | 'Trash';

export const VALID_PHASES: JobPhase[] = [
  'Queued', 'Generating', 'Ready',
  'Applied', 'Follow-Up', 'Negotiation', 'Accepted',
  'Skipped', 'Expired', 'Errored', 'Trash'
];

export const ACTIVE_PHASES: JobPhase[] = [
  'Queued', 'Generating', 'Ready',
  'Applied', 'Follow-Up', 'Negotiation'
];

// Generation States
export type GenerationState = 'locked' | 'ready' | 'generating' | 'complete' | 'error';

// Generation Types
export type GenerationType = 'manual' | 'ai' | 'omit';

// Subcomponent Types
export type SubcomponentType = 
  | 'contact' | 'summary' | 'skills' | 'highlights'
  | 'experience' | 'education' | 'awards' | 'keynotes' | 'coverletter';

export const SUBCOMPONENTS: SubcomponentType[] = [
  'contact', 'summary', 'skills', 'highlights',
  'experience', 'education', 'awards', 'keynotes', 'coverletter'
];

// Generation type restrictions per component
export const GENERATION_TYPE_RESTRICTIONS: Partial<Record<SubcomponentType, GenerationType[]>> = {
  experience: ['manual', 'ai'],      // Cannot be 'omit'
  highlights: ['ai', 'omit'],        // Cannot be 'manual'
  coverletter: ['ai', 'omit'],       // Cannot be 'manual'
};

// Contact Item (for list of contact methods)
export interface ContactItem {
  icon: 'email-at' | 'phone' | 'phone-volume' | 'linkedin' | 'x-twitter' | 'bluesky' | 'github' | 'github-square' | 'globe-solid' | 'house-solid' | 'facebook' | 'discord' | 'slack' | 'telegram' | 'whatsapp' | 'signal-chat';
  title: string;
  url: string;
}

// Contact Info
export interface Contact {
  name: string;
  location?: string;
  items: ContactItem[];
}

// Experience Bullet
export interface ExperienceBullet {
  text: string;
  tags: string[];
}

// Experience Role
export interface ExperienceRole {
  title: string;
  startDate: string;
  endDate?: string;
  current: boolean;
  location?: string;
  bullets: ExperienceBullet[];
}

// Experience Company
export interface ExperienceCompany {
  name: string;
  url?: string;
  employees?: string;
  startDate: string;
  endDate?: string;
  current: boolean;
  location?: string;
  description?: string;
  roles: ExperienceRole[];
}

// Legacy Experience Entry (for backward compatibility)
export interface Experience {
  company: string;
  title: string;
  startDate: string;
  endDate?: string;
  current: boolean;
  description: string;
  achievements: string[];
}

// Education Entry
export interface Education {
  institution: string;
  degree: string;
  field: string;
  graduationDate: string;
  gpa?: string;
}

// Award Entry
export interface Award {
  title: string;
  issuer: string;
  date: string;
  description?: string;
}

// Keynote Entry
export interface Keynote {
  title: string;
  event: string;
  date: string;
  location?: string;
}

// Resume JSON
export interface ResumeJSON {
  contact: Contact;
  summary: string;
  skills: string[];
  highlights: string[];
  experience: Experience[] | ExperienceCompany[];
  education: Education[];
  awards: Award[];
  keynotes: Keynote[];
}

// Resume
export interface Resume {
  userid: string;
  resumename: string;
  resumejson: ResumeJSON;
  lastupdate: string;
}

// Job
export interface Job {
  jobid: string;
  postedts: string;
  jobcompany: string;
  joblistid?: string;
  jobtitle: string;
  jobtitlesafe: string;
  jobdesc: string;
  joblocation?: string;
  jobsalary?: string;
  jobposteddate: string;
  joburl?: string;
  jobcompanylogo?: string;
  jobtags: string[];
  createdAt: string;
}

// User Job (combined with Job for display)
export interface UserJob extends Job {
  userid: string;
  resumeid: string;
  jobphase: JobPhase;
  
  // Subcomponent data
  datacontact?: string;
  datasummary?: string;
  dataskills?: string;
  datahighlights?: string;
  dataexperience?: string;
  dataeducation?: string;
  dataawards?: string;
  datakeynotes?: string;
  datacoverletter?: string;
  
  // Generation states
  statecontact: GenerationState;
  statesummary: GenerationState;
  stateskills: GenerationState;
  statehighlights: GenerationState;
  stateexperience: GenerationState;
  stateeducation: GenerationState;
  stateawards: GenerationState;
  statekeynotes: GenerationState;
  statecoverletter: GenerationState;
  
  // Generation types
  typecontact: GenerationType;
  typesummary: GenerationType;
  typeskills: GenerationType;
  typehighlights: GenerationType;
  typeexperience: GenerationType;
  typeeducation: GenerationType;
  typeawards: GenerationType;
  typekeynotes: GenerationType;
  typecoverletter: GenerationType;
  
  // Final file locations
  s3locresumehtml?: string;
  s3locresumepdf?: string;
  s3loccoverletterhtml?: string;
  s3loccoverletterpdf?: string;
  
  // Calculated fields
  postingAge?: number;
  updatedAt: string;
}

// User Preferences
export interface UserPreferences {
  default_gen_contact: GenerationType;
  default_gen_summary: GenerationType;
  default_gen_skills: GenerationType;
  default_gen_highlights: GenerationType;
  default_gen_experience: GenerationType;
  default_gen_education: GenerationType;
  default_gen_awards: GenerationType;
  default_gen_keynotes: GenerationType;
  default_gen_coverletter: GenerationType;
  // Resume Generation Options
  show_year_education?: boolean;
  show_year_awards?: boolean;
  show_year_keynotes?: boolean;
  combine_awards_keynotes?: boolean;
  cutoff_year?: number;
}

// API Response Types
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface JobListResponse {
  jobs: UserJob[];
  count: number;
  phaseCounts: Record<JobPhase, number>;
  totalCount: number;
}

export interface ResumeListResponse {
  resumes: Resume[];
  count: number;
}

export interface GenerationStatusResponse {
  jobid: string;
  phase: JobPhase;
  overallStatus: 'ready' | 'generating' | 'complete' | 'error';
  subcomponents: Record<SubcomponentType, {
    state: GenerationState;
    type: GenerationType;
    hasContent: boolean;
  }>;
  finalFiles: {
    resumeHtml: { ready: boolean; generated: boolean; s3loc: string };
    resumePdf: { ready: boolean; generated: boolean; s3loc: string };
    coverLetterHtml: { ready: boolean; generated: boolean; s3loc: string };
    coverLetterPdf: { ready: boolean; generated: boolean; s3loc: string };
  };
  allComplete: boolean;
}

// User
export interface User {
  userid: string;
  userhandle: string;
  email: string;
  username: string;
}
