import express from 'express';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import { ZodRawShape, ZodTypeAny } from 'zod';
import { config } from './config';
import { authTools } from './tools/auth';
import { tenantTools } from './tools/tenants';
import { catalogTools } from './tools/catalog';
import { searchTools } from './tools/search';
import { channelTools } from './tools/channels';
import { aiSearchTools } from './tools/ai-search';
import { airflowTools } from './tools/airflow';
import { analyticsTools } from './tools/analytics';

const allTools = [
  ...authTools,
  ...tenantTools,
  ...catalogTools,
  ...searchTools,
  ...channelTools,
  ...aiSearchTools,
  ...airflowTools,
  ...analyticsTools,
];

function getShape(schema: ZodTypeAny): ZodRawShape {
  // Handle ZodEffects (from .refine()) by unwrapping
  if (schema._def?.typeName === 'ZodEffects') {
    return getShape(schema._def.schema as ZodTypeAny);
  }
  // Handle ZodObject (including passthrough)
  if (schema._def?.shape) {
    return (schema._def.shape as () => ZodRawShape)();
  }
  return {};
}

export function createMcpServer() {
  const server = new McpServer({
    name: 'retail-mcp-server',
    version: '1.0.0',
  });

  for (const tool of allTools) {
    const shape = getShape(tool.inputSchema as ZodTypeAny);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handler = tool.handler as (args: any) => Promise<unknown>;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const callback = async (args: any) => {
      try {
        const result = await handler(args);
        return {
          content: [{ type: 'text' as const, text: JSON.stringify(result, null, 2) }],
        };
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : String(err);
        return {
          content: [{ type: 'text' as const, text: `Error: ${message}` }],
          isError: true,
        };
      }
    };
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (server.tool as any)(tool.name, tool.description, shape, callback);
  }

  return server;
}

export async function startHttpServer() {
  const app = express();
  app.use(express.json());

  const transports: Map<string, SSEServerTransport> = new Map();

  app.get('/sse', async (_req, res) => {
    const transport = new SSEServerTransport('/messages', res);
    const server = createMcpServer();
    transports.set(transport.sessionId, transport);

    res.on('close', () => {
      transports.delete(transport.sessionId);
    });

    await server.connect(transport);
  });

  app.post('/messages', async (req, res) => {
    const sessionId = req.query['sessionId'] as string;
    const transport = transports.get(sessionId);
    if (!transport) {
      res.status(404).json({ error: 'Session not found' });
      return;
    }
    await transport.handlePostMessage(req, res);
  });

  app.get('/health', (_req, res) => {
    res.json({ status: 'ok', server: 'retail-mcp-server' });
  });

  app.listen(config.port, () => {
    console.log(`Retail MCP Server running on http://localhost:${config.port}`);
    console.log(`SSE endpoint: http://localhost:${config.port}/sse`);
    console.log(`Messages endpoint: http://localhost:${config.port}/messages`);
  });
}
