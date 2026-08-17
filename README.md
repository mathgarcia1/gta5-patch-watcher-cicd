# GTA 5 Patch Watcher

[![CI](https://github.com/mathgarcia1/gta5-patch-watcher-cicd/actions/workflows/ci.yml/badge.svg)](https://github.com/mathgarcia1/gta5-patch-watcher-cicd/actions/workflows/ci.yml)
[![Patch Watcher](https://github.com/mathgarcia1/gta5-patch-watcher-cicd/actions/workflows/watch.yml/badge.svg)](https://github.com/mathgarcia1/gta5-patch-watcher-cicd/actions/workflows/watch.yml)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-blue)

A small CI/CD project that automatically monitors **Grand Theft Auto V patches for PS4**, detects changes and creates a Pull Request whenever a new patch is found.

The project was created as a practical exercise to learn **Python, web scraping, APIs, Git, automated testing and GitHub Actions CI/CD**.

## How it works

The watcher monitors the GTA V PS4 title:

```text
CUSA00411
```

The source used by the project is:

```text
ORBISPatches
```

The workflow follows this process:

```text
ORBISPatches
      |
      v
Python watcher
      |
      v
Fetch current patch
      |
      v
Generate latest_patch.json
      |
      v
git diff
      |
      v
Did the patch change?
   /          \
 no            yes
 |              |
stop       bot branch
                |
              commit
                |
               push
                |
          Pull Request
                |
                v
             CI tests
```

## Patch detection

The project first loads the game page and extracts the parameters required by the internal patch API.

```text
GET /CUSA00411
```

The page contains a dynamic element with parameters such as:

```python
{
    "titleid": "CUSA00411",
    "key": "..."
}
```

Those parameters are then used to request the patch information:

```text
POST /api/internal/loadpatches
```

The API returns structured patch data including:

```json
{
  "is_latest": true,
  "version": "01.57",
  "filesize": "49.3GB",
  "required_firmware": "13.52",
  "creation_date": "2026-07-09",
  "changelog_preview": "..."
}
```

The latest patch is normalized and stored in:

```text
data/latest_patch.json
```

Example:

```json
{
  "version": "01.57",
  "filesize": "49.3GB",
  "required_firmware": "13.52",
  "creation_date": "2026-07-09",
  "changelog_preview": "The Kortz Center Heist update in GTA Online, alongside several upgrades, experience improvements and bug fixes."
}
```

## Change detection

The Python script does not decide whether a patch is new.

Instead, it always generates the **current state**.

Git is responsible for detecting whether that state changed:

```bash
git diff --quiet -- data/latest_patch.json
```

This creates a clean separation of responsibilities:

```text
Python
  |
  +--> discovers the current state

Git
  |
  +--> detects differences

GitHub Actions
  |
  +--> reacts to differences
```

## CI

The CI workflow runs automatically on:

```text
push
pull_request
```

It:

```text
checks out the repository
        |
        v
configures Python 3.12
        |
        v
installs dependencies
        |
        v
runs pytest
```

Tests can also be executed locally:

```bash
python -m pytest -v
```

The CI workflow is located at:

```text
.github/workflows/ci.yml
```

## Automated patch watcher

The patch watcher can be executed manually through:

```text
GitHub
→ Actions
→ GTA 5 Patch Watcher - Watch
→ Run workflow
```

It is also scheduled to run automatically once per day:

```text
09:00 America/Sao_Paulo
```

The workflow is located at:

```text
.github/workflows/watch.yml
```

## Automatic Pull Requests

When a new patch is detected, GitHub Actions uses the branch:

```text
bot/patch-update
```

The automation then:

```text
creates or updates bot/patch-update
        |
        v
creates a commit
        |
        v
pushes the branch
        |
        v
checks for an existing PR
        |
        +-- exists --> reuse it
        |
        +-- missing --> create a new PR
```

Automated commits are created by:

```text
github-actions[bot]
```

This makes it easy to distinguish automated changes from human commits.

## Duplicate protection

The workflow avoids creating duplicate Pull Requests.

If an open PR already contains the latest patch:

```text
main = 01.56

bot/patch-update = 01.57

ORBISPatches = 01.57
```

the workflow detects that the bot branch already contains the desired state and skips creating another commit.

```text
Bot branch already contains the current patch.
```

The existing Pull Request is reused.

## Concurrency protection

Only one watcher execution is allowed to modify the bot branch at a time:

```yaml
concurrency:
  group: gta5-patch-watcher
  cancel-in-progress: false
```

This prevents a scheduled execution and a manual execution from attempting to update the same branch simultaneously.

## Project structure

```text
gta5-patch-watcher-cicd/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── watch.yml
│
├── data/
│   └── latest_patch.json
│
├── tests/
│   └── test_watcher.py
│
├── watcher.py
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Running locally

Clone the repository:

```bash
git clone https://github.com/mathgarcia1/gta5-patch-watcher-cicd.git
cd gta5-patch-watcher-cicd
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the watcher:

```bash
python watcher.py
```

Run the tests:

```bash
python -m pytest -v
```

## Technologies

* Python 3.12
* Requests
* BeautifulSoup
* Pytest
* Git
* GitHub Actions
* GitHub CLI
* REST APIs

## What this project demonstrates

This project is intentionally small, but demonstrates several concepts used in real automation systems:

* HTTP requests
* HTML parsing
* discovering and consuming internal APIs
* JSON normalization
* deterministic snapshots
* automated testing
* Continuous Integration
* scheduled workflows
* change detection with Git
* automated commits
* automated branch management
* automated Pull Requests
* idempotent workflows
* concurrency control

The same architecture could be adapted to monitor other kinds of information, such as:

```text
software releases
game patches
regulatory documents
environmental legislation
public datasets
documentation changes
```

The monitored source changes, but the CI/CD pipeline can remain largely the same.

## Disclaimer

This project is intended for educational purposes.

ORBISPatches and Grand Theft Auto V are owned by their respective owners. This repository is not affiliated with Rockstar Games, Sony Interactive Entertainment or ORBISPatches.
