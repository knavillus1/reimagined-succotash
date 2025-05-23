
# Contributor Guide

## CODEX Dev Environment Tips

Do NOT Run `install.sh` this script, which references `requirements.txt`. This script will be executed during environement setup for you. You can reference`install.sh` and `requirements.txt` to review causes of dependency issues and update these files as needed to address, but the effects will not take place until the next task session.

Do NOT attempt to run any command which requires open network communication.  Your Dev environment is isolated for safety.

## Style Instructions

## Testing Instructions

## CHANGELOG/DEVELOPMENT Instructions
Append a single line summary to CHANGELOG.md describing the changes with a preceeding timestamp
if errors were encountered, list them indented below the changelog row with a single line summary

When components are added that require manual application startup for local testing/debug, document all steps and commands neccessary to set up the local environment and start services/components in DEVELOPMENT.md using explcit commands.  These changes will need to be mirrored on dev.sh (see below), which is a one-stop script to set up the environment from scratch and start the application for local testing.

## README

README.md just describes the project.  Do not look here for guidance on how to proceed with your task, but update if major changes that affect user interaction have been made.
## PR instructions


## dev.sh startup script
When there are code changes that need targeted environment setup, review dev.sh and modify as needed to completely setup the application and start it.  