import { z } from 'zod';
import { apiClient } from '../api-client';

export const authTools = [
  {
    name: 'auth_admin_login',
    description: 'Admin login (no client header). POST /tenants/login/',
    inputSchema: z.object({
      username: z.string().describe('Admin username'),
      password: z.string().describe('Admin password'),
    }),
    async handler(args: { username: string; password: string }) {
      return apiClient.request('POST', '/tenants/login/', {
        body: { username: args.username, password: args.password },
        skipAuth: true,
      });
    },
  },
  {
    name: 'auth_tenant_login',
    description: 'Tenant login with client header. POST /tenants/login/',
    inputSchema: z.object({
      username: z.string(),
      password: z.string(),
      client: z.string().describe('Tenant domain for the client header'),
    }),
    async handler(args: { username: string; password: string; client: string }) {
      return apiClient.request('POST', '/tenants/login/', {
        body: { username: args.username, password: args.password },
        headers: { client: args.client },
        skipAuth: true,
      });
    },
  },
  {
    name: 'auth_refresh_token',
    description: 'Refresh access token. POST /api/auth/token/refresh/',
    inputSchema: z.object({
      refresh: z.string().describe('Refresh token'),
    }),
    async handler(args: { refresh: string }) {
      return apiClient.request('POST', '/api/auth/token/refresh/', {
        body: { refresh: args.refresh },
        skipAuth: true,
      });
    },
  },
  {
    name: 'auth_client_login',
    description: 'Client login with client header. POST /api/auth/login/',
    inputSchema: z.object({
      username: z.string(),
      password: z.string(),
      client: z.string().describe('Tenant domain for the client header'),
    }),
    async handler(args: { username: string; password: string; client: string }) {
      return apiClient.request('POST', '/api/auth/login/', {
        body: { username: args.username, password: args.password },
        headers: { client: args.client },
        skipAuth: true,
      });
    },
  },
];
