#!/bin/bash
echo "Clearing stale templates..."
rm -f /workspaces/steno-platform/templates/admin/*.html
echo "Done. Now run: python app.py"
