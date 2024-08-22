"use client";

import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface ClusterSelectorProps {
    onClusterChange: (cluster: string) => void;
}

const ClusterSelector: React.FC<ClusterSelectorProps> = ({ onClusterChange }) => {
    const [clusters, setClusters] = useState<string[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [selectedCluster, setSelectedCluster] = useState<string>('');

    useEffect(() => {
        const fetchClusters = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await axios.get('http://localhost:5000/api/clusters');
                setClusters(response.data);
            } catch (err) {
                setError('Failed to load clusters');
            } finally {
                setLoading(false);
            }
        };

        fetchClusters();
    }, []);

    const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedCluster(event.target.value);
    };

    const handleSubmit = async () => {
        if (selectedCluster === '') {
            setError('Please select a cluster');
            return;
        }
        
        try {
            await axios.post('http://localhost:5000/api/selected-cluster', { cluster: selectedCluster });
            onClusterChange(selectedCluster);
            
            // Dispatch custom event with the selected cluster
            const event = new CustomEvent('update-statistics', { detail: { cluster: selectedCluster } });
            window.dispatchEvent(event);
        } catch (err) {
            setError('Failed to select cluster');
        }
    };

    return (
        <div>
            {loading && <p>Loading clusters...</p>}
            {error && <p>{error}</p>}
            <select onChange={handleChange} value={selectedCluster}>
                <option value="" disabled>Select a cluster</option>
                {clusters.map((cluster) => (
                    <option key={cluster} value={cluster}>
                        {cluster}
                    </option>
                ))}
            </select>
            <button
                onClick={handleSubmit}
                style={{ backgroundColor: 'blue', color: 'white', padding: '10px', border: 'none', borderRadius: '5px', marginTop: '10px' }}
            >
                Submit
            </button>
        </div>
    );
};

export default ClusterSelector;
