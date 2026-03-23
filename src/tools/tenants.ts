import { z } from 'zod';
import { apiClient } from '../api-client';

export const tenantTools = [
  {
    name: 'tenant_onboard',
    description: 'Onboard a new tenant. POST /tenants/onboard/ (Bearer)',
    inputSchema: z.object({
      name: z.string(),
      domain: z.string(),
      email: z.string().optional(),
    }).passthrough(),
    async handler(args: Record<string, unknown>) {
      return apiClient.request('POST', '/tenants/onboard/', { body: args });
    },
  },
  {
    name: 'tenant_create_admin',
    description: 'Create a tenant admin user. POST /tenants/create-admin/ (Bearer)',
    inputSchema: z.object({
      username: z.string(),
      password: z.string(),
      email: z.string().optional(),
    }).passthrough(),
    async handler(args: Record<string, unknown>) {
      return apiClient.request('POST', '/tenants/create-admin/', { body: args });
    },
  },
  {
    name: 'tenant_offboard',
    description: 'Offboard (delete) a tenant. DELETE /tenants/offboarding/ (Bearer). Requires confirm=true.',
    inputSchema: z.object({
      tenant_id: z.string().describe('Tenant ID to offboard'),
      confirm: z.boolean().default(false).describe('Must be true to proceed with destructive operation'),
    }),
    async handler(args: { tenant_id: string; confirm: boolean }) {
      if (!args.confirm) {
        return { error: 'confirm must be true to offboard a tenant. This is a destructive operation.' };
      }
      return apiClient.request('DELETE', '/tenants/offboarding/', {
        body: { tenant_id: args.tenant_id },
      });
    },
  },
];
