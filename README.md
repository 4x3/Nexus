# Nexus

[![GitHub stars](https://img.shields.io/github/stars/4x3/Nexus?style=for-the-badge&color=blue)](https://github.com/4x3/Nexus/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/4x3/Nexus?style=for-the-badge&color=blue)](https://github.com/4x3/Nexus/network/members)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An automated, zero-dependency forensic auditor for mapping local credential surfaces and browser database exposure on Windows environments.

## Architecture & Capabilities

Nexus is designed to operate as a local footprint auditor. It bypasses standard file explorer restrictions to locate, map, and analyze the security posture of local SQLite databases utilized by Chromium and Gecko-based browsers. 

* **Heuristic Discovery:** Automatically maps the `%LOCALAPPDATA%` and `%APPDATA%` environments to locate active and dormant browser installations.
* **Surface Auditing:** Analyzes the exact file paths, OS-level read permissions, and modification metadata of sensitive databases (Login Data, Cookies, Web Data, Local State).
* **Automated Compilation:** Structures all telemetry and system host data into a clean, parsed `.txt` report routed securely to an isolated output directory.
* **Zero-Dependency:** Written entirely with standard Python libraries. Requires no external packages to execute.

## Installation & Deployment

Nexus is built to run natively in the standard Windows Command Prompt. 

1. Clone the repository to your local machine:
```bash
git clone [https://github.com/4x3/Nexus.git](https://github.com/4x3/Nexus.git)
