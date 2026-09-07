import { apiRequest } from "./api";

export async function getNotifications() {
  return apiRequest("/notifications");
}

export async function markNotificationRead(notificationId) {
  return apiRequest(`/notifications/${notificationId}/read`, {
    method: "PUT",
  });
}