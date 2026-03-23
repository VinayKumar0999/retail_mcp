import { z } from 'zod';
import { apiClient } from '../api-client';

export const catalogTools = [
  {
    name: 'catalog_settings_bulk_create',
    description: 'Bulk create catalog settings. POST /api/catalog/settings/bulk-create/ (Bearer)',
    inputSchema: z.object({
      settings: z.array(z.record(z.unknown())).describe('Array of catalog setting objects'),
    }),
    async handler(args: { settings: unknown[] }) {
      return apiClient.request('POST', '/api/catalog/settings/bulk-create/', {
        body: { settings: args.settings } as Record<string, unknown>,
      });
    },
  },
  {
    name: 'catalog_settings_active_fields',
    description: 'Get active catalog settings fields. GET /api/catalog/settings/fields/active/ (Bearer)',
    inputSchema: z.object({
      client: z.string().optional().describe('Tenant domain (optional client header override)'),
    }),
    async handler(args: { client?: string }) {
      return apiClient.request('GET', '/api/catalog/settings/fields/active/', {
        headers: args.client ? { client: args.client } : {},
      });
    },
  },
  {
    name: 'catalog_settings_search_fields_active',
    description: 'Get active search fields. GET /api/catalog/settings/search-fields/active/ (Bearer)',
    inputSchema: z.object({}),
    async handler(_args: Record<string, never>) {
      return apiClient.request('GET', '/api/catalog/settings/search-fields/active/');
    },
  },
  {
    name: 'catalog_settings_create_search_fields',
    description: 'Create search field settings. POST /api/catalog/settings/search-fields/ (Bearer)',
    inputSchema: z.object({
      fields: z.array(z.record(z.unknown())).describe('Array of search field objects'),
    }),
    async handler(args: { fields: unknown[] }) {
      return apiClient.request('POST', '/api/catalog/settings/search-fields/', {
        body: { fields: args.fields } as Record<string, unknown>,
      });
    },
  },
  {
    name: 'catalog_sync_status',
    description: 'Get catalog sync status. GET /api/catalog/sync/ (Bearer)',
    inputSchema: z.object({}),
    async handler(_args: Record<string, never>) {
      return apiClient.request('GET', '/api/catalog/sync/');
    },
  },
  {
    name: 'catalog_sync_trigger',
    description: 'Trigger a catalog sync. POST /api/catalog/sync/ (Bearer)',
    inputSchema: z.object({
      full_sync: z.boolean().optional().describe('Trigger a full sync'),
    }).passthrough(),
    async handler(args: Record<string, unknown>) {
      return apiClient.request('POST', '/api/catalog/sync/', { body: args });
    },
  },
  {
    name: 'catalog_upload',
    description: 'Upload catalog file. POST /tenants/catalog/upload/ (multipart). Provide file as base64 string or a URL.',
    inputSchema: z.object({
      file_base64: z.string().optional().describe('Base64-encoded file content'),
      file_url: z.string().url().optional().describe('URL to download the file from'),
      filename: z.string().optional().describe('Filename for the upload'),
    }).refine((d) => d.file_base64 || d.file_url, {
      message: 'Provide either file_base64 or file_url',
    }),
    async handler(args: { file_base64?: string; file_url?: string; filename?: string }) {
      let fileBuffer: Buffer;
      const filename = args.filename ?? 'catalog.csv';

      if (args.file_base64) {
        fileBuffer = Buffer.from(args.file_base64, 'base64');
      } else if (args.file_url) {
        const axiosLib = (await import('axios')).default;
        const resp = await axiosLib.get<ArrayBuffer>(args.file_url, { responseType: 'arraybuffer' });
        fileBuffer = Buffer.from(resp.data);
      } else {
        throw new Error('file_base64 or file_url required');
      }

      return apiClient.request('POST', '/tenants/catalog/upload/', {
        multipart: { file: { data: fileBuffer, filename } },
      });
    },
  },
];
