import { apiRequest } from "./api";

export async function getResources() {
  return apiRequest("/resources");
}

export async function getAdminReservations() {
  return apiRequest("/admin/reservations");
}

export async function updateResource(resourceId, updates) {
  return apiRequest(`/admin/resources/${resourceId}`, {
    method: "PUT",
    body: JSON.stringify(updates),
  });
}

export async function deleteResource(resourceId) {
  return apiRequest(`/admin/resources/${resourceId}`, {
    method: "DELETE",
  });
}

export async function updateResourceStatus(resourceId, status) {
  return apiRequest(`/admin/resources/${resourceId}/status`, {
    method: "PUT",
    body: JSON.stringify({ status }),
  });
}

export async function updateReservationStatus(reservationId, status) {
  return apiRequest(`/admin/reservations/${reservationId}/status`, {
    method: "PUT",
    body: JSON.stringify({ status }),
  });
}
