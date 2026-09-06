import { apiRequest } from "./services/api";
import { useEffect, useState } from "react";
import "./App.css";
import {
  adminLogin,
  adminLogout,
  isAdminLoggedIn,
} from "./services/auth";
import {
  getResources,
  getAdminReservations,
  updateReservationStatus,
  getAdminCheckIns,
  getAdminUsers,
  updateResource,
  deleteResource,
  updateResourceStatus,
} from "./services/admin";

function LoginScreen({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await adminLogin(email, password);
      onLogin(data.user);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="brand-icon">CR</div>
        <h1>CampusReserve</h1>
        <p>Administrator Portal</p>

        <form onSubmit={handleSubmit}>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="Enter administrator email"
            required
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Enter administrator password"
            required
          />

          {error && <div className="login-error">{error}</div>}

          <button type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
}

function AdminDashboard({ user, onLogout }) {
  const [activePage, setActivePage] = useState("Dashboard");

  const [resources, setResources] = useState([]);
  const [resourcesLoading, setResourcesLoading] = useState(false);
  const [resourcesError, setResourcesError] = useState("");
  const [resourceModalOpen, setResourceModalOpen] = useState(false);
  const [editingResource, setEditingResource] = useState(null);
  const [resourceSaving, setResourceSaving] = useState(false);
  const [resourceFormError, setResourceFormError] = useState("");

  const [reservations, setReservations] = useState([]);
  const [reservationsLoading, setReservationsLoading] = useState(false);
  const [reservationsError, setReservationsError] = useState("");
  const [updatingReservationId, setUpdatingReservationId] = useState(null);

  const [checkIns, setCheckIns] = useState([]);
  const [checkInsLoading, setCheckInsLoading] = useState(false);
  const [checkInsError, setCheckInsError] = useState("");

  const [users, setUsers] = useState([]);
  const [usersLoading, setUsersLoading] = useState(false);
  const [usersError, setUsersError] = useState("");

  const menuItems = [
    "Dashboard",
    "Reservations",
    "Resources",
    "Check-ins",
    "Users",
  ];

  useEffect(() => {
    if (activePage !== "Resources") {
      return;
    }

    async function loadResources() {
      setResourcesLoading(true);
      setResourcesError("");

      try {
        const data = await getResources();
        setResources(data.resources || []);
      } catch (err) {
        setResourcesError(err.message);
      } finally {
        setResourcesLoading(false);
      }
    }

    loadResources();
  }, [activePage]);

  async function handleDeleteResource(resourceId) {
    if (!window.confirm("Delete this resource? This action cannot be undone.")) {
      return;
    }

    try {
      await deleteResource(resourceId);
      setResources((current) =>
        current.filter((resource) => resource.id !== resourceId)
      );
    } catch (err) {
      setResourcesError(err.message);
    }
  }

  async function handleToggleResourceStatus(resource) {
    const nextStatus =
      resource.status === "AVAILABLE" ? "UNAVAILABLE" : "AVAILABLE";

    try {
      await updateResourceStatus(resource.id, nextStatus);
      setResources((current) =>
        current.map((item) =>
          item.id === resource.id
            ? { ...item, status: nextStatus }
            : item
        )
      );
    } catch (err) {
      setResourcesError(err.message);
    }
  }

  function openCreateResourceModal() {
    setEditingResource(null);
    setResourceFormError("");
    setResourceModalOpen(true);
  }

  function openEditResourceModal(resource) {
    setEditingResource(resource);
    setResourceFormError("");
    setResourceModalOpen(true);
  }

  async function handleResourceSubmit(event) {
    event.preventDefault();
    setResourceFormError("");
    setResourceSaving(true);

    const formData = new FormData(event.currentTarget);

    const updates = {
      name: formData.get("name")?.trim(),
      type: formData.get("type"),
      description: formData.get("description")?.trim(),
      location: formData.get("location")?.trim(),
      capacity: Number(formData.get("capacity")),
    };

    if (
      !updates.name ||
      !updates.type ||
      !updates.location ||
      !Number.isInteger(updates.capacity) ||
      updates.capacity < 1
    ) {
      setResourceFormError(
        "Name, type, location and a positive capacity are required."
      );
      setResourceSaving(false);
      return;
    }

    try {
      if (editingResource) {
        const data = await updateResource(editingResource.id, updates);

        setResources((current) =>
          current.map((resource) =>
            resource.id === editingResource.id
              ? data.resource
              : resource
          )
        );
      } else {
        const data = await apiRequest("/resources", {
          method: "POST",
          body: JSON.stringify(updates),
        });

        setResources((current) => [...current, data.resource]);
      }

      closeResourceModal();
    } catch (err) {
      setResourceFormError(err.message);
    } finally {
      setResourceSaving(false);
    }
  }
  function closeResourceModal() {
    if (resourceSaving) {
      return;
    }

    setResourceModalOpen(false);
    setEditingResource(null);
    setResourceFormError("");
  }
  useEffect(() => {
    if (activePage !== "Reservations") {
      return;
    }

    async function loadReservations() {
      setReservationsLoading(true);
      setReservationsError("");

      try {
        const data = await getAdminReservations();
        setReservations(data.reservations || []);
      } catch (err) {
        setReservationsError(err.message);
      } finally {
        setReservationsLoading(false);
      }
    }

    loadReservations();
  }, [activePage]);

  useEffect(() => {
    if (activePage !== "Check-ins") {
      return;
    }

    async function loadCheckIns() {
      setCheckInsLoading(true);
      setCheckInsError("");

      try {
        const data = await getAdminCheckIns();
        setCheckIns(data.check_ins || []);
      } catch (err) {
        setCheckInsError(err.message);
      } finally {
        setCheckInsLoading(false);
      }
    }

    loadCheckIns();
  }, [activePage]);

  useEffect(() => {
    if (activePage !== "Users") {
      return;
    }

    async function loadUsers() {
      setUsersLoading(true);
      setUsersError("");

      try {
        const data = await getAdminUsers();
        setUsers(data.users || []);
      } catch (err) {
        setUsersError(err.message);
      } finally {
        setUsersLoading(false);
      }
    }

    loadUsers();
  }, [activePage]);

  return (
    <div className="admin-app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon" aria-label="CampusReserve logo"><svg viewBox="0 0 48 48" aria-hidden="true"><rect x="8" y="8" width="32" height="32" rx="10" fill="none" stroke="currentColor" strokeWidth="3"/><path d="M18 30V18h7.5a6 6 0 0 1 0 12H18Zm0-7h7a2.5 2.5 0 0 0 0-5h-7v5Z" fill="currentColor"/><path d="M30 18h-2.5l-4 6 4 6H30l-4-6 4-6Z" fill="currentColor"/></svg></div>
          <div>
            <h2>CampusReserve</h2>
            <span>Admin Portal</span>
          </div>
        </div>

        <nav className="navigation">
          {menuItems.map((item) => (
            <button
              key={item}
              className={
                activePage === item ? "nav-item active" : "nav-item"
              }
              onClick={() => setActivePage(item)}
            >
              <span></span>
              {item}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="admin-avatar">
            {user?.name?.slice(0, 2).toUpperCase() || "SA"}
          </div>
          <div>
            <strong>{user?.name || "System Admin"}</strong>
            <small>Administrator</small>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <h1>{activePage}</h1>
            <p>Campus Resource Reservation System</p>
          </div>

          <div className="topbar-actions">
            <button className="notification" type="button">
              Notifications
            </button>

            <button className="logout" type="button" onClick={onLogout}>
              Logout
            </button>
          </div>
        </header>

        {activePage === "Dashboard" && (
          <>
            <section className="welcome-card">
              <div>
                <span className="eyebrow">ADMINISTRATOR</span>
                <h2>Welcome back, {user?.name || "System Admin"}</h2>
                <p>
                  Manage campus resources, reservations, users and check-ins
                  from one place.
                </p>
              </div>

              <div className="welcome-icon" aria-hidden="true"></div>
            </section>

            <section className="stats-grid">
              <div className="stat-card">
                <span>Total Resources</span>
                <strong>5</strong>
                <small>Available campus resources</small>
              </div>

              <div className="stat-card">
                <span>Total Reservations</span>
                <strong>2</strong>
                <small>Reservations in the system</small>
              </div>

              <div className="stat-card">
                <span>Active Check-ins</span>
                <strong>1</strong>
                <small>Currently checked in</small>
              </div>

              <div className="stat-card">
                <span>Registered Users</span>
                <strong>2</strong>
                <small>Students and administrators</small>
              </div>
            </section>

            <section className="dashboard-grid">
              <div className="panel">
                <div className="panel-header">
                  <div>
                    <h3>Recent Reservations</h3>
                    <p>Latest reservation activity</p>
                  </div>

                  <button
                    className="btn-secondary"
                    type="button"
                    onClick={() => setActivePage("Reservations")}
                  >
                    View all
                  </button>
                </div>

                <div className="reservation-row">
                  <div className="reservation-icon">CR</div>
                  <div>
                    <strong>Computer Lab 1</strong>
                    <span>Test Student - Sep 2, 2026</span>
                  </div>
                  <span className="status confirmed">CONFIRMED</span>
                </div>

                <div className="reservation-row">
                  <div className="reservation-icon">CR</div>
                  <div>
                    <strong>Computer Lab 1</strong>
                    <span>Test Student - Sep 1, 2026</span>
                  </div>
                  <span className="status cancelled">CANCELLED</span>
                </div>
              </div>

              <div className="panel">
                <div className="panel-header">
                  <div>
                    <h3>System Overview</h3>
                    <p>Current system status</p>
                  </div>
                </div>

                <div className="overview-item">
                  <span>API Status</span>
                  <strong className="online">Online</strong>
                </div>

                <div className="overview-item">
                  <span>Database</span>
                  <strong className="online">Connected</strong>
                </div>

                <div className="overview-item">
                  <span>Check-in System</span>
                  <strong className="online">Active</strong>
                </div>
              </div>
            </section>
          </>
        )}

        {activePage === "Resources" && (
          <section className="resources-page">
            <div className="page-section-header">
              <div>
                <h2>Campus Resources</h2>
                <p>Manage resources available for student reservations.</p>
              </div>

              <button
                className="primary-button"
                onClick={openCreateResourceModal}
              >
                Add Resource
              </button>
            </div>

            {resourcesLoading && (
              <div className="placeholder-panel">
                <div className="placeholder-icon">CR</div>
                <h2>Loading resources...</h2>
                <p>Please wait while resources are retrieved.</p>
              </div>
            )}

            {resourcesError && (
              <div className="login-error">{resourcesError}</div>
            )}

            {!resourcesLoading && !resourcesError && (
              <div className="resource-list">
                {resources.length === 0 ? (
                  <div className="placeholder-panel">
                    <div className="placeholder-icon">CR</div>
                    <h2>No resources found</h2>
                    <p>No campus resources are currently registered.</p>
                  </div>
                ) : (
                  resources.map((resource) => (
                    <div className="resource-card" key={resource.id}>
                      <div>
                        <span className="eyebrow">{resource.type}</span>
                        <h3>{resource.name}</h3>
                        <p>
                          {resource.description ||
                            "No description provided."}
                        </p>
                        <small>
                          Location: {resource.location} Capacity:{" "}
                          {resource.capacity}
                        </small>
                      </div>

                      <div className="resource-actions">
                        <span
                          className={
                            resource.status === "AVAILABLE"
                              ? "status confirmed"
                              : "status cancelled"
                          }
                        >
                          {resource.status}
                        </span>

                        <button
                          type="button"
                          onClick={() => openEditResourceModal(resource)}
                        >
                          Edit
                        </button>

                        <button
                          type="button"
                          onClick={() => handleToggleResourceStatus(resource)}
                        >
                          {resource.status === "AVAILABLE" ? "Disable" : "Enable"}
                        </button>

                        <button
                          type="button"
                          onClick={() => handleDeleteResource(resource.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </section>
        )}

        {activePage === "Reservations" && (
          <section className="resources-page">
            <div className="page-section-header">
              <div>
                <h2>Reservations</h2>
                <p>Review and manage student reservations.</p>
              </div>
            </div>

            {reservationsLoading && (
              <div className="placeholder-panel">
                <div className="placeholder-icon">CR</div>
                <h2>Loading reservations...</h2>
                <p>Please wait while reservations are retrieved.</p>
              </div>
            )}

            {reservationsError && (
              <div className="login-error">{reservationsError}</div>
            )}

            {!reservationsLoading && !reservationsError && (
              <div className="resource-list">
                {reservations.length === 0 ? (
                  <div className="placeholder-panel">
                    <div className="placeholder-icon">CR</div>
                    <h2>No reservations found</h2>
                    <p>
                      There are currently no reservations in the system.
                    </p>
                  </div>
                ) : (
                  reservations.map((reservation) => (
                    <div className="resource-card" key={reservation.id}>
                      <div>
                        <span className="eyebrow">
                          RESERVATION #{reservation.id}
                        </span>

                        <h3>
                          {reservation.resource_name || `Resource #${reservation.resource_id}`}
                        </h3>

                        <p>
                          User #{reservation.user_id}
                          {reservation.purpose
                            ? ` ${reservation.purpose}`
                            : ""}
                        </p>

                        <small>
                          Date: {reservation.reservation_date} Time:{" "}
                          {reservation.start_time} - {reservation.end_time}
                        </small>
                      </div>

                      <div className="reservation-actions">
                        <span
                          className={
                            reservation.status === "CONFIRMED"
                              ? "status confirmed"
                              : reservation.status === "CANCELLED"
                              ? "status cancelled"
                              : "status"
                          }
                        >
                          {reservation.status}
                        </span>

                        {reservation.status === "PENDING" && (
                          <button
                            type="button"
                            disabled={
                              updatingReservationId === reservation.id
                            }
                            onClick={async () => {
                              setUpdatingReservationId(reservation.id);

                              try {
                                await updateReservationStatus(
                                  reservation.id,
                                  "CONFIRMED"
                                );

                                setReservations((current) =>
                                  current.map((item) =>
                                    item.id === reservation.id
                                      ? {
                                          ...item,
                                          status: "CONFIRMED",
                                        }
                                      : item
                                  )
                                );
                              } catch (err) {
                                setReservationsError(err.message);
                              } finally {
                                setUpdatingReservationId(null);
                              }
                            }}
                          >
                            {updatingReservationId === reservation.id
                              ? "Updating..."
                              : "Confirm"}
                          </button>
                        )}

                        {(reservation.status === "PENDING" ||
                          reservation.status === "CONFIRMED") && (
                          <button
                            className="reservation-cancel"
                            type="button"
                            disabled={
                              updatingReservationId === reservation.id
                            }
                            onClick={async () => {
                              setUpdatingReservationId(reservation.id);

                              try {
                                await updateReservationStatus(
                                  reservation.id,
                                  "CANCELLED"
                                );

                                setReservations((current) =>
                                  current.map((item) =>
                                    item.id === reservation.id
                                      ? {
                                          ...item,
                                          status: "CANCELLED",
                                        }
                                      : item
                                  )
                                );
                              } catch (err) {
                                setReservationsError(err.message);
                              } finally {
                                setUpdatingReservationId(null);
                              }
                            }}
                          >
                            {updatingReservationId === reservation.id
                              ? "Updating..."
                              : "Cancel"}
                          </button>
                        )}
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </section>
        )}

        {activePage === "Check-ins" && (
          <section className="resources-page">
            <div className="page-section-header">
              <div>
                <h2>Check-ins</h2>
                <p>Monitor student reservation check-ins.</p>
              </div>
            </div>

            {checkInsLoading && (
              <div className="placeholder-panel">
                <div className="placeholder-icon">CR</div>
                <h2>Loading check-ins...</h2>
                <p>Please wait while check-in records are retrieved.</p>
              </div>
            )}

            {checkInsError && (
              <div className="login-error">{checkInsError}</div>
            )}

            {!checkInsLoading && !checkInsError && (
              <div className="resource-list">
                {checkIns.length === 0 ? (
                  <div className="placeholder-panel">
                    <div className="placeholder-icon">CR</div>
                    <h2>No check-ins found</h2>
                    <p>
                      There are currently no check-in records in the system.
                    </p>
                  </div>
                ) : (
                  checkIns.map((checkIn) => (
                    <div className="resource-card" key={checkIn.id}>
                      <div>
                        <span className="eyebrow">
                          CHECK-IN #{checkIn.id}
                        </span>

                        <h3>Reservation #{checkIn.reservation_id}</h3>

                        <p>QR Token: {checkIn.qr_token}</p>

                        <small>
                          Checked in:{" "}
                          {checkIn.checked_in_at
                            ? new Date(
                                checkIn.checked_in_at
                              ).toLocaleString()
                            : "Not checked in"}
                        </small>
                      </div>

                      <div>
                        <span
                          className={
                            checkIn.status === "CHECKED_IN"
                              ? "status confirmed"
                              : "status cancelled"
                          }
                        >
                          {checkIn.status}
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </section>
        )}

        {activePage === "Users" && (
          <section className="resources-page">
            <div className="page-section-header">
              <div>
                <h2>Users</h2>
                <p>Manage registered students and administrators.</p>
              </div>
            </div>

            {usersLoading && (
              <div className="placeholder-panel">
                <div className="placeholder-icon">CR</div>
                <h2>Loading users...</h2>
                <p>Please wait while users are retrieved.</p>
              </div>
            )}

            {usersError && (
              <div className="login-error">{usersError}</div>
            )}

            {!usersLoading && !usersError && (
              <div className="resource-list">
                {users.length === 0 ? (
                  <div className="placeholder-panel">
                    <div className="placeholder-icon">CR</div>
                    <h2>No users found</h2>
                    <p>
                      There are currently no registered users in the system.
                    </p>
                  </div>
                ) : (
                  users.map((account) => (
                    <div className="resource-card" key={account.id}>
                      <div>
                        <span className="eyebrow">
                          USER #{account.id}
                        </span>

                        <h3>{account.name}</h3>

                        <p>{account.email}</p>

                        <small>
                          Student ID:{" "}
                          {account.student_id || "Not assigned"}{" "}
                          Role: {account.role}
                        </small>
                      </div>

                      <div>
                        <span
                          className={
                            account.role === "ADMIN"
                              ? "status confirmed"
                              : "status"
                          }
                        >
                          {account.role}
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </section>
        )}
      {resourceModalOpen && (
        <div className="modal-overlay" onClick={closeResourceModal}>
          <div className="modal-card" onClick={(event) => event.stopPropagation()}>
            <div className="modal-header">
              <div>
                <span className="eyebrow">RESOURCE MANAGEMENT</span>
                <h2>{editingResource ? "Edit Resource" : "Add Resource"}</h2>
                <p>
                  {editingResource
                    ? "Update the details of this campus resource."
                    : "Register a new resource for student reservations."}
                </p>
              </div>

              <button
                className="modal-close"
                type="button"
                onClick={closeResourceModal}
                disabled={resourceSaving}
                aria-label="Close modal"
                title="Close"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path
                    d="M6 6l12 12M18 6L6 18"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                  />
                </svg>
              </button>
            </div>

            <form onSubmit={handleResourceSubmit}>
              <div className="modal-body">
                {resourceFormError && (
                <div className="login-error">{resourceFormError}</div>
              )}

              <label>
                Name
                <input
                  name="name"
                  type="text"
                  defaultValue={editingResource?.name || ""}
                  placeholder="e.g. Computer Lab 3"
                  required
                />
              </label>

              <label>
                Type
                <select name="type" defaultValue={editingResource?.type || ""} required>
                  <option value="">Select resource type</option>
                  <option value="LABORATORY">Lab</option>
                  <option value="STUDY_ROOM">Room</option>
                  <option value="EQUIPMENT">Equipment</option>
                </select>
              </label>

              <label>
                Description
                <textarea
                  name="description"
                  defaultValue={editingResource?.description || ""}
                  placeholder="Describe this resource"
                  rows="3"
                />
              </label>

              <div className="modal-grid-row">
                <label>
                  Location
                  <input
                    name="location"
                    type="text"
                    defaultValue={editingResource?.location || ""}
                    placeholder="e.g. Main Campus Block A"
                    required
                  />
                </label>

                <label>
                  Capacity
                  <input
                    name="capacity"
                    type="number"
                    min="1"
                    step="1"
                    defaultValue={editingResource?.capacity || ""}
                    required
                  />
                </label>
              </div>
              </div>

              <div className="modal-actions modal-footer">
                <button
                  className="btn-cancel"
                  type="button"
                  onClick={closeResourceModal}
                  disabled={resourceSaving}
                >
                  Cancel
                </button>
                <button className="btn-primary" type="submit" disabled={resourceSaving}>
                  {resourceSaving
                    ? "Saving..."
                    : editingResource
                    ? "Save Changes"
                    : "Create Resource"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      </main>
    </div>
  );
}

function App() {
  const [loggedIn, setLoggedIn] = useState(isAdminLoggedIn());

  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("adminUser");

    try {
      return savedUser ? JSON.parse(savedUser) : null;
    } catch {
      return null;
    }
  });

  function handleLogin(loggedInUser) {
    localStorage.setItem("adminUser", JSON.stringify(loggedInUser));
    setUser(loggedInUser);
    setLoggedIn(true);
  }

  function handleLogout() {
    adminLogout();
    localStorage.removeItem("adminUser");
    setUser(null);
    setLoggedIn(false);
  }

  if (!loggedIn) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  return <AdminDashboard user={user} onLogout={handleLogout} />;
}

export default App;
