/**
 * Resume Editor Modal Component
 * Requirements: 4.1, 4.2, 4.4, 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 7.1, 7.2, 7.3, 7.4
 */
import { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';
import { X, Loader2, Save, Plus, Trash2, ChevronUp, ChevronDown, Edit2, Building2, Briefcase, Upload, Download } from 'lucide-react';
import { importResumeFile, ImportValidationError, ImportUploadError, ImportProcessError, ImportAuthError, ImportTimeoutError } from '../services/importService';
import type { ResumeJSON, ContactItem, Education, Award, Keynote, ExperienceCompany, ExperienceRole, ExperienceBullet } from '../types';

interface ResumeEditorProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  resumename?: string;
}

const ICON_OPTIONS: { value: ContactItem['icon']; label: string; svg: string; placeholder: string }[] = [
  { value: 'email-at', label: 'Email', svg: '/icons/email-at.svg', placeholder: 'mailto:email@example.com' },
  { value: 'phone', label: 'Phone', svg: '/icons/phone.svg', placeholder: 'tel:+18889871234' },
  { value: 'phone-volume', label: 'Phone Alt', svg: '/icons/phone-volume.svg', placeholder: 'tel:+18889871234' },
  { value: 'linkedin', label: 'LinkedIn', svg: '/icons/linkedin.svg', placeholder: 'https://www.linkedin.com/in/username' },
  { value: 'x-twitter', label: 'X/Twitter', svg: '/icons/x-twitter.svg', placeholder: 'https://x.com/username' },
  { value: 'bluesky', label: 'Bluesky', svg: '/icons/bluesky.svg', placeholder: 'https://bsky.app/profile/username.bsky.social' },
  { value: 'github', label: 'GitHub', svg: '/icons/github.svg', placeholder: 'https://github.com/username' },
  { value: 'github-square', label: 'GitHub Square', svg: '/icons/github-square.svg', placeholder: 'https://github.com/username' },
  { value: 'globe-solid', label: 'Website', svg: '/icons/globe-solid.svg', placeholder: 'https://your.website.com' },
  { value: 'house-solid', label: 'Home', svg: '/icons/house-solid.svg', placeholder: 'https://www.google.com/maps/place/San+Francisco+Bay+Area' },
  { value: 'facebook', label: 'Facebook', svg: '/icons/facebook.svg', placeholder: 'https://www.facebook.com/username' },
  { value: 'discord', label: 'Discord', svg: '/icons/discord.svg', placeholder: 'https://discord.com/users/username' },
  { value: 'slack', label: 'Slack', svg: '/icons/slack.svg', placeholder: 'https://yourworkspace.slack.com/team/yourslackid' },
  { value: 'telegram', label: 'Telegram', svg: '/icons/telegram.svg', placeholder: 'https://t.me/username' },
  { value: 'whatsapp', label: 'WhatsApp', svg: '/icons/whatsapp.svg', placeholder: 'https://wa.me/phonenumber' },
  { value: 'signal-chat', label: 'Signal', svg: '/icons/signal-chat.svg', placeholder: 'https://signal.me/#u/username' },
];

const emptyResume: ResumeJSON = {
  contact: { name: '', items: [] },
  summary: '',
  skills: [],
  highlights: [],
  experience: [],
  education: [],
  awards: [],
  keynotes: [],
};

export function ResumeEditor({ isOpen, onClose, onSuccess, resumename }: ResumeEditorProps) {
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [name, setName] = useState('');
  const [resume, setResume] = useState<ResumeJSON>(emptyResume);
  const [newSkill, setNewSkill] = useState('');
  
  // New contact item state
  const [newContactIcon, setNewContactIcon] = useState<ContactItem['icon']>('email-at');
  const [newContactTitle, setNewContactTitle] = useState('');
  const [newContactUrl, setNewContactUrl] = useState('');
  
  // New education state
  const [newEduTitle, setNewEduTitle] = useState('');
  const [newEduOrg, setNewEduOrg] = useState('');
  const [newEduYear, setNewEduYear] = useState('');
  
  // New award state
  const [newAwardTitle, setNewAwardTitle] = useState('');
  const [newAwardIssuer, setNewAwardIssuer] = useState('');
  const [newAwardYear, setNewAwardYear] = useState('');

  // New keynote state
  const [newKeynoteTitle, setNewKeynoteTitle] = useState('');
  const [newKeynoteEvent, setNewKeynoteEvent] = useState('');
  const [newKeynoteYear, setNewKeynoteYear] = useState('');

  // Experience editing state
  const [editingCompanyIndex, setEditingCompanyIndex] = useState<number | null>(null);
  const [editingRoleIndex, setEditingRoleIndex] = useState<{ companyIdx: number; roleIdx: number } | null>(null);

  // Import state
  const [importing, setImporting] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      if (resumename) {
        loadResume();
      } else {
        setName('');
        setResume(emptyResume);
      }
    }
  }, [isOpen, resumename]);


  async function loadResume() {
    if (!resumename) return;
    setLoading(true);
    try {
      const data = await api.getResume(resumename);
      setName(resumename);
      const loadedResume = data.resumejson;
      // Handle migration from old contact format
      if (!loadedResume.contact.items) {
        const items: ContactItem[] = [];
        const oldContact = loadedResume.contact as any;
        if (oldContact.email) items.push({ icon: 'email-at', title: 'Email', url: `mailto:${oldContact.email}` });
        if (oldContact.phone) items.push({ icon: 'phone', title: 'Phone', url: `tel:${oldContact.phone}` });
        if (oldContact.linkedin) items.push({ icon: 'linkedin', title: 'LinkedIn', url: oldContact.linkedin });
        if (oldContact.website) items.push({ icon: 'globe-solid', title: 'Website', url: oldContact.website });
        loadedResume.contact = { name: oldContact.name || '', location: oldContact.location, items };
      }
      // Migrate contact items with old 'value' field
      if (loadedResume.contact.items) {
        loadedResume.contact.items = loadedResume.contact.items.map((item: any) => {
          if (item.value && !item.title) {
            return { icon: item.icon || 'globe-solid', title: item.value, url: item.url || '' };
          }
          return item;
        });
      }
      // Migrate old experience format to new hierarchical format
      if (loadedResume.experience && loadedResume.experience.length > 0) {
        const firstExp = loadedResume.experience[0] as any;
        if (firstExp.company && !firstExp.roles) {
          // Old format - migrate to new
          loadedResume.experience = migrateOldExperience(loadedResume.experience as any);
        }
      }
      setResume(loadedResume);
    } catch (err) {
      setError('Failed to load resume');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function migrateOldExperience(oldExp: any[]): ExperienceCompany[] {
    const companyMap = new Map<string, ExperienceCompany>();
    for (const exp of oldExp) {
      const companyName = exp.company || 'Unknown Company';
      if (!companyMap.has(companyName)) {
        companyMap.set(companyName, {
          name: companyName,
          startDate: exp.startDate || '',
          endDate: exp.endDate,
          current: exp.current || false,
          roles: []
        });
      }
      const company = companyMap.get(companyName)!;
      company.roles.push({
        title: exp.title || '',
        startDate: exp.startDate || '',
        endDate: exp.endDate,
        current: exp.current || false,
        bullets: (exp.achievements || []).map((a: string) => ({ text: a, tags: [] }))
      });
    }
    return Array.from(companyMap.values());
  }

  async function handleSave() {
    if (!name.trim()) {
      setError('Resume name is required');
      return;
    }
    if (!resume.contact.name) {
      setError('Your full professional name is required');
      return;
    }

    setSaving(true);
    setError(null);
    try {
      if (resumename) {
        await api.updateResume(resumename, resume);
      } else {
        await api.createResume(name, resume);
      }
      onSuccess();
      onClose();
    } catch (err) {
      setError('Failed to save resume');
      console.error(err);
    } finally {
      setSaving(false);
    }
  }

  // Skills functions
  function addSkill() {
    if (newSkill.trim()) {
      setResume({ ...resume, skills: [...resume.skills, newSkill.trim()] });
      setNewSkill('');
    }
  }

  function removeSkill(index: number) {
    setResume({ ...resume, skills: resume.skills.filter((_, i) => i !== index) });
  }

  // Contact functions
  function addContactItem() {
    if (newContactTitle.trim()) {
      const newItem: ContactItem = {
        icon: newContactIcon,
        title: newContactTitle.trim(),
        url: newContactUrl.trim(),
      };
      setResume({
        ...resume,
        contact: { ...resume.contact, items: [...resume.contact.items, newItem] }
      });
      setNewContactTitle('');
      setNewContactUrl('');
    }
  }

  function removeContactItem(index: number) {
    setResume({
      ...resume,
      contact: { ...resume.contact, items: resume.contact.items.filter((_, i) => i !== index) }
    });
  }

  function moveContactItem(index: number, direction: 'up' | 'down') {
    const items = [...resume.contact.items];
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    if (newIndex < 0 || newIndex >= items.length) return;
    [items[index], items[newIndex]] = [items[newIndex], items[index]];
    setResume({ ...resume, contact: { ...resume.contact, items } });
  }

  // Education functions
  function addEducation() {
    if (newEduTitle.trim() && newEduOrg.trim()) {
      const newEdu: Education = {
        degree: newEduTitle.trim(),
        institution: newEduOrg.trim(),
        field: '',
        graduationDate: newEduYear.trim(),
      };
      setResume({ ...resume, education: [...resume.education, newEdu] });
      setNewEduTitle('');
      setNewEduOrg('');
      setNewEduYear('');
    }
  }

  function removeEducation(index: number) {
    setResume({ ...resume, education: resume.education.filter((_, i) => i !== index) });
  }

  function moveEducation(index: number, direction: 'up' | 'down') {
    const items = [...resume.education];
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    if (newIndex < 0 || newIndex >= items.length) return;
    [items[index], items[newIndex]] = [items[newIndex], items[index]];
    setResume({ ...resume, education: items });
  }

  // Award functions
  function addAward() {
    if (newAwardTitle.trim()) {
      const newAwardItem: Award = {
        title: newAwardTitle.trim(),
        issuer: newAwardIssuer.trim(),
        date: newAwardYear.trim(),
      };
      setResume({ ...resume, awards: [...resume.awards, newAwardItem] });
      setNewAwardTitle('');
      setNewAwardIssuer('');
      setNewAwardYear('');
    }
  }

  function removeAward(index: number) {
    setResume({ ...resume, awards: resume.awards.filter((_, i) => i !== index) });
  }

  function moveAward(index: number, direction: 'up' | 'down') {
    const items = [...resume.awards];
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    if (newIndex < 0 || newIndex >= items.length) return;
    [items[index], items[newIndex]] = [items[newIndex], items[index]];
    setResume({ ...resume, awards: items });
  }

  // Keynote functions
  function addKeynote() {
    if (newKeynoteTitle.trim()) {
      const newKeynoteItem: Keynote = {
        title: newKeynoteTitle.trim(),
        event: newKeynoteEvent.trim(),
        date: newKeynoteYear.trim(),
      };
      setResume({ ...resume, keynotes: [...(resume.keynotes || []), newKeynoteItem] });
      setNewKeynoteTitle('');
      setNewKeynoteEvent('');
      setNewKeynoteYear('');
    }
  }

  function removeKeynote(index: number) {
    setResume({ ...resume, keynotes: (resume.keynotes || []).filter((_, i) => i !== index) });
  }

  function moveKeynote(index: number, direction: 'up' | 'down') {
    const items = [...(resume.keynotes || [])];
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    if (newIndex < 0 || newIndex >= items.length) return;
    [items[index], items[newIndex]] = [items[newIndex], items[index]];
    setResume({ ...resume, keynotes: items });
  }


  // Experience functions
  function getExperience(): ExperienceCompany[] {
    return (resume.experience || []) as ExperienceCompany[];
  }

  function setExperience(exp: ExperienceCompany[]) {
    setResume({ ...resume, experience: exp });
  }

  function addCompany() {
    const newCompany: ExperienceCompany = {
      name: '',
      startDate: '',
      current: false,
      roles: []
    };
    setExperience([...getExperience(), newCompany]);
    setEditingCompanyIndex(getExperience().length);
  }

  function updateCompany(index: number, updates: Partial<ExperienceCompany>) {
    const exp = [...getExperience()];
    exp[index] = { ...exp[index], ...updates };
    setExperience(exp);
  }

  function removeCompany(index: number) {
    setExperience(getExperience().filter((_, i) => i !== index));
    setEditingCompanyIndex(null);
  }

  function moveCompany(index: number, direction: 'up' | 'down') {
    const exp = [...getExperience()];
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    if (newIndex < 0 || newIndex >= exp.length) return;
    [exp[index], exp[newIndex]] = [exp[newIndex], exp[index]];
    setExperience(exp);
  }

  function addRole(companyIndex: number) {
    const exp = [...getExperience()];
    const newRole: ExperienceRole = {
      title: '',
      startDate: '',
      current: false,
      bullets: []
    };
    exp[companyIndex].roles = [...exp[companyIndex].roles, newRole];
    setExperience(exp);
    setEditingRoleIndex({ companyIdx: companyIndex, roleIdx: exp[companyIndex].roles.length - 1 });
  }

  function updateRole(companyIndex: number, roleIndex: number, updates: Partial<ExperienceRole>) {
    const exp = [...getExperience()];
    exp[companyIndex].roles[roleIndex] = { ...exp[companyIndex].roles[roleIndex], ...updates };
    setExperience(exp);
  }

  function removeRole(companyIndex: number, roleIndex: number) {
    const exp = [...getExperience()];
    exp[companyIndex].roles = exp[companyIndex].roles.filter((_, i) => i !== roleIndex);
    setExperience(exp);
    setEditingRoleIndex(null);
  }

  function moveRole(companyIndex: number, roleIndex: number, direction: 'up' | 'down') {
    const exp = [...getExperience()];
    const roles = [...exp[companyIndex].roles];
    const newIndex = direction === 'up' ? roleIndex - 1 : roleIndex + 1;
    if (newIndex < 0 || newIndex >= roles.length) return;
    [roles[roleIndex], roles[newIndex]] = [roles[newIndex], roles[roleIndex]];
    exp[companyIndex].roles = roles;
    setExperience(exp);
  }

  function addBullet(companyIndex: number, roleIndex: number) {
    const exp = [...getExperience()];
    const newBullet: ExperienceBullet = { text: '', tags: [] };
    exp[companyIndex].roles[roleIndex].bullets = [...exp[companyIndex].roles[roleIndex].bullets, newBullet];
    setExperience(exp);
  }

  function updateBullet(companyIndex: number, roleIndex: number, bulletIndex: number, updates: Partial<ExperienceBullet>) {
    const exp = [...getExperience()];
    exp[companyIndex].roles[roleIndex].bullets[bulletIndex] = {
      ...exp[companyIndex].roles[roleIndex].bullets[bulletIndex],
      ...updates
    };
    setExperience(exp);
  }

  function removeBullet(companyIndex: number, roleIndex: number, bulletIndex: number) {
    const exp = [...getExperience()];
    exp[companyIndex].roles[roleIndex].bullets = exp[companyIndex].roles[roleIndex].bullets.filter((_, i) => i !== bulletIndex);
    setExperience(exp);
  }

  function moveBullet(companyIndex: number, roleIndex: number, bulletIndex: number, direction: 'up' | 'down') {
    const exp = [...getExperience()];
    const bullets = [...exp[companyIndex].roles[roleIndex].bullets];
    const newIndex = direction === 'up' ? bulletIndex - 1 : bulletIndex + 1;
    if (newIndex < 0 || newIndex >= bullets.length) return;
    [bullets[bulletIndex], bullets[newIndex]] = [bullets[newIndex], bullets[bulletIndex]];
    exp[companyIndex].roles[roleIndex].bullets = bullets;
    setExperience(exp);
  }

  function getIconSvg(iconName: ContactItem['icon']) {
    const iconConfig = ICON_OPTIONS.find(i => i.value === iconName);
    return iconConfig?.svg || '/icons/globe-solid.svg';
  }

  function getUrlPlaceholder(iconName: ContactItem['icon']) {
    const iconConfig = ICON_OPTIONS.find(i => i.value === iconName);
    return iconConfig?.placeholder || 'https://example.com';
  }

  // Import functions
  function handleLoadFromFileClick() {
    fileInputRef.current?.click();
  }

  async function handleFileSelect(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    // Reset file input so the same file can be selected again
    event.target.value = '';

    setImporting(true);
    setError(null);

    try {
      const result = await importResumeFile(file);
      
      // Populate form with imported data
      setResume(result.resumejson);
      
      // Show warnings if any
      if (result.warnings && result.warnings.length > 0) {
        setError(`Import completed with warnings: ${result.warnings.join(', ')}`);
      }
    } catch (err) {
      // Preserve existing form data on error (Requirement 6.6)
      // Handle specific error types with user-friendly messages (Requirements 8.1-8.5)
      if (err instanceof ImportValidationError) {
        setError(err.message);
      } else if (err instanceof ImportUploadError) {
        setError(err.message);
      } else if (err instanceof ImportProcessError) {
        setError(err.message);
      } else if (err instanceof ImportAuthError) {
        setError(err.message);
      } else if (err instanceof ImportTimeoutError) {
        setError(err.message);
      } else {
        // Generic fallback error (Requirement 8.4)
        setError('Could not read file. Please ensure it\'s a valid YAML, JSON, or PDF file.');
        // Log detailed error for debugging (Requirement 8.5)
        console.error('Import error:', err);
      }
    } finally {
      setImporting(false);
    }
  }

  function handleDownloadTemplate() {
    const link = document.createElement('a');
    link.href = '/skillsnap-resume-template.yaml';
    link.download = 'skillsnap-resume-template.yaml';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // Prevent modal close during import
  function handleClose() {
    if (importing) return;
    onClose();
  }

  if (!isOpen) return null;


  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-lg font-semibold">
            {resumename ? 'Edit Resume' : 'Create Resume'}
          </h2>
          <button onClick={handleClose} disabled={importing} className="p-1 hover:bg-gray-100 rounded disabled:opacity-50">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Import Progress Overlay */}
        {importing && (
          <div className="absolute inset-0 bg-white bg-opacity-80 flex flex-col items-center justify-center z-10">
            <Loader2 className="w-12 h-12 animate-spin text-primary-600 mb-4" />
            <p className="text-gray-700 font-medium">Analyzing resume file...</p>
          </div>
        )}

        {/* Hidden file input */}
        <input
          ref={fileInputRef}
          type="file"
          accept=".yaml,.yml,.json,.pdf"
          onChange={handleFileSelect}
          className="hidden"
        />

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto p-4 space-y-6">
            {error && (
              <div className="p-3 bg-red-50 text-red-700 rounded-lg text-sm">{error}</div>
            )}

            {/* Resume Name with Import Buttons */}
            {!resumename && (
              <div>
                <label className="block text-base font-bold text-gray-700 mb-1">
                  Resume Name *
                </label>
                <div className="flex gap-2 items-center">
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="flex-1 max-w-md px-3 py-2 border border-gray-300 rounded-lg"
                    placeholder="My Professional Resume"
                    disabled={importing}
                  />
                  <button
                    onClick={handleLoadFromFileClick}
                    disabled={importing || loading}
                    className="flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                    title="Load from File"
                  >
                    <Upload className="w-4 h-4" />
                    <span>Load from File</span>
                  </button>
                  <button
                    onClick={handleDownloadTemplate}
                    disabled={importing || loading}
                    className="flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                    title="Download Template"
                  >
                    <Download className="w-4 h-4" />
                    <span>Download Template</span>
                  </button>
                </div>
              </div>
            )}

            {/* Import buttons for edit mode */}
            {resumename && (
              <div className="flex gap-2 items-center justify-end">
                <button
                  onClick={handleLoadFromFileClick}
                  disabled={importing || loading}
                  className="flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                  title="Load from File"
                >
                  <Upload className="w-4 h-4" />
                  <span>Load from File</span>
                </button>
                <button
                  onClick={handleDownloadTemplate}
                  disabled={importing || loading}
                  className="flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                  title="Download Template"
                >
                  <Download className="w-4 h-4" />
                  <span>Download Template</span>
                </button>
              </div>
            )}

            {/* Full Professional Name */}
            <div>
              <label className="block text-base font-bold text-gray-700 mb-1">
                Your Full Professional Name *
              </label>
              <input
                type="text"
                value={resume.contact.name}
                onChange={(e) => setResume({
                  ...resume,
                  contact: { ...resume.contact, name: e.target.value }
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                placeholder="John Doe"
              />
            </div>

            <hr className="border-gray-200" />

            {/* Contact Information */}
            <div>
              <label className="block text-base font-bold text-gray-700 mb-2">Contact Information</label>
              <div className="space-y-2 mb-3">
                {resume.contact.items.map((item, i) => (
                  <div key={i} className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                    <img src={getIconSvg(item.icon)} alt="" className="w-4 h-4" />
                    <span className="flex-1 text-sm truncate">
                      {item.title}
                      {item.url && <span className="text-gray-400 ml-2 text-xs">({item.url})</span>}
                    </span>
                    <button onClick={() => moveContactItem(i, 'up')} disabled={i === 0} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                      <ChevronUp className="w-4 h-4" />
                    </button>
                    <button onClick={() => moveContactItem(i, 'down')} disabled={i === resume.contact.items.length - 1} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                      <ChevronDown className="w-4 h-4" />
                    </button>
                    <button onClick={() => removeContactItem(i)} className="text-gray-500 hover:text-red-500">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
              <div className="flex gap-2 items-end">
                <div className="w-20">
                  <label className="block text-xs text-gray-500 mb-1">Icon</label>
                  <div className="relative">
                    <select
                      value={newContactIcon}
                      onChange={(e) => setNewContactIcon(e.target.value as ContactItem['icon'])}
                      className="w-full px-2 py-2 border border-gray-300 rounded-lg text-sm appearance-none pl-8"
                    >
                      {ICON_OPTIONS.map(i => (
                        <option key={i.value} value={i.value}>{i.label}</option>
                      ))}
                    </select>
                    <img src={getIconSvg(newContactIcon)} alt="" className="w-4 h-4 absolute left-2 top-1/2 -translate-y-1/2 pointer-events-none" />
                  </div>
                </div>
                <div className="flex-1">
                  <label className="block text-xs text-gray-500 mb-1">Title</label>
                  <input type="text" value={newContactTitle} onChange={(e) => setNewContactTitle(e.target.value)} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder="name displayed" />
                </div>
                <div className="flex-1">
                  <label className="block text-xs text-gray-500 mb-1">URL / Link</label>
                  <input type="text" value={newContactUrl} onChange={(e) => setNewContactUrl(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && addContactItem()} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder={getUrlPlaceholder(newContactIcon)} />
                </div>
                <button onClick={addContactItem} className="px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200">
                  <Plus className="w-4 h-4" />
                </button>
              </div>
            </div>

            <hr className="border-gray-200" />

            {/* Summary */}
            <div>
              <label className="block text-base font-bold text-gray-700 mb-1">Professional Summary</label>
              <textarea
                rows={5}
                value={resume.summary}
                onChange={(e) => setResume({ ...resume, summary: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                placeholder="Brief professional summary..."
              />
            </div>

            <hr className="border-gray-200" />

            {/* Skills */}
            <div>
              <label className="block text-base font-bold text-gray-700 mb-2">Skills</label>
              <div className="flex flex-wrap gap-2 mb-2">
                {resume.skills.map((skill, i) => (
                  <span key={i} className="flex items-center px-2 py-1 bg-gray-100 rounded text-sm">
                    {skill}
                    <button onClick={() => removeSkill(i)} className="ml-1 text-gray-500 hover:text-red-500">
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
              <div className="flex gap-2">
                <input type="text" value={newSkill} onChange={(e) => setNewSkill(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && addSkill()} className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder="Add skill..." />
                <button onClick={addSkill} className="px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200">
                  <Plus className="w-4 h-4" />
                </button>
              </div>
            </div>


            <hr className="border-gray-200" />

            {/* Experience */}
            <div>
              <label className="block text-base font-bold text-gray-700 mb-2">Experience</label>
              <div className="space-y-4 mb-3">
                {getExperience().map((company, companyIdx) => (
                  <div key={companyIdx} className="border border-gray-200 rounded-lg p-3">
                    {/* Company Header */}
                    <div className="flex items-start gap-2 mb-2">
                      <Building2 className="w-5 h-5 text-gray-400 mt-1" />
                      <div className="flex-1">
                        {editingCompanyIndex === companyIdx ? (
                          <div className="space-y-2">
                            <input type="text" value={company.name} onChange={(e) => updateCompany(companyIdx, { name: e.target.value })} className="w-full px-2 py-1 border border-gray-300 rounded text-sm" placeholder="Company Name" />
                            <div className="grid grid-cols-3 gap-2">
                              <input type="text" value={company.url || ''} onChange={(e) => updateCompany(companyIdx, { url: e.target.value })} className="px-2 py-1 border border-gray-300 rounded text-sm" placeholder="Company URL" />
                              <input type="text" value={company.employees || ''} onChange={(e) => updateCompany(companyIdx, { employees: e.target.value })} className="px-2 py-1 border border-gray-300 rounded text-sm" placeholder="# Employees" />
                              <input type="text" value={company.location || ''} onChange={(e) => updateCompany(companyIdx, { location: e.target.value })} className="px-2 py-1 border border-gray-300 rounded text-sm" placeholder="Location" />
                            </div>
                            <div className="grid grid-cols-3 gap-2">
                              <input type="text" value={company.startDate} onChange={(e) => updateCompany(companyIdx, { startDate: e.target.value })} className="px-2 py-1 border border-gray-300 rounded text-sm" placeholder="Start Year / Month" />
                              <input type="text" value={company.endDate || ''} onChange={(e) => updateCompany(companyIdx, { endDate: e.target.value })} disabled={company.current} className="px-2 py-1 border border-gray-300 rounded text-sm disabled:bg-gray-100" placeholder="End Year / Month" />
                              <label className="flex items-center text-sm">
                                <input type="checkbox" checked={company.current} onChange={(e) => updateCompany(companyIdx, { current: e.target.checked, endDate: e.target.checked ? undefined : company.endDate })} className="mr-2" />
                                Current
                              </label>
                            </div>
                            <textarea value={company.description || ''} onChange={(e) => updateCompany(companyIdx, { description: e.target.value })} className="w-full px-2 py-1 border border-gray-300 rounded text-sm" rows={2} placeholder="Short company description" />
                            <button onClick={() => setEditingCompanyIndex(null)} className="text-xs text-primary-600 hover:underline">Done editing</button>
                          </div>
                        ) : (
                          <div>
                            <span className="font-medium">{company.name || 'New Company'}</span>
                            {company.location && <span className="text-gray-500 text-sm ml-2">({company.location})</span>}
                            <div className="text-xs text-gray-400">{company.startDate} - {company.current ? 'Present' : company.endDate}</div>
                          </div>
                        )}
                      </div>
                      <div className="flex gap-1">
                        <button onClick={() => setEditingCompanyIndex(editingCompanyIndex === companyIdx ? null : companyIdx)} className="text-gray-400 hover:text-gray-600">
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button onClick={() => moveCompany(companyIdx, 'up')} disabled={companyIdx === 0} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                          <ChevronUp className="w-4 h-4" />
                        </button>
                        <button onClick={() => moveCompany(companyIdx, 'down')} disabled={companyIdx === getExperience().length - 1} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                          <ChevronDown className="w-4 h-4" />
                        </button>
                        <button onClick={() => removeCompany(companyIdx)} className="text-gray-500 hover:text-red-500">
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>

                    {/* Roles */}
                    <div className="ml-6 space-y-3">
                      {company.roles.map((role, roleIdx) => (
                        <div key={roleIdx} className="border-l-2 border-gray-200 pl-3">
                          <div className="flex items-start gap-2">
                            <Briefcase className="w-4 h-4 text-gray-400 mt-1" />
                            <div className="flex-1">
                              {editingRoleIndex?.companyIdx === companyIdx && editingRoleIndex?.roleIdx === roleIdx ? (
                                <div className="space-y-2">
                                  <input type="text" value={role.title} onChange={(e) => updateRole(companyIdx, roleIdx, { title: e.target.value })} className="w-full px-2 py-1 border border-gray-300 rounded text-sm" placeholder="Role Title" />
                                  <div className="grid grid-cols-3 gap-2">
                                    <input type="text" value={role.startDate} onChange={(e) => updateRole(companyIdx, roleIdx, { startDate: e.target.value })} className="px-2 py-1 border border-gray-300 rounded text-sm" placeholder="Start Year / Month" />
                                    <input type="text" value={role.endDate || ''} onChange={(e) => updateRole(companyIdx, roleIdx, { endDate: e.target.value })} disabled={role.current} className="px-2 py-1 border border-gray-300 rounded text-sm disabled:bg-gray-100" placeholder="End Year / Month" />
                                    <label className="flex items-center text-sm">
                                      <input type="checkbox" checked={role.current} onChange={(e) => updateRole(companyIdx, roleIdx, { current: e.target.checked, endDate: e.target.checked ? undefined : role.endDate })} className="mr-2" />
                                      Current
                                    </label>
                                  </div>
                                  <input type="text" value={role.location || ''} onChange={(e) => updateRole(companyIdx, roleIdx, { location: e.target.value })} className="w-full px-2 py-1 border border-gray-300 rounded text-sm" placeholder="Location (if different from company)" />
                                  <button onClick={() => setEditingRoleIndex(null)} className="text-xs text-primary-600 hover:underline">Done editing</button>
                                </div>
                              ) : (
                                <div>
                                  <span className="text-sm font-medium">{role.title || 'New Role'}</span>
                                  <div className="text-xs text-gray-400">{role.startDate} - {role.current ? 'Present' : role.endDate}</div>
                                </div>
                              )}
                            </div>
                            <div className="flex gap-1">
                              <button onClick={() => setEditingRoleIndex(editingRoleIndex?.companyIdx === companyIdx && editingRoleIndex?.roleIdx === roleIdx ? null : { companyIdx, roleIdx })} className="text-gray-400 hover:text-gray-600">
                                <Edit2 className="w-3 h-3" />
                              </button>
                              <button onClick={() => moveRole(companyIdx, roleIdx, 'up')} disabled={roleIdx === 0} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                                <ChevronUp className="w-3 h-3" />
                              </button>
                              <button onClick={() => moveRole(companyIdx, roleIdx, 'down')} disabled={roleIdx === company.roles.length - 1} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                                <ChevronDown className="w-3 h-3" />
                              </button>
                              <button onClick={() => removeRole(companyIdx, roleIdx)} className="text-gray-500 hover:text-red-500">
                                <Trash2 className="w-3 h-3" />
                              </button>
                            </div>
                          </div>

                          {/* Bullets */}
                          <div className="ml-5 mt-2 space-y-1">
                            {role.bullets.map((bullet, bulletIdx) => (
                              <div key={bulletIdx} className="flex items-start gap-2">
                                <span className="text-gray-400 mt-1">•</span>
                                <div className="flex-1">
                                  <input type="text" value={bullet.text} onChange={(e) => updateBullet(companyIdx, roleIdx, bulletIdx, { text: e.target.value })} className="w-full px-2 py-1 border border-gray-200 rounded text-sm" placeholder="Achievement or responsibility" />
                                  <input 
                                    type="text" 
                                    defaultValue={bullet.tags.join(', ')} 
                                    onBlur={(e) => updateBullet(companyIdx, roleIdx, bulletIdx, { tags: e.target.value.split(',').map(t => t.trim()).filter(Boolean) })} 
                                    className="w-full px-2 py-0.5 border border-gray-100 rounded text-xs text-gray-500 mt-1" 
                                    placeholder="Tags (comma-separated)" 
                                  />
                                </div>
                                <div className="flex gap-1">
                                  <button onClick={() => moveBullet(companyIdx, roleIdx, bulletIdx, 'up')} disabled={bulletIdx === 0} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                                    <ChevronUp className="w-3 h-3" />
                                  </button>
                                  <button onClick={() => moveBullet(companyIdx, roleIdx, bulletIdx, 'down')} disabled={bulletIdx === role.bullets.length - 1} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                                    <ChevronDown className="w-3 h-3" />
                                  </button>
                                  <button onClick={() => removeBullet(companyIdx, roleIdx, bulletIdx)} className="text-gray-500 hover:text-red-500">
                                    <Trash2 className="w-3 h-3" />
                                  </button>
                                </div>
                              </div>
                            ))}
                            <button onClick={() => addBullet(companyIdx, roleIdx)} className="text-xs text-primary-600 hover:underline flex items-center gap-1">
                              <Plus className="w-3 h-3" /> Add bullet
                            </button>
                          </div>
                        </div>
                      ))}
                      <button onClick={() => addRole(companyIdx)} className="text-xs text-primary-600 hover:underline flex items-center gap-1 ml-1">
                        <Plus className="w-3 h-3" /> Add role
                      </button>
                    </div>
                  </div>
                ))}
              </div>
              <button onClick={addCompany} className="flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 text-sm">
                <Plus className="w-4 h-4" /> Add Company
              </button>
            </div>


            <hr className="border-gray-200" />

            {/* Education */}
            <div>
              <label className="block text-base font-bold text-gray-700 mb-2">Education</label>
              <div className="space-y-2 mb-3">
                {resume.education.map((edu, i) => (
                  <div key={i} className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                    <div className="flex-1">
                      <span className="text-sm font-medium">{edu.degree}</span>
                      <span className="text-sm text-gray-500"> — {edu.institution}</span>
                      {edu.graduationDate && <span className="text-xs text-gray-400 ml-2">({edu.graduationDate})</span>}
                    </div>
                    <button onClick={() => moveEducation(i, 'up')} disabled={i === 0} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                      <ChevronUp className="w-4 h-4" />
                    </button>
                    <button onClick={() => moveEducation(i, 'down')} disabled={i === resume.education.length - 1} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                      <ChevronDown className="w-4 h-4" />
                    </button>
                    <button onClick={() => removeEducation(i)} className="text-gray-500 hover:text-red-500">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
              <div className="flex gap-2 items-end">
                <div className="flex-1">
                  <label className="block text-xs text-gray-500 mb-1">Title/Degree</label>
                  <input type="text" value={newEduTitle} onChange={(e) => setNewEduTitle(e.target.value)} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder="B.S. Computer Science" />
                </div>
                <div className="flex-1">
                  <label className="block text-xs text-gray-500 mb-1">Organization</label>
                  <input type="text" value={newEduOrg} onChange={(e) => setNewEduOrg(e.target.value)} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder="University Name" />
                </div>
                <div className="w-24">
                  <label className="block text-xs text-gray-500 mb-1">Year</label>
                  <input type="text" value={newEduYear} onChange={(e) => setNewEduYear(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && addEducation()} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder="2020" />
                </div>
                <button onClick={addEducation} className="px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200">
                  <Plus className="w-4 h-4" />
                </button>
              </div>
            </div>

            <hr className="border-gray-200" />

            {/* Awards */}
            <div>
              <label className="block text-base font-bold text-gray-700 mb-2">Awards</label>
              <div className="space-y-2 mb-3">
                {resume.awards.map((award, i) => (
                  <div key={i} className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                    <div className="flex-1">
                      <span className="text-sm font-medium">{award.title}</span>
                      {award.issuer && <span className="text-sm text-gray-500"> — {award.issuer}</span>}
                      {award.date && <span className="text-xs text-gray-400 ml-2">({award.date})</span>}
                    </div>
                    <button onClick={() => moveAward(i, 'up')} disabled={i === 0} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                      <ChevronUp className="w-4 h-4" />
                    </button>
                    <button onClick={() => moveAward(i, 'down')} disabled={i === resume.awards.length - 1} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                      <ChevronDown className="w-4 h-4" />
                    </button>
                    <button onClick={() => removeAward(i)} className="text-gray-500 hover:text-red-500">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
              <div className="flex gap-2 items-end">
                <div className="flex-1">
                  <label className="block text-xs text-gray-500 mb-1">Title</label>
                  <input type="text" value={newAwardTitle} onChange={(e) => setNewAwardTitle(e.target.value)} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder="Award Name" />
                </div>
                <div className="flex-1">
                  <label className="block text-xs text-gray-500 mb-1">Reward</label>
                  <input type="text" value={newAwardIssuer} onChange={(e) => setNewAwardIssuer(e.target.value)} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder="Reward provided" />
                </div>
                <div className="w-24">
                  <label className="block text-xs text-gray-500 mb-1">Year</label>
                  <input type="text" value={newAwardYear} onChange={(e) => setNewAwardYear(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && addAward()} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder="2023" />
                </div>
                <button onClick={addAward} className="px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200">
                  <Plus className="w-4 h-4" />
                </button>
              </div>
            </div>

            <hr className="border-gray-200" />

            {/* Keynotes */}
            <div>
              <label className="block text-base font-bold text-gray-700 mb-2">Keynotes & Presentations</label>
              <div className="space-y-2 mb-3">
                {(resume.keynotes || []).map((keynote, i) => (
                  <div key={i} className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                    <div className="flex-1">
                      <span className="text-sm font-medium">{keynote.title}</span>
                      {keynote.event && <span className="text-sm text-gray-500"> — {keynote.event}</span>}
                      {keynote.date && <span className="text-xs text-gray-400 ml-2">({keynote.date})</span>}
                    </div>
                    <button onClick={() => moveKeynote(i, 'up')} disabled={i === 0} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                      <ChevronUp className="w-4 h-4" />
                    </button>
                    <button onClick={() => moveKeynote(i, 'down')} disabled={i === (resume.keynotes || []).length - 1} className="text-gray-400 hover:text-gray-600 disabled:opacity-30">
                      <ChevronDown className="w-4 h-4" />
                    </button>
                    <button onClick={() => removeKeynote(i)} className="text-gray-500 hover:text-red-500">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
              <div className="flex gap-2 items-end">
                <div className="flex-1">
                  <label className="block text-xs text-gray-500 mb-1">Title</label>
                  <input type="text" value={newKeynoteTitle} onChange={(e) => setNewKeynoteTitle(e.target.value)} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder="Keynote or Presentation Title" />
                </div>
                <div className="flex-1">
                  <label className="block text-xs text-gray-500 mb-1">Event/Location</label>
                  <input type="text" value={newKeynoteEvent} onChange={(e) => setNewKeynoteEvent(e.target.value)} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder="Event name or location" />
                </div>
                <div className="w-24">
                  <label className="block text-xs text-gray-500 mb-1">Year</label>
                  <input type="text" value={newKeynoteYear} onChange={(e) => setNewKeynoteYear(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && addKeynote()} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder="2023" />
                </div>
                <button onClick={addKeynote} className="px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200">
                  <Plus className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="flex justify-end space-x-3 p-4 border-t">
          <button onClick={handleClose} disabled={importing} className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg disabled:opacity-50">
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={saving || loading || importing}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 flex items-center"
          >
            {saving ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Save className="w-4 h-4 mr-2" />}
            Save
          </button>
        </div>
      </div>
    </div>
  );
}
