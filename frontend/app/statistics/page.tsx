"use client";

import { Navbar } from "../components/Navbar";
import { Stat } from "../components/Stat";
import ClusterSelector from "../components/ClusterSelector";
import All from "../components/All";
import React, { useState } from 'react';
import ClusterMigrationForm from "../components/ClusterMigration";
import { CopyImageForm } from "../components/CopyImage";

export default function Statistics() {
    const [selectedCluster, setSelectedCluster] = useState<string | null>(null);
    const [availableImages, setAvailableImages] = useState<string[]>([]);

    // Handle cluster selection
    const handleClusterChange = (cluster: string) => {
        setSelectedCluster(cluster);
    };

    // Callback to handle images fetched from All component
    const handleImagesFetched = (images: string[]) => {
        setAvailableImages(images);
    };

    return (
        <>
            <Navbar />
            <div className="pt-4 min-h-screen" style={{ backgroundImage: 'linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%)' }}>
                <ClusterSelector onClusterChange={handleClusterChange} />
                <Stat />
                {selectedCluster && (
                    <All 
                        cluster={selectedCluster} 
                        onImagesFetched={handleImagesFetched} 
                    />
                )}
                <ClusterMigrationForm />
                {selectedCluster && (
                    <CopyImageForm
                        cluster={selectedCluster || ""} // Ensure selectedCluster is not null
                        availableImages={availableImages} // Pass availableImages correctly
                    />
                )}
            </div>
        </>
    );
}
