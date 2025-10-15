'use client';

import { useState } from 'react';
import { VehicleType } from '../lib/types';
import { validateLicensePlate } from '../lib/utils';

interface SearchFormProps {
    onSubmit: (licensePlate: string, vehicleType: VehicleType) => void;
    isLoading?: boolean;
}

export default function SearchForm({ onSubmit, isLoading = false }: SearchFormProps) {
    const [licensePlate, setLicensePlate] = useState('');
    const [vehicleType, setVehicleType] = useState<VehicleType>('xemay');
    const [error, setError] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        // Validation
        if (!licensePlate.trim()) {
            setError('Vui lòng nhập biển số xe');
            return;
        }

        if (!validateLicensePlate(licensePlate)) {
            setError('Biển số xe không hợp lệ');
            return;
        }

        onSubmit(licensePlate.trim(), vehicleType);
    };

    return (
        <form onSubmit={handleSubmit} className="w-full max-w-3xl mx-auto space-y-6">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 space-y-6">
                <div className="text-center">
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        🔍 Tra cứu thông tin vi phạm
                    </h2>
                    <p className="text-gray-600 text-sm">
                        Nhập biển kiểm soát để tra cứu thông tin vi phạm giao thông của phương tiện
                    </p>
                </div>

                {/* License Plate Input */}
                <div>
                    <label htmlFor="licensePlate" className="block text-sm font-medium text-gray-700 mb-2">
                        🚘 Biển kiểm soát <span className="text-red-600">*</span>
                    </label>
                    <input
                        type="text"
                        id="licensePlate"
                        value={licensePlate}
                        onChange={(e) => {
                            setLicensePlate(e.target.value.toUpperCase());
                            setError('');
                        }}
                        placeholder="Ví dụ: 59C13647 hoặc 59C-136.47"
                        disabled={isLoading}
                        className="w-full px-4 py-3 text-lg font-mono border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:cursor-not-allowed bg-white text-gray-900 placeholder-gray-400"
                    />
                    <p className="mt-1 text-xs text-gray-500">
                        💡 Nhập biển số xe không dấu, có thể bỏ qua dấu gạch ngang và chấm
                    </p>
                </div>

                {/* Vehicle Type Selector */}
                <div>
                    <label htmlFor="vehicleType" className="block text-sm font-medium text-gray-700 mb-2">
                        🏍️ Loại phương tiện <span className="text-red-600">*</span>
                    </label>
                    <select
                        id="vehicleType"
                        value={vehicleType}
                        onChange={(e) => setVehicleType(e.target.value as VehicleType)}
                        disabled={isLoading}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50 disabled:cursor-not-allowed bg-white text-gray-900 cursor-pointer"
                    >
                        <option value="xemay">🏍️ Xe máy</option>
                        <option value="oto">🚗 Ô tô</option>
                        <option value="xedapdien">🛵 Xe đạp điện</option>
                    </select>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                        <p className="text-sm text-red-700">⚠️ {error}</p>
                    </div>
                )}

                {/* Submit Button */}
                <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                    {isLoading ? (
                        <>
                            <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            <span>Đang tra cứu...</span>
                        </>
                    ) : (
                        <>
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                            <span>Tra cứu</span>
                        </>
                    )}
                </button>
            </div>

            {/* Information Box */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex gap-3">
                    <svg className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                    </svg>
                    <div className="text-sm text-blue-900">
                        <p className="font-medium mb-1">💡 Lưu ý:</p>
                        <ul className="list-disc list-inside space-y-1 text-xs">
                            <li>Hệ thống sẽ tự động giải captcha và tra cứu thông tin</li>
                            <li>Quá trình tra cứu có thể mất 15-30 giây</li>
                            <li>Dữ liệu được lấy trực tiếp từ website CSGT Việt Nam</li>
                        </ul>
                    </div>
                </div>
            </div>
        </form>
    );
}

