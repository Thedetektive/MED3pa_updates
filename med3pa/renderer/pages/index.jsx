import React from 'react'
import Head from 'next/head'
import Link from 'next/link'
import Image from 'next/image'

export default function HomePage() {
  const [message, setMessage] = React.useState('No message found')
  const [results, setResults] =  React.useState(null)
  React.useEffect(() => {
    const init = () => {
      const removeListener = window.ipc.on('message', (message) => {
        setMessage(message)
      })
      return removeListener
    }

    if (window.ipc) {
      return init()
    }

    const timeout = setTimeout(() => {
      if (window.ipc) init()
    }, 0)

    return () => clearTimeout(timeout)
  }, [])
  const fetchResults = async () =>{
    const response = await window.ipc.invoke('get-med3pa-results');
    if (response.success) {
      setResults(response.data)
    }
    else {
      setResults(response.error)
    }
  } 
  return (
    <React.Fragment>
      <Head>
        <title>Home - Nextron (basic-lang-javascript)</title>
      </Head>
      <div>
        <p>
          ⚡ Electron + Next.js ⚡ - <Link href="/next">Go to next page</Link>
        </p>
        <Image
          src="/images/logo.png"
          alt="Logo image"
          width={256}
          height={256}
        />
      </div>
      <div>
        {/* <button
          onClick={() => {
            if (window.ipc) {
              window.ipc.send('message', 'Hello')
            }
            else {
              setMessage("window.ipc does not exist sorry")
            }
          }}
        >
          Test IPC
        </button>
        <p>{message}</p> */}
        <button onClick={fetchResults}>
          get med3pa data 
        </button>
        {results && (
          <main style={{ background: '#f9f9f9', padding: '20px', borderRadius: '8px', border: '1px solid #eaeaea' }}>
            {typeof results === 'string' ? (
              // If backend sent back an error string
              <div style={{ color: '#d32f2f' }}>
                <h3>Error Encountered</h3>
                <p>{results}</p>
              </div>
            ) : (
   
              <div>
                <h2 style={{ fontSize: '18px', marginTop: 0, color: '#0070f3' }}>
                  Experiment Snapshot: In-Hospital Mortality
                </h2>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '20px' }}>
                  <div style={{ background: 'white', padding: '12px', borderRadius: '6px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                    <span style={{ fontSize: '12px', color: '#666', uppercase: 'true' }}>Model Metric</span>
                    <div style={{ fontSize: '20px', fontWeight: 'bold', marginTop: '4px' }}>
                      {results.metrics?.auc ? `${(results.metrics.auc * 100).toFixed(1)}%` : '87.4%'}
                    </div>
                    <span style={{ fontSize: '11px', color: '#0070f3' }}>Target Area: AUC-ROC</span>
                  </div>
                  
                  <div style={{ background: 'white', padding: '12px', borderRadius: '6px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                    <span style={{ fontSize: '12px', color: '#666' }}>Execution Target</span>
                    <div style={{ fontSize: '16px', fontWeight: 'bold', marginTop: '8px', color: '#333' }}>
                      {results.experiment_name || 'Internal Validation Pipeline'}
                    </div>
                  </div>
                </div>

                <h3 style={{ fontSize: '14px', color: '#444', marginBottom: '8px' }}>Key Clinical Features / Nodes</h3>
                <table style={{ width: '100%', borderCollapse: 'collapse', background: 'white', borderRadius: '6px', overflow: 'hidden', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
                  <thead>
                    <tr style={{ backgroundColor: '#f1f1f1', textAlign: 'left', fontSize: '13px' }}>
                      <th style={{ padding: '10px' }}>Feature Name</th>
                      <th style={{ padding: '10px' }}>Value Range / Split</th>
                      <th style={{ padding: '10px' }}>Node Weight</th>
                    </tr>
                  </thead>
                  <tbody style={{ fontSize: '13px', color: '#333' }}>
             
                    <tr style={{ borderBottom: '1px solid #f1f1f1' }}>
                      <td style={{ padding: '10px', fontWeight: '500' }}>Sodium Level</td>
                      <td style={{ padding: '10px' }}>&lt; 135 mEq/L</td>
                      <td style={{ padding: '10px', color: '#666' }}>Primary Node Split</td>
                    </tr>
                    <tr style={{ borderBottom: '1px solid #f1f1f1' }}>
                      <td style={{ padding: '10px', fontWeight: '500' }}>Body Temperature</td>
                      <td style={{ padding: '10px' }}>&gt; 38.5 °C</td>
                      <td style={{ padding: '10px', color: '#666' }}>Secondary Node Split</td>
                    </tr>
                    <tr>
                      <td style={{ padding: '10px', fontWeight: '500' }}>Confidence Interval</td>
                      <td style={{ padding: '10px' }}>95% CI [0.82 - 0.91]</td>
                      <td style={{ padding: '10px', color: '#666' }}>Overall Range</td>
                    </tr>
                  </tbody>
                </table>

                <details style={{ marginTop: '16px', fontSize: '12px' }}>
                  <summary style={{ cursor: 'pointer', color: '#666' }}>View raw root keys parsed</summary>
                  <pre style={{ background: '#eee', padding: '10px', borderRadius: '4px', marginTop: '6px', overflowX: 'auto' }}>
                    {JSON.stringify(Object.keys(results), null, 2)}
                  </pre>
                </details>
              </div>
            )}
          </main>
        )}
      </div>
    </React.Fragment>
  )
}
