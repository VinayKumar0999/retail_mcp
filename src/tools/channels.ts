import { z } from 'zod';
import { apiClient } from '../api-client';

export const channelTools = [
  {
    name: 'channels_search',
    description: 'Search channels. GET /api/channels/search/ (requires client and X-SECRET-KEY headers)',
    inputSchema: z.object({
      q: z.string().describe('Search query'),
      client: z.string().describe('Tenant domain'),
      secret_key: z.string().optional().describe('Secret key override'),
    }).passthrough(),
    async handler(args: { q: string; client: string; secret_key?: string; [k: string]: unknown }) {
      const { client, secret_key, q, ...rest } = args;
      const effectiveSecretKey = secret_key ?? process.env.SECRET_KEY;
      if (!effectiveSecretKey) {
        throw new Error(
          "channels_search requires a secret key: provide 'secret_key' in the tool arguments or set the SECRET_KEY environment variable."
        );
      }
      return apiClient.request('GET', '/api/channels/search/', {
        query: { q, ...(rest as Record<string, string | number | boolean | undefined>) },
        headers: {
          client,
          'X-SECRET-KEY': effectiveSecretKey,
        },
        skipAuth: true,
      });
    },
  },
  {
    name: 'channels_brands',
    description: 'Get channel brands. GET /api/channels/brands/ (Bearer)',
    inputSchema: z.object({}),
    async handler(_args: Record<string, never>) {
      return apiClient.request('GET', '/api/channels/brands/');
    },
  },
  {
    name: 'channels_synonyms',
    description: 'Get channel synonyms. GET /api/channels/synonyms/ (Bearer)',
    inputSchema: z.object({}),
    async handler(_args: Record<string, never>) {
      return apiClient.request('GET', '/api/channels/synonyms/');
    },
  },
];
