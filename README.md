# Band-to-Gvoice

A Python service that polls the Band API for new notifications and sends them as SMS via Google Voice.

## Deployment

This app is designed to run as a **worker** on modern PaaS platforms such as **Render**, **Railway**, or **Heroku**.

---

## Render Setup Instructions

Render makes it easy to deploy always-on background workers. Here’s how to set up this project on Render’s free tier:

### 1. Fork or Clone the Repo
Push this repository to your own GitHub account if you haven’t already.

### 2. Create a New Background Worker in Render
- Go to [https://dashboard.render.com/](https://dashboard.render.com/)
- Click **New > Background Worker**
- Connect your GitHub account and select your repository

### 3. Configure the Worker
- **Name:** Choose a name for your worker (e.g., Band-to-Gvoice)
- **Environment:** Python 3.x is detected automatically
- **Start Command:**
  ```
  python band_to_gvoice.py
  ```

### 4. Add Environment Variables
Set the following variables via the Render dashboard (under Environment tab):
- `BAND_ACCESS_TOKEN`
- `BAND_BAND_KEY`
- `GV_EMAIL`
- `GV_PASSWORD`
- `SMS_TARGET_NUMBER`

### 5. Deploy
- Click **Create Background Worker**
- The worker will build, install dependencies, and start automatically

### Notes
- The script writes IDs to `sent_notifications.txt` to ensure notifications are not sent multiple times. This file is stored on ephemeral Disk and may reset if the worker is redeployed, restarted, or moved.
- For true persistence, consider integrating a simple cloud database or remote storage.

---

## Manual Setup (Any PaaS or VM)

1. Clone the repository
2. Run `pip install -r requirements.txt`
3. Create environment variables as above (or use a `.env` with `python-dotenv`)
4. Execute: `python band_to_gvoice.py`

---

## Security

**Never** commit real API credentials or Google Voice passwords to your repository. Use only platform environment variables.
