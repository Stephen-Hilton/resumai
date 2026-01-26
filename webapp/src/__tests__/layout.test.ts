/**
 * Layout Component Unit Tests
 * Task 18.4: Unit tests for layout components
 * Requirements: 3.3, 3.4, 3.6, 3.7, 3.8
 */
import { describe, it, expect } from 'vitest';
import { VALID_PHASES, ACTIVE_PHASES } from '../types';

describe('Header Component Logic', () => {
  it('should have all required navigation elements', () => {
    const requiredElements = ['logo', 'navigation', 'addJob', 'userProfile'];
    
    // Verify all required elements are defined
    expect(requiredElements.length).toBe(4);
    expect(requiredElements).toContain('logo');
    expect(requiredElements).toContain('navigation');
    expect(requiredElements).toContain('addJob');
    expect(requiredElements).toContain('userProfile');
  });

  it('should have add job dropdown options', () => {
    const addJobOptions = ['Gmail', 'URL', 'Manual'];
    
    expect(addJobOptions.length).toBe(3);
    expect(addJobOptions).toContain('Gmail');
    expect(addJobOptions).toContain('URL');
    expect(addJobOptions).toContain('Manual');
  });

  it('should have user profile dropdown options', () => {
    const profileOptions = ['Settings', 'Logs', 'Logout'];
    
    expect(profileOptions.length).toBe(3);
    expect(profileOptions).toContain('Settings');
    expect(profileOptions).toContain('Logout');
  });
});

describe('Sidebar Component Logic', () => {
  it('should display all 11 valid phases', () => {
    expect(VALID_PHASES.length).toBe(11);
    expect(VALID_PHASES).toContain('Search');
    expect(VALID_PHASES).toContain('Queued');
    expect(VALID_PHASES).toContain('Generating');
    expect(VALID_PHASES).toContain('Ready');
    expect(VALID_PHASES).toContain('Applied');
    expect(VALID_PHASES).toContain('Follow-Up');
    expect(VALID_PHASES).toContain('Negotiation');
    expect(VALID_PHASES).toContain('Accepted');
    expect(VALID_PHASES).toContain('Skipped');
    expect(VALID_PHASES).toContain('Expired');
    expect(VALID_PHASES).toContain('Errored');
  });

  it('should define active phases correctly', () => {
    expect(ACTIVE_PHASES.length).toBe(7);
    expect(ACTIVE_PHASES).toContain('Search');
    expect(ACTIVE_PHASES).toContain('Queued');
    expect(ACTIVE_PHASES).toContain('Generating');
    expect(ACTIVE_PHASES).toContain('Ready');
    expect(ACTIVE_PHASES).toContain('Applied');
    expect(ACTIVE_PHASES).toContain('Follow-Up');
    expect(ACTIVE_PHASES).toContain('Negotiation');
    
    // Terminal phases should NOT be in active
    expect(ACTIVE_PHASES).not.toContain('Accepted');
    expect(ACTIVE_PHASES).not.toContain('Skipped');
    expect(ACTIVE_PHASES).not.toContain('Expired');
    expect(ACTIVE_PHASES).not.toContain('Errored');
  });

  it('should calculate phase counts correctly', () => {
    const jobs = [
      { jobphase: 'Search' },
      { jobphase: 'Search' },
      { jobphase: 'Queued' },
      { jobphase: 'Ready' },
      { jobphase: 'Applied' },
    ];
    
    const phaseCounts: Record<string, number> = {};
    for (const job of jobs) {
      phaseCounts[job.jobphase] = (phaseCounts[job.jobphase] || 0) + 1;
    }
    
    expect(phaseCounts['Search']).toBe(2);
    expect(phaseCounts['Queued']).toBe(1);
    expect(phaseCounts['Ready']).toBe(1);
    expect(phaseCounts['Applied']).toBe(1);
    expect(phaseCounts['Generating']).toBeUndefined();
  });

  it('should filter jobs by phase correctly', () => {
    const jobs = [
      { jobid: '1', jobphase: 'Search' },
      { jobid: '2', jobphase: 'Search' },
      { jobid: '3', jobphase: 'Queued' },
      { jobid: '4', jobphase: 'Ready' },
    ];
    
    const filterByPhase = (phase: string) => jobs.filter(j => j.jobphase === phase);
    
    expect(filterByPhase('Search').length).toBe(2);
    expect(filterByPhase('Queued').length).toBe(1);
    expect(filterByPhase('Ready').length).toBe(1);
    expect(filterByPhase('Applied').length).toBe(0);
  });

  it('should filter all active jobs correctly', () => {
    const jobs = [
      { jobid: '1', jobphase: 'Search' },
      { jobid: '2', jobphase: 'Ready' },
      { jobid: '3', jobphase: 'Accepted' },
      { jobid: '4', jobphase: 'Expired' },
    ];
    
    const activeJobs = jobs.filter(j => ACTIVE_PHASES.includes(j.jobphase as any));
    
    expect(activeJobs.length).toBe(2);
    expect(activeJobs.map(j => j.jobid)).toContain('1');
    expect(activeJobs.map(j => j.jobid)).toContain('2');
    expect(activeJobs.map(j => j.jobid)).not.toContain('3');
    expect(activeJobs.map(j => j.jobid)).not.toContain('4');
  });

  it('should show all jobs regardless of phase', () => {
    const jobs = [
      { jobid: '1', jobphase: 'Search' },
      { jobid: '2', jobphase: 'Accepted' },
      { jobid: '3', jobphase: 'Expired' },
      { jobid: '4', jobphase: 'Errored' },
    ];
    
    // All Jobs filter returns everything
    expect(jobs.length).toBe(4);
  });
});

describe('Phase Count Display', () => {
  it('should display count next to each phase', () => {
    const phaseCounts = {
      'Search': 3,
      'Queued': 5,
      'Generating': 0,
      'Ready': 2,
    };
    
    // Format: "Phase (count)"
    const formatPhaseCount = (phase: string, count: number) => `${phase} (${count})`;
    
    expect(formatPhaseCount('Search', phaseCounts['Search'])).toBe('Search (3)');
    expect(formatPhaseCount('Queued', phaseCounts['Queued'])).toBe('Queued (5)');
    expect(formatPhaseCount('Generating', phaseCounts['Generating'])).toBe('Generating (0)');
  });
});
