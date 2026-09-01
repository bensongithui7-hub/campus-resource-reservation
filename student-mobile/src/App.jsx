import { useEffect, useState } from "react";
import "./App.css";

import {
  loginStudent,
  registerStudent,
  saveStudentSession,
  getStudent,
  logoutStudent,
} from "./services/auth";

import { getResources } from "./services/resources";

import {
  createReservation,
  getReservations,
  cancelReservation,
} from "./services/reservations";

import {
  generateCheckIn,
  getCheckIn,
  performCheckIn,
} from "./services/checkin";


function formatResourceType(type) {
  return type
    .replace(/_/g, " ")
    .toLowerCase()
    .replace(/\b\w/g, (char) => char.toUpperCase());
}


function App() {
  const [user, setUser] = useState(getStudent());
  const [page, setPage] = useState("dashboard");

  if (!user) {
    return (
      <AuthScreen
        onLogin={(data) => {
          saveStudentSession(data);
          setUser(data.user);
        }}
      />
    );
  }

  return (
    <StudentApp
      user={user}
      page={page}
      setPage={setPage}
      onLogout={() => {
        logoutStudent();
        setUser(null);
      }}
    />
  );
}


function AuthScreen({ onLogin }) {
  const [mode, setMode] = useState("login");

  const [name, setName] = useState("");
  const [studentId, setStudentId] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function submit(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setMessage("");

    try {
      if (mode === "login") {
        const response = await loginStudent(email, password);

        onLogin(response);
      } else {
        const response = await registerStudent(
          name,
          studentId,
          email,
          password
        );

        setMessage(response.message || "Registration successful.");

        setMode("login");
        setPassword("");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-page">
      <div className="auth-card">
        <div className="brand-mark">CR</div>

        <h1>Campus Resource Reservation</h1>

        <p className="subtitle">
          {mode === "login"
            ? "Sign in to manage your campus reservations."
            : "Create your student account."}
        </p>

        {error && <div className="alert error">{error}</div>}
        {message && <div className="alert success">{message}</div>}

        <form onSubmit={submit}>
          {mode === "register" && (
            <>
              <label>
                Full Name
                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Enter your full name"
                  required
                />
              </label>

              <label>
                Student ID
                <input
                  value={studentId}
                  onChange={(e) => setStudentId(e.target.value)}
                  placeholder="Enter your student ID"
                />
              </label>
            </>
          )}

          <label>
            Email
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
            />
          </label>

          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </label>

          <button className="primary-button" disabled={loading}>
            {loading
              ? "Please wait..."
              : mode === "login"
                ? "Sign In"
                : "Create Account"}
          </button>
        </form>

        <button
          className="link-button"
          onClick={() => {
            setMode(mode === "login" ? "register" : "login");
            setError("");
            setMessage("");
          }}
        >
          {mode === "login"
            ? "Don't have an account? Register"
            : "Already have an account? Sign in"}
        </button>
      </div>
    </main>
  );
}


function StudentApp({ user, page, setPage, onLogout }) {
  return (
    <div className="student-app">
      <header className="topbar">
        <div>
          <strong>Campus Resources</strong>
          <span>Student Portal</span>
        </div>

        <div className="user-area">
          <span>{user.name}</span>

          <button onClick={onLogout}>
            Logout
          </button>
        </div>
      </header>

      <nav className="navigation">
        <button
          className={page === "dashboard" ? "active" : ""}
          onClick={() => setPage("dashboard")}
        >
          Dashboard
        </button>

        <button
          className={page === "resources" ? "active" : ""}
          onClick={() => setPage("resources")}
        >
          Resources
        </button>

        <button
          className={page === "reservations" ? "active" : ""}
          onClick={() => setPage("reservations")}
        >
          My Reservations
        </button>
      </nav>

      <main className="content">
        {page === "dashboard" && (
          <Dashboard user={user} setPage={setPage} />
        )}

        {page === "resources" && (
          <Resources />
        )}

        {page === "reservations" && (
          <Reservations />
        )}
      </main>
    </div>
  );
}


function Dashboard({ user, setPage }) {
  return (
    <section>
      <div className="welcome-card">
        <p>Welcome back</p>
        <h1>{user.name}</h1>
        <p>
          Find a campus resource, make a reservation,
          and manage your check-ins.
        </p>

        <button
          className="primary-button"
          onClick={() => setPage("resources")}
        >
          Browse Resources
        </button>
      </div>

      <div className="dashboard-cards">
        <div className="info-card">
          <span className="card-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/></svg></span>
          <h3>Resources</h3>
          <p>
            Browse laboratories, study rooms and equipment.
          </p>
        </div>

        <div className="info-card">
          <span className="card-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/><path d="M8 14h3M13 14h3M8 17h3"/></svg></span>
          <h3>Reservations</h3>
          <p>
            View and manage your existing reservations.
          </p>
        </div>

        <div className="info-card">
          <span className="card-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h3M8 15h8"/><path d="M15 11h1"/></svg></span>
          <h3>Check-in</h3>
          <p>
            Generate your check-in token for confirmed reservations.
          </p>
        </div>
      </div>
    </section>
  );
}


function Resources() {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [selectedResource, setSelectedResource] = useState(null);
  const [detailsResource, setDetailsResource] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await getResources();
        setResources(data.resources || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  if (loading) {
    return <div className="loading">Loading resources...</div>;
  }

  if (error) {
    return <div className="alert error">{error}</div>;
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h1>Campus Resources</h1>
          <p>Available resources for student reservations.</p>
        </div>
      </div>

      {resources.length === 0 ? (
        <div className="empty-state">
          <h2>No resources available</h2>
          <p>
            There are currently no campus resources registered.
          </p>
        </div>
      ) : (
        <div className="resource-grid">
          {resources.map((resource) => (
            <article className="resource-card" key={resource.id}>
              <div className="resource-header">
                <span>{formatResourceType(resource.type)}</span>

                <span
                  className={
                    resource.status === "AVAILABLE"
                      ? "status available"
                      : "status unavailable"
                  }
                >
                  {resource.status}
                </span>
              </div>

              <h2>{resource.name}</h2>

              <p>
                {resource.description ||
                  "No description provided."}
              </p>

              <div className="resource-details">
                <span>Location: {resource.location}</span>
                <span>Capacity: {resource.capacity}</span>
              </div>

              <div className="resource-actions">
                <button
                  className="secondary-button"
                  onClick={() => setDetailsResource(resource)}
                >
                  View Details
                </button>

                <button
                  className="primary-button"
                  disabled={resource.status !== "AVAILABLE"}
                  onClick={() => setSelectedResource(resource)}
                >
                  {resource.status === "AVAILABLE"
                    ? "Reserve"
                    : "Unavailable"}
                </button>
              </div>
            </article>
          ))}
        </div>
      )}

      {selectedResource && (
        <ReservationModal
          resource={selectedResource}
          onClose={() => setSelectedResource(null)}
        />
      )}

      {detailsResource && (
        <ResourceDetailsModal
          resource={detailsResource}
          onClose={() => setDetailsResource(null)}
        />
      )}
    </section>
  );
}


function ResourceDetailsModal({ resource, onClose }) {
  return (
    <div className="modal-backdrop">
      <div className="modal">
        <button className="close-button" onClick={onClose}>
          &times;
        </button>

        <h2>{resource.name}</h2>

        <p>
          <strong>Type:</strong> {formatResourceType(resource.type)}
        </p>

        <p>
          <strong>Description:</strong>{" "}
          {resource.description || "No description provided."}
        </p>

        <p>
          <strong>Location:</strong> {resource.location}
        </p>

        <p>
          <strong>Capacity:</strong> {resource.capacity}
        </p>

        <p>
          <strong>Status:</strong> {resource.status}
        </p>
      </div>
    </div>
  );
}

function ReservationModal({ resource, onClose }) {
  const [date, setDate] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [purpose, setPurpose] = useState("");

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setMessage("");

    try {
      const response = await createReservation({
        resource_id: resource.id,
        reservation_date: date,
        start_time: startTime,
        end_time: endTime,
        purpose,
      });

      setMessage(response.message);

      setTimeout(() => {
        onClose();
      }, 1200);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <button className="close-button" onClick={onClose}>
          &times;
        </button>

        <div className="modal-body">
          <h2>Reserve {resource.name}</h2>

          <p>
            Location: {resource.location}
          </p>

          {error && <div className="alert error">{error}</div>}
          {message && <div className="alert success">{message}</div>}

          <form id="reservation-form" onSubmit={submit}>
            <label>
              Reservation Date
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
              />
            </label>

            <label>
              Start Time
              <input
                type="time"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                required
              />
            </label>

            <label>
              End Time
              <input
                type="time"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
                required
              />
            </label>

            <label>
              Purpose
              <textarea
                value={purpose}
                onChange={(e) => setPurpose(e.target.value)}
                placeholder="Why do you need this resource?"
              />
            </label>
          </form>
        </div>

        <div className="modal-footer">
          <button
            className="primary-button"
            type="submit"
            form="reservation-form"
            disabled={loading}
          >
            {loading ? "Creating..." : "Confirm Reservation"}
          </button>
        </div>
      </div>
    </div>
  );
}


function Reservations() {
  const [reservations, setReservations] = useState([]);
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [checkIn, setCheckIn] = useState(null);

  async function loadReservations() {
    try {
      setLoading(true);

      const [reservationData, resourceData] = await Promise.all([
        getReservations(),
        getResources(),
      ]);

      setReservations(reservationData.reservations || []);
      setResources(resourceData.resources || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function loadInitialReservations() {
      try {
        const [reservationData, resourceData] = await Promise.all([
          getReservations(),
          getResources(),
        ]);

        if (!cancelled) {
          setReservations(reservationData.reservations || []);
          setResources(resourceData.resources || []);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadInitialReservations();

    return () => {
      cancelled = true;
    };
  }, []);

  async function cancel(id) {
    if (!window.confirm("Cancel this reservation?")) {
      return;
    }

    try {
      await cancelReservation(id);
      await loadReservations();
    } catch (err) {
      setError(err.message);
    }
  }

  async function showCheckIn(id) {
    try {
      const data = await getCheckIn(id);
      setCheckIn(data.check_in);
    } catch {
      try {
        const data = await generateCheckIn(id);
        setCheckIn(data.check_in);
      } catch (err) {
        setError(err.message);
      }
    }
  }

  async function completeCheckIn() {
    try {
      const data = await performCheckIn(checkIn.qr_token);
      setCheckIn(data.check_in);
      await loadReservations();
    } catch (err) {
      setError(err.message);
    }
  }

  if (loading) {
    return <div className="loading">Loading reservations...</div>;
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h1>My Reservations</h1>
          <p>Manage your campus resource reservations.</p>
        </div>
      </div>

      {error && <div className="alert error">{error}</div>}

      {reservations.length === 0 ? (
        <div className="empty-state">
          <h2>No reservations yet</h2>
          <p>
            Your confirmed and previous reservations will appear here.
          </p>
        </div>
      ) : (
        <div className="reservation-list">
          {reservations.map((reservation) => {
            const resource = resources.find(
              (item) => item.id === reservation.resource_id
            );

            return (
            <article
              className="reservation-card"
              key={reservation.id}
            >
              <div>
                <h2>
                  Reservation #{reservation.id}
                </h2>

                <p>
                  Resource: {resource ? resource.name : `Resource #${reservation.resource_id}`}
                </p>

                <p>
                  Date: {reservation.reservation_date}
                </p>

                <p>
                  Time: {reservation.start_time} -{" "}
                  {reservation.end_time}
                </p>

                {reservation.purpose && (
                  <p>Purpose: {reservation.purpose.replace(/^Purpose:\s*/i, "")}</p>
                )}
              </div>

              <div className="reservation-actions">
                <span className="status">
                  {reservation.status}
                </span>

                {reservation.status === "CONFIRMED" && (
                  <>
                    <button
                      className="secondary-button"
                      onClick={() =>
                        showCheckIn(reservation.id)
                      }
                    >
                      Check-in
                    </button>

                    <button
                      className="danger-button"
                      onClick={() =>
                        cancel(reservation.id)
                      }
                    >
                      Cancel
                    </button>
                  </>
                )}
              </div>
            </article>
            );
          })}
        </div>
      )}

      {checkIn && (
        <div className="checkin-panel">
          <button
            className="close-button"
            onClick={() => setCheckIn(null)}
          >
            &times;
          </button>

          <h2>Check-in Token</h2>

          <p>
            Present this token when checking in.
          </p>

          <div className="qr-token">
            {checkIn.qr_token}
          </div>

          <strong>
            Status: {checkIn.status}
          </strong>

          {checkIn.status === "NOT_CHECKED_IN" && (
            <button
              className="primary-button"
              onClick={completeCheckIn}
            >
              Complete Check-in
            </button>
          )}
        </div>
      )}
    </section>
  );
}


export default App;








