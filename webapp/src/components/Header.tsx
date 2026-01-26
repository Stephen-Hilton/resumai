/**
 * Header Component
 * Requirements: 3.3
 */
import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../services/api';
import type { Resume } from '../types';
import { 
  Menu, 
  X, 
  Plus, 
  User, 
  LogOut, 
  Settings, 
  FileText,
  Link,
  Mail,
  ChevronDown,
  Edit,
  Search,
  Home,
  Trash2,
  AlertTriangle
} from 'lucide-react';

interface HeaderProps {
  onAddJobUrl: () => void;
  onAddJobManual: () => void;
  onAddJobGmail: () => void;
  onOpenSettings: () => void;
  selectedResume: string | null;
  onSelectResume: (resumename: string) => void;
  onEditResume: (resumename: string) => void;
  onDeleteResume: (resumename: string) => Promise<void>;
  onNewResume: () => void;
  searchQuery: string;
  onSearchChange: (query: string) => void;
}

export function Header({ 
  onAddJobUrl, 
  onAddJobManual, 
  onAddJobGmail,
  onOpenSettings,
  selectedResume,
  onSelectResume,
  onEditResume,
  onDeleteResume,
  onNewResume,
  searchQuery,
  onSearchChange,
}: HeaderProps) {
  const { user, logout } = useAuth();
  const [showResumeDropdown, setShowResumeDropdown] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loadingResumes, setLoadingResumes] = useState(true);
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);

  const resumeDropdownRef = useRef<HTMLDivElement>(null);
  const userMenuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadResumes();
  }, []);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (resumeDropdownRef.current && !resumeDropdownRef.current.contains(event.target as Node)) {
        setShowResumeDropdown(false);
      }
      if (userMenuRef.current && !userMenuRef.current.contains(event.target as Node)) {
        setShowUserMenu(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  async function loadResumes() {
    try {
      const response = await api.listResumes();
      setResumes(response.resumes);
      if (response.resumes.length > 0 && !selectedResume) {
        onSelectResume(response.resumes[0].resumename);
      }
    } catch (error) {
      console.error('Failed to load resumes:', error);
    } finally {
      setLoadingResumes(false);
    }
  }

  function handleReturnToLanding() {
    window.location.href = '/landing/';
  }

  async function handleDeleteResume() {
    if (!deleteConfirm) return;
    setDeleting(true);
    try {
      await onDeleteResume(deleteConfirm);
      setResumes(resumes.filter(r => r.resumename !== deleteConfirm));
      if (selectedResume === deleteConfirm) {
        const remaining = resumes.filter(r => r.resumename !== deleteConfirm);
        onSelectResume(remaining.length > 0 ? remaining[0].resumename : '');
      }
    } finally {
      setDeleting(false);
      setDeleteConfirm(null);
    }
  }

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="w-full px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo - fully left justified */}
          <div className="flex items-center">
            <a href="/" className="flex items-center space-x-2">
              <img src="/assets/skillsnap_logo.png" alt="SkillSnap" className="h-8 w-auto" />
              <span className="text-xl font-semibold text-primary-600">SkillSnap</span>
            </a>
          </div>

          {/* Desktop Navigation - fully right justified */}
          <nav className="hidden md:flex items-center space-x-4 ml-auto">
            {/* Search Box */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search jobs..."
                value={searchQuery}
                onChange={(e) => onSearchChange(e.target.value)}
                className="pl-9 pr-3 py-2 w-48 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            {/* Resume Selector */}
            <div className="relative" ref={resumeDropdownRef}>
              <button
                onClick={() => setShowResumeDropdown(!showResumeDropdown)}
                className="flex items-center space-x-1 px-3 py-2 border border-gray-300 rounded-lg bg-white hover:bg-gray-50"
              >
                <FileText className="w-4 h-4 text-gray-500" />
                <span className="text-sm text-gray-700 max-w-32 truncate">
                  {loadingResumes ? 'Loading...' : (selectedResume || 'Select Resume')}
                </span>
                <ChevronDown className="w-4 h-4 text-gray-500" />
              </button>
              
              {showResumeDropdown && (
                <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 py-1">
                  {resumes.map((resume) => (
                    <button
                      key={resume.resumename}
                      onClick={() => {
                        onSelectResume(resume.resumename);
                        setShowResumeDropdown(false);
                      }}
                      className={`flex items-center justify-between w-full px-4 py-2 text-sm hover:bg-gray-100 ${
                        selectedResume === resume.resumename ? 'bg-primary-50 text-primary-700' : 'text-gray-700'
                      }`}
                    >
                      <span className="truncate">{resume.resumename}</span>
                      {selectedResume === resume.resumename && (
                        <div className="flex items-center ml-2">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              onEditResume(resume.resumename);
                              setShowResumeDropdown(false);
                            }}
                            className="p-1 hover:bg-gray-200 rounded"
                            title="Edit resume"
                          >
                            <Edit className="w-3 h-3" />
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              setDeleteConfirm(resume.resumename);
                              setShowResumeDropdown(false);
                            }}
                            className="p-1 hover:bg-red-100 rounded text-red-500"
                            title="Delete resume"
                          >
                            <Trash2 className="w-3 h-3" />
                          </button>
                        </div>
                      )}
                    </button>
                  ))}
                  {resumes.length === 0 && (
                    <div className="px-4 py-2 text-sm text-gray-500">
                      No resumes yet
                    </div>
                  )}
                  <hr className="my-1" />
                  <button
                    onClick={() => {
                      onNewResume();
                      setShowResumeDropdown(false);
                    }}
                    className="flex items-center w-full px-4 py-2 text-sm text-primary-600 hover:bg-gray-100"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Resume
                  </button>
                </div>
              )}
            </div>

            {/* User Menu */}
            <div className="relative" ref={userMenuRef}>
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-gray-600" />
                </div>
                <span className="text-sm text-gray-700">{user?.username || 'User'}</span>
              </button>

              {showUserMenu && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1">
                  <button
                    onClick={() => { onOpenSettings(); setShowUserMenu(false); }}
                    className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    <Settings className="w-4 h-4 mr-2" />
                    Settings
                  </button>
                  <button
                    onClick={() => { handleReturnToLanding(); setShowUserMenu(false); }}
                    className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    <Home className="w-4 h-4 mr-2" />
                    Website
                  </button>
                  <hr className="my-1" />
                  <button
                    onClick={() => { logout(); setShowUserMenu(false); }}
                    className="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
                  >
                    <LogOut className="w-4 h-4 mr-2" />
                    Logout
                  </button>
                </div>
              )}
            </div>
          </nav>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-gray-100"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-gray-200 bg-white">
          <div className="px-4 py-3 space-y-2">
            {/* Mobile Search */}
            <div className="relative mb-2">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search jobs..."
                value={searchQuery}
                onChange={(e) => onSearchChange(e.target.value)}
                className="pl-9 pr-3 py-2 w-full border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <button
              onClick={() => { onAddJobUrl(); setMobileMenuOpen(false); }}
              className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              <Link className="w-4 h-4 mr-2" />
              Add Job from URL
            </button>
            <button
              onClick={() => { onAddJobGmail(); setMobileMenuOpen(false); }}
              className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              <Mail className="w-4 h-4 mr-2" />
              Add Job from Gmail
            </button>
            <button
              onClick={() => { onAddJobManual(); setMobileMenuOpen(false); }}
              className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              <FileText className="w-4 h-4 mr-2" />
              Add Job Manually
            </button>
            <hr />
            <button
              onClick={() => { onOpenSettings(); setMobileMenuOpen(false); }}
              className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              <Settings className="w-4 h-4 mr-2" />
              Settings
            </button>
            <button
              onClick={() => { handleReturnToLanding(); setMobileMenuOpen(false); }}
              className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              <Home className="w-4 h-4 mr-2" />
              Website
            </button>
            <button
              onClick={() => { logout(); setMobileMenuOpen(false); }}
              className="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-gray-100 rounded-lg"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </button>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 overflow-hidden">
            <div className="p-6">
              <div className="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full mb-4">
                <AlertTriangle className="w-6 h-6 text-red-600" />
              </div>
              <h3 className="text-lg font-semibold text-center text-gray-900 mb-2">
                Delete Resume
              </h3>
              <p className="text-sm text-gray-600 text-center mb-1">
                Are you sure you want to delete <span className="font-medium">"{deleteConfirm}"</span>?
              </p>
              <p className="text-sm text-red-600 text-center font-medium">
                This action cannot be undone.
              </p>
            </div>
            <div className="bg-gray-50 px-6 py-4 flex justify-end space-x-3">
              <button
                onClick={() => setDeleteConfirm(null)}
                disabled={deleting}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteResume}
                disabled={deleting}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 disabled:opacity-50"
              >
                {deleting ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
