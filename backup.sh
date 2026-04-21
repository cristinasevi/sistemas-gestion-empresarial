#!/bin/bash

set -euo pipefail

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILENAME="${BACKUP_DIR}/erp_${TIMESTAMP}.sqlite3"
SOURCE="./db.sqlite3"

if [ ! -f "$SOURCE" ]; then
    echo "ERROR: No se encontró $SOURCE"
    exit 1
fi

mkdir -p "$BACKUP_DIR"

cp "$SOURCE" "$FILENAME"

SIZE=$(du -sh "$FILENAME" | cut -f1)
echo ">>> Backup completado: ${FILENAME} (${SIZE})"

# Rotar: conservar solo los últimos 7 backups
TOTAL=$(ls -1 "${BACKUP_DIR}"/*.sqlite3 2>/dev/null | wc -l)
if [ "$TOTAL" -gt 7 ]; then
    ls -1t "${BACKUP_DIR}"/*.sqlite3 | tail -n +8 | xargs rm -f
    echo ">>> Backups antiguos eliminados"
fi
