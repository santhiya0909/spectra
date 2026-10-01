export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://spectra-wlmc.onrender.com";

interface RequestOptions extends RequestInit {
  data?: any;
}

class ApiClient {
  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    if (typeof window !== "undefined") {
      const token = localStorage.getItem("spectra_token");
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }
    }

    return headers;
  }

  async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const url = endpoint.startsWith("http")
      ? endpoint
      : `${API_BASE_URL}${endpoint.startsWith("/") ? "" : "/"}${endpoint}`;

    const { data, ...customConfig } = options;

    const config: RequestInit = {
      ...customConfig,
      headers: {
        ...this.getHeaders(),
        ...customConfig.headers,
      },
    };

    if (data !== undefined) {
      config.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(url, config);

      if (response.status === 401) {
        if (typeof window !== "undefined" && !window.location.pathname.includes("/login")) {
          // Token expired or invalid
          localStorage.removeItem("spectra_token");
          localStorage.removeItem("spectra_user");
          window.location.href = "/login?expired=1";
        }
      }

      if (!response.ok) {
        let errorMessage = `Request failed with status ${response.status}`;
        try {
          const errorBody = await response.json();
          if (typeof errorBody.detail === "string") {
            errorMessage = errorBody.detail;
          } else if (Array.isArray(errorBody.detail)) {
            // Format FastAPI 422 validation errors into user-friendly message
            errorMessage = errorBody.detail
              .map((err: any) => {
                const field = Array.isArray(err.loc) ? err.loc[err.loc.length - 1] : "";
                return field ? `${field}: ${err.msg}` : err.msg;
              })
              .join("; ");
          } else if (typeof errorBody.message === "string") {
            errorMessage = errorBody.message;
          }
        } catch {
          // Non-JSON response body
        }
        throw new Error(errorMessage);
      }

      // If response has no content (204 or empty)
      const text = await response.text();
      return text ? JSON.parse(text) : ({} as T);
    } catch (error: any) {
      console.error(`[API Error] ${options.method || "GET"} ${url}:`, error.message);
      if (
        error.message === "Failed to fetch" ||
        error.name === "TypeError" ||
        error.message?.includes("NetworkError") ||
        error.message?.includes("fetch")
      ) {
        throw new Error(
          "Unable to connect to the SPECTRA server. Please verify that the backend is running on http://127.0.0.1:8000."
        );
      }
      throw error;
    }
  }

  get<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: "GET" });
  }

  post<T>(endpoint: string, data?: any, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: "POST", data });
  }

  patch<T>(endpoint: string, data?: any, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: "PATCH", data });
  }

  delete<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: "DELETE" });
  }
}

export const api = new ApiClient();
