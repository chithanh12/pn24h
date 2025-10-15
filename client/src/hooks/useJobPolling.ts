/**
 * Custom hook for polling job status
 */

import { useEffect, useState, useRef, useCallback } from 'react';
import { getJobStatus } from '../lib/api';
import { JobResponse, JobStatus } from '../lib/types';

interface UseJobPollingOptions {
    jobId: string | null;
    enabled?: boolean;
    interval?: number; // milliseconds
    onComplete?: (job: JobResponse) => void;
    onError?: (error: Error) => void;
}

export function useJobPolling({
    jobId,
    enabled = true,
    interval = 3000,
    onComplete,
    onError,
}: UseJobPollingOptions) {
    const [job, setJob] = useState<JobResponse | null>(null);
    const [isPolling, setIsPolling] = useState(false);
    const [error, setError] = useState<Error | null>(null);
    const intervalRef = useRef<NodeJS.Timeout | null>(null);

    // Use refs to store callbacks to avoid recreating the effect
    const onCompleteRef = useRef(onComplete);
    const onErrorRef = useRef(onError);

    // Update refs when callbacks change
    useEffect(() => {
        onCompleteRef.current = onComplete;
        onErrorRef.current = onError;
    }, [onComplete, onError]);

    useEffect(() => {
        if (!jobId || !enabled) {
            return;
        }

        const poll = async () => {
            try {
                setIsPolling(true);
                const jobData = await getJobStatus(jobId);
                setJob(jobData);

                // Stop polling if job is completed or failed
                if (jobData.status === 'completed' || jobData.status === 'failed') {
                    if (intervalRef.current) {
                        clearInterval(intervalRef.current);
                        intervalRef.current = null;
                    }
                    setIsPolling(false);

                    if (jobData.status === 'completed' && onCompleteRef.current) {
                        onCompleteRef.current(jobData);
                    }

                    if (jobData.status === 'failed' && jobData.error) {
                        const err = new Error(jobData.error);
                        setError(err);
                        if (onErrorRef.current) {
                            onErrorRef.current(err);
                        }
                    }
                }
            } catch (err) {
                const error = err instanceof Error ? err : new Error('Failed to fetch job status');
                setError(error);
                setIsPolling(false);
                if (onErrorRef.current) {
                    onErrorRef.current(error);
                }
                // Stop polling on error
                if (intervalRef.current) {
                    clearInterval(intervalRef.current);
                    intervalRef.current = null;
                }
            }
        };

        // Initial poll
        poll();

        // Set up polling interval
        intervalRef.current = setInterval(poll, interval);

        // Cleanup
        return () => {
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
                intervalRef.current = null;
            }
        };
    }, [jobId, enabled, interval]); // Removed onComplete and onError from dependencies

    return { job, isPolling, error };
}

