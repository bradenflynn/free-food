# Phase 3: Security & Admin - Context

**Gathered:** 2026-03-10
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase secures the dashboard so that only the project owner can approve or reject food events. It introduces Supabase Auth and Row Level Security (RLS) policies to protect the data from unauthorized modifications.

</domain>

<decisions>
## Implementation Decisions

### Authentication
- **Provider**: Supabase Email/Password Auth.
- **Scope**: Single admin user (you).

### Row Level Security (RLS)
- **Select**: Public (Everyone can view approved/pending events).
- **Insert/Update/Delete**: Restricted to Authenticated users.
- **Exception**: The local scraper (using the anon key) needs to be able to insert/upsert. We handled this in Phase 1 with a specific policy.

### Admin UI
- **Components**: Simple login footer or modal.
- **Controls**: "Approve" and "Reject" buttons appear on event cards only when a valid admin session exists.

### Claude's Discretion
- Logout functionality.
- Persisting session across page refreshes using Supabase's built-in session management.

</decisions>

<specifics>
## Specific Ideas
- The "Dismiss" button from the old local version should return as a "Reject" button in the admin view.
- Visual feedback (e.g., a "Logged In" badge) to indicate admin status.

</specifics>

<deferred>
## Deferred Ideas
- Multi-user roles (Phase 4+).
- Vercel Deployment (Phase 4).

</deferred>

---
*Phase: 03-security-admin*
*Context gathered: 2026-03-10 after Phase 2 Completion*
