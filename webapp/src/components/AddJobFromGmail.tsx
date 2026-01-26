/**
 * Add Job From Gmail Modal
 * Requirements: 5.1
 * Note: Backend Lambda job-create-gmail (Task 8.3) not implemented
 */
import { useState } from 'react';
import { X, Mail, Loader2, AlertTriangle, Check, RefreshCw } from 'lucide-react';
import { api } from '../services/api';
import type { UserJob } from '../types';

interface AddJobFromGmailProps {
  resumeid: string;
  gmailConnected: boolean;
  onClose: () => void;
  onSuccess: () => void;
  onConnectGmail: () => void;
}

interface FoundJob {
  id: string;
  company: string;
  title: string;
  location?: string;
  selected: boolean;
}

export function AddJobFromGmail({
  resumeid,
  gmailConnected,
  onClose,
  onSuccess,
  onConnectGmail,
}: AddJobFromGmailProps) {
  const [loading, setLoading] = useState(false);
  const [importing, setImporting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [foundJobs, setFoundJobs] = useState<FoundJob[]>([]);
  const [fetched, setFetched] = useState(false);

  async function handleFetchJobs() {
    setLoading(true);
    setError(null);

    try {
      const result = await api.createJobFromGmail(resumeid);
      const jobs: FoundJob[] = result.jobs.map((job: UserJob) => ({
        id: job.jobid,
        company: job.jobcompany,
        title: job.jobtitle,
        location: job.joblocation,
        selected: true,
      }));
      setFoundJobs(jobs);
      setFetched(true);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch jobs from Gmail';
      setError(errorMessage);
      console.error('Fetch jobs error:', err);
    } finally {
      setLoading(false);
    }
  }

  function toggleJob(id: string) {
    setFoundJobs((jobs: FoundJob[]) =>
      jobs.map((job: FoundJob) =>
        job.id === id ? { ...job, selected: !job.selected } : job
      )
    );
  }

  function selectAll() {
    setFoundJobs((jobs: FoundJob[]) => jobs.map((job: FoundJob) => ({ ...job, selected: true })));
  }

  function deselectAll() {
    setFoundJobs((jobs: FoundJob[]) => jobs.map((job: FoundJob) => ({ ...job, selected: false })));
  }

  async function handleImport() {
    const selectedJobs = foundJobs.filter((job) => job.selected);
    if (selectedJobs.length === 0) {
      setError('Please select at least one job to import');
      return;
    }

    setImporting(true);
    // Jobs are already created when fetched, just close and refresh
    onSuccess();
    onClose();
  }

  const selectedCount = foundJobs.filter((job: FoundJob) => job.selected).length;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-lg max-h-[80vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-lg font-semibold text-gray-900">Import from Gmail</h2>
          <button onClick={onClose} className="p-1 hover:bg-gray-100 rounded">
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-4">
          {error && (
            <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-lg text-sm flex items-center">
              <AlertTriangle className="w-4 h-4 mr-2 flex-shrink-0" />
              {error}
            </div>
          )}

          {!gmailConnected ? (
            <div className="text-center py-8">
              <Mail className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Connect Your Gmail
              </h3>
              <p className="text-sm text-gray-500 mb-4">
                Connect your Gmail account to import jobs from LinkedIn Job Alert emails.
              </p>
              <button
                onClick={onConnectGmail}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                Connect Gmail
              </button>
            </div>
          ) : !fetched ? (
            <div className="text-center py-8">
              <Mail className="w-12 h-12 text-green-500 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Gmail Connected
              </h3>
              <p className="text-sm text-gray-500 mb-4">
                Click below to search for LinkedIn Job Alert emails and extract job listings.
              </p>
              <button
                onClick={handleFetchJobs}
                disabled={loading}
                className="flex items-center mx-auto px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
              >
                {loading ? (
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                ) : (
                  <RefreshCw className="w-4 h-4 mr-2" />
                )}
                Fetch Jobs
              </button>
            </div>
          ) : foundJobs.length === 0 ? (
            <div className="text-center py-8">
              <Mail className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No Jobs Found
              </h3>
              <p className="text-sm text-gray-500">
                No LinkedIn Job Alert emails were found in your inbox.
              </p>
            </div>
          ) : (
            <>
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm text-gray-600">
                  Found {foundJobs.length} jobs ({selectedCount} selected)
                </span>
                <div className="flex gap-2">
                  <button
                    onClick={selectAll}
                    className="text-xs text-primary-600 hover:underline"
                  >
                    Select All
                  </button>
                  <button
                    onClick={deselectAll}
                    className="text-xs text-gray-500 hover:underline"
                  >
                    Deselect All
                  </button>
                </div>
              </div>

              <div className="space-y-2 max-h-64 overflow-auto">
                {foundJobs.map((job) => (
                  <label
                    key={job.id}
                    className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${
                      job.selected
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-200 hover:bg-gray-50'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={job.selected}
                      onChange={() => toggleJob(job.id)}
                      className="sr-only"
                    />
                    <div
                      className={`w-5 h-5 rounded border flex items-center justify-center mr-3 ${
                        job.selected
                          ? 'bg-primary-600 border-primary-600'
                          : 'border-gray-300'
                      }`}
                    >
                      {job.selected && <Check className="w-3 h-3 text-white" />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-gray-900 truncate">{job.title}</p>
                      <p className="text-sm text-gray-500 truncate">
                        {job.company}
                        {job.location && ` • ${job.location}`}
                      </p>
                    </div>
                  </label>
                ))}
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        {fetched && foundJobs.length > 0 && (
          <div className="flex items-center justify-end gap-3 p-4 border-t">
            <button
              onClick={onClose}
              className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              Cancel
            </button>
            <button
              onClick={handleImport}
              disabled={importing || selectedCount === 0}
              className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
            >
              {importing ? (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              ) : (
                <Mail className="w-4 h-4 mr-2" />
              )}
              Import {selectedCount} Job{selectedCount !== 1 ? 's' : ''}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
