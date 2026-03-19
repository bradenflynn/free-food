# Roadmap: Free Food Finder (Full-Stack)

## Overview

The journey from a local Python-only script to a live, professional web application. This roadmap covers the migration of data to the cloud, the implementation of security, and the final deployment to the web.

## Phases

- [x] **Phase 1: Cloud Foundation (Supabase)** - Migrating the database and scraper logic to the cloud.
- [x] **Phase 2: Live Dashboard (Frontend)** - Updating the UI to talk to Supabase and enabling real-time updates. <!-- id: 24 -->
- [/] **Phase 3: Security & Admin** - Locking down the curator dashboard with Supabase Auth. <!-- id: 25 -->
- [ ] **Phase 4: Launch & Deployment (Vercel)** - Going live on the public web.

## Phase Details

### Phase 1: Cloud Foundation (Supabase)
**Goal**: Scraper data lives in the cloud instead of a local file.
**Requirements**: [DATA-01, DATA-02]
**Success Criteria**:
  1. `food_events` table exists in Supabase.
  2. Scraper successfully inserts a test event to Supabase.
**Plans**: 2 plans

### Phase 2: Live Dashboard (Frontend)
**Goal**: Dashboard displays live data from the cloud instantly.
**Requirements**: [DATA-03, RT-01]
**Success Criteria**:
  1. Frontend fetches all events from Supabase on load.
  2. Adding an event in Supabase UI instantly appears on the local dashboard.
**Plans**: 2 plans

### Phase 3: Security & Admin
**Goal**: Onlyauthorized users can manage events.
**Requirements**: [SEC-01, SEC-02]
**Success Criteria**:
  1. Admin login screen protects the "Approve/Reject" actions.
  2. Unauthenticated requests to "Update" an event are rejected by the DB.

### Phase 4: Launch & Deployment (Vercel)
**Goal**: Anyone can access the dashboard via a URL.
**Requirements**: [DEP-01, DEP-02]
**Success Criteria**:
  1. Dashboard is accessible at `*.vercel.app`.
  2. No sensitive keys are committed to GitHub.

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Cloud | v1.0 | 2/2 | Complete | 2026-03-10 |
| 2. Dash | v1.0 | 2/2 | Complete | 2026-03-10 |
| 3. Security | v1.0 | 0/2 | In progress | - |
| 4. Launch | v1.0 | 0/1 | Not started | - |
