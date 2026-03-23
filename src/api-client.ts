import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { config as appConfig } from './config';

export class ApiClient {
  baseUrl: string;
  accessToken: string;
  refreshToken: string;
  tenantDomain: string;
  secretKey: string;

  constructor(cfg: typeof appConfig) {
    this.baseUrl = cfg.baseUrl;
    this.accessToken = cfg.accessToken;
    this.refreshToken = cfg.refreshToken;
    this.tenantDomain = cfg.tenantDomain;
    this.secretKey = cfg.secretKey;
  }

  async request<T = unknown>(
    method: string,
    path: string,
    opts: {
      body?: Record<string, unknown>;
      query?: Record<string, string | number | boolean | undefined>;
      headers?: Record<string, string>;
      multipart?: Record<string, string | Buffer>;
      skipAuth?: boolean;
    } = {}
  ): Promise<T> {
    const url = new URL(path, this.baseUrl);
    if (opts.query) {
      for (const [k, v] of Object.entries(opts.query)) {
        if (v !== undefined) url.searchParams.set(k, String(v));
      }
    }

    const headers: Record<string, string> = { ...opts.headers };
    if (this.accessToken && !opts.skipAuth) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }
    if (this.tenantDomain && !headers['client']) {
      headers['client'] = this.tenantDomain;
    }
    if (this.secretKey && !headers['X-SECRET-KEY'] && !headers['X-Secret-key']) {
      headers['X-SECRET-KEY'] = this.secretKey;
    }

    const axiosConfig: AxiosRequestConfig = {
      method,
      url: url.toString(),
      headers,
    };

    if (opts.multipart) {
      // eslint-disable-next-line @typescript-eslint/no-var-requires
      const FormData = require('form-data');
      const fd = new FormData();
      for (const [k, v] of Object.entries(opts.multipart)) {
        if (Buffer.isBuffer(v)) {
          fd.append(k, v, { filename: k });
        } else {
          fd.append(k, v);
        }
      }
      axiosConfig.data = fd;
      axiosConfig.headers = { ...axiosConfig.headers, ...fd.getHeaders() };
    } else if (opts.body) {
      axiosConfig.data = opts.body;
      axiosConfig.headers = {
        'Content-Type': 'application/json',
        ...axiosConfig.headers,
      };
    }

    try {
      const resp: AxiosResponse<T> = await axios(axiosConfig);
      return resp.data;
    } catch (err: unknown) {
      if (
        axios.isAxiosError(err) &&
        err.response?.status === 401 &&
        this.refreshToken &&
        !opts.skipAuth
      ) {
        const refreshResp = await axios.post<{ access: string }>(
          new URL('/api/auth/token/refresh/', this.baseUrl).toString(),
          { refresh: this.refreshToken },
          { headers: { 'Content-Type': 'application/json' } }
        );
        this.accessToken = refreshResp.data.access;
        axiosConfig.headers!['Authorization'] = `Bearer ${this.accessToken}`;
        const retryResp: AxiosResponse<T> = await axios(axiosConfig);
        return retryResp.data;
      }
      if (axios.isAxiosError(err) && err.response) {
        throw new Error(
          `API error ${err.response.status}: ${JSON.stringify(err.response.data)}`
        );
      }
      throw err;
    }
  }
}

export const apiClient = new ApiClient(appConfig);
