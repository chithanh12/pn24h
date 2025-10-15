'use client';

import { ViolationResult } from '../lib/types';
import { formatDateTime, getVehicleTypeName } from '../lib/utils';

interface ViolationResultsProps {
    result: ViolationResult;
    onNewSearch?: () => void;
}

export default function ViolationResults({ result, onNewSearch }: ViolationResultsProps) {
    if (!result.violation_found || result.violation_details.length === 0) {
        return (
            <div className="w-full max-w-2xl mx-auto">
                <div className="bg-white border border-green-200 rounded-lg p-8 text-center shadow-sm">
                    <div className="flex justify-center mb-4">
                        <div className="bg-green-100 rounded-full p-4">
                            <svg className="w-16 h-16 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 mb-2">
                        ✅ Không có vi phạm
                    </h3>
                    <p className="text-gray-600 mb-6">
                        Phương tiện <span className="font-mono font-semibold text-gray-900 bg-gray-100 px-2 py-1 rounded">{result.license_plate}</span> không có vi phạm giao thông
                    </p>
                    {onNewSearch && (
                        <button
                            onClick={onNewSearch}
                            className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
                        >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                            Tra cứu mới
                        </button>
                    )}
                </div>
            </div>
        );
    }

    return (
        <div className="w-full max-w-4xl mx-auto space-y-6">
            {/* Header */}
            <div className="bg-white border border-red-200 rounded-lg p-6 shadow-sm">
                <div className="flex items-start justify-between">
                    <div>
                        <h3 className="text-xl font-bold text-gray-900 mb-1">
                            ⚠️ Phát hiện vi phạm giao thông
                        </h3>
                        <p className="text-red-600 font-medium">
                            🚨 Tìm thấy {result.violation_details.length} vi phạm
                        </p>
                    </div>
                    {onNewSearch && (
                        <button
                            onClick={onNewSearch}
                            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                        >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                            Tra cứu mới
                        </button>
                    )}
                </div>
            </div>

            {/* Violation Cards */}
            {result.violation_details.map((violation, index) => (
                <div key={index} className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
                    {/* Card Header */}
                    <div className="bg-red-600 px-6 py-4">
                        <div className="flex items-center justify-between">
                            <h4 className="text-lg font-bold text-white">
                                🚫 Vi phạm #{index + 1}
                            </h4>
                            <span className="bg-white/20 px-3 py-1 rounded-full text-sm font-semibold text-white">
                                {violation.payment_status}
                            </span>
                        </div>
                    </div>

                    {/* Card Body */}
                    <div className="p-6 space-y-4">
                        {/* License Plate and Vehicle Info */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                                    Biển kiểm soát
                                </label>
                                <p className="mt-1 text-lg font-mono font-bold text-gray-900">
                                    {violation.license_plate}
                                </p>
                            </div>
                            <div>
                                <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                                    Loại phương tiện
                                </label>
                                <p className="mt-1 text-lg font-semibold text-gray-900">
                                    {violation.vehicle_type}
                                </p>
                            </div>
                        </div>

                        {/* Vehicle Color */}
                        <div>
                            <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                                Màu sắc
                            </label>
                            <p className="mt-1 text-gray-900">
                                {violation.vehicle_color}
                            </p>
                        </div>

                        {/* Violation Time and Location */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                                    Thời gian vi phạm
                                </label>
                                <p className="mt-1 text-gray-900 flex items-center gap-2">
                                    <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    {violation.violation_time}
                                </p>
                            </div>
                        </div>

                        <div>
                            <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                                Địa điểm vi phạm
                            </label>
                            <p className="mt-1 text-gray-900 flex items-start gap-2">
                                <svg className="w-4 h-4 text-gray-400 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                                <span>{violation.violation_location}</span>
                            </p>
                        </div>

                        {/* Violation Behavior */}
                        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                            <label className="text-xs font-semibold text-red-700 uppercase tracking-wide">
                                Hành vi vi phạm
                            </label>
                            <p className="mt-2 text-red-900 font-medium">
                                {violation.violation_behavior}
                            </p>
                        </div>

                        {/* Detecting Unit */}
                        <div>
                            <label className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                                Đơn vị phát hiện
                            </label>
                            <p className="mt-1 text-sm text-gray-700">
                                {violation.detecting_unit}
                            </p>
                        </div>
                    </div>
                </div>
            ))}

            {/* Footer Info */}
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <div className="flex items-start gap-3">
                    <svg className="w-5 h-5 text-gray-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                    </svg>
                    <div className="text-xs text-gray-600">
                        <p>📊 Dữ liệu được tra cứu từ website Cảnh sát giao thông Việt Nam</p>
                        <p className="mt-1">🕐 Thời gian tra cứu: {formatDateTime(result.scraped_at)}</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

