# Mazaya Recycling Portal

Mazaya is a bilingual Oman-focused paper and book recycling portal for school container reports and collection operations.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- `artifacts/mazaya/src/App.tsx` — school portal, secure admin gate, bilingual UI, and live report queue
- `artifacts/mazaya/src/index.css` — Mazaya eco-brand tokens and responsive UI styling
- `artifacts/api-server/src/routes/reports.ts` — report CRUD/status API and admin summary endpoints
- `lib/db/src/schema/reports.ts` — PostgreSQL report schema
- `lib/api-spec/openapi.yaml` — source of truth for report API contracts

## Architecture decisions

- School submissions remain public; report list, dashboard metrics, and collection updates require Clerk authentication.
- The dashboard identifies urgent reports at 80% fill or higher, but only while they are still pending.
- The interface keeps English and Arabic copy in one responsive shell with RTL support instead of duplicating the application.

## Product

- Schools submit fill percentage, contact phone, and optional collection notes.
- Mazaya staff review a live queue, filter by status, see high-fill containers, and mark requests collected.
- The admin queue is protected by Replit-managed Clerk authentication.

## User preferences

_Populate as you build — explicit user instructions worth remembering across sessions._

## Gotchas

- Run API codegen after OpenAPI changes; the generated client is used by the frontend.
- `CLERK_PUBLISHABLE_KEY`, `CLERK_SECRET_KEY`, and `VITE_CLERK_PUBLISHABLE_KEY` are provisioned automatically for authentication.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
