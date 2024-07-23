# Static Site Generator

Python-based static site generator takes in Markdown files, converts them to HTML, and serves them on a built-in Python server.

## Overview
- src/
Our python code is going to be in this directory.
Output will be in static dir.
- ==> content/*.md
- ==> template.html
- static/
The output directory with the final HTML & CSS.
- <==> File Server
- python -m http.server port
Serves the static files
- ==> Browser Renderer

## Tech Stack
- Python 3