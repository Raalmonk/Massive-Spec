
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
