# HOW TO DEPLOY YOUR WEBSITE FOR FREE (0 COST)

You can host your "NASA Level" website for free using **Netlify** or **Vercel**. It takes 2 minutes.

## Option 1: Netlify (Easiest)
1.  Go to [Netlify Drop](https://app.netlify.com/drop).
2.  Open your file explorer to `e:\Anti-Lust app\`.
3.  Drag and drop the `website` folder onto the Netlify page.
4.  **Done!** Netlify will give you a live URL (e.g., `https://orbital-defense-123.netlify.app`).

## Option 2: GitHub Pages (Best for Updates)
1.  Create a new repository on GitHub (e.g., `anti-lust-website`).
2.  Upload your `index.html` file to the repository.
3.  Go to **Settings > Pages**.
4.  Under "Source", select `main` branch.
5.  **Done!** Your site will be at `https://yourusername.github.io/anti-lust-website`.

## IMPORTANT: Connecting to Backend
Since your backend runs on your computer (localhost), the website needs to know where to send requests.
- For a **local demo**, the website works as-is.
- For **remote control** (Parent App), you would need to host the backend on a cloud server (like Render, Railway, or AWS), which usually costs money for high-performance ML.
- **Recommendation**: Keep the backend running on your powerful PC for the "0 Lies" ML performance, and use the website as a local dashboard or control panel.
