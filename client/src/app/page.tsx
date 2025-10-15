'use client';

import { useState } from 'react';
import SearchForm from '../components/SearchForm';
import ViolationResults from '../components/ViolationResults';
import JobStatusIndicator from '../components/JobStatusIndicator';
import { submitScrapeJob } from '../lib/api';
import { useJobPolling } from '../hooks/useJobPolling';
import { VehicleType, ViolationResult } from '../lib/types';

export default function Home() {
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);
  const [result, setResult] = useState<ViolationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const { job, isPolling } = useJobPolling({
    jobId: currentJobId,
    enabled: currentJobId !== null,
    onComplete: (completedJob) => {
      if (completedJob.result) {
        setResult(completedJob.result);
      }
    },
    onError: (err) => {
      setError(err.message);
    },
  });

  const handleSearch = async (licensePlate: string, vehicleType: VehicleType) => {
    try {
      // Reset state
      setError(null);
      setResult(null);
      setCurrentJobId(null);

      // Submit job
      const response = await submitScrapeJob({
        license_plate: licensePlate,
        vehicle_type: vehicleType,
      });

      setCurrentJobId(response.job_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Có lỗi xảy ra khi gửi yêu cầu');
    }
  };

  const handleNewSearch = () => {
    setCurrentJobId(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-center gap-3">
            <div className="bg-blue-600 rounded-lg p-2 shadow-sm">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div className="text-center">
              <h1 className="text-xl font-bold text-gray-900">
                🚗 Tra cứu vi phạm giao thông
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                Cảnh sát giao thông Việt Nam
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="space-y-8">
          {/* Search Form */}
          {!job && !result && !error && (
            <SearchForm onSubmit={handleSearch} isLoading={isPolling} />
          )}

          {/* Job Status */}
          {job && !result && job.status !== 'completed' && (
            <JobStatusIndicator status={job.status} message={job.error} />
          )}

          {/* Error State */}
          {error && !job && (
            <div className="w-full max-w-2xl mx-auto">
              <div className="bg-red-50 border-2 border-red-200 rounded-lg p-6">
                <div className="flex items-start gap-4">
                  <svg className="w-6 h-6 text-red-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-red-800 mb-1">
                      Có lỗi xảy ra
                    </h3>
                    <p className="text-sm text-red-700">{error}</p>
                  </div>
                </div>
                <button
                  onClick={handleNewSearch}
                  className="mt-4 bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                >
                  Thử lại
                </button>
              </div>
            </div>
          )}

          {/* Results */}
          {result && (
            <ViolationResults result={result} onNewSearch={handleNewSearch} />
          )}
        </div>
      </main>

      {/* Footer - Sticky at bottom */}
      <footer className="mt-auto bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-600">
            <p className="text-sm">© 2025 Vietnamese Traffic Police Scraper</p>
            <p className="mt-2 text-xs text-gray-500">
              Dữ liệu được tra cứu từ{' '}
              <a
                href="https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-700 underline"
              >
                website CSGT Việt Nam
              </a>
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
