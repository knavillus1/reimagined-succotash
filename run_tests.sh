#!/usr/bin/env bash
set -euo pipefail

# Set required Azure environment variables with sane defaults
# These are needed for the integration tests to run.

echo "Setting Azure environment variables for tests..."

: "${AZURE_TABLES_ACCOUNT_URL:=https://knavillus10portfoliostrg.table.core.windows.net}"
: "${AZURE_TABLES_TABLE_NAME:=projects}"
: "${AZURE_BLOB_STORAGE_ACCOUNT_URL:=https://knavillus10portfoliostrg.blob.core.windows.net}"
: "${AZURE_BLOB_CONTAINER_NAME:=images}"

export AZURE_TABLES_ACCOUNT_URL
export AZURE_TABLES_TABLE_NAME
export AZURE_BLOB_STORAGE_ACCOUNT_URL
export AZURE_BLOB_CONTAINER_NAME

echo "Running pytest..."
# Pass all arguments received by this script to pytest
pytest "$@"
