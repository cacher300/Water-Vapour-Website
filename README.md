# Water Vapour Games

A small Flask website with a home page and a collection of game pages.

## Run locally

Install Python 3.9 or newer, then run these commands from this folder:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py main.py
```

Open <http://127.0.0.1:5000> in your browser. Stop the server with `Ctrl+C`.

You can set `HOST` and `PORT` environment variables when running the app on a
hosted service. The homepage and game pages do not require API keys.
