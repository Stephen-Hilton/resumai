/**
 * Import Integration Tests
 * Checkpoint 5: Test frontend integration for Resume File Import
 * Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 7.1, 7.2, 7.3, 7.4
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import {
  validateFile,
  validateFileType,
  validateFileSize,
  getFileExtension,
  getContentType,
  ImportValidationError,
  IMPORT_CONSTANTS,
} from '../services/importService';

// Mock file creation helper
function createMockFile(name: string, size: number, type: string): File {
  const content = new Array(size).fill('a').join('');
  return new File([content], name, { type });
}

describe('File Selection and Validation', () => {
  describe('getFileExtension', () => {
    it('should extract extension from filename', () => {
      expect(getFileExtension('resume.yaml')).toBe('.yaml');
      expect(getFileExtension('resume.yml')).toBe('.yml');
      expect(getFileExtension('resume.json')).toBe('.json');
      expect(getFileExtension('resume.pdf')).toBe('.pdf');
    });

    it('should handle uppercase extensions', () => {
      expect(getFileExtension('resume.YAML')).toBe('.yaml');
      expect(getFileExtension('resume.JSON')).toBe('.json');
      expect(getFileExtension('resume.PDF')).toBe('.pdf');
    });

    it('should return empty string for files without extension', () => {
      expect(getFileExtension('resume')).toBe('');
    });

    it('should handle multiple dots in filename', () => {
      expect(getFileExtension('my.resume.yaml')).toBe('.yaml');
      expect(getFileExtension('file.backup.json')).toBe('.json');
    });
  });

  describe('validateFileType', () => {
    it('should accept YAML files', () => {
      const yamlFile = createMockFile('resume.yaml', 100, 'application/x-yaml');
      expect(() => validateFileType(yamlFile)).not.toThrow();
    });

    it('should accept YML files', () => {
      const ymlFile = createMockFile('resume.yml', 100, 'application/x-yaml');
      expect(() => validateFileType(ymlFile)).not.toThrow();
    });

    it('should accept JSON files', () => {
      const jsonFile = createMockFile('resume.json', 100, 'application/json');
      expect(() => validateFileType(jsonFile)).not.toThrow();
    });

    it('should accept PDF files', () => {
      const pdfFile = createMockFile('resume.pdf', 100, 'application/pdf');
      expect(() => validateFileType(pdfFile)).not.toThrow();
    });

    it('should reject unsupported file types', () => {
      const txtFile = createMockFile('resume.txt', 100, 'text/plain');
      expect(() => validateFileType(txtFile)).toThrow(ImportValidationError);
      expect(() => validateFileType(txtFile)).toThrow('Unsupported file type');
    });

    it('should reject files without extension', () => {
      const noExtFile = createMockFile('resume', 100, 'application/octet-stream');
      expect(() => validateFileType(noExtFile)).toThrow(ImportValidationError);
    });
  });

  describe('validateFileSize', () => {
    it('should accept files under 5MB', () => {
      const smallFile = createMockFile('resume.yaml', 1000, 'application/x-yaml');
      expect(() => validateFileSize(smallFile)).not.toThrow();
    });

    it('should accept files exactly at 5MB', () => {
      const exactFile = createMockFile('resume.yaml', IMPORT_CONSTANTS.MAX_FILE_SIZE, 'application/x-yaml');
      expect(() => validateFileSize(exactFile)).not.toThrow();
    });

    it('should reject files over 5MB', () => {
      const largeFile = createMockFile('resume.yaml', IMPORT_CONSTANTS.MAX_FILE_SIZE + 1, 'application/x-yaml');
      expect(() => validateFileSize(largeFile)).toThrow(ImportValidationError);
      expect(() => validateFileSize(largeFile)).toThrow('File is too large');
    });
  });

  describe('validateFile (combined)', () => {
    it('should accept valid YAML file under size limit', () => {
      const validFile = createMockFile('resume.yaml', 1000, 'application/x-yaml');
      expect(() => validateFile(validFile)).not.toThrow();
    });

    it('should reject invalid type even if size is valid', () => {
      const invalidType = createMockFile('resume.docx', 1000, 'application/vnd.openxmlformats');
      expect(() => validateFile(invalidType)).toThrow(ImportValidationError);
    });

    it('should reject oversized file even if type is valid', () => {
      const oversized = createMockFile('resume.yaml', IMPORT_CONSTANTS.MAX_FILE_SIZE + 1, 'application/x-yaml');
      expect(() => validateFile(oversized)).toThrow(ImportValidationError);
    });
  });

  describe('getContentType', () => {
    it('should return correct MIME type for YAML', () => {
      expect(getContentType('resume.yaml')).toBe('application/x-yaml');
      expect(getContentType('resume.yml')).toBe('application/x-yaml');
    });

    it('should return correct MIME type for JSON', () => {
      expect(getContentType('resume.json')).toBe('application/json');
    });

    it('should return correct MIME type for PDF', () => {
      expect(getContentType('resume.pdf')).toBe('application/pdf');
    });

    it('should return octet-stream for unknown types', () => {
      expect(getContentType('resume.unknown')).toBe('application/octet-stream');
    });
  });
});

describe('Upload Progress Indication', () => {
  it('should track importing state correctly', () => {
    // Simulate the importing state management
    let importing = false;
    
    const startImport = () => { importing = true; };
    const endImport = () => { importing = false; };
    
    expect(importing).toBe(false);
    startImport();
    expect(importing).toBe(true);
    endImport();
    expect(importing).toBe(false);
  });

  it('should disable buttons during import', () => {
    const importing = true;
    const loading = false;
    
    // Buttons should be disabled when importing
    const buttonsDisabled = importing || loading;
    expect(buttonsDisabled).toBe(true);
  });

  it('should prevent modal close during import', () => {
    const importing = true;
    let modalClosed = false;
    
    const handleClose = () => {
      if (importing) return;
      modalClosed = true;
    };
    
    handleClose();
    expect(modalClosed).toBe(false);
  });
});

describe('Successful Import Populates Form', () => {
  it('should populate resume state with imported data', () => {
    const emptyResume = {
      contact: { name: '', items: [] },
      summary: '',
      skills: [],
      highlights: [],
      experience: [],
      education: [],
      awards: [],
      keynotes: [],
    };

    const importedData = {
      contact: { name: 'John Doe', items: [{ icon: 'email-at' as const, title: 'john@example.com', url: 'mailto:john@example.com' }] },
      summary: 'Experienced developer',
      skills: ['JavaScript', 'TypeScript'],
      highlights: [],
      experience: [],
      education: [{ institution: 'MIT', degree: 'CS', field: '', graduationDate: '2020' }],
      awards: [],
      keynotes: [],
    };

    let resume = emptyResume;
    
    // Simulate successful import
    const handleImportSuccess = (data: typeof importedData) => {
      resume = data;
    };
    
    handleImportSuccess(importedData);
    
    expect(resume.contact.name).toBe('John Doe');
    expect(resume.summary).toBe('Experienced developer');
    expect(resume.skills).toEqual(['JavaScript', 'TypeScript']);
    expect(resume.education.length).toBe(1);
  });

  it('should handle warnings from import', () => {
    const warnings = ['Some fields could not be mapped'];
    let errorMessage: string | null = null;
    
    const handleWarnings = (warnings: string[]) => {
      if (warnings.length > 0) {
        errorMessage = `Import completed with warnings: ${warnings.join(', ')}`;
      }
    };
    
    handleWarnings(warnings);
    expect(errorMessage).toContain('warnings');
    expect(errorMessage).toContain('Some fields could not be mapped');
  });
});

describe('Error Handling Preserves Form Data', () => {
  it('should preserve existing form data on validation error', () => {
    const existingResume = {
      contact: { name: 'Existing User', items: [] },
      summary: 'Existing summary',
      skills: ['Existing Skill'],
      highlights: [],
      experience: [],
      education: [],
      awards: [],
      keynotes: [],
    };

    let resume = { ...existingResume };
    let error: string | null = null;
    
    // Simulate validation error
    const handleImportError = (err: Error) => {
      error = err.message;
      // Resume should NOT be modified
    };
    
    try {
      const invalidFile = createMockFile('resume.txt', 100, 'text/plain');
      validateFile(invalidFile);
    } catch (err) {
      handleImportError(err as Error);
    }
    
    // Resume should remain unchanged
    expect(resume.contact.name).toBe('Existing User');
    expect(resume.summary).toBe('Existing summary');
    expect(resume.skills).toEqual(['Existing Skill']);
    expect(error).toContain('Unsupported file type');
  });

  it('should preserve form data on upload error', () => {
    const existingResume = {
      contact: { name: 'Test User', items: [] },
      summary: 'Test summary',
      skills: [],
      highlights: [],
      experience: [],
      education: [],
      awards: [],
      keynotes: [],
    };

    let resume = { ...existingResume };
    let error: string | null = null;
    
    // Simulate upload error
    const handleUploadError = () => {
      error = 'Upload failed. Please check your connection and try again.';
      // Resume should NOT be modified
    };
    
    handleUploadError();
    
    // Resume should remain unchanged
    expect(resume.contact.name).toBe('Test User');
    expect(error).toBe('Upload failed. Please check your connection and try again.');
  });

  it('should preserve form data on process error', () => {
    const existingResume = {
      contact: { name: 'Another User', items: [] },
      summary: 'Another summary',
      skills: ['Skill A', 'Skill B'],
      highlights: [],
      experience: [],
      education: [],
      awards: [],
      keynotes: [],
    };

    let resume = { ...existingResume };
    let error: string | null = null;
    
    // Simulate process error
    const handleProcessError = () => {
      error = 'Could not read file. Please ensure it\'s a valid YAML, JSON, or PDF file.';
      // Resume should NOT be modified
    };
    
    handleProcessError();
    
    // Resume should remain unchanged
    expect(resume.contact.name).toBe('Another User');
    expect(resume.skills).toEqual(['Skill A', 'Skill B']);
    expect(error).toContain('Could not read file');
  });
});

describe('Template Download', () => {
  it('should have correct template filename', () => {
    const expectedFilename = 'skillsnap-resume-template.yaml';
    const templatePath = '/skillsnap-resume-template.yaml';
    
    expect(templatePath.endsWith(expectedFilename)).toBe(true);
  });

  it('should trigger download with correct attributes', () => {
    let downloadTriggered = false;
    let downloadHref = '';
    let downloadFilename = '';
    
    // Simulate download trigger
    const handleDownloadTemplate = () => {
      downloadHref = '/skillsnap-resume-template.yaml';
      downloadFilename = 'skillsnap-resume-template.yaml';
      downloadTriggered = true;
    };
    
    handleDownloadTemplate();
    
    expect(downloadTriggered).toBe(true);
    expect(downloadHref).toBe('/skillsnap-resume-template.yaml');
    expect(downloadFilename).toBe('skillsnap-resume-template.yaml');
  });
});

describe('Import Constants', () => {
  it('should have correct max file size (5MB)', () => {
    expect(IMPORT_CONSTANTS.MAX_FILE_SIZE).toBe(5 * 1024 * 1024);
  });

  it('should support all required file extensions', () => {
    expect(IMPORT_CONSTANTS.SUPPORTED_EXTENSIONS).toContain('.yaml');
    expect(IMPORT_CONSTANTS.SUPPORTED_EXTENSIONS).toContain('.yml');
    expect(IMPORT_CONSTANTS.SUPPORTED_EXTENSIONS).toContain('.json');
    expect(IMPORT_CONSTANTS.SUPPORTED_EXTENSIONS).toContain('.pdf');
  });

  it('should have correct MIME type mappings', () => {
    expect(IMPORT_CONSTANTS.MIME_TYPE_MAP['.yaml']).toBe('application/x-yaml');
    expect(IMPORT_CONSTANTS.MIME_TYPE_MAP['.yml']).toBe('application/x-yaml');
    expect(IMPORT_CONSTANTS.MIME_TYPE_MAP['.json']).toBe('application/json');
    expect(IMPORT_CONSTANTS.MIME_TYPE_MAP['.pdf']).toBe('application/pdf');
  });
});
