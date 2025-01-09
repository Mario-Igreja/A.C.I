#!/bin/bash

set -e  # Finaliza o script em caso de erro

SOURCE="/app/tinydb/db1.json"
DEST="/app/tinydb/db2.json"

while true; do
  if [ -f "$SOURCE" ]; then
    rsync -avz --ignore-errors "$SOURCE" "$DEST"
    echo "Sincronização concluída: $(date)"
  else
    echo "Arquivo fonte não encontrado: $SOURCE"
  fi
  sleep 10  # Aguarda 10 segundos antes da próxima sincronização
done
