/**
 * Job Card Component
 * Requirements: 6.1, 6.2, 6.3, 6.4, 7.1-7.8, 10.1
 */
import { useState } from 'react';
import { api } from '../services/api';
import type { UserJob, JobPhase, SubcomponentType, GenerationState, GenerationType } from '../types';
import { VALID_PHASES, GENERATION_TYPE_RESTRICTIONS } from '../types';
import {
  MapPin,
  DollarSign,
  Calendar,
  ExternalLink,
  ChevronDown,
  Play,
  Loader2,
  Settings,
  Brain,
  Zap,
  FileText,
  Download,
  Trash2,
  XCircle,
  CheckCircle2,
  Pencil,
} from 'lucide-react';

// Define the two-column layout order
const COLUMN_1: SubcomponentType[] = ['contact', 'summary', 'skills', 'highlights'];
const COLUMN_2: SubcomponentType[] = ['experience', 'education', 'awards', 'keynotes', 'coverletter'];

interface JobCardProps {
  job: UserJob;
  onRefresh: () => void;
  onEditSubcomponent: (jobid: string, component: SubcomponentType) => void;
  onEditJob?: (jobid: string) => void;
}

export function JobCard({ job, onRefresh, onEditSubcomponent, onEditJob }: JobCardProps) {
  const [showMoveToMenu, setShowMoveToMenu] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [generatingComponents, setGeneratingComponents] = useState<Set<SubcomponentType>>(new Set());

  const phaseColors: Record<JobPhase, string> = {
    'Queued': 'bg-yellow-100 text-yellow-800',
    'Generating': 'bg-purple-100 text-purple-800',
    'Ready': 'bg-green-100 text-green-800',
    'Applied': 'bg-indigo-100 text-indigo-800',
    'Follow-Up': 'bg-orange-100 text-orange-800',
    'Negotiation': 'bg-pink-100 text-pink-800',
    'Accepted': 'bg-emerald-100 text-emerald-800',
    'Skipped': 'bg-gray-100 text-gray-800',
    'Expired': 'bg-red-100 text-red-800',
    'Errored': 'bg-red-200 text-red-900',
    'Trash': 'bg-gray-300 text-gray-700',
  };

  async function handlePhaseChange(phase: JobPhase) {
    try {
      await api.updateJobPhase(job.jobid, phase);
      setShowMoveToMenu(false);
      onRefresh();
    } catch (error) {
      console.error('Failed to update phase:', error);
    }
  }

  async function handleGenerateAll() {
    setGenerating(true);
    // Mark all non-omit components as generating
    const componentsToGenerate = [...COLUMN_1, ...COLUMN_2].filter(comp => {
      const type = job[`type${comp}` as keyof UserJob] as GenerationType;
      return type !== 'omit';
    });
    setGeneratingComponents(new Set(componentsToGenerate));
    try {
      await api.generateAll(job.jobid);
      onRefresh();
    } catch (error) {
      console.error('Failed to generate all:', error);
    } finally {
      setGenerating(false);
      setGeneratingComponents(new Set());
    }
  }

  async function handleGenerateSingle(component: SubcomponentType) {
    setGeneratingComponents(prev => new Set(prev).add(component));
    try {
      await api.generateSingle(job.jobid, component);
      onRefresh();
    } catch (error) {
      console.error('Failed to generate:', error);
    } finally {
      setGeneratingComponents(prev => {
        const next = new Set(prev);
        next.delete(component);
        return next;
      });
    }
  }

  async function handleToggleType(component: SubcomponentType) {
    const currentType = job[`type${component}` as keyof UserJob] as GenerationType;
    const restrictions = GENERATION_TYPE_RESTRICTIONS[component];
    const allowedTypes: GenerationType[] = restrictions || ['manual', 'ai', 'omit'];
    
    // Cycle through allowed types
    const currentIndex = allowedTypes.indexOf(currentType);
    const nextIndex = (currentIndex + 1) % allowedTypes.length;
    const newType = allowedTypes[nextIndex];
    
    try {
      // Optimistic update - don't wait for refresh
      await api.toggleGenerationType(job.jobid, component, newType);
      onRefresh();
    } catch (error) {
      console.error('Failed to toggle type:', error);
    }
  }

  async function handleGenerateFinal(type: 'resume' | 'cover', format: 'html' | 'pdf') {
    try {
      if (format === 'html') {
        await api.generateFinalHtml(job.jobid, type);
      } else {
        await api.generateFinalPdf(job.jobid, type);
      }
      onRefresh();
    } catch (error) {
      console.error('Failed to generate final:', error);
    }
  }

  const allComplete = [...COLUMN_1, ...COLUMN_2].every(
    (comp) => (job[`state${comp}` as keyof UserJob] as GenerationState) === 'complete'
  );

  // Check if component has data
  function hasData(component: SubcomponentType): boolean {
    const data = job[`data${component}` as keyof UserJob] as string | undefined;
    return !!data && data.trim().length > 0;
  }

  const subcomponentLabels: Record<SubcomponentType, string> = {
    contact: 'Contacts',
    summary: 'Summary',
    skills: 'Skills',
    highlights: 'Highlights',
    experience: 'Experience',
    education: 'Education',
    awards: 'Awards',
    keynotes: 'Keynotes',
    coverletter: 'Cover Letter',
  };

  // Filter out current phase and Trash for move-to options (Trash shown separately)
  const moveToPhases = VALID_PHASES.filter(p => p !== job.jobphase && p !== 'Trash');

  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-visible">
      {/* Header */}
      <div className="p-3 border-b border-gray-100">
        {/* Company Name (left) and Phase/Move To (right) */}
        <div className="flex items-start justify-between mb-2">
          {/* Company Name - Large */}
          <p className="text-lg font-bold text-gray-800 truncate flex-1 mr-3">{job.jobcompany}</p>
          
          {/* Phase and Move To - Right justified */}
          <div className="flex items-center space-x-2 flex-shrink-0">
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${phaseColors[job.jobphase]}`}>
              {job.jobphase}
            </span>
            <div className="relative">
              <div className="flex items-center space-x-1">
                <span className="text-xs text-gray-500">Move To</span>
                <button
                  onClick={() => setShowMoveToMenu(!showMoveToMenu)}
                  onBlur={() => setTimeout(() => setShowMoveToMenu(false), 150)}
                  className="px-2 py-0.5 text-xs border border-gray-300 rounded hover:bg-gray-50 flex items-center"
                >
                  Select
                  <ChevronDown className="w-3 h-3 ml-1" />
                </button>
              </div>
              {showMoveToMenu && (
                <div className="absolute right-0 mt-1 w-36 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
                  {moveToPhases.map((phase) => (
                    <button
                      key={phase}
                      onClick={() => handlePhaseChange(phase)}
                      className="w-full px-3 py-1.5 text-left text-xs hover:bg-gray-100"
                    >
                      {phase}
                    </button>
                  ))}
                  <div className="border-t border-gray-200">
                    <button
                      onClick={() => handlePhaseChange('Trash')}
                      className="w-full px-3 py-1.5 text-left text-xs hover:bg-red-50 text-red-600 flex items-center"
                    >
                      <Trash2 className="w-3 h-3 mr-1" />
                      Trash
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Job Title */}
        <div className="flex items-start">
          <div className="flex-1 min-w-0">
            <h3 className="text-sm font-semibold text-gray-900 truncate">
              {job.joburl ? (
                <a
                  href={job.joburl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-primary-600 flex items-center"
                >
                  <span className="truncate">{job.jobtitle}</span>
                  <ExternalLink className="w-3 h-3 ml-1 flex-shrink-0" />
                </a>
              ) : (
                job.jobtitle
              )}
            </h3>
          </div>
        </div>

        {/* Meta info */}
        <div className="flex flex-col gap-1 mt-2 text-xs text-gray-500">
          {/* Row 1: Location, Salary */}
          {(job.joblocation || job.jobsalary) && (
            <div className="flex items-center gap-4">
              {job.joblocation && (
                <span className="flex items-center">
                  <MapPin className="w-3 h-3 mr-1 flex-shrink-0" />
                  <span>{job.joblocation}</span>
                </span>
              )}
              {job.jobsalary && (
                <span className="flex items-center">
                  <DollarSign className="w-3 h-3 mr-1 flex-shrink-0" />
                  <span>{job.jobsalary}</span>
                </span>
              )}
            </div>
          )}
          {/* Row 2: Age, Source, Edit */}
          <div className="flex items-center gap-4">
            <span className="flex items-center">
              <Calendar className="w-3 h-3 mr-1 flex-shrink-0" />
              {job.postingAge !== undefined ? `${job.postingAge}d ago` : job.jobposteddate}
            </span>
            <span className="text-gray-400">
              {job.joblistid ? 'LinkedIn Job Alert' : job.joburl ? 'URL Added' : 'Manually Added'}
            </span>
            {onEditJob && (
              <button
                onClick={() => onEditJob(job.jobid)}
                className="flex items-center text-gray-400 hover:text-primary-600"
                title="Edit Job"
              >
                <Pencil className="w-3 h-3" />
              </button>
            )}
          </div>
        </div>

        {/* Tags - Row 3 */}
        {job.jobtags && job.jobtags.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-1">
            {job.jobtags.slice(0, 3).map((tag) => (
              <span
                key={tag}
                className="px-1.5 py-0.5 bg-gray-100 text-gray-600 text-[10px] rounded"
              >
                {tag}
              </span>
            ))}
            {job.jobtags.length > 3 && (
              <span className="text-[10px] text-gray-400">+{job.jobtags.length - 3}</span>
            )}
          </div>
        )}
      </div>

      {/* Resume Sections Grid */}
      <div className="p-3 border-b border-gray-100">
        <h4 className="text-xs font-medium text-gray-700 mb-2">Resume Sections</h4>

        <div className="grid grid-cols-2 gap-1">
          {/* Column 1 */}
          <div className="flex flex-col gap-1">
            {/* Generate All Button */}
            <button
              onClick={handleGenerateAll}
              disabled={generating}
              className="flex items-center justify-center p-1.5 bg-primary-600 text-white text-xs rounded hover:bg-primary-700 disabled:opacity-50"
            >
              {generating ? (
                <Loader2 className="w-3 h-3 mr-1 animate-spin" />
              ) : (
                <Zap className="w-4 h-4 mr-1" />
              )}
              Generate All
            </button>
            {COLUMN_1.map((component) => {
              const state = job[`state${component}` as keyof UserJob] as GenerationState;
              const type = (job[`type${component}` as keyof UserJob] as GenerationType) || 'ai';
              const isGenerating = generatingComponents.has(component) || state === 'generating';
              const isComplete = hasData(component) || state === 'complete';
              const isOmit = type === 'omit';

              return (
                <div
                  key={component}
                  className="flex items-center justify-between p-1.5 bg-gray-50 rounded"
                >
                  <div className="flex items-center space-x-1">
                    {/* Generate button - hidden for omit */}
                    {!isOmit && (
                      <button
                        type="button"
                        onClick={() => {
                          if (state !== 'locked' && !isGenerating) {
                            handleGenerateSingle(component);
                          }
                        }}
                        disabled={state === 'locked' || isGenerating}
                        className="p-0.5 hover:bg-gray-200 rounded disabled:opacity-50 group relative"
                      >
                        {isGenerating ? (
                          <Loader2 className="w-3 h-3 text-purple-500 animate-spin pointer-events-none" />
                        ) : isComplete ? (
                          <CheckCircle2 className="w-3 h-3 text-green-500 fill-green-500 pointer-events-none" />
                        ) : (
                          <Play className="w-3 h-3 text-green-500 pointer-events-none" />
                        )}
                        <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 text-[10px] text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity delay-500 whitespace-nowrap pointer-events-none z-[100]">
                          Generate Now
                        </span>
                      </button>
                    )}
                    {/* Type toggle button */}
                    <button
                      type="button"
                      onClick={() => handleToggleType(component)}
                      className="p-0.5 hover:bg-gray-200 rounded group relative"
                    >
                      {type === 'manual' && <Settings className="w-4 h-4 text-gray-500 pointer-events-none" />}
                      {type === 'ai' && <Brain className="w-4 h-4 text-purple-500 pointer-events-none" />}
                      {type === 'omit' && <XCircle className="w-4 h-4 text-gray-400 pointer-events-none" />}
                      <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 text-[10px] text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity delay-500 whitespace-nowrap pointer-events-none z-[100]">
                        {type === 'ai' ? 'AI Generation' : type === 'omit' ? 'Omit Section' : 'No Modification'}
                      </span>
                    </button>
                    <button
                      type="button"
                      onClick={() => onEditSubcomponent(job.jobid, component)}
                      className={`text-xs truncate ${isOmit ? 'text-gray-400 line-through' : 'text-gray-700 hover:text-primary-600'}`}
                    >
                      {subcomponentLabels[component]}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
          {/* Column 2 */}
          <div className="flex flex-col gap-1">
            {COLUMN_2.map((component) => {
              const state = job[`state${component}` as keyof UserJob] as GenerationState;
              const type = (job[`type${component}` as keyof UserJob] as GenerationType) || 'ai';
              const isGenerating = generatingComponents.has(component) || state === 'generating';
              const isComplete = hasData(component) || state === 'complete';
              const isOmit = type === 'omit';

              return (
                <div
                  key={component}
                  className="flex items-center justify-between p-1.5 bg-gray-50 rounded"
                >
                  <div className="flex items-center space-x-1">
                    {/* Generate button - hidden for omit */}
                    {!isOmit && (
                      <button
                        type="button"
                        onClick={() => {
                          if (state !== 'locked' && !isGenerating) {
                            handleGenerateSingle(component);
                          }
                        }}
                        disabled={state === 'locked' || isGenerating}
                        className="p-0.5 hover:bg-gray-200 rounded disabled:opacity-50 group relative"
                      >
                        {isGenerating ? (
                          <Loader2 className="w-3 h-3 text-purple-500 animate-spin pointer-events-none" />
                        ) : isComplete ? (
                          <CheckCircle2 className="w-3 h-3 text-green-500 fill-green-500 pointer-events-none" />
                        ) : (
                          <Play className="w-3 h-3 text-green-500 pointer-events-none" />
                        )}
                        <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 text-[10px] text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity delay-500 whitespace-nowrap pointer-events-none z-[100]">
                          Generate Now
                        </span>
                      </button>
                    )}
                    {/* Type toggle button */}
                    <button
                      type="button"
                      onClick={() => handleToggleType(component)}
                      className="p-0.5 hover:bg-gray-200 rounded group relative"
                    >
                      {type === 'manual' && <Settings className="w-4 h-4 text-gray-500 pointer-events-none" />}
                      {type === 'ai' && <Brain className="w-4 h-4 text-purple-500 pointer-events-none" />}
                      {type === 'omit' && <XCircle className="w-4 h-4 text-gray-400 pointer-events-none" />}
                      <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 text-[10px] text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 transition-opacity delay-500 whitespace-nowrap pointer-events-none z-[100]">
                        {type === 'ai' ? 'AI Generation' : type === 'omit' ? 'Omit Section' : 'No Modification'}
                      </span>
                    </button>
                    <button
                      type="button"
                      onClick={() => onEditSubcomponent(job.jobid, component)}
                      className={`text-xs truncate ${isOmit ? 'text-gray-400 line-through' : 'text-gray-700 hover:text-primary-600'}`}
                    >
                      {subcomponentLabels[component]}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Final Files */}
      <div className="p-3">
        <h4 className="text-xs font-medium text-gray-700 mb-2">Final Files</h4>
        <div className="grid grid-cols-2 gap-1">
          <button
            onClick={() => handleGenerateFinal('resume', 'html')}
            disabled={!allComplete}
            className="flex items-center justify-center p-1.5 border border-gray-200 rounded text-xs hover:bg-gray-50 disabled:opacity-50"
          >
            <FileText className="w-3 h-3 mr-1" />
            Resume.html
          </button>
          <button
            onClick={() => handleGenerateFinal('resume', 'pdf')}
            disabled={!allComplete || !job.s3locresumehtml}
            className="flex items-center justify-center p-1.5 border border-gray-200 rounded text-xs hover:bg-gray-50 disabled:opacity-50"
          >
            <Download className="w-3 h-3 mr-1" />
            Resume.pdf
          </button>
          <button
            onClick={() => handleGenerateFinal('cover', 'html')}
            disabled={!allComplete}
            className="flex items-center justify-center p-1.5 border border-gray-200 rounded text-xs hover:bg-gray-50 disabled:opacity-50"
          >
            <FileText className="w-3 h-3 mr-1" />
            Cover.html
          </button>
          <button
            onClick={() => handleGenerateFinal('cover', 'pdf')}
            disabled={!allComplete || !job.s3loccoverletterhtml}
            className="flex items-center justify-center p-1.5 border border-gray-200 rounded text-xs hover:bg-gray-50 disabled:opacity-50"
          >
            <Download className="w-3 h-3 mr-1" />
            Cover.pdf
          </button>
        </div>
      </div>
    </div>
  );
}
