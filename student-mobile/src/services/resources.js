import { apiRequest } from "./api";

export async function getResources() {
  return apiRequest("/resources");
}

export async function getResource(resourceId) {
  return apiRequest(`/resources/${resourceId}`);
}
