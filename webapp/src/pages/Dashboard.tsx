/**
 * Dashboard Page
 * Requirements: 3.5
 */
import { useState, useEffect, useCallback, useMemo } from 'react';
import { api } from '../services/api';
import { Header } from '../components/Header';
import { Sidebar } from '../components/Sidebar';
import { JobCard } from '../components/JobCard';
import { AddJobModal } from '../components/AddJobModal';
import { AddJobFromURL } from '../components/AddJobFromURL';
import { AddJobFromGmail } from '../components/AddJobFromGmail';
import { PreferencesModal } from '../components/PreferencesModal';
import { SubcomponentEditor } from '../components/SubcomponentEditor';
import { ResumeEditor } from '../components/ResumeEditor';
import { JobDescriptionEditor } from '../components/JobDescriptionEditor';
import type { UserJob, JobPhase, SubcomponentType } from '../types';
import { Loader2, Inbox } from 'lucide-react';

export function Dashboard() {
  const [jobs, setJobs] = useState<UserJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedResume, setSelectedResume] = useState<string | null>(null);
  const [selectedPhase, setSelectedPhase] = useState<JobPhase | 'active' | 'all'>('active');
  const [phaseCounts, setPhaseCounts] = useState<Record<JobPhase, number>>({} as Record<JobPhase, number>);
  const [searchQuery, setSearchQuery] = useState('');

  // Modals
  const [showAddJobModal, setShowAddJobModal] = useState(false);
  const [showAddJobUrlModal, setShowAddJobUrlModal] = useState(false);
  const [showAddJobGmailModal, setShowAddJobGmailModal] = useState(false);
  const [showPreferencesModal, setShowPreferencesModal] = useState(false);
  const [showResumeEditor, setShowResumeEditor] = useState(false);
  const [editingResumeName, setEditingResumeName] = useState<string | undefined>(undefined);
  const [editingSubcomponent, setEditingSubcomponent] = useState<{
    jobid: string;
    component: SubcomponentType;
    content: string;
  } | null>(null);
  const [editingJob, setEditingJob] = useState<{
    jobid: string;
    jobdesc: string;
  } | null>(null);

  const loadJobs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      let response;
      if (selectedPhase === 'active') {
        response = await api.listJobs(undefined, 'active');
      } else if (selectedPhase === 'all') {
        response = await api.listJobs(undefined, 'all');
      } else {
        response = await api.listJobs(selectedPhase);
      }
      setJobs(response.jobs || []);
      setPhaseCounts(response.phaseCounts || {});
    } catch (err: any) {
      console.error('Failed to load jobs:', err);
      setError(err?.message || 'Failed to load jobs');
      setJobs([]);
    } finally {
      setLoading(false);
    }
  }, [selectedPhase]);

  useEffect(() => {
    loadJobs();
  }, [loadJobs]);

  // Poll for updates when jobs are generating
  useEffect(() => {
    const hasGenerating = jobs.some((job) => {
      // Check if job phase is Generating OR any subcomponent is generating
      if (job.jobphase === 'Generating') return true;

      const subcomponents: SubcomponentType[] = ['contact', 'summary', 'skills', 'highlights', 'experience', 'education', 'awards', 'keynotes', 'coverletter'];
      return subcomponents.some(comp => {
        const state = job[`state${comp}` as keyof UserJob] as string;
        return state === 'generating';
      });
    });

    if (hasGenerating) {
      const interval = setInterval(loadJobs, 2000); // Poll every 2 seconds for faster updates
      return () => clearInterval(interval);
    }
  }, [jobs, loadJobs]);

  // Filter jobs based on search query
  const filteredJobs = useMemo(() => {
    if (!searchQuery.trim()) return jobs;
    const query = searchQuery.toLowerCase();
    return jobs.filter((job) =>
      job.jobtitle.toLowerCase().includes(query) ||
      job.jobcompany.toLowerCase().includes(query) ||
      (job.joblocation && job.joblocation.toLowerCase().includes(query)) ||
      (job.jobtags && job.jobtags.some(tag => tag.toLowerCase().includes(query)))
    );
  }, [jobs, searchQuery]);

  function handleEditSubcomponent(jobid: string, component: SubcomponentType) {
    const job = jobs.find((j) => j.jobid === jobid);
    if (job) {
      const content = job[`data${component}` as keyof UserJob] as string || '';
      setEditingSubcomponent({ jobid, component, content });
    }
  }

  function handleEditJob(jobid: string) {
    const job = jobs.find((j) => j.jobid === jobid);
    if (job) {
      setEditingJob({ jobid, jobdesc: job.jobdesc });
    }
  }

  async function handleSaveSubcomponent(_content: string) {
    if (!editingSubcomponent) return;
    await loadJobs();
  }

  function handleNewResume() {
    setEditingResumeName(undefined);
    setShowResumeEditor(true);
  }

  function handleEditResume(resumename: string) {
    setEditingResumeName(resumename);
    setShowResumeEditor(true);
  }

  async function handleDeleteResume(resumename: string) {
    await api.deleteResume(resumename);
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <Header
        onAddJobUrl={() => setShowAddJobUrlModal(true)}
        onAddJobManual={() => setShowAddJobModal(true)}
        onAddJobGmail={() => setShowAddJobGmailModal(true)}
        onOpenSettings={() => setShowPreferencesModal(true)}
        selectedResume={selectedResume}
        onSelectResume={setSelectedResume}
        onEditResume={handleEditResume}
        onDeleteResume={handleDeleteResume}
        onNewResume={handleNewResume}
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
      />

      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          selectedPhase={selectedPhase}
          onSelectPhase={setSelectedPhase}
          phaseCounts={phaseCounts}
          onAddJobUrl={() => setShowAddJobUrlModal(true)}
          onAddJobManual={() => setShowAddJobModal(true)}
          onAddJobGmail={() => setShowAddJobGmailModal(true)}
        />

        <main className="flex-1 overflow-y-auto p-6">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
            </div>
          ) : error ? (
            <div className="flex flex-col items-center justify-center h-64 text-red-500">
              <p className="text-lg">Error loading jobs</p>
              <p className="text-sm">{error}</p>
              <button 
                onClick={loadJobs}
                className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                Retry
              </button>
            </div>
          ) : filteredJobs.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-64 text-gray-500">
              <Inbox className="w-12 h-12 mb-4" />
              <p className="text-lg">{searchQuery ? 'No matching jobs' : 'No jobs found'}</p>
              <p className="text-sm">{searchQuery ? 'Try a different search term' : 'Add a job to get started'}</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {filteredJobs.map((job) => (
                <JobCard
                  key={job.jobid}
                  job={job}
                  onRefresh={loadJobs}
                  onEditSubcomponent={handleEditSubcomponent}
                  onEditJob={handleEditJob}
                />
              ))}
            </div>
          )}
        </main>
      </div>

      {/* Modals */}
      <AddJobModal
        isOpen={showAddJobModal}
        onClose={() => setShowAddJobModal(false)}
        onSuccess={loadJobs}
        selectedResume={selectedResume || ''}
      />

      {showAddJobUrlModal && (
        <AddJobFromURL
          resumeid={selectedResume || ''}
          onClose={() => setShowAddJobUrlModal(false)}
          onSuccess={loadJobs}
        />
      )}

      {showAddJobGmailModal && (
        <AddJobFromGmail
          resumeid={selectedResume || ''}
          gmailConnected={true}
          onClose={() => setShowAddJobGmailModal(false)}
          onSuccess={loadJobs}
          onConnectGmail={() => {/* Gmail OAuth would go here */}}
        />
      )}

      <PreferencesModal
        isOpen={showPreferencesModal}
        onClose={() => setShowPreferencesModal(false)}
      />

      <ResumeEditor
        isOpen={showResumeEditor}
        onClose={() => setShowResumeEditor(false)}
        onSuccess={() => {
          setShowResumeEditor(false);
          // Trigger sidebar to reload resumes
          window.location.reload();
        }}
        resumename={editingResumeName}
      />

      {editingSubcomponent && (
        <SubcomponentEditor
          isOpen={true}
          onClose={() => setEditingSubcomponent(null)}
          onSave={handleSaveSubcomponent}
          jobid={editingSubcomponent.jobid}
          component={editingSubcomponent.component}
          initialContent={editingSubcomponent.content}
        />
      )}

      {editingJob && (
        <JobDescriptionEditor
          jobid={editingJob.jobid}
          initialContent={editingJob.jobdesc}
          onClose={() => setEditingJob(null)}
          onSave={loadJobs}
        />
      )}
    </div>
  );
}
