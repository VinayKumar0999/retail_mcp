# Retail MCP Server

A Model Context Protocol (MCP) server that exposes retail backoffice APIs as tools for AI assistants. Built with Node.js, TypeScript, and the official MCP SDK.

## Prerequisites

- Node.js 18 or higher
- npm 9 or higher

## Installation

```bash
npm install
```

## Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|---|---|---|
| `BASE_URL` | Base URL of the retail backoffice API | `http://172.168.168.36:8006` |
| `ACCESS_TOKEN` | JWT access token for authenticated requests | _(empty)_ |
| `REFRESH_TOKEN` | JWT refresh token for automatic token renewal | _(empty)_ |
| `TENANT_DOMAIN` | Default tenant domain sent as the `client` header | _(empty)_ |
| `SECRET_KEY` | Default secret key sent as `X-SECRET-KEY` header | _(empty)_ |
| `PORT` | HTTP port for the MCP server | `3000` |

## Running

**Development** (with ts-node):

```bash
npm run dev
```

**Production** (compile first, then run):

```bash
npm run build
npm start
```

## Connecting an MCP Client

Use the SSE endpoint to connect any MCP-compatible client:

```
http://localhost:3000/sse
```

### Example: Claude Desktop config

```json
{
  "mcpServers": {
    "retail": {
      "url": "http://localhost:3000/sse"
    }
  }
}
```

### Health check

```
GET http://localhost:3000/health
```

## Available Tools

### Authentication

| Tool | Description |
|---|---|
| `auth_admin_login` | Admin login — POST `/tenants/login/` (no client header) |
| `auth_tenant_login` | Tenant login — POST `/tenants/login/` (with client header) |
| `auth_client_login` | Client login — POST `/api/auth/login/` (with client header) |
| `auth_refresh_token` | Refresh JWT access token — POST `/api/auth/token/refresh/` |

### Tenant Management

| Tool | Description |
|---|---|
| `tenant_onboard` | Onboard a new tenant — POST `/tenants/onboard/` |
| `tenant_create_admin` | Create a tenant admin user — POST `/tenants/create-admin/` |
| `tenant_offboard` | Delete a tenant — DELETE `/tenants/offboarding/` (**destructive**, requires `confirm: true`) |

### Catalog

| Tool | Description |
|---|---|
| `catalog_settings_bulk_create` | Bulk create catalog settings — POST `/api/catalog/settings/bulk-create/` |
| `catalog_settings_active_fields` | Get active catalog fields — GET `/api/catalog/settings/fields/active/` |
| `catalog_settings_search_fields_active` | Get active search fields — GET `/api/catalog/settings/search-fields/active/` |
| `catalog_settings_create_search_fields` | Create search fields — POST `/api/catalog/settings/search-fields/` |
| `catalog_sync_status` | Get catalog sync status — GET `/api/catalog/sync/` |
| `catalog_sync_trigger` | Trigger a catalog sync — POST `/api/catalog/sync/` |
| `catalog_upload` | Upload catalog file (multipart) — POST `/tenants/catalog/upload/` |

### Search

| Tool | Description |
|---|---|
| `search_query` | Full-text catalog search — GET `/api/search/` |
| `ai_agent_search` | AI-powered agent search — GET `/ai/agent_search/` |
| `ai_agent_suggestions` | AI search suggestions — GET `/ai/agent_suggestions/` |
| `ai_purge` | Purge AI search cache — POST `/ai/purge/` (**destructive**, requires `confirm: true`) |

### Channels

| Tool | Description |
|---|---|
| `channels_search` | Search channels — GET `/api/channels/search/` |
| `channels_brands` | Get channel brands — GET `/api/channels/brands/` |
| `channels_synonyms` | Get channel synonyms — GET `/api/channels/synonyms/` |

### AI Search

| Tool | Description |
|---|---|
| `ai_search` | AI-powered search — GET `/api/ai/ai_search/` |

### Airflow

| Tool | Description |
|---|---|
| `airflow_trigger_dag` | Trigger an Airflow DAG — POST `/api/airflow/trigger-dag/` |

### Analytics

| Tool | Description |
|---|---|
| `analytics_search_performance` | Search performance report — GET `/analytics/search_performance/` |
| `analytics_track_event` | Track an analytics event — POST `/analytics/events/` |
| `analytics_funnel_search` | Funnel search analytics — GET `/analytics/funnel_search/` |

## Security Notes

- **Never commit `.env`** — it is listed in `.gitignore`.
- **Destructive tools** (`tenant_offboard`, `ai_purge`) require an explicit `confirm: true` argument to prevent accidental data loss.
- Access tokens are stored in memory only; they are never logged or persisted to disk by this server.
- The server does not enforce authentication on its own endpoints — deploy behind a reverse proxy with TLS and access controls in production.
- Rotate `SECRET_KEY` and tokens regularly and use short-lived JWT access tokens with refresh-token rotation.
