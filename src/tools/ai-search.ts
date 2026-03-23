import { z } from 'zod';
import { apiClient } from '../api-client';

export const aiSearchTools = [
  {
    name: 'ai_search',
    description: 'AI-powered search. GET /api/ai/ai_search/ (Bearer + client)',
    inputSchema: z.object({
      q: z.string().describe('Search query'),
      client: z.string().optional().describe('Tenant domain override'),
    }).passthrough(),
    async handler(args: { q: string; client?: string; [k: string]: unknown }) {
      const { client, q, ...rest } = args;
      return apiClient.request('GET', '/api/ai/ai_search/', {
        query: { q, ...(rest as Record<string, string | number | boolean | undefined>) },
        headers: client ? { client } : {},
      });
    },
  },
];
