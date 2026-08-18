import { useEffect, useState } from "react"

function App() {
  const [stats, setStats] = useState({
    total: 0,
    applied: 0,
    interview: 0,
    offer: 0,
    rejected: 0,
  })
  const [editingId, setEditingId] = useState(null)
  const [applications, setApplications] = useState([])
  const [showForm, setShowForm] = useState(false)
  const handleSubmit = async () => {
    const payload = {
      ...formData,
      applied_date: formData.applied_date || null,
    }

    const url = editingId
      ? `http://127.0.0.1:8000/applications/${editingId}`
      : "http://127.0.0.1:8000/applications"

    const method = editingId ? "PUT" : "POST"

    const response = await fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      alert(editingId ? "Failed to update application" : "Failed to add application")
      return
    }

    setShowForm(false)
    setEditingId(null)

    setFormData({
      company: "",
      role: "",
      location: "",
      job_url: "",
      notes: "",
      applied_date: "",
      status: "Interested",
    })

    const applicationsResponse = await fetch(
      "http://127.0.0.1:8000/applications?skip=0&limit=20"
    )
    const applicationsData = await applicationsResponse.json()
    setApplications(applicationsData.applications)

    const statsResponse = await fetch("http://127.0.0.1:8000/stats")
    const statsData = await statsResponse.json()
    setStats(statsData)
  }
  const handleDelete = async (id) => {
    const response = await fetch(
      `http://127.0.0.1:8000/applications/${id}`,
      {
        method: "DELETE",
      }
    )

    if (!response.ok) {
      alert("Failed to delete application")
      return
    }

    const applicationsResponse = await fetch(
      "http://127.0.0.1:8000/applications?skip=0&limit=20"
    )
    const applicationsData = await applicationsResponse.json()
    setApplications(applicationsData.applications)

    const statsResponse = await fetch("http://127.0.0.1:8000/stats")
    const statsData = await statsResponse.json()
    setStats(statsData)
  }
  const handleEdit = (application) => {
    setEditingId(application.id)

    setFormData({
      company: application.company,
      role: application.role,
      location: application.location,
      job_url: application.job_url,
      notes: application.notes,
      applied_date: application.applied_date || "",
      status: application.status,
    })

    setShowForm(true)
  }
  const [formData, setFormData] = useState({
    company: "",
    role: "",
    location: "",
    job_url: "",
    notes: "",
    applied_date: "",
    status: "Interested",
  })

  useEffect(() => {
    fetch("http://127.0.0.1:8000/stats")
      .then((response) => response.json())
      .then((data) => setStats(data))

    fetch("http://127.0.0.1:8000/applications?skip=0&limit=20")
      .then((response) => response.json())
      .then((data) => setApplications(data.applications))
  }, [])

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>CareerFlow</h1>
          <p>Job Application Tracker</p>
        </div>

        <button
          className="add-button"
          onClick={() => setShowForm(true)}
        >
          + Add Application
        </button>
      </header>
      {showForm && (
        <div className="form-overlay">
          <div className="application-form">
            <h2>{editingId ? "Edit Application" : "Add Application"}</h2>

            <input
              type="text"
              placeholder="Company"
              value={formData.company}
              onChange={(e) =>
                setFormData({ ...formData, company: e.target.value })
              }
            />

            <input
              type="text"
              placeholder="Role"
              value={formData.role}
              onChange={(e) =>
                setFormData({ ...formData, role: e.target.value })
              }
            />

            <input
              type="text"
              placeholder="Location"
              value={formData.location}
              onChange={(e) =>
                setFormData({ ...formData, location: e.target.value })
              }
            />

            <input
              type="text"
              placeholder="Job URL"
              value={formData.job_url}
              onChange={(e) =>
                setFormData({ ...formData, job_url: e.target.value })
              }
            />

            <textarea
              placeholder="Notes"
              value={formData.notes}
              onChange={(e) =>
                setFormData({ ...formData, notes: e.target.value })
              }
            />

            <input
              type="date"
              value={formData.applied_date}
              onChange={(e) =>
                setFormData({ ...formData, applied_date: e.target.value })
              }
            />

            <select
              value={formData.status}
              onChange={(e) =>
                setFormData({ ...formData, status: e.target.value })
              }
            >
              <option>Interested</option>
              <option>Applied</option>
              <option>Assessment</option>
              <option>Interview</option>
              <option>Offer</option>
              <option>Rejected</option>
            </select>

            <div className="form-actions">
              <button
                onClick={() => {
                  setShowForm(false)
                  setEditingId(null)
                }}
              >
                Cancel
              </button>

              <button onClick={handleSubmit}>
                {editingId ? "Update" : "Save"}
              </button>
            </div>
          </div>
        </div>
      )}

      <main className="dashboard">
        <section className="stats-grid">
          <div className="stat-card">
            <h3>Total Applications</h3>
            <p>{stats.total}</p>
          </div>

          <div className="stat-card">
            <h3>Applied</h3>
            <p>{stats.applied}</p>
          </div>

          <div className="stat-card">
            <h3>Interviews</h3>
            <p>{stats.interview}</p>
          </div>

          <div className="stat-card">
            <h3>Offers</h3>
            <p>{stats.offer}</p>
          </div>
        </section>

        <section className="applications-section">
          <h2>Applications</h2>

          {applications.map((application) => (
            <div className="application-card" key={application.id}>
              <div>
                <h3>{application.role}</h3>
                <p>{application.company}</p>
                <p>{application.location}</p>
              </div>

              <div className="application-actions">
                <span>{application.status}</span>

                <button
                  className="edit-button"
                  onClick={() => handleEdit(application)}
                >
                  Edit
                </button>

                <button
                  className="delete-button"
                  onClick={() => handleDelete(application.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </section>
      </main>
    </div>
  )
}

export default App