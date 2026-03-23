import { z } from 'zod';
import { apiClient } from '../api-client';

export const searchTools = [
  {
    name: 'search_query',
    description: 'Search catalog. GET /api/search/ (requires client and X-SECRET-KEY headers)',
    inputSchema: z.object({
      q: z.string().describe('Search query'),
      client: z.string().describe('Tenant domain'),
      secret_key: z.string().optional().describe('Secret key (overrides env SECRET_KEY)'),
      page: z.number().optional(),
      page_size: z.number().optional(),
    }).passthrough(),
    async handler(args: { q: string; client: string; secret_key?: string; page?: number; page_size?: number; [k: string]: unknown }) {
      const { client, secret_key, q, page, page_size, ...rest } = args;
      return apiClient.request('GET', '/api/search/', {
        query: { q, page, page_size, ...(rest as Record<string, string | number | boolean | undefined>) },
        headers: {
          client,
          ...(secret_key ? { 'X-SECRET-KEY': secret_key } : {}),
        },
        skipAuth: true,
      });
    },
  },
  {
    name: 'ai_agent_search',
    description: 'AI agent search. GET /ai/agent_search/ (requires X-Secret-key header)',
    inputSchema: z.object({
      q: z.string().describe('Search query'),
      secret_key: z.string().optional().describe('Secret key (overrides env SECRET_KEY)'),
    }).passthrough(),
    async handler(args: { q: string; secret_key?: string; [k: string]: unknown }) {
      const { secret_key, q, ...rest } = args;
      return apiClient.request('GET', '/ai/agent_search/', {
        query: { q, ...(rest as Record<string, string | number | boolean | undefined>) },
        headers: {
          'X-Secret-key': secret_key ?? apiClient.secretKey,
        },
        skipAuth: true,
      });
    },
  },
  {
    name: 'ai_agent_suggestions',
    description: 'AI agent search suggestions. GET /ai/agent_suggestions/',
    inputSchema: z.object({
      q: z.string().describe('Partial query for suggestions'),
      secret_key: z.string().optional(),
    }).passthrough(),
    async handler(args: { q: string; secret_key?: string; [k: string]: unknown }) {
      const { secret_key, q, ...rest } = args;
      return apiClient.request('GET', '/ai/agent_suggestions/', {
        query: { q, ...(rest as Record<string, string | number | boolean | undefined>) },
        headers: {
          'X-Secret-key': secret_key ?? apiClient.secretKey,
        },
        skipAuth: true,
      });
    },
  },
  {
    name: 'ai_purge',
    description: 'Purge AI search cache. POST /ai/purge/ (Bearer + client). Requires confirm=true.',
    inputSchema: z.object({
      client: z.string().describe('Tenant domain'),
      confirm: z.boolean().default(false).describe('Must be true to proceed with destructive purge'),
    }),
    async handler(args: { client: string; confirm: boolean }) {
      if (!args.confirm) {
        return { error: 'confirm must be true to purge cache. This is a destructive operation.' };
      }
      return apiClient.request('POST', '/ai/purge/', {
        headers: { client: args.client },
      });
    },
  },
];
