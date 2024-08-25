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

  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [statusType, setStatusType] = useState<'success' | 'error' | null>(null); // Added state for status type

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const query = new URLSearchParams({
        registry: formData.registry,
        tag: formData.tag,
        username: formData.username,
        password: formData.password,
        helm_chart_path: formData.helm_chart_path,
    }).toString();

    try {
        const response = await fetch(`http://localhost:5000/api/clustermigration?${query}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            setStatusMessage('Success: Image migrated and Helm chart updated.');
            setStatusType('success');
        } else {
            setStatusMessage(`Error: ${response.statusText}`);
            setStatusType('error');
        }
    } catch (error) {
        setStatusMessage(`Network Error: ${error}`);
        setStatusType('error');
    }
  };

  if (!isOpen) return null;

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <button onClick={onClose} style={styles.closeButton}>X</button>
        <h1>Cluster Migration</h1>
        <form onSubmit={handleSubmit} className="form-container">
          <div className="form-body">
            <div>
              <label htmlFor="registry">Registry:</label>
              <input
                type="text"
                id="registry"
                name="registry"
                value={formData.registry}
                onChange={handleChange}
                placeholder="Enter registry URL"
                style={styles.input}
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
                placeholder="Enter image tag"
                style={styles.input}
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
                placeholder="Enter your username"
                style={styles.input}
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
                placeholder="Enter your password"
                style={styles.input}
              />
            </div>
            <div>
              <label htmlFor="helm_chart_path">Helm Chart Path:</label>
              <input
                type="text"
                id="helm_chart_path"
                name="helm_chart_path"
                onChange={handleChange}
                style={styles.input}
              />
            </div>
          </div>
          <div className="form-footer">
            <button className="button-small" type="submit">Submit</button>
          </div>
        </form>
        {statusMessage && (
          <div style={{ ...styles.statusMessage, backgroundColor: statusType === 'success' ? 'lightgreen' : 'salmon' }}>
            {statusMessage}
            <button
              style={styles.closeStatusButton}
              onClick={() => setStatusMessage(null)}
            >
              X
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

// Styles for the modal and form
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
    backgroundColor: 'transparent',
    color: 'black',
    border: 'none',
    fontSize: '18px',
    fontWeight: 'bold',
    cursor: 'pointer',
  },
  input: {
    width: '100%',
    padding: '10px',
    marginBottom: '15px',
    border: '1px solid #ccc',
    borderRadius: '5px',
  },
  statusMessage: {
    marginTop: '20px',
    padding: '10px',
    borderRadius: '5px',
    color: '#333',
    position: 'relative' as 'relative',
  },
  closeStatusButton: {
    position: 'absolute' as 'absolute',
    top: '10px',
    right: '10px',
    backgroundColor: 'transparent',
    color: 'black',
    border: 'none',
    fontSize: '16px',
    cursor: 'pointer',
  }
};

export default function ClusterMigration() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  return (
    <div>
      {/* Button to open the modal */}
      <button
        className="button-small"
        onClick={openModal}
      >
        Open Cluster Migration Form
      </button>

      {/* Modal Component */}
      <ClusterMigrationForm isOpen={isModalOpen} onClose={closeModal} />
    </div>
  );
}
