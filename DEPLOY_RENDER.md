# Deploying to Render.com

Your application is ready for deployment. Follow these steps to get it running live.

## Option 1: Automatic Deployment (Blueprint)

1.  **Sign in to [Render.com](https://render.com)**.
2.  Click **New +** and select **Blueprint**.
3.  Connect your GitHub repository: `abhishekaryavart/computer-lab-monitoring`.
    *   *If you haven't connected GitHub to Render yet, you'll need to authorize it first.*
4.  Render will detect the `render.yaml` file.
5.  **Important:** It will ask for the `MONGO_URI` value.
    *   Paste your **MongoDB Atlas Connection String** here.
    *   *Format:* `mongodb+srv://<username>:<password>@cluster0.example.mongodb.net/lab_monitoring_db?retryWrites=true&w=majority`
6.  Click **Apply**. Render will start building and deploying your app.

## Option 2: Manual Setup

If the Blueprint method fails or you prefer manual control:

1.  **New Web Service:**
    *   Click **New +** -> **Web Service**.
    *   Connect your repository.
2.  **Settings:**
    *   **Name:** `lab-monitoring` (or similar)
    *   **Runtime:** `Python 3`
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `gunicorn app:app`
3.  **Environment Variables:**
    *   Scroll down to "Environment Variables".
    *   Add Key: `MONGO_URI`
    *   Add Value: *(Your MongoDB Atlas Connection String)*
4.  **Deploy:** Click **Create Web Service**.

## Verifying Deployment

Once the build finishes (usually 3-5 minutes), Render will give you a URL (e.g., `https://lab-monitoring.onrender.com`).
Click it to visit your live site!
