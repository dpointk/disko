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

    //setLoading(false);
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
        //setLoading(false);
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
            {loading ? (
                <p>Loading...</p>
            ) : error ? (
                <p>{error}</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Registry</th>
                            <th>Number of Images</th>
                            <th>Percentage</th>
                        </tr>
                    </thead>
                    <tbody>
                        {statistics.map((stat, index) => (
                            <tr key={index}>
                                <td>{stat.registry}</td>
                                <td>{stat.amount}</td>
                                <td>{stat.percentage}%</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}