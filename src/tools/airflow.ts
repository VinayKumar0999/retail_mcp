import { z } from 'zod';
import { apiClient } from '../api-client';

export const airflowTools = [
  {
    name: 'airflow_trigger_dag',
    description: 'Trigger an Airflow DAG. POST /api/airflow/trigger-dag/ (Bearer)',
    inputSchema: z.object({
      dag_id: z.string().describe('DAG ID to trigger'),
      conf: z.record(z.unknown()).optional().describe('Optional DAG run configuration'),
    }),
    async handler(args: { dag_id: string; conf?: Record<string, unknown> }) {
      return apiClient.request('POST', '/api/airflow/trigger-dag/', {
        body: { dag_id: args.dag_id, ...(args.conf ? { conf: args.conf } : {}) },
      });
    },
  },
];
