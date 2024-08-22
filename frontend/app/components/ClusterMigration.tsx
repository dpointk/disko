"use client";
import { useState } from 'react';

interface ClusterMigrationFormProps {
  isOpen: boolean;
  onClose: () => void;
}

export function ClusterMigrationForm({ isOpen, onClose }: ClusterMigrationFormProps) {
  const [formData, setFormData] = useState({
    registry: '',
    tag: '',
    username: '',
    password: '',
    helm_chart_path: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/clustermigration', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Success:', result);
        // Handle successful form submission, e.g., show a success message
      } else {
        console.error('Error:', response.statusText);
        // Handle server errors, e.g., show an error message
      }
    } catch (error) {
      console.error('Error:', error);
      // Handle network errors, e.g., show a network error message
    }
  };

  if (!isOpen) return null;

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <button onClick={onClose} style={styles.closeButton}>X</button>
        <h1>Input Form</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="registry">Registry:</label>
            <input
              type="text"
              id="registry"
              name="registry"
              value={formData.registry}
              onChange={handleChange}
            />
          </div>
          <div>
            <label htmlFor="tag">Tag:</label>
            <input
              type="text"
              id="tag"
              name="tag"
              value={formData.tag}
              onChange={handleChange}
            />
          </div>
          <div>
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
            />
          </div>
          <div>
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
            />
          </div>
          <div>
            <label htmlFor="helm_chart_path">Helm Chart Path:</label>
            <input
              type="text"
              id="helm_chart_path"
              name="helm_chart_path"
              value={formData.helm_chart_path}
              onChange={handleChange}
            />
          </div>
          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
}

// Styles for the modal
const styles = {
  overlay: {
    position: 'fixed' as 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    display: 'flex' as 'flex',
    justifyContent: 'center' as 'center',
    alignItems: 'center' as 'center',
  },
  modal: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    width: '400px',
    position: 'relative' as 'relative',
  },
  closeButton: {
    position: 'absolute' as 'absolute',
    top: '10px',
    right: '10px',
    backgroundColor: 'red',
    color: 'white',
    border: 'none',
    borderRadius: '50%',
    width: '30px',
    height: '30px',
    cursor: 'pointer',
    display: 'flex' as 'flex',
    justifyContent: 'center' as 'center',
    alignItems: 'center' as 'center',
  },
};

export default function ClusterMigration() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  return (
    <div>
      {/* Button to open the modal */}
      <button
        onClick={openModal}
        style={{ backgroundColor: 'blue', color: 'white', padding: '10px', border: 'none', borderRadius: '5px' }}
      >
        Open Cluster Migration Form
      </button>
      
      {/* Modal Component */}
      <ClusterMigrationForm isOpen={isModalOpen} onClose={closeModal} />
    </div>
  );
}
