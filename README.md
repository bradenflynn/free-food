# 🍕 Free Food Finder (FFF)

A tool designed for University of San Diego students to automatically discover, analyze, and share free food events from Instagram.

## 🚀 How to Run

To start the project and update the dashboard, simply run this file from your project folder:

```bash
"/Users/bradenflynn/Downloads/free food/FreeFoodFinder.command"
```

### What happens when you run it:
1.  **Scan**: The script checks the latest Instagram posts for student clubs.
2.  **Analyze**: AI (GPT-4o) scans the flyers for mention of free food.
3.  **Approve**: It opens a local dashboard where you can approve or skip events.
4.  **Sync**: It automatically pushes the findings to your public website.

---

## 🌐 Public Link
Your shared dashboard is live here:
**[https://bradenflynn.github.io/free-food/](https://bradenflynn.github.io/free-food/)**

---

## 🛠 Project Structure
- `FreeFoodFinder.command`: The main launcher script.
- `index.html`: The dashboard UI.
- `main.py`: The brain that coordinates the scan and AI.
- `handles.txt`: The list of Instagram accounts being tracked.
- `downloads/`: Folder containing all current event flyers.
