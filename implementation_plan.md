# Implementation Plan: Free Food Finder (FFF)

## Project Overview
A software system designed to aggregate event data from school club Instagram accounts and email newsletters, identify events offering free food, and distribute a curated newsletter to students.

## 🏗️ Technical Architecture

### Phase 1: Data Acquisition (The "Hunters")
*   **Instagram Scraper (Custom):**
    *   **Target:** Start with `@usdbas`.
    *   **Logic:** Use Python with Playwright (headless browser).
    *   **Scanning:** Must scan the **actual post content** (images/videos), not just the captions.
    *   **Vision/OCR:** Use Google's Gemini Vision API via the `google-generativeai` package.
*   **Email Newsletter Parser:**
    *   **Target:** `bradenflynn@gmail.com`.
    *   **Logic:** Authenticate via Gmail API/OAuth2.
    *   **Language:** Python.

### Phase 2: Approval & Processing (The "Admin Dash")
*   **Manual Approval Workflow:**
    *   Instead of full autonomy, the system will stage events.
    *   Braden reviews each event (Approve/Edit/Reject) before it's eligible for the newsletter.
*   **Structured Storage:** 
    *   Database (SQLite) to keep track of `Pending`, `Approved`, and `Sent` events.

### Phase 3: Distribution (The "Broadcaster")
*   **Sending Engine:**
    *   Sent directly from `bradenflynn@gmail.com`.
    *   Beautiful HTML email template featuring the "Best Free Food" items.
*   **Landing Page:**
    *   A sleek sign-up page for students to join the list.

---

## 🚀 Execution Roadmap

### Step 1: Instagram Image Extraction (Next)
Build a script that:
1. Navigates to `@usdbas`.
2. Downloads the latest post image.
3. Uses AI to "look" at the image and find food details.

### Step 2: Gmail Connectivity
Set up the script to read from and eventually send from `bradenflynn@gmail.com`.

### Step 3: Approval UI
Create a simple web interface (Internal Use) where Braden can quickly swipe or click through findings.
