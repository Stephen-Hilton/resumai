/**
 * Sidebar Component
 * Requirements: 3.4, 3.6, 3.7, 3.8
 */
import type { JobPhase } from '../types';
import { VALID_PHASES, ACTIVE_PHASES } from '../types';
import { 
  Plus, 
  Filter
} from 'lucide-react';

interface SidebarProps {
  selectedPhase: JobPhase | 'active' | 'all';
  onSelectPhase: (phase: JobPhase | 'active' | 'all') => void;
  phaseCounts: Record<JobPhase, number>;
  onAddJobUrl: () => void;
  onAddJobManual: () => void;
  onAddJobGmail: () => void;
}

export function Sidebar({
  selectedPhase,
  onSelectPhase,
  phaseCounts,
  onAddJobUrl,
  onAddJobManual,
  onAddJobGmail,
}: SidebarProps) {
  const totalActive = ACTIVE_PHASES.reduce((sum, phase) => sum + (phaseCounts[phase] || 0), 0);
  const totalAll = VALID_PHASES.reduce((sum, phase) => sum + (phaseCounts[phase] || 0), 0);

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

  return (
    <aside className="w-64 bg-white border-r border-gray-200 h-full overflow-y-auto">
      <div className="p-4 space-y-6">
        {/* Add Job Button */}
        <div className="relative">
          <AddJobDropdown
            onAddJobUrl={onAddJobUrl}
            onAddJobManual={onAddJobManual}
            onAddJobGmail={onAddJobGmail}
          />
        </div>

        {/* Phase Filters */}
        <div>
          <div className="flex items-center mb-2">
            <Filter className="w-4 h-4 mr-2 text-gray-500" />
            <span className="text-sm font-medium text-gray-700">Phases</span>
          </div>

          <div className="space-y-1">
            {VALID_PHASES.map((phase) => (
              <button
                key={phase}
                onClick={() => onSelectPhase(phase)}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-colors ${
                  selectedPhase === phase
                    ? 'bg-primary-100 text-primary-700'
                    : 'hover:bg-gray-100 text-gray-700'
                }`}
              >
                <span className="flex items-center">
                  <span className={`w-2 h-2 rounded-full mr-2 ${phaseColors[phase].split(' ')[0]}`} />
                  {phase}
                </span>
                <span className={`px-2 py-0.5 rounded-full text-xs ${phaseColors[phase]}`}>
                  {phaseCounts[phase] || 0}
                </span>
              </button>
            ))}
          </div>

          <hr className="my-3" />

          {/* Aggregations */}
          <div className="space-y-1">
            <button
              onClick={() => onSelectPhase('active')}
              className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-colors ${
                selectedPhase === 'active'
                  ? 'bg-primary-100 text-primary-700'
                  : 'hover:bg-gray-100 text-gray-700'
              }`}
            >
              <span>All Active</span>
              <span className="px-2 py-0.5 rounded-full text-xs bg-gray-100 text-gray-800">
                {totalActive}
              </span>
            </button>
            <button
              onClick={() => onSelectPhase('all')}
              className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-colors ${
                selectedPhase === 'all'
                  ? 'bg-primary-100 text-primary-700'
                  : 'hover:bg-gray-100 text-gray-700'
              }`}
            >
              <span>All Jobs</span>
              <span className="px-2 py-0.5 rounded-full text-xs bg-gray-100 text-gray-800">
                {totalAll}
              </span>
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
}

// Add Job Dropdown component for sidebar
import { useState } from 'react';
import { Link, Mail, FileText, ChevronDown } from 'lucide-react';

function AddJobDropdown({
  onAddJobUrl,
  onAddJobManual,
  onAddJobGmail,
}: {
  onAddJobUrl: () => void;
  onAddJobManual: () => void;
  onAddJobGmail: () => void;
}) {
  const [showMenu, setShowMenu] = useState(false);

  return (
    <div className="relative">
      <button
        onClick={() => setShowMenu(!showMenu)}
        className="w-full flex items-center justify-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
      >
        <Plus className="w-4 h-4 mr-2" />
        <span>Add Job</span>
        <ChevronDown className="w-4 h-4 ml-2" />
      </button>
      
      {showMenu && (
        <div className="absolute left-0 right-0 mt-2 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10">
          <button
            onClick={() => { onAddJobUrl(); setShowMenu(false); }}
            className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            <Link className="w-4 h-4 mr-2" />
            From URL
          </button>
          <button
            onClick={() => { onAddJobGmail(); setShowMenu(false); }}
            className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            <Mail className="w-4 h-4 mr-2" />
            From Gmail
          </button>
          <button
            onClick={() => { onAddJobManual(); setShowMenu(false); }}
            className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            <FileText className="w-4 h-4 mr-2" />
            Manual Entry
          </button>
        </div>
      )}
    </div>
  );
}
