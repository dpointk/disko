"use client";

import axios from 'axios';
import React, { useState, useEffect } from 'react';

interface Statistic {
    registry: string;
    amount: number;
    percentage: number;
}

export function Stat() {
    const [statistics, setStatistics] = useState<Statistic[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [cluster, setCluster] = useState<string | null>(null);

    const fetchStatistics = async (cluster: string) => {
        try {
            setLoading(true);
            setError(null);
            const response = await axios.get(`http://localhost:5000/api/statistics?cluster=${cluster}`);
            setStatistics(response.data.results);
        } catch (err) {
            setError('Failed to load statistics');
            console.error("Error fetching statistics:", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const handleUpdateStatistics = (event: CustomEvent) => {
            const selectedCluster = event.detail.cluster;
            setCluster(selectedCluster);
        };

        window.addEventListener('update-statistics', handleUpdateStatistics as EventListener);

        return () => {
            window.removeEventListener('update-statistics', handleUpdateStatistics as EventListener);
        };
    }, []);

    useEffect(() => {
        if (cluster) {
            fetchStatistics(cluster);
        }
    }, [cluster]);

    return (
        <div>
            <h3>Image Statistics</h3>
            {loading ? (
                <p>Loading...</p>
            ) : error ? (
                <p>{error}</p>
            ) : (
                <table className="table table-dark table-hover" style={{ 
                    borderCollapse: 'separate', 
                    borderSpacing: '10px', 
                    width: '50%' ,
                    border: '1px solid #ddd'
                }}>
                    <thead>
                        <tr>
                            <th style={{ padding: '10px', borderBottom: '2px solid #ccc', textAlign: 'left' }}>Registry</th>
                            <th style={{ padding: '10px', borderBottom: '2px solid #ccc', textAlign: 'left' }}>Number of Images</th>
                            <th style={{ padding: '10px', borderBottom: '2px solid #ccc', textAlign: 'left' }}>Percentage</th>
                        </tr>
                    </thead>
                    <tbody>
                        {statistics.map((stat, index) => (
                            <tr key={index}>
                                <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>{stat.registry}</td>
                                <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>{stat.amount}</td>
                                <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>{stat.percentage}%</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
