
## Local frontend

This fork serves the timeline from `front_end/timeline.html` through `main.py`
(`timelinev2.html` stays as a redirect for previously bookmarked links).
Generated ranking JSON files live in `front_end/data`.

### Frontend build (required after editing frontend source)

The timeline React app source is `front_end/src/app.jsx`; the pages load
precompiled `front_end/dist/app.js` + `app.css` (no CDNs, no in-browser Babel).
After changing `app.jsx`, any Tailwind classes, or `tailwind.config.js`, run:

```bash
python scripts/build_frontend.py
```

The built files are committed to git, so the server only needs `git pull`
(no Node toolchain required there — locally Node comes from the
`nodejs-wheel-binaries` pip package).

Server tuning notes (Apache, cron updater, log rotation) live in
[SERVER_OPS.md](SERVER_OPS.md).

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the local frontend/API server:

```bash
python main.py
```

3. Open a boss/spec URL, for example:

```text
http://127.0.0.1:5000/?boss=vamp-fatale&spec=scholar-scholar
```

## Local FRU Dark Knight debug

1. Put this in project-root `.env`:

```env
WCL_CLIENT_ID=...
WCL_CLIENT_SECRET=...
```

2. Run:

```bash
python scripts/debug_darkknight_fru.py
```

3. Start frontend:

```bash
python main.py
```

4. Open:

```text
http://127.0.0.1:5000/?boss=futures-rewritten&spec=darkknight-darkknight
```

## Local Dancing Mad Astrologian debug

1. Put this in project-root `.env`:

```env
WCL_CLIENT_ID=...
WCL_CLIENT_SECRET=...
```

2. Run:

```bash
python scripts/debug_astrologian_dancing_mad.py
```

3. Start frontend:

```bash
python main.py
```

4. Open:

```text
http://127.0.0.1:5000/?boss=dancing-mad&spec=astrologian-astrologian
```
