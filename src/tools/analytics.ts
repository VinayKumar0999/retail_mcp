import { z } from 'zod';
import { apiClient } from '../api-client';

export const analyticsTools = [
  {
    name: 'analytics_search_performance',
    description: 'Get search performance analytics. GET /analytics/search_performance/ (client header, range required)',
    inputSchema: z.object({
      client: z.string().describe('Tenant domain'),
      range: z.string().describe('Date range (e.g. last_7_days, last_30_days)'),
      start: z.string().optional().describe('Start date (ISO 8601)'),
      end: z.string().optional().describe('End date (ISO 8601)'),
    }),
    async handler(args: { client: string; range: string; start?: string; end?: string }) {
      return apiClient.request('GET', '/analytics/search_performance/', {
        query: { range: args.range, start: args.start, end: args.end },
        headers: { client: args.client },
        skipAuth: true,
      });
    },
  },
  {
    name: 'analytics_track_event',
    description: 'Track analytics event. POST /analytics/events/ (client header)',
    inputSchema: z.object({
      client: z.string().describe('Tenant domain'),
      event: z.record(z.unknown()).describe('Event payload'),
    }),
    async handler(args: { client: string; event: Record<string, unknown> }) {
      return apiClient.request('POST', '/analytics/events/', {
        body: args.event,
        headers: { client: args.client },
        skipAuth: true,
      });
    },
  },
  {
    name: 'analytics_funnel_search',
    description: 'Get funnel search analytics. GET /analytics/funnel_search/ (Bearer + client)',
    inputSchema: z.object({
      client: z.string().optional().describe('Tenant domain override'),
    }).passthrough(),
    async handler(args: { client?: string; [k: string]: unknown }) {
      const { client, ...rest } = args;
      return apiClient.request('GET', '/analytics/funnel_search/', {
        query: rest as Record<string, string | number | boolean | undefined>,
        headers: client ? { client } : {},
      });
    },
  },
];
