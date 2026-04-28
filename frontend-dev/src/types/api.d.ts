export {};

declare global {
  const API: {
    baseURL: string;
    token: string | null;

    init(baseURL: string): typeof API;
    setToken(token: string): void;

    query(params?: {
      query?: Record<string, any>;
      filters?:
        | Record<string, Record<string, any>>[]
        | Record<string, Record<string, any>>;
    }): string;

    get(
      endpoint: string,
      params?: Parameters<typeof API.query>[0],
      headers?: HeadersInit,
    ): Promise<any>;

    post(endpoint: string, body?: any, headers?: HeadersInit): Promise<any>;

    put(endpoint: string, body?: any, headers?: HeadersInit): Promise<any>;

    patch(endpoint: string, body?: any, headers?: HeadersInit): Promise<any>;

    delete(endpoint: string, headers?: HeadersInit): Promise<any>;

    form(
      endpoint: string,
      body: Record<string, string>,
      headers?: HeadersInit,
    ): Promise<any>;

    request(
      endpoint: string,
      options?: {
        method?: string;
        body?: any;
        headers?: HeadersInit;
      },
    ): Promise<any>;
  };
}
