/**
 * Preferences Modal Component
 * Requirements: 13.1, 13.2, 13.4
 */
import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { X, Loader2, Save, Brain, Settings, XCircle, ChevronDown, ChevronRight } from 'lucide-react';
import type { UserPreferences, SubcomponentType, GenerationType } from '../types';
import { SUBCOMPONENTS, GENERATION_TYPE_RESTRICTIONS } from '../types';

interface PreferencesModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function PreferencesModal({ isOpen, onClose }: PreferencesModalProps) {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [preferences, setPreferences] = useState<UserPreferences>({
    default_gen_contact: 'manual',
    default_gen_summary: 'ai',
    default_gen_skills: 'ai',
    default_gen_highlights: 'ai',
    default_gen_experience: 'ai',
    default_gen_education: 'ai',
    default_gen_awards: 'ai',
    default_gen_keynotes: 'ai',
    default_gen_coverletter: 'ai',
    show_year_education: false,
    show_year_awards: false,
    show_year_keynotes: false,
    combine_awards_keynotes: true,
    cutoff_year: undefined,
  });
  
  // Accordion state (default closed)
  const [generationSectionOpen, setGenerationSectionOpen] = useState(false);
  const [optionsSectionOpen, setOptionsSectionOpen] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadPreferences();
    }
  }, [isOpen]);

  async function loadPreferences() {
    setLoading(true);
    try {
      const prefs = await api.getPreferences();
      setPreferences({
        ...preferences,
        ...prefs,
      });
    } catch (error) {
      console.error('Failed to load preferences:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleSave() {
    setSaving(true);
    try {
      await api.updatePreferences(preferences);
      onClose();
    } catch (error) {
      console.error('Failed to save preferences:', error);
    } finally {
      setSaving(false);
    }
  }

  function cycleGenerationType(component: SubcomponentType) {
    const key = `default_gen_${component}` as keyof UserPreferences;
    const current = preferences[key] as GenerationType;
    const restrictions = GENERATION_TYPE_RESTRICTIONS[component];
    const allowedTypes: GenerationType[] = restrictions || ['manual', 'ai', 'omit'];
    
    const currentIndex = allowedTypes.indexOf(current);
    const nextIndex = (currentIndex + 1) % allowedTypes.length;
    const newValue = allowedTypes[nextIndex];
    
    setPreferences({ ...preferences, [key]: newValue });
  }

  if (!isOpen) return null;

  const componentLabels: Record<SubcomponentType, string> = {
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

  const typeIcons: Record<GenerationType, { icon: React.ReactNode; label: string; className: string }> = {
    ai: { icon: <Brain className="w-4 h-4 mr-1" />, label: 'AI', className: 'bg-purple-100 text-purple-700' },
    manual: { icon: <Settings className="w-4 h-4 mr-1" />, label: 'Manual', className: 'bg-gray-200 text-gray-700' },
    omit: { icon: <XCircle className="w-4 h-4 mr-1" />, label: 'Omit', className: 'bg-red-100 text-red-700' },
  };

  // Generate year options (current year down to 1970)
  const currentYear = new Date().getFullYear();
  const yearOptions = Array.from({ length: currentYear - 1969 }, (_, i) => currentYear - i);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-lg max-h-[90vh] overflow-hidden flex flex-col">
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-lg font-semibold">Preferences</h2>
          <button onClick={onClose} className="p-1 hover:bg-gray-100 rounded">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-4">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-6 h-6 animate-spin text-primary-600" />
            </div>
          ) : (
            <div className="space-y-4">
              {/* Default Generation by Section Accordion */}
              <div className="border border-gray-200 rounded-lg overflow-hidden">
                <button
                  onClick={() => setGenerationSectionOpen(!generationSectionOpen)}
                  className="w-full flex items-center justify-between p-3 bg-gray-50 hover:bg-gray-100 transition-colors"
                >
                  <span className="font-medium text-gray-700">Default Generation by Section</span>
                  {generationSectionOpen ? (
                    <ChevronDown className="w-5 h-5 text-gray-500" />
                  ) : (
                    <ChevronRight className="w-5 h-5 text-gray-500" />
                  )}
                </button>
                
                {generationSectionOpen && (
                  <div className="p-3 space-y-2">
                    <p className="text-xs text-gray-500 mb-3">
                      Set default generation type for each section when creating new jobs.
                    </p>
                    {SUBCOMPONENTS.map((component) => {
                      const key = `default_gen_${component}` as keyof UserPreferences;
                      const currentType = (preferences[key] || 'ai') as GenerationType;
                      const typeConfig = typeIcons[currentType];

                      return (
                        <div
                          key={component}
                          className="flex items-center justify-between p-2 bg-gray-50 rounded-lg"
                        >
                          <span className="text-sm font-medium text-gray-700">
                            {componentLabels[component]}
                          </span>
                          <button
                            onClick={() => cycleGenerationType(component)}
                            className={`flex items-center px-3 py-1 rounded-full text-sm ${typeConfig.className}`}
                          >
                            {typeConfig.icon}
                            {typeConfig.label}
                          </button>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

              {/* Resume Generation Options Accordion */}
              <div className="border border-gray-200 rounded-lg overflow-hidden">
                <button
                  onClick={() => setOptionsSectionOpen(!optionsSectionOpen)}
                  className="w-full flex items-center justify-between p-3 bg-gray-50 hover:bg-gray-100 transition-colors"
                >
                  <span className="font-medium text-gray-700">Resume Generation Options</span>
                  {optionsSectionOpen ? (
                    <ChevronDown className="w-5 h-5 text-gray-500" />
                  ) : (
                    <ChevronRight className="w-5 h-5 text-gray-500" />
                  )}
                </button>
                
                {optionsSectionOpen && (
                  <div className="p-3 space-y-3">
                    {/* Show Year for Education */}
                    <label className="flex items-center justify-between p-2 bg-gray-50 rounded-lg cursor-pointer">
                      <span className="text-sm text-gray-700">Show Year for Education Items</span>
                      <input
                        type="checkbox"
                        checked={preferences.show_year_education || false}
                        onChange={(e) => setPreferences({ ...preferences, show_year_education: e.target.checked })}
                        className="w-4 h-4 text-primary-600 rounded border-gray-300 focus:ring-primary-500"
                      />
                    </label>

                    {/* Show Year for Awards */}
                    <label className="flex items-center justify-between p-2 bg-gray-50 rounded-lg cursor-pointer">
                      <span className="text-sm text-gray-700">Show Year for Award Items</span>
                      <input
                        type="checkbox"
                        checked={preferences.show_year_awards || false}
                        onChange={(e) => setPreferences({ ...preferences, show_year_awards: e.target.checked })}
                        className="w-4 h-4 text-primary-600 rounded border-gray-300 focus:ring-primary-500"
                      />
                    </label>

                    {/* Show Year for Keynotes */}
                    <label className="flex items-center justify-between p-2 bg-gray-50 rounded-lg cursor-pointer">
                      <span className="text-sm text-gray-700">Show Year for Keynote Items</span>
                      <input
                        type="checkbox"
                        checked={preferences.show_year_keynotes || false}
                        onChange={(e) => setPreferences({ ...preferences, show_year_keynotes: e.target.checked })}
                        className="w-4 h-4 text-primary-600 rounded border-gray-300 focus:ring-primary-500"
                      />
                    </label>

                    {/* Combine Awards & Keynotes */}
                    <label className="flex items-center justify-between p-2 bg-gray-50 rounded-lg cursor-pointer">
                      <span className="text-sm text-gray-700">Combine "Awards & Keynotes"</span>
                      <input
                        type="checkbox"
                        checked={preferences.combine_awards_keynotes !== false}
                        onChange={(e) => setPreferences({ ...preferences, combine_awards_keynotes: e.target.checked })}
                        className="w-4 h-4 text-primary-600 rounded border-gray-300 focus:ring-primary-500"
                      />
                    </label>

                    {/* Cutoff Year */}
                    <div className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-700">Remove data that ended before</span>
                      <select
                        value={preferences.cutoff_year || ''}
                        onChange={(e) => setPreferences({ 
                          ...preferences, 
                          cutoff_year: e.target.value ? parseInt(e.target.value) : undefined 
                        })}
                        className="px-2 py-1 border border-gray-300 rounded text-sm focus:ring-primary-500 focus:border-primary-500"
                      >
                        <option value="">No cutoff</option>
                        {yearOptions.map((year) => (
                          <option key={year} value={year}>{year}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="flex justify-end space-x-3 p-4 border-t">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={saving || loading}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 flex items-center"
          >
            {saving ? (
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <Save className="w-4 h-4 mr-2" />
            )}
            Save
          </button>
        </div>
      </div>
    </div>
  );
}
