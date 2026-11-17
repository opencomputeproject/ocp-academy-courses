# OCP Academy pages (`gh-pages` branch)

This branch holds only the web pages GitHub Pages publishes for OCP Academy. The course sources stay on `main`.

- **Feedback survey:** `feedback/index.html` → https://opencomputeproject.github.io/ocp-academy-courses/feedback/
- **Backend:** `apps-script/Code.gs` is a copy of the Google Apps Script bound to the survey's response Sheet ("OCP Academy Feedback Survey … (Responses)", tab **Submissions**). Answers are saved there; respondents get a branded thank-you email.

## Changing the survey
1. Edit `FIELDS` / `CONFIG` in the Apps Script editor (and keep this copy in step).
2. Deploy → Manage deployments → pencil → Version: **New version** → Deploy (the `/exec` URL stays the same).
3. The page reads its questions from the backend, so it usually needs no change. If you do change `feedback/index.html`, browsers may cache it for ~10 minutes; check with `?v=2`.

`ENDPOINT` near the bottom of `feedback/index.html` must hold the web app's `/exec` URL. Nothing secret lives in this repository: the `/exec` URL is public by design, and the edit-link secret is kept in the script's properties.
