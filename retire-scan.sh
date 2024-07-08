#!/bin/bash

prompt_for_path() {
  read -p "Enter the file or directory path to scan: " FILE_PATH
  if [ -z "$FILE_PATH" ]; then
    echo "No path provided. Exiting."
    exit 1
  fi
}

prompt_for_path

if ! command -v retire &> /dev/null; then
  echo "Retire.js is not installed. Installing it now..."
  npm install -g retire
fi

echo "Running Retire.js scan on $FILE_PATH..."
retire --path $FILE_PATH

if [ $? -eq 0 ]; then
  echo "Scan completed successfully."
else
  echo "An error occurred during the scan."
fi

