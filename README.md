
## Local frontend

This fork serves the timeline from `front_end/timelinev2.html` through `main.py`.
Generated ranking JSON files live in `front_end/data`.

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
