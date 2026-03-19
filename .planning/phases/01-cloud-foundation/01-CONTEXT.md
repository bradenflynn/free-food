# Phase 1: Cloud Foundation - Context

**Gathered:** 2026-03-09
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase migrates the project's data storage from a local SQLite database to a cloud-based Supabase PostgreSQL instance. It also updates the Python scraper to upsert data to the cloud.

</domain>

<decisions>
## Implementation Decisions

### Database
- **Provider**: Supabase (PostgreSQL).
- **Schema**: Replicate `food_events` table from `free_food.db`.
- **Primary Key**: `post_id` (Instagram unique ID).

### Scraper (Backend)
- **Library**: `supabase-py`.
- **Logic**: Use `upsert` on `post_id` to prevent duplicate events.
- **Config**: Supabase URL and Keys stored in `.env`.

### Claude's Discretion
- Table row security (RLS) setup.
- Error handling for network timeouts.
- Data backup before migration.

</decisions>

<specifics>
## Specific Ideas
- Use the existing SQL in `main.py` as the blueprint for the Supabase table.
- Ensure the `downloads/` images are still served correctly (this phase focuses on data, not images yet).

</specifics>

<deferred>
## Deferred Ideas
- Real-time frontend updates (Phase 2).
- Admin Authentication (Phase 3).
- Vercel Deployment (Phase 4).

</deferred>

---
*Phase: 01-cloud-foundation*
*Context gathered: 2026-03-09 after GSD Initialization*
