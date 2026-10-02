const rawApiBaseUrl = process.env.NEXT_PUBLIC_API_URL || "https://spectra-v1nc.onrender.com";

// Normalize API base URL: strip trailing slashes
export const API_BASE_URL = rawApiBaseUrl.replace(/\/+$/, "");

/**
 * Build absolute API URL preventing accidental double slashes or double /api/api/...
 */
export function buildApiUrl(endpoint: string): string {
  if (endpoint.startsWith("http://") || endpoint.startsWith("https://")) {
    return endpoint;
  }
  const cleanEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;

  // If base URL already ends with /api and endpoint starts with /api/, avoid /api/api/...
  if (API_BASE_URL.endsWith("/api") && cleanEndpoint.startsWith("/api/")) {
    return `${API_BASE_URL}${cleanEndpoint.slice(4)}`;
  }

  return `${API_BASE_URL}${cleanEndpoint}`;
}

interface RequestOptions extends RequestInit {
  data?: any;
}

class ApiClient {
  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    if (typeof window !== "undefined") {
      const token = localStorage.getItem("spectra_token")?.trim();
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }
    }

    return headers;
  }

  async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const url = buildApiUrl(endpoint);
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
        if (
          typeof window !== "undefined" &&
          !window.location.pathname.includes("/login") &&
          !window.location.pathname.includes("/register") &&
          !url.includes("/auth/login") &&
          !url.includes("/auth/register")
        ) {
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
        console.error(`[API ${response.status}] ${options.method || "GET"} ${url}:`, errorMessage);
        throw new Error(errorMessage);
      }

      // If response has no content (204 or empty)
      const text = await response.text();
      return text ? JSON.parse(text) : ({} as T);
    } catch (error: any) {
      console.error(`[API Error] ${options.method || "GET"} ${url}:`, error.message || error);
      if (
        error.message === "Failed to fetch" ||
        error.name === "TypeError" ||
        error.message?.includes("NetworkError") ||
        error.message?.includes("fetch")
      ) {
        throw new Error(
          `Unable to connect to the SPECTRA server at ${API_BASE_URL}. Please check your connection or verify that the backend is running.`
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
