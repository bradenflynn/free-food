# Free Food Finder (VÉLOCE)

## What This Is

A real-time aggregator and dashboard for local free food events, powered by AI vision and Instagram scraping. It helps students find confirmed free food events on campus without manual searching.

## Core Value

The ONE thing that matters most: **Students can reliably find and navigate to active free food events in real-time.**

## Requirements

### Validated

- ✓ Local IG scraping engine — Phase 1
- ✓ AI Vision event classification — Phase 1
- ✓ Static dashboard UI — Phase 1
- ✓ SQLite local database — Phase 1

### Active

- [ ] **Cloud Database Migration**: Move from local SQLite to Supabase PostgreSQL.
- [ ] **Real-time UI Updates**: Dashboard updates instantly when new food is found.
- [ ] **Secure Admin Flow**: Authenticated "Approve/Reject" capability for the curator.
- [ ] **Public Hosting**: Deploy the frontend to Vercel for public access.

### Out of Scope

- **Native Mobile App** — Web-first approach is faster for MVP.
- **Automated Social Posting** — Keeping as a separate "Engine" (backend) for now.

## Context

The project is currently a series of Python scripts and a local HTML dashboard. It's ready for a "Stage 2" upgrade to become a proper full-stack application to support more users and real-time features.

## Constraints

- **Tech Stack**: Must use Supabase (Backend/DB) and Vercel (Hosting).
- **Cost**: Must remain within Free Tiers for both services.
- **Compatibility**: Scraper must continue running on a local mac machine (NIMBUS).

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Supabase | Robust free tier, built-in Auth and Real-time. | — Pending |
| Vercel | Industry standard for frontend hosting, easy GitHub sync. | — Pending |

---
*Last updated: 2026-03-09 after GSD Initialization*
