import { apiRequest } from "./api";

export async function loginStudent(email, password) {
  return apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function registerStudent(name, student_id, email, password) {
  return apiRequest("/auth/register", {
    method: "POST",
    body: JSON.stringify({
      name,
      student_id,
      email,
      password,
    }),
  });
}

export function saveStudentSession(data) {
  localStorage.setItem("student_token", data.access_token);
  localStorage.setItem("student_user", JSON.stringify(data.user));
}

export function getStudent() {
  const user = localStorage.getItem("student_user");
  return user ? JSON.parse(user) : null;
}

export function isStudentLoggedIn() {
  return Boolean(localStorage.getItem("student_token"));
}

export function logoutStudent() {
  localStorage.removeItem("student_token");
  localStorage.removeItem("student_user");
}
