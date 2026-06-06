# Portfolio — Customization Guide

## 1. Personal Info (Name, Bio, Experience, Skills, Titles)

Edit **`app/translations/en.json`** (English) and **`app/translations/fr.json`** (French).

| Key | What it is |
|---|---|
| `site.author` | Your full name (appears everywhere) |
| `site.title` | Site title in the browser tab |
| `sidebar.subtitle` | Tagline under your name (e.g. "Python & AI Developer") |
| `hero.title1`, `title2`, `title3` | Hero section headline |
| `hero.description` | Hero section paragraph |
| `about.bio1`, `bio2`, `bio3` | About page bio paragraphs |
| `about.exp1_title`, `exp1_company`, `exp1_desc` | Experience 1 |
| `about.exp2_title`, `exp2_company`, `exp2_desc` | Experience 2 |
| `about.exp3_title`, `exp3_company`, `exp3_desc` | Experience 3 |
| `about.education_title`, `education_school` | Education entry |
| `about.skill_*` | Skill names in the About page sidebar |
| *All other keys* | UI labels, buttons, project descriptions |

> **Add/remove experience blocks?** Edit `app/templates/about.html` lines 25-40.

---

## 2. Social Links & Email

**`app/templates/components/sidebar.html`**

| Line | What to change |
|---|---|
| 50 | GitHub URL (`https://github.com/your-username`) |
| 53 | LinkedIn URL (`https://linkedin.com/in/your-profile`) |
| 56 | Email (`mailto:you@example.com`) |
| 6 | Initials avatar (`JD` → your initials) |

---

## 3. CV Upload

```powershell
curl.exe -X POST -F "file=@C:\path\to\your-cv.pdf" http://localhost:8000/api/cv/upload
```

Only PDF, max 10 MB. Uploaded CV replaces any previous one. View it via the "View CV / Resume" button in the sidebar.

---

## 4. Contact Form — Email Notification

Edit **`.env`**:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_TO=you@example.com
EMAIL_FROM=your-email@gmail.com
```

- Gmail: use an [App Password](https://myaccount.google.com/apppasswords) (enable 2FA first)
- Other providers: use their SMTP (Outlook, Yahoo, etc.)

If `SMTP_HOST` is empty, email is skipped (messages still saved to DB).

### View stored messages

```powershell
python -c "import sqlite3; c=sqlite3.connect('portfolio.db'); [print(r) for r in c.execute('SELECT name, email, subject, message, created_at FROM contact_messages').fetchall()]"
```

Or open `portfolio.db` with any SQLite browser.

---

## 5. Site Config & Styling

| File | What it controls |
|---|---|
| `.env` | Database URL, secret key, app name, SMTP config |
| `app/config.py` | Default settings & upload directory |
| `app/static/css/style.css` | Custom CSS overrides |
| `app/static/js/main.js` | Theme toggling, language switching, sidebar, CV modal |

---

## 6. Projects Content

Project descriptions live in **`app/translations/en.json`** and **`fr.json`** under the `featured.*`, `projects.*`, `rag.*`, `anomaly.*`, and `n8n.*` keys.

Project detail templates (HTML structure):
- `app/templates/project_rag.html`
- `app/templates/project_anomaly.html`
- `app/templates/project_n8n.html`

To add a new project, duplicate one of those templates and add a route in `app/routes/pages.py`.

---

## 7. Running the App

```powershell
python run.py
```

Opens at **http://localhost:8000** with auto-reload on file changes.
