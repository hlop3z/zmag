class BackendAPI {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.token = null;
  }

  static init(baseURL) {
    return new BackendAPI(baseURL);
  }

  setToken(token) {
    this.token = token;
  }

  query({ query = {}, filters = [] } = {}) {
    const qs = new URLSearchParams();

    const append = (key, value) => {
      if (Array.isArray(value)) {
        value.forEach((v) => qs.append(key, v));
      } else {
        qs.append(key, value);
      }
    };

    for (const [key, value] of Object.entries(query)) {
      append(key, value);
    }

    for (const filter of [filters].flat()) {
      for (const [field, ops] of Object.entries(filter)) {
        for (const [op, value] of Object.entries(ops)) {
          append(`${field}__${op}`, value);
        }
      }
    }

    return "?" + qs.toString();
  }

  get(endpoint, params, headers) {
    const _endpoint = params ? endpoint + this.query(params) : endpoint;
    return this.request(_endpoint, { method: "GET", headers });
  }

  post(endpoint, body, headers) {
    return this.request(endpoint, { method: "POST", body, headers });
  }

  put(endpoint, body, headers) {
    return this.request(endpoint, { method: "PUT", body, headers });
  }

  patch(endpoint, body, headers) {
    return this.request(endpoint, { method: "PATCH", body, headers });
  }

  delete(endpoint, headers) {
    return this.request(endpoint, { method: "DELETE", headers });
  }

  form(endpoint, body, headers) {
    return this.request(endpoint, {
      method: "POST",
      body: new URLSearchParams(body),
      headers,
    });
  }

  async request(endpoint, { method = "GET", body = null, headers = {} } = {}) {
    const isForm = body instanceof URLSearchParams || body instanceof FormData;
    const config = {
      method,
      headers: {
        ...(isForm ? {} : { "Content-Type": "application/json" }),
        ...(this.token ? { Authorization: `Bearer ${this.token}` } : {}),
        ...headers,
      },
    };

    if (body) {
      config.body = isForm ? body : JSON.stringify(body);
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, config);
    const data = await response.json().catch(() => null);

    if (!response.ok) {
      throw new Error(data?.detail || data?.message || "Request failed");
    }

    return data;
  }
}
