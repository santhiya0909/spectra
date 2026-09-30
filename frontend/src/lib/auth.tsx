"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { api } from "./api";

export interface User {
  id: number;
  name: string;
  email: string;
  role: "STUDENT" | "TEACHER" | "ADMIN";
  student_profile?: {
    id: number;
    student_id: string;
    department: string;
    semester: number;
  };
  teacher_profile?: {
    id: number;
    employee_id: string;
    department: string;
  };
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  role: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: any) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  const redirectByRole = (userRole: string) => {
    if (userRole === "STUDENT") router.push("/student/dashboard");
    else if (userRole === "TEACHER") router.push("/teacher/dashboard");
    else if (userRole === "ADMIN") router.push("/admin/dashboard");
    else router.push("/login");
  };

  const refreshUser = async () => {
    try {
      const storedToken = localStorage.getItem("spectra_token");
      if (!storedToken) {
        setIsLoading(false);
        return;
      }
      setToken(storedToken);
      const userData = await api.get<User>("/api/auth/me");
      setUser(userData);
      localStorage.setItem("spectra_user", JSON.stringify(userData));
    } catch (err) {
      console.error("Session verification failed:", err);
      localStorage.removeItem("spectra_token");
      localStorage.removeItem("spectra_user");
      setUser(null);
      setToken(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshUser();
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const res = await api.post<{
        access_token: string;
        role: "STUDENT" | "TEACHER" | "ADMIN";
        user_id: number;
        name: string;
        email: string;
      }>("/api/auth/login", { email, password });

      localStorage.setItem("spectra_token", res.access_token);
      setToken(res.access_token);

      // Fetch user profile with explicit auth header
      const userData = await api.get<User>("/api/auth/me", {
        headers: { Authorization: `Bearer ${res.access_token}` },
      });
      setUser(userData);
      localStorage.setItem("spectra_user", JSON.stringify(userData));

      redirectByRole(userData.role);
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: any) => {
    setIsLoading(true);
    try {
      const res = await api.post<{
        access_token: string;
        role: "STUDENT" | "TEACHER" | "ADMIN";
        user_id: number;
        name: string;
        email: string;
      }>("/api/auth/register", data);

      localStorage.setItem("spectra_token", res.access_token);
      setToken(res.access_token);

      // Fetch user profile with explicit auth header
      const userData = await api.get<User>("/api/auth/me", {
        headers: { Authorization: `Bearer ${res.access_token}` },
      });
      setUser(userData);
      localStorage.setItem("spectra_user", JSON.stringify(userData));

      redirectByRole(userData.role);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem("spectra_token");
    localStorage.removeItem("spectra_user");
    setUser(null);
    setToken(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        role: user?.role || null,
        isLoading,
        login,
        register,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
