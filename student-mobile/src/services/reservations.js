import { apiRequest } from "./api";

export async function createReservation(reservation) {
  return apiRequest("/reservations", {
    method: "POST",
    body: JSON.stringify(reservation),
  });
}

export async function getReservations() {
  return apiRequest("/reservations");
}

export async function getReservation(reservationId) {
  return apiRequest(`/reservations/${reservationId}`);
}

export async function cancelReservation(reservationId) {
  return apiRequest(`/reservations/${reservationId}`, {
    method: "DELETE",
  });
}
