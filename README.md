# Gmail Email Fetcher Script

This repository contains a standalone script that fetches emails from the Gmail API, stores them in a database, and applies rules specified in `rules.json`.

## Prerequisites

- A `credentials.json` file containing client secret keys for Google OAuth. This file is necessary for authentication and authorization with the Gmail API.

## Setup Instructions

1. **Obtain `credentials.json`**: 
   - Follow Google's [guide](https://developers.google.com/workspace/guides/create-credentials) to create and download the `credentials.json` file.
   - Place the `credentials.json` file in the root directory of the project.

2. **Run the script**:
   - Make sure the `runscript.sh` executable bash script is in the project root directory.
   - This script will:
     - Create a virtual environment.
     - Install the required dependencies.
     - Run test cases.
     - Start the main script.

   ```bash
   source runscript.sh
    ```

3. **First-time setup**:
    - On the first run, you will be prompted to log in using your Google account.
    - It's recommended to use a backup/secondary account for authorization.
    - After logging in, you will be asked to grant permission to the script to access your Gmail account.
    - Click on `Allow` to grant the necessary permissions.

4. **Token Storage**
    - After authorization, a `token.json` file will be saved in the current directory.
    - This file will be used for subsequent authorizations.
    - Ideally, this token should be stored in a database linked to a user for better security.

5. **Database**
    - Emails will be fetched and stored using SQLite as the database engine.
    - Ensure the database is set up correctly by following the instructions in the `core/database.py` file.

6. **Rules**
    - Update `rules.json` as required.
    - The script will apply the predefined rules from this file while running.

7. **Logging**
    - The script includes appropriate print statements for logging the process.
    - Monitor the console output to track the script's progress and actions.


## Folder Structure

```bash
core/
|---- database.py       # Initializes SQLite DB engine using SQLAlchemy
|---- models.py         # Defines Mail model and imports DB from database.py
|---- queries.py        # Executes queries using DB from database.py
|---- rules.py          # Applies rules from rules.json, updates DB, imports api.py from gmail module
gmail/
|---- oauth.py          # Implements Google's OAuth to get tokens, stores tokens in token.json
|---- gmail.py          # Fetches emails using Google Python API client, uses authorize method from oauth.py
|---- api.py            # Makes API calls to add labels to mail using credentials from oauth.py
main.py                 # Fetches emails, stores them in the DB, processes emails based on rules, performs actions using REST API
runscript.sh            # Bash script to set up environment, install dependencies, run tests, and start the script
credentials.json        # Client secret keys for Google OAuth (to be placed in root directory)
token.json              # OAuth token file (generated after first authorization)
rules.json              # JSON file containing rules to apply to fetched emails

```
