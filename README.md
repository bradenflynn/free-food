# 🍕 Free Food Finder (FFF)

### 🌎 **[VIEW DASHBOARD (Public Link)](https://bradenflynn.github.io/free-food/)**
### 🖥️ **[OPEN DASHBOARD (Local File)](file:///Users/bradenflynn/Downloads/free%20food/frontend/index.html)**
*Terminal command to open locally:* `open "frontend/index.html"`

---

A tool designed for University of San Diego students to automatically discover, analyze, and share free food events from Instagram.

A tool designed for University of San Diego students to automatically discover, analyze, and share free food events from Instagram.

## 🚀 How to Run

To start the project and update the dashboard, simply run this file from your project folder:

```bash
"/Users/bradenflynn/Downloads/free food/FreeFoodFinder.command"
```

### What happens when you run it:
1.  **Scan**: The script checks the latest Instagram posts for student clubs.
2.  **Analyze**: AI scans the flyers for mention of free food.
3.  **Approve**: It opens a local dashboard where you can approve or skip events.
4.  **Sync**: It automatically updates the data for the public website.

---

## 🌐 Public Link
Your shared dashboard is live here:
**[https://bradenflynn.github.io/free-food/](https://bradenflynn.github.io/free-food/)**

---

## 💼 GSD Business Automation
Run these commands to execute the faceless business engine:

### 1. Generate Social Content
Auto-wraps flyers in VÉLOCE stickers for IG:
```bash
python3 ig_content_gen.py
```

### 2. Send Daily Haul Newsletter
Blasts the current "HAUL" to your subscribers (Configure `.env` first with SMTP details):
```bash
python3 newsletter_engine.py
```

### 3. Monetization (Inner Circle)
Manage your first 10 paying users via the **Buy Me A Coffee** dashboard linked in the UI.

---

## 🛠 Project Structure
- `FreeFoodFinder.command`: The main launcher script (root).
- `frontend/index.html`: The dashboard UI.
- `backend/core/main.py`: Core scraping and AI vision.
- `backend/api/api.py`: Dashboard local API.
- `backend/engines/`: Content generation and newsletter systems.
- `data/config/handles.txt`: Instagram tracking list.
- `data/database/`: Local SQLite storage.
- `data/exports/`: Processed data for frontend.
- `downloads/`: Scraped event flyers.
- `scripts/`: Automation and start scripts.
