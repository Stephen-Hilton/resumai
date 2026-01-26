/**
 * API Service
 * Requirements: 14.2
 */
import axios, { AxiosInstance, AxiosError } from 'axios';
import { fetchAuthSession } from 'aws-amplify/auth';
import { apiConfig } from '../config/amplify';
import type {
  Resume,
  ResumeJSON,
  UserJob,
  JobListResponse,
  ResumeListResponse,
  GenerationStatusResponse,
  UserPreferences,
  SubcomponentType,
  GenerationType,
  JobPhase,
} from '../types';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: apiConfig.baseUrl,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token to requests
    this.client.interceptors.request.use(async (config) => {
      try {
        const session = await fetchAuthSession();
        const token = session.tokens?.idToken?.toString();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
      } catch (error) {
        console.error('Failed to get auth token:', error);
      }
      return config;
    });

    // Handle 401 responses
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Resume endpoints
  async listResumes(): Promise<ResumeListResponse> {
    const response = await this.client.get('/resumes');
    return response.data;
  }

  async getResume(resumename: string): Promise<Resume> {
    const response = await this.client.get(`/resumes/${encodeURIComponent(resumename)}`);
    return response.data.resume;
  }

  async createResume(resumename: string, resumejson: ResumeJSON): Promise<Resume> {
    const response = await this.client.post('/resumes', { resumename, resumejson });
    return response.data.resume;
  }

  async updateResume(resumename: string, resumejson: ResumeJSON): Promise<Resume> {
    const response = await this.client.put(`/resumes/${encodeURIComponent(resumename)}`, { resumejson });
    return response.data.resume;
  }

  async deleteResume(resumename: string): Promise<void> {
    await this.client.delete(`/resumes/${encodeURIComponent(resumename)}`);
  }

  // Job endpoints
  async listJobs(phase?: JobPhase, filter?: 'active' | 'all'): Promise<JobListResponse> {
    const params = new URLSearchParams();
    if (phase) params.append('phase', phase);
    if (filter) params.append('filter', filter);
    const response = await this.client.get(`/jobs?${params.toString()}`);
    return response.data;
  }

  async getJob(jobid: string): Promise<UserJob> {
    const response = await this.client.get(`/jobs/${jobid}`);
    return response.data.job;
  }

  async createJobManual(data: {
    jobcompany: string;
    jobtitle: string;
    jobdesc: string;
    resumeid: string;
    joblocation?: string;
    jobsalary?: string;
    jobposteddate?: string;
    joburl?: string;
    jobtags?: string[];
  }): Promise<UserJob> {
    const response = await this.client.post('/jobs/manual', data);
    return response.data;
  }

  async createJobFromUrl(url: string, resumeid: string): Promise<UserJob> {
    const response = await this.client.post('/jobs/url', { url, resumeid });
    return response.data;
  }

  async createJobFromGmail(resumeid: string): Promise<{ jobs: UserJob[]; count: number }> {
    const response = await this.client.post('/jobs/gmail', { resumeid });
    return response.data;
  }

  async updateJobPhase(jobid: string, phase: JobPhase): Promise<UserJob> {
    const response = await this.client.put(`/jobs/${jobid}/phase`, { phase });
    return response.data.userJob;
  }

  async deleteJob(jobid: string): Promise<void> {
    await this.client.delete(`/jobs/${jobid}`);
  }

  async updateJobDescription(jobid: string, jobdesc: string): Promise<UserJob> {
    const response = await this.client.put(`/jobs/${jobid}/description`, { jobdesc });
    return response.data.job;
  }

  // Generation endpoints
  async generateAll(jobid: string): Promise<{ message: string; status: string }> {
    const response = await this.client.post(`/jobs/${jobid}/generate-all`);
    return response.data;
  }

  async generateSingle(jobid: string, component: SubcomponentType): Promise<{ message: string; status: string }> {
    const response = await this.client.post(`/jobs/${jobid}/generate/${component}`);
    return response.data;
  }

  async getGenerationStatus(jobid: string): Promise<GenerationStatusResponse> {
    const response = await this.client.get(`/jobs/${jobid}/status`);
    return response.data;
  }

  async toggleGenerationType(jobid: string, component: SubcomponentType, type: GenerationType): Promise<void> {
    await this.client.put(`/jobs/${jobid}/type/${component}`, { type });
  }

  // Final file endpoints
  async generateFinalHtml(jobid: string, type: 'resume' | 'cover'): Promise<{ s3Uri: string; publicUrl: string }> {
    const endpoint = type === 'resume' ? 'resume-html' : 'cover-html';
    const response = await this.client.post(`/jobs/${jobid}/final/${endpoint}?type=${type}`);
    return response.data;
  }

  async generateFinalPdf(jobid: string, type: 'resume' | 'cover'): Promise<{ s3Uri: string; publicUrl: string }> {
    const endpoint = type === 'resume' ? 'resume-pdf' : 'cover-pdf';
    const response = await this.client.post(`/jobs/${jobid}/final/${endpoint}?type=${type}`);
    return response.data;
  }

  // Preferences endpoints
  async getPreferences(): Promise<UserPreferences> {
    const response = await this.client.get('/preferences');
    return response.data.preferences;
  }

  async updatePreferences(preferences: Partial<UserPreferences>): Promise<void> {
    await this.client.put('/preferences', { preferences });
  }
}

export const api = new ApiService();
