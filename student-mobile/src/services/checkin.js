import { apiRequest } from "./api";

export async function generateCheckIn(reservationId) {
  return apiRequest(`/reservations/${reservationId}/check-in`, {
    method: "POST",
  });
}

export async function getCheckIn(reservationId) {
  return apiRequest(`/reservations/${reservationId}/check-in`);
}

export async function performCheckIn(qrToken) {
  return apiRequest(`/check-in/${qrToken}`, {
    method: "POST",
  });
}
