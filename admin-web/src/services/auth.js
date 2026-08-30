import { apiRequest } from "./api";

export async function adminLogin(email, password) {
  const data = await apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify({
      email,
      password,
    }),
  });

  if (!data.user || data.user.role !== "ADMIN") {
    throw new Error("Admin account required");
  }

  localStorage.setItem("adminToken", data.access_token);

  return data;
}

export function adminLogout() {
  localStorage.removeItem("adminToken");
}

export function isAdminLoggedIn() {
  return Boolean(localStorage.getItem("adminToken"));
}
