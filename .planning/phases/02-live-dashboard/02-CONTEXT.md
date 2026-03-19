# Phase 2: Live Dashboard - Context

**Gathered:** 2026-03-10
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase transitions the frontend from reading a local `data.js` file to fetching live data directly from Supabase. It also introduces real-time capabilities so the dashboard updates without a page refresh.

</domain>

<decisions>
## Implementation Decisions

### Frontend Client
- **Library**: Supabase JavaScript Client (via CDN for simplicity in MVP).
- **Authentication**: Using the 'anon' key for public read access.

### Data Fetching
- **Logic**: Use `supabase.from('food_events').select('*')` instead of the local array.
- **Sorting**: Order by `date` ascending to keep upcoming events at the top.

### Real-time
- **Mechanism**: Supabase Realtime (WebSockets) to listen for `INSERT` and `UPDATE` events on the `food_events` table.

### Claude's Discretion
- Loading states (spinner/skeleton) during initial fetch.
- Error handling for failed cloud connections.

</decisions>

<specifics>
## Specific Ideas
- Maintain the current "Galaxy" UI theme.
- Ensure the "Dismiss" logic still works (potentially purely client-side for now, or synced to DB if requested).

</specifics>

<deferred>
## Deferred Ideas
- Admin Login (Phase 3).
- Vercel Deployment (Phase 4).

</deferred>

---
*Phase: 02-live-dashboard*
*Context gathered: 2026-03-10 after Phase 1 Completion*
