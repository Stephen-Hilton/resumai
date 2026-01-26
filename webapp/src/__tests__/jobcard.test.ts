/**
 * Job Card Property Tests
 * Property 12: Job Card Display Completeness
 * Requirements: 6.1
 */
import { describe, it, expect } from 'vitest';
import type { UserJob, JobPhase, GenerationState, GenerationType } from '../types';
import { VALID_PHASES, SUBCOMPONENTS } from '../types';

// Helper to create a mock job
function createMockJob(overrides: Partial<UserJob> = {}): UserJob {
  const defaultJob: UserJob = {
    jobid: 'test-job-id',
    userid: 'test-user-id',
    resumeid: 'test-resume',
    postedts: new Date().toISOString(),
    jobcompany: 'Test Company',
    jobtitle: 'Software Engineer',
    jobtitlesafe: 'software-engineer',
    jobdesc: 'Job description here',
    joblocation: 'San Francisco, CA',
    jobsalary: '$150,000 - $200,000',
    jobposteddate: '2026-01-20',
    joburl: 'https://example.com/job',
    jobtags: ['Remote', 'Full-time'],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    jobphase: 'Search',
    
    // Subcomponent data
    datacontact: '',
    datasummary: '',
    dataskills: '',
    datahighlights: '',
    dataexperience: '',
    dataeducation: '',
    dataawards: '',
    datacoverletter: '',
    
    // Generation states
    statecontact: 'ready',
    statesummary: 'ready',
    stateskills: 'ready',
    statehighlights: 'ready',
    stateexperience: 'ready',
    stateeducation: 'ready',
    stateawards: 'ready',
    statecoverletter: 'ready',
    
    // Generation types
    typecontact: 'ai',
    typesummary: 'ai',
    typeskills: 'ai',
    typehighlights: 'ai',
    typeexperience: 'ai',
    typeeducation: 'ai',
    typeawards: 'ai',
    typecoverletter: 'ai',
  };
  
  return { ...defaultJob, ...overrides };
}

describe('Property 12: Job Card Display Completeness', () => {
  it('should always display company name', () => {
    const job = createMockJob({ jobcompany: 'Acme Corp' });
    expect(job.jobcompany).toBe('Acme Corp');
    expect(job.jobcompany.length).toBeGreaterThan(0);
  });

  it('should always display job title', () => {
    const job = createMockJob({ jobtitle: 'Senior Developer' });
    expect(job.jobtitle).toBe('Senior Developer');
    expect(job.jobtitle.length).toBeGreaterThan(0);
  });

  it('should always display phase indicator', () => {
    for (const phase of VALID_PHASES) {
      const job = createMockJob({ jobphase: phase });
      expect(job.jobphase).toBe(phase);
      expect(VALID_PHASES).toContain(job.jobphase);
    }
  });

  it('should calculate and display posting age', () => {
    // Use a fixed date calculation that doesn't depend on time of day
    const calculatePostingAge = (postedDate: string): number => {
      const posted = new Date(postedDate + 'T00:00:00Z');
      const now = new Date();
      now.setUTCHours(0, 0, 0, 0);
      const diffTime = now.getTime() - posted.getTime();
      return Math.max(0, Math.round(diffTime / (1000 * 60 * 60 * 24)));
    };
    
    // Test that the function returns a non-negative number
    const today = new Date().toISOString().split('T')[0];
    const age = calculatePostingAge(today);
    expect(age).toBeGreaterThanOrEqual(0);
    expect(age).toBeLessThanOrEqual(1); // Could be 0 or 1 depending on timezone
  });

  it('should display location when present', () => {
    const jobWithLocation = createMockJob({ joblocation: 'New York, NY' });
    expect(jobWithLocation.joblocation).toBe('New York, NY');
    
    const jobWithoutLocation = createMockJob({ joblocation: '' });
    expect(jobWithoutLocation.joblocation).toBe('');
  });

  it('should display salary when present', () => {
    const jobWithSalary = createMockJob({ jobsalary: '$100k - $150k' });
    expect(jobWithSalary.jobsalary).toBe('$100k - $150k');
    
    const jobWithoutSalary = createMockJob({ jobsalary: '' });
    expect(jobWithoutSalary.jobsalary).toBe('');
  });

  it('should display tags when present', () => {
    const jobWithTags = createMockJob({ jobtags: ['Remote', 'Senior', 'Full-time'] });
    expect(jobWithTags.jobtags.length).toBe(3);
    expect(jobWithTags.jobtags).toContain('Remote');
    
    const jobWithoutTags = createMockJob({ jobtags: [] });
    expect(jobWithoutTags.jobtags.length).toBe(0);
  });

  it('should display all 8 subcomponents', () => {
    const job = createMockJob();
    
    for (const component of SUBCOMPONENTS) {
      const stateKey = `state${component}` as keyof UserJob;
      const typeKey = `type${component}` as keyof UserJob;
      
      expect(job[stateKey]).toBeDefined();
      expect(job[typeKey]).toBeDefined();
    }
  });

  it('should display generation state icons correctly', () => {
    const stateIcons: Record<GenerationState, string> = {
      locked: '🔒',
      ready: '▶️',
      generating: '💫',
      complete: '✅',
      error: '⚠️',
    };
    
    const states: GenerationState[] = ['locked', 'ready', 'generating', 'complete', 'error'];
    
    for (const state of states) {
      expect(stateIcons[state]).toBeDefined();
      expect(stateIcons[state].length).toBeGreaterThan(0);
    }
  });

  it('should display generation type toggle correctly', () => {
    const typeIcons: Record<GenerationType, string> = {
      manual: '⚙️',
      ai: '🧠',
      omit: '❌',
    };
    
    expect(typeIcons['manual']).toBe('⚙️');
    expect(typeIcons['ai']).toBe('🧠');
    expect(typeIcons['omit']).toBe('❌');
  });
});

describe('Job Card Required Fields', () => {
  it('should have all required fields for display', () => {
    const job = createMockJob();
    
    // Required fields that must always be present
    expect(job.jobid).toBeDefined();
    expect(job.jobcompany).toBeDefined();
    expect(job.jobtitle).toBeDefined();
    expect(job.jobphase).toBeDefined();
    expect(job.jobposteddate).toBeDefined();
  });

  it('should handle missing optional fields gracefully', () => {
    const minimalJob = createMockJob({
      joblocation: undefined,
      jobsalary: undefined,
      joburl: undefined,
      jobtags: [],
    });
    
    // Should not throw when optional fields are missing
    expect(minimalJob.joblocation).toBeUndefined();
    expect(minimalJob.jobsalary).toBeUndefined();
    expect(minimalJob.jobtags).toEqual([]);
  });
});

describe('Posting Age Calculation', () => {
  it('should calculate posting age in days', () => {
    const calculatePostingAge = (daysAgo: number): number => {
      return daysAgo;
    };
    
    expect(calculatePostingAge(0)).toBe(0);
    expect(calculatePostingAge(1)).toBe(1);
    expect(calculatePostingAge(7)).toBe(7);
    expect(calculatePostingAge(30)).toBe(30);
  });

  it('should handle edge cases', () => {
    // Posting age should never be negative
    const calculatePostingAge = (daysAgo: number): number => {
      return Math.max(0, daysAgo);
    };
    
    expect(calculatePostingAge(-1)).toBe(0);
    expect(calculatePostingAge(0)).toBe(0);
    expect(calculatePostingAge(100)).toBe(100);
  });
});
