/**
 * Subcomponent Editor Modal
 * Requirements: 9.1, 9.2, 9.3, 9.4
 */
import { useState, useEffect } from 'react';
import { X, Loader2, Save } from 'lucide-react';
import type { SubcomponentType } from '../types';

interface SubcomponentEditorProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (content: string) => Promise<void>;
  jobid: string;
  component: SubcomponentType;
  initialContent: string;
}

export function SubcomponentEditor({
  isOpen,
  onClose,
  onSave,
  component,
  initialContent,
}: SubcomponentEditorProps) {
  const [content, setContent] = useState(initialContent);
  const [saving, setSaving] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);

  useEffect(() => {
    setContent(initialContent);
    setHasChanges(false);
  }, [initialContent, isOpen]);

  if (!isOpen) return null;

  const componentLabels: Record<SubcomponentType, string> = {
    contact: 'Contact Information',
    summary: 'Professional Summary',
    skills: 'Skills',
    highlights: 'Career Highlights',
    experience: 'Work Experience',
    education: 'Education',
    awards: 'Awards & Certifications',
    keynotes: 'Keynotes & Presentations',
    coverletter: 'Cover Letter',
  };

  async function handleSave() {
    setSaving(true);
    try {
      await onSave(content);
      setHasChanges(false);
      onClose();
    } catch (error) {
      console.error('Failed to save:', error);
    } finally {
      setSaving(false);
    }
  }

  function handleCancel() {
    if (hasChanges) {
      if (confirm('You have unsaved changes. Are you sure you want to close?')) {
        onClose();
      }
    } else {
      onClose();
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] flex flex-col">
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-lg font-semibold">Edit {componentLabels[component]}</h2>
          <button onClick={handleCancel} className="p-1 hover:bg-gray-100 rounded">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex-1 p-4 overflow-hidden">
          <div className="h-full flex flex-col">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              HTML Content
            </label>
            <textarea
              value={content}
              onChange={(e) => {
                setContent(e.target.value);
                setHasChanges(true);
              }}
              className="flex-1 w-full px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
              placeholder="Enter HTML content..."
            />
          </div>
        </div>

        <div className="flex items-center justify-between p-4 border-t bg-gray-50">
          <div className="text-sm text-gray-500">
            {hasChanges && <span className="text-amber-600">Unsaved changes</span>}
          </div>
          <div className="flex space-x-3">
            <button
              onClick={handleCancel}
              className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={saving || !hasChanges}
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
    </div>
  );
}
