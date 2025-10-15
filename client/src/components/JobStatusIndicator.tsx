'use client';

import { JobStatus } from '../lib/types';

interface JobStatusIndicatorProps {
    status: JobStatus;
    message?: string;
}

export default function JobStatusIndicator({ status, message }: JobStatusIndicatorProps) {
    const getStatusConfig = () => {
        switch (status) {
            case 'pending':
                return {
                    icon: (
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    ),
                    title: '⏳ Đang chờ xử lý',
                    description: 'Yêu cầu của bạn đang được xếp hàng...',
                    bgColor: 'bg-yellow-50',
                    borderColor: 'border-yellow-200',
                    textColor: 'text-yellow-900',
                    iconColor: 'text-yellow-600',
                };
            case 'running':
                return {
                    icon: (
                        <svg className="animate-spin w-6 h-6" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                    ),
                    title: '🔍 Đang tra cứu',
                    description: 'Hệ thống đang giải captcha và thu thập dữ liệu...',
                    bgColor: 'bg-blue-50',
                    borderColor: 'border-blue-200',
                    textColor: 'text-blue-900',
                    iconColor: 'text-blue-600',
                };
            case 'completed':
                return {
                    icon: (
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    ),
                    title: '✅ Hoàn thành',
                    description: 'Tra cứu thành công!',
                    bgColor: 'bg-green-50',
                    borderColor: 'border-green-200',
                    textColor: 'text-green-900',
                    iconColor: 'text-green-600',
                };
            case 'failed':
                return {
                    icon: (
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    ),
                    title: '❌ Tra cứu thất bại',
                    description: message || 'Có lỗi xảy ra trong quá trình tra cứu',
                    bgColor: 'bg-red-50',
                    borderColor: 'border-red-200',
                    textColor: 'text-red-900',
                    iconColor: 'text-red-600',
                };
        }
    };

    const config = getStatusConfig();

    return (
        <div className={`w-full max-w-2xl mx-auto border rounded-lg p-6 shadow-sm ${config.bgColor} ${config.borderColor}`}>
            <div className="flex items-center gap-4">
                <div className={`${config.iconColor}`}>
                    {config.icon}
                </div>
                <div className="flex-1">
                    <h3 className={`text-lg font-semibold ${config.textColor}`}>
                        {config.title}
                    </h3>
                    <p className={`text-sm ${config.textColor} mt-1 opacity-90`}>
                        {config.description}
                    </p>
                </div>
            </div>

            {/* Progress bar for running status */}
            {status === 'running' && (
                <div className="mt-5">
                    <div className="w-full bg-blue-200 rounded-full h-2 overflow-hidden">
                        <div className="bg-blue-600 h-full rounded-full animate-pulse" style={{ width: '70%' }}></div>
                    </div>
                    <p className="text-xs text-blue-700 font-medium mt-2 text-center">
                        ⏱️ Vui lòng đợi, quá trình này có thể mất 15-30 giây...
                    </p>
                </div>
            )}
        </div>
    );
}

