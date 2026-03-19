# Requirements: Free Food Finder (Full-Stack)

**Defined:** 2026-03-09
**Core Value:** Students can reliably find and navigate to active free food events in real-time.

## v1 Requirements (Full-Stack Transition)

### Data & Cloud
- [ ] **DATA-01**: Migrated `food_events` table to Supabase PostgreSQL.
- [ ] **DATA-02**: Python scraper upserts discovered events to Supabase via API.
- [ ] **DATA-03**: Frontend fetches live events directly from Supabase client.

### Real-time / Speed
- [ ] **RT-01**: Dashboard UI reflects new events instantly via Supabase Realtime (WebSockets).

### Security & Admin
- [ ] **SEC-01**: Supabase Auth enabled for admin login.
- [ ] **SEC-02**: Row Level Security (RLS) restricts "Approve/Reject" updates to authenticated users only.

### Deployment
- [ ] **DEP-01**: Frontend deployed to Vercel at a custom subdomain.
- [ ] **DEP-02**: Environment variables safely managed in Vercel/Local (.env).

## v2 Requirements
- **NOTF-01**: Push notifications for "High Priority" food.
- **MAP-01**: Interactive campus map view for event locations.

## Out of Scope
| Feature | Reason |
|---------|--------|
| Multi-tenant orgs | Focus on single-campus (USD) scale for now. |
| Payment Gateway | No monetization planned for FFF. |

---
*Last updated: 2026-03-09 after GSD Initialization*
