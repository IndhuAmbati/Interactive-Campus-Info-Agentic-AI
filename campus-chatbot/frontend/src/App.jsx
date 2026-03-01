import React, { useEffect, useRef, useState } from 'react'

const tabs = [
  { id: 'chat', label: 'Chatbot', short: 'CB' },
  { id: 'placements', label: 'Placements', short: 'PL' },
  { id: 'hostels', label: 'Hostels', short: 'HS' },
  { id: 'departments', label: 'Departments & Faculty', short: 'DF' },
  { id: 'clubs', label: 'Clubs', short: 'CL' },
  { id: 'others', label: 'Others', short: 'OT' }
]

const quickQuestions = [
  'Where is the placement cell?',
  'Hostel timings and fee details',
  'Who is the CSE HOD?',
  'How to join coding club?'
]

const placementStats = [
  { label: 'Companies Visited', value: 'To be added' },
  { label: 'Students Placed', value: 'To be added' },
  { label: 'Highest Package', value: 'To be added' }
]

const companiesVisited = [
 /* { company: 'TCS', role: 'Software Trainee', package: 'To be added', year: '2025-26' },
  { company: 'Infosys', role: 'Systems Engineer', package: 'To be added', year: '2025-26' },
  { company: 'Accenture', role: 'Associate Engineer', package: 'To be added', year: '2025-26' },
  { company: 'Wipro', role: 'Project Engineer', package: 'To be added', year: '2025-26' }*/
]

const hostelData = [
 /* { name: 'Girls Hostel Block 1', capacity: 'To be added', fee: 'To be added', warden: 'To be added' },
  { name: 'Girls Hostel Block 2', capacity: 'To be added', fee: 'To be added', warden: 'To be added' }*/
]

const departmentData = [
  /*{
    name: 'Computer Science and Engineering',
    hod: 'To be added',
    email: 'cse@college.edu',
    faculty: ['Faculty 1', 'Faculty 2', 'Faculty 3'],
    labs: ['Programming Lab', 'AI Lab']
  },
  {
    name: 'Electronics and Communication Engineering',
    hod: 'To be added',
    email: 'ece@college.edu',
    faculty: ['Faculty 1', 'Faculty 2'],
    labs: ['VLSI Lab', 'Embedded Systems Lab']
  }*/
]

const clubData = [
  /*{ name: 'Coding Club', type: 'Technical', coordinator: 'To be added', join: 'Fill club form + attend orientation' },
  { name: 'ACM Student Chapter', type: 'Technical', coordinator: 'To be added', join: 'Contact faculty coordinator' },
  { name: 'Cultural Club', type: 'Cultural', coordinator: 'To be added', join: 'Join during club registrations' },
  { name: 'NSS', type: 'Service', coordinator: 'To be added', join: 'Apply through student activities cell' }*/
]

export default function App() {
  const [activeTab, setActiveTab] = useState('chat')
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [backendStatus, setBackendStatus] = useState('checking')
  const [collegeSites, setCollegeSites] = useState([])
  const [sitesLoading, setSitesLoading] = useState(true)
  const [sitesError, setSitesError] = useState('')
  const inputRef = useRef(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/health')
      .then((res) => res.json())
      .then(() => setBackendStatus('connected'))
      .catch(() => setBackendStatus('disconnected'))
  }, [])

  const fetchCollegeSites = async () => {
    setSitesLoading(true)
    setSitesError('')
    try {
      const res = await fetch('http://127.0.0.1:8000/api/otherwebsites')
      if (!res.ok) {
        throw new Error(`API ${res.status}`)
      }
      const data = await res.json()
      setCollegeSites((data.items || []).map((item) => ({ name: item.name, url: item.site_url })))
    } catch (err) {
      setCollegeSites([])
      setSitesError('Could not fetch websites from backend.')
    } finally {
      setSitesLoading(false)
    }
  }

  useEffect(() => {
    fetchCollegeSites()
  }, [])

  useEffect(() => {
    if (activeTab === 'others') {
      fetchCollegeSites()
    }
  }, [activeTab])

  useEffect(() => {
    if (activeTab === 'chat' && inputRef.current) {
      inputRef.current.focus()
    }
  }, [activeTab])

  const sendMessage = async () => {
    const trimmed = question.trim()
    if (!trimmed || loading) return

    const userMsg = { role: 'user', text: trimmed, ts: new Date().toLocaleTimeString() }
    setMessages((prev) => [userMsg, ...prev])
    setQuestion('')
    setLoading(true)

    try {
      const res = await fetch('http://127.0.0.1:8000/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ q: trimmed })
      })
      const data = await res.json()
      setMessages((prev) => [{ role: 'bot', text: data.answer || 'No answer returned', ts: new Date().toLocaleTimeString() }, ...prev])
    } catch {
      setMessages((prev) => [{ role: 'bot', text: 'Backend unavailable. Start backend and ingest data first.', ts: new Date().toLocaleTimeString() }, ...prev])
    } finally {
      setLoading(false)
    }
  }

  const renderChat = () => (
    <section className="panel">
      <div className="panel-header">
        <h1>Campus Info Chatbot</h1>
        <p>Ask about placements, hostels, departments, faculty, and clubs.</p>
      </div>

      <div className="quick-actions">
        {quickQuestions.map((item) => (
          <button key={item} onClick={() => setQuestion(item)}>{item}</button>
        ))}
      </div>

      <div className="chat-window">
        {messages.length === 0 && (
          <div className="empty-state">
            <h3>Chatbot ready</h3>
            <p>Your team can add project data later. UI is ready now.</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <article key={`${msg.ts}-${index}`} className={`message ${msg.role}`}>
            <p>{msg.text}</p>
            <span>{msg.ts}</span>
          </article>
        ))}

        {loading && <article className="message bot"><p>Generating answer...</p></article>}
      </div>

      <div className="chat-input">
        <input
          ref={inputRef}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type your campus question..."
        />
        <button onClick={sendMessage} disabled={!question.trim() || loading}>
          {loading ? 'Sending' : 'Send'}
        </button>
      </div>
    </section>
  )

  const renderPlacements = () => (
    <section className="panel">
      <div className="panel-header">
        <h2>Placements and Companies Visited</h2>
        <p>Snapshot section for placement outcomes and recruiter visits.</p>
      </div>

      <div className="stats-grid three">
        {placementStats.map((s) => (
          <div className="stat-card" key={s.label}>
            <strong>{s.value}</strong>
            <span>{s.label}</span>
          </div>
        ))}
      </div>

      <div className="table-wrap">
        <h3>Company Visits (Placeholder)</h3>
        <table>
          <thead>
            <tr>
              <th>Company</th>
              <th>Role</th>
              <th>Package</th>
              <th>Academic Year</th>
            </tr>
          </thead>
          <tbody>
            {companiesVisited.map((c) => (
              <tr key={`${c.company}-${c.role}`}>
                <td>{c.company}</td>
                <td>{c.role}</td>
                <td>{c.package}</td>
                <td>{c.year}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )

  const renderHostels = () => (
    <section className="panel">
      <div className="panel-header">
        <h2>Hostels</h2>
        <p>Quick hostel overview for capacity, fee, and warden details.</p>
      </div>

      <div className="cards-grid two">
        {hostelData.map((h) => (
          <article key={h.name} className="category-card">
            <header>
              <h3>{h.name}</h3>
              <span>Hostel</span>
            </header>
            <p>Capacity: {h.capacity}</p>
            <p>Fee: {h.fee}</p>
            <p>Warden: {h.warden}</p>
          </article>
        ))}
      </div>
    </section>
  )

  const renderDepartments = () => (
    <section className="panel">
      <div className="panel-header">
        <h2>Departments and Faculty</h2>
        <p>Academic departments, HOD contacts, labs, and faculty list.</p>
      </div>

      <div className="cards-grid">
        {departmentData.map((d) => (
          <article key={d.name} className="category-card">
            <header>
              <h3>{d.name}</h3>
              <span>Department</span>
            </header>
            <p>HOD: {d.hod}</p>
            <p>Email: {d.email}</p>
            <p><strong>Faculty:</strong> {d.faculty.join(', ')}</p>
            <p><strong>Labs:</strong> {d.labs.join(', ')}</p>
          </article>
        ))}
      </div>
    </section>
  )

  const renderClubs = () => (
    <section className="panel">
      <div className="panel-header">
        <h2>Clubs and Student Activities</h2>
        <p>Technical, cultural, and service club information.</p>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Club</th>
              <th>Type</th>
              <th>Coordinator</th>
              <th>How to Join</th>
            </tr>
          </thead>
          <tbody>
            {clubData.map((club) => (
              <tr key={club.name}>
                <td>{club.name}</td>
                <td>{club.type}</td>
                <td>{club.coordinator}</td>
                <td>{club.join}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )

  const renderOthers = () => (
    <section className="panel">
      <div className="panel-header">
        <h2>Other: College Sites</h2>
        <p>Quick links to official college pages.</p>
      </div>

      <div className="cards-grid">
        {sitesLoading && <p>Loading websites...</p>}
        {!sitesLoading && sitesError && <p>{sitesError}</p>}
        {!sitesLoading && collegeSites.length === 0 && <p>No websites found in database.</p>}
        {!sitesLoading && collegeSites.map((site) => (
          <article key={site.name} className="category-card site-card">
            <header>
              <h3>{site.name}</h3>
              <span>Official</span>
            </header>
            <a href={site.url} target="_blank" rel="noreferrer">
              {site.url}
            </a>
          </article>
        ))}
      </div>
    </section>
  )

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <h2>BVRIT Hyderabad Campus AI Assistant</h2>
          <p>Smart campus info hub for students, freshers, and visitors</p>
        </div>
        <div className="status-group">
          <span className="status-label">Backend</span>
          <span className={`status-dot ${backendStatus}`} />
          <span className="status-text">{backendStatus}</span>
        </div>
      </header>

      <nav className="tabs">
        {tabs.map((item) => (
          <button
            key={item.id}
            className={activeTab === item.id ? 'active' : ''}
            onClick={() => setActiveTab(item.id)}
          >
            <span className="tab-badge">{item.short}</span>
            {item.label}
          </button>
        ))}
      </nav>

      <main>
        {activeTab === 'chat' && renderChat()}
        {activeTab === 'placements' && renderPlacements()}
        {activeTab === 'hostels' && renderHostels()}
        {activeTab === 'departments' && renderDepartments()}
        {activeTab === 'clubs' && renderClubs()}
        {activeTab === 'others' && renderOthers()}
      </main>
    </div>
  )
}
