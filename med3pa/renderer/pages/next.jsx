import React, {useState} from 'react'
import Head from 'next/head'
import Link from 'next/link'
const FIELD_CONFIGS = [
  { id: 'stayId', label: 'Stay Id:' },
  { id: 'hospitalId', label: 'Hospitalid:' },
  { id: 'deceased', label: 'Deceased:' },
  { id: 'age', label: 'Age:' },
  { id: 'bicarbonateMin', label: 'Bicarbonate Min:' },
  { id: 'bicarbonateMax', label: 'Bicarbonate Max:' },
  { id: 'bilirubinMin', label: 'Bilirubin Min:' },
  { id: 'bilirubinMax', label: 'Bilirubin Max:' },
  { id: 'potassiumMin', label: 'Potassium Min:' },
  { id: 'potassiumMax', label: 'Potassium Max:' },
  { id: 'sodiumMin', label: 'Sodium Min:' },
  { id: 'sodiumMax', label: 'Sodium Max:' },
  { id: 'bunMin', label: 'Bun Min:' },
  { id: 'bunMax', label: 'Bun Max:' },
  { id: 'wbcMin', label: 'Wbc Min:' },
  { id: 'wbcMax', label: 'Wbc Max:' },
  { id: 'pao2Fio2', label: 'Pao2Fio2:' },
  { id: 'cpap', label: 'Cpap:' },
  { id: 'vent', label: 'Vent:' },
  { id: 'gcsMin', label: 'Gcs Min:' },
  { id: 'hrMin', label: 'Hr Min:' },
  { id: 'hrMax', label: 'Hr Max:' },
  { id: 'tempcMin', label: 'Tempc Min:' },
  { id: 'tempcMax', label: 'Tempc Max:' },
  { id: 'sbpMin', label: 'Sbp Min:' },
  { id: 'sbpMax', label: 'Sbp Max:' },
  { id: 'uo', label: 'Uo:' },
  { id: 'aids', label: 'Aids:' },
  { id: 'hem', label: 'Hem:' },
  { id: 'mets', label: 'Mets:' },
  { id: 'admissionType', label: 'Admissiontype:' },
];

const initialFormState = FIELD_CONFIGS.reduce((acc, field) => {
  acc[field.id] = '';
  return acc;
}, {});

export default function PatientDataInput() {
  const [activeTab, setActiveTab] = useState('single'); // 'batch' or 'single'
  const [formData, setFormData] = useState(initialFormState);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };


  const handleClearFields = () => {
    setFormData(initialFormState);
  };


  const handleRunInference = (e) => {
    e.preventDefault();
    console.log('Running single inference with data:', formData);
    // add med3pa API call logic here 
  };

  return (
    <div style={styles.container}>

      <div style={styles.header}>
        {/* <span style={styles.headerIcon}>📝</span> */}
        <h2 style={styles.headerTitle}>Patient Data Input</h2>
      </div>


      <div style={styles.tabContainer}>
        <button
          style={{
            ...styles.tabButton,
            ...(activeTab === 'batch' ? styles.activeTabLeft : styles.inactiveTabLeft),
          }}
          onClick={() => setActiveTab('batch')}
        >
          Batch Processing (CSV)
        </button>
        <button
          style={{
            ...styles.tabButton,
            ...(activeTab === 'single' ? styles.activeTabRight : styles.inactiveTabRight),
          }}
          onClick={() => setActiveTab('single')}
        >
          Single Patient (Manual Entry)
        </button>
      </div>


      <form onSubmit={handleRunInference}>
        <div style={styles.grid}>
          {FIELD_CONFIGS.map((field) => (
            <div key={field.id} style={styles.inputGroup}>
              <label htmlFor={field.id} style={styles.label}>
                {field.label}
              </label>
              <input
                type="text"
                id={field.id}
                name={field.id}
                value={formData[field.id]}
                onChange={handleInputChange}
                style={styles.input}
              />
            </div>
          ))}
        </div>

        
        <div style={styles.footer}>
          <button
            type="button"
            onClick={handleClearFields}
            style={styles.clearButton}
          >
            Clear Fields
          </button>
          <button type="submit" style={styles.submitButton}>
            <span style={{ marginRight: '8px' }}>▶</span> Run Single Inference
          </button>
        </div>
      </form>
    </div>
  );
}


const styles = {
  container: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    backgroundColor: '#f8fafc',
    padding: '24px',
    borderRadius: '12px',
    border: '1px solid #e2e8f0',
    maxWidth: '1200px',
    margin: '20px auto',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '20px',
  },
  headerIcon: {
    color: '#1e40af',
    fontSize: '18px',
    marginRight: '8px',
  },
  headerTitle: {
    color: '#1e40af',
    fontSize: '18px',
    fontWeight: '600',
    margin: 0,
  },
  tabContainer: {
    display: 'flex',
    justifyContent: 'center',
    marginBottom: '30px',
  },
  tabButton: {
    padding: '8px 16px',
    fontSize: '14px',
    border: 'none',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  activeTabLeft: {
    backgroundColor: '#0f5132',
    color: '#fff',
    borderRadius: '6px 0 0 6px',
  },
  inactiveTabLeft: {
    backgroundColor: '#94a3b8',
    color: '#fff',
    borderRadius: '6px 0 0 6px',
  },
  activeTabRight: {
    backgroundColor: '#0f5132',
    color: '#fff',
    borderRadius: '0 6px 6px 0',
  },
  inactiveTabRight: {
    backgroundColor: '#94a3b8',
    color: '#fff',
    borderRadius: '0 6px 6px 0',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(5, minmax(0, 1fr))', // Exact 5-column layout matching the UI
    gap: '20px 16px',
    marginBottom: '30px',
  },
  inputGroup: {
    display: 'flex',
    flexDirection: 'column',
  },
  label: {
    fontSize: '13px',
    fontWeight: '600',
    color: '#334155',
    marginBottom: '6px',
  },
  input: {
    padding: '10px 12px',
    borderRadius: '8px',
    border: '1px solid #94a3b8',
    fontSize: '14px',
    outline: 'none',
    backgroundColor: '#fff',
    transition: 'border-color 0.15s ease',
  },
  footer: {
    display: 'flex',
    justifyContent: 'flex-end',
    gap: '16px',
    marginTop: '20px',
  },
  clearButton: {
    padding: '10px 24px',
    borderRadius: '6px',
    border: '1px solid #dc3545',
    backgroundColor: '#fff',
    color: '#dc3545',
    fontSize: '14px',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  submitButton: {
    display: 'flex',
    alignItems: 'center',
    padding: '10px 20px',
    borderRadius: '6px',
    border: 'none',
    backgroundColor: '#0f5132',
    color: '#fff',
    fontSize: '14px',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
};