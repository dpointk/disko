"use client";

import React, { useState, useEffect, CSSProperties } from 'react';
import axios from 'axios';

interface AllProps {
    cluster: string;
    onImagesFetched: (images: string[]) => void; 
}

const All: React.FC<AllProps> = ({ cluster, onImagesFetched }) => {
    const [images, setImages] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [showTable, setShowTable] = useState(false);

    useEffect(() => {
        if (cluster) {
            fetchImages();
        }
    }, [cluster]);

    const fetchImages = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await axios.get(`http://localhost:5000/api/images/${cluster}`);
            const fetchedImages = response.data;
            setImages(fetchedImages);
            onImagesFetched(fetchedImages.map((image: any) => image[0])); 
            setShowTable(true);
        } catch (err) {
            setError('Failed to load images');
        } finally {
            setLoading(false);
        }
    };

    const toggleTable = () => {
        if (!showTable) {
            fetchImages();
        }
        setShowTable(prev => !prev);
    };

    const styles: { [key: string]: CSSProperties } = {
        imageContainer: {
            marginTop: '20px',
        },
        showImagesButton: {
            backgroundColor: '#4CAF50',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            cursor: 'pointer',
            borderRadius: '5px',
        },
        imageTable: {
            width: '100%',
            marginTop: '20px',
            borderCollapse: 'collapse',
        },
        tableHeader: {
            backgroundColor: '#f2f2f2',
        },
        tableCell: {
            border: '1px solid #ddd',
            padding: '8px',
            textAlign: 'left',
        },
    };

    return (
        <div style={styles.imageContainer}>
            <button onClick={toggleTable} style={styles.showImagesButton}>
                {showTable ? 'Hide Images' : 'Show Images'}
            </button>
            {loading && <p>Loading images...</p>}
            {error && <p>{error}</p>}
            {showTable && images.length > 0 && (
                <table style={styles.imageTable}>
                    <thead>
                        <tr>
                            <th style={styles.tableHeader}>Image Name</th>
                            <th style={styles.tableHeader}>Date</th>
                            <th style={styles.tableHeader}>Registry</th>
                        </tr>
                    </thead>
                    <tbody>
                        {images.map((image, index) => (
                            <tr key={index}>
                                <td style={styles.tableCell}>{image[0]}</td> {/* Image Name */}
                                <td style={styles.tableCell}>{image[1]}</td> {/* Date */}
                                <td style={styles.tableCell}>{image[2]}</td> {/* Registry */}
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default All;
