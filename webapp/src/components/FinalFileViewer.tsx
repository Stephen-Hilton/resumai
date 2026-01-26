/**
 * Final File Viewer Modal
 * Requirements: 11.1
 */
import { useState } from 'react';
import { X, Download, Copy, Check, ExternalLink } from 'lucide-react';

interface FinalFileViewerProps {
  title: string;
  content?: string;
  s3Url?: string;
  publicUrl?: string;
  fileType: 'html' | 'pdf';
  onClose: () => void;
}

export function FinalFileViewer({
  title,
  content,
  s3Url,
  publicUrl,
  fileType,
  onClose,
}: FinalFileViewerProps) {
  const [copied, setCopied] = useState(false);

  async function handleCopyUrl() {
    if (publicUrl) {
      await navigator.clipboard.writeText(publicUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }

  function handleDownload() {
    if (fileType === 'html' && content) {
      const blob = new Blob([content], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${title.toLowerCase().replace(/\s+/g, '-')}.html`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } else if (s3Url) {
      window.open(s3Url, '_blank');
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-5xl max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
          <div className="flex items-center gap-2">
            {publicUrl && (
              <>
                <button
                  onClick={handleCopyUrl}
                  className="flex items-center px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded-lg"
                  title="Copy public URL"
                >
                  {copied ? (
                    <Check className="w-4 h-4 mr-1 text-green-500" />
                  ) : (
                    <Copy className="w-4 h-4 mr-1" />
                  )}
                  {copied ? 'Copied!' : 'Copy URL'}
                </button>
                <a
                  href={publicUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded-lg"
                >
                  <ExternalLink className="w-4 h-4 mr-1" />
                  Open
                </a>
              </>
            )}
            <button
              onClick={handleDownload}
              className="flex items-center px-3 py-1.5 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              <Download className="w-4 h-4 mr-1" />
              Download
            </button>
            <button
              onClick={onClose}
              className="p-1 hover:bg-gray-100 rounded"
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-4">
          {fileType === 'html' && content ? (
            <iframe
              srcDoc={content}
              className="w-full h-full min-h-[600px] border border-gray-200 rounded-lg"
              title={title}
            />
          ) : fileType === 'pdf' && s3Url ? (
            <iframe
              src={s3Url}
              className="w-full h-full min-h-[600px] border border-gray-200 rounded-lg"
              title={title}
            />
          ) : (
            <div className="flex items-center justify-center h-64 text-gray-500">
              No content available
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
