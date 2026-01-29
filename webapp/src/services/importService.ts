/**
 * Import Service
 * Handles file validation, presigned URL upload, and import processing
 * Requirements: 2.3, 2.4, 2.5, 8.1, 8.2, 8.3, 8.4, 8.5
 */
import { api } from './api';
import type { ResumeJSON, ImportProcessResponse } from '../types';

// Constants
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

const SUPPORTED_EXTENSIONS = ['.yaml', '.yml', '.json', '.pdf'];

const MIME_TYPE_MAP: Record<string, string> = {
  '.yaml': 'application/x-yaml',
  '.yml': 'application/x-yaml',
  '.json': 'application/json',
  '.pdf': 'application/pdf',
};

// Error types with user-friendly messages (Requirements 8.1-8.5)
export class ImportValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ImportValidationError';
  }
}

export class ImportUploadError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ImportUploadError';
  }
}

export class ImportProcessError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ImportProcessError';
  }
}

export class ImportAuthError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ImportAuthError';
  }
}

export class ImportTimeoutError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ImportTimeoutError';
  }
}

// User-friendly error messages (Requirements 8.1-8.5)
const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Upload failed. Please check your connection and try again.',
  AUTH_ERROR: 'Session expired. Please refresh the page and try again.',
  TIMEOUT_ERROR: 'Processing took too long. Please try a smaller file or simpler format.',
  FILE_CORRUPTED: 'Could not read file. Please ensure it\'s a valid YAML, JSON, or PDF file.',
  FILE_TOO_LARGE: 'File is too large. Please select a file under 5MB.',
  UNSUPPORTED_TYPE: 'Unsupported file type. Please select a YAML, JSON, or PDF file.',
  GENERIC_ERROR: 'An error occurred while processing your file. Please try again.',
};

// Validation functions
export function getFileExtension(filename: string): string {
  const lastDot = filename.lastIndexOf('.');
  if (lastDot === -1) return '';
  return filename.slice(lastDot).toLowerCase();
}

export function validateFileType(file: File): void {
  const extension = getFileExtension(file.name);
  if (!SUPPORTED_EXTENSIONS.includes(extension)) {
    throw new ImportValidationError(ERROR_MESSAGES.UNSUPPORTED_TYPE);
  }
}

export function validateFileSize(file: File): void {
  if (file.size > MAX_FILE_SIZE) {
    throw new ImportValidationError(ERROR_MESSAGES.FILE_TOO_LARGE);
  }
}

export function validateFile(file: File): void {
  validateFileType(file);
  validateFileSize(file);
}

export function getContentType(filename: string): string {
  const extension = getFileExtension(filename);
  return MIME_TYPE_MAP[extension] || 'application/octet-stream';
}

// Parse error response from API
function parseApiError(response: Response, errorBody: any): Error {
  const status = response.status;
  const errorMessage = errorBody?.message || '';
  const errorType = errorBody?.error || '';
  
  // Log detailed error for debugging (Requirement 8.5)
  console.error('Import API error:', { status, errorType, errorMessage, errorBody });
  
  // Map to user-friendly errors (Requirements 8.1-8.5)
  if (status === 401 || status === 403) {
    return new ImportAuthError(ERROR_MESSAGES.AUTH_ERROR);
  }
  
  if (status === 504 || errorType === 'Timeout') {
    return new ImportTimeoutError(ERROR_MESSAGES.TIMEOUT_ERROR);
  }
  
  if (status === 404) {
    return new ImportUploadError('File not found or expired. Please try uploading again.');
  }
  
  // Check for specific error messages from backend
  if (errorMessage.includes('MIME') || errorMessage.includes('type does not match')) {
    return new ImportValidationError(errorMessage);
  }
  
  if (errorMessage.includes('Could not read') || errorMessage.includes('Could not parse')) {
    return new ImportProcessError(ERROR_MESSAGES.FILE_CORRUPTED);
  }
  
  if (errorMessage.includes('extract text')) {
    return new ImportProcessError('Could not extract text from PDF. The file may be image-based or password-protected.');
  }
  
  // Return the backend message if it's user-friendly, otherwise use generic
  if (errorMessage && !errorMessage.includes('Error:') && errorMessage.length < 200) {
    return new ImportProcessError(errorMessage);
  }
  
  return new ImportProcessError(ERROR_MESSAGES.GENERIC_ERROR);
}

// Upload function with comprehensive error handling
export async function uploadFileToS3(file: File, uploadUrl: string): Promise<void> {
  const contentType = getContentType(file.name);
  
  try {
    const response = await fetch(uploadUrl, {
      method: 'PUT',
      headers: {
        'Content-Type': contentType,
      },
      body: file,
    });

    if (!response.ok) {
      // Log detailed error for debugging (Requirement 8.5)
      console.error('S3 upload failed:', { status: response.status, statusText: response.statusText });
      
      if (response.status === 403) {
        throw new ImportAuthError(ERROR_MESSAGES.AUTH_ERROR);
      }
      throw new ImportUploadError(ERROR_MESSAGES.NETWORK_ERROR);
    }
  } catch (error) {
    // Log detailed error for debugging (Requirement 8.5)
    console.error('S3 upload error:', error);
    
    if (error instanceof ImportAuthError || error instanceof ImportUploadError) {
      throw error;
    }
    
    // Network error (Requirement 8.1)
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new ImportUploadError(ERROR_MESSAGES.NETWORK_ERROR);
    }
    
    throw new ImportUploadError(ERROR_MESSAGES.NETWORK_ERROR);
  }
}

// Main import flow with comprehensive error handling
export interface ImportResult {
  resumejson: ResumeJSON;
  warnings?: string[];
  source: 'yaml' | 'json' | 'pdf';
}

export async function importResumeFile(file: File): Promise<ImportResult> {
  // Step 1: Validate file
  validateFile(file);

  // Step 2: Get presigned URL
  let uploadUrl: string;
  let s3Key: string;
  
  try {
    const contentType = getContentType(file.name);
    const urlResponse = await api.getImportUrl(file.name, contentType);
    uploadUrl = urlResponse.uploadUrl;
    s3Key = urlResponse.s3Key;
  } catch (error: any) {
    // Log detailed error for debugging (Requirement 8.5)
    console.error('Get import URL error:', error);
    
    if (error.status === 401 || error.status === 403) {
      throw new ImportAuthError(ERROR_MESSAGES.AUTH_ERROR);
    }
    
    // Check for MIME type validation error from backend
    if (error.message?.includes('type does not match') || error.message?.includes('MIME')) {
      throw new ImportValidationError(error.message);
    }
    
    throw new ImportUploadError(ERROR_MESSAGES.NETWORK_ERROR);
  }

  // Step 3: Upload file to S3
  await uploadFileToS3(file, uploadUrl);

  // Step 4: Process the uploaded file
  try {
    const result: ImportProcessResponse = await api.processImport(s3Key);
    
    return {
      resumejson: result.resumejson,
      warnings: result.warnings,
      source: result.source,
    };
  } catch (error: any) {
    // Log detailed error for debugging (Requirement 8.5)
    console.error('Process import error:', error);
    
    // Try to parse the error response
    if (error.response) {
      try {
        const errorBody = await error.response.json();
        throw parseApiError(error.response, errorBody);
      } catch (parseError) {
        if (parseError instanceof ImportAuthError || 
            parseError instanceof ImportTimeoutError ||
            parseError instanceof ImportValidationError ||
            parseError instanceof ImportProcessError) {
          throw parseError;
        }
      }
    }
    
    // Handle specific error types
    if (error.status === 401 || error.status === 403) {
      throw new ImportAuthError(ERROR_MESSAGES.AUTH_ERROR);
    }
    
    if (error.status === 504) {
      throw new ImportTimeoutError(ERROR_MESSAGES.TIMEOUT_ERROR);
    }
    
    // Check error message for specific cases
    const errorMessage = error.message || '';
    if (errorMessage.includes('timeout') || errorMessage.includes('Timeout')) {
      throw new ImportTimeoutError(ERROR_MESSAGES.TIMEOUT_ERROR);
    }
    
    if (errorMessage.includes('Could not read') || errorMessage.includes('Could not parse')) {
      throw new ImportProcessError(ERROR_MESSAGES.FILE_CORRUPTED);
    }
    
    // Return backend message if available and user-friendly
    if (errorMessage && !errorMessage.includes('Error:') && errorMessage.length < 200) {
      throw new ImportProcessError(errorMessage);
    }
    
    throw new ImportProcessError(ERROR_MESSAGES.GENERIC_ERROR);
  }
}

// Export constants for testing
export const IMPORT_CONSTANTS = {
  MAX_FILE_SIZE,
  SUPPORTED_EXTENSIONS,
  MIME_TYPE_MAP,
  ERROR_MESSAGES,
};
