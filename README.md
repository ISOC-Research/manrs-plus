# MANRS+ tool (Supply-chain security)

[![Project Logo](logo.png)](https://www.manrs.org/wp-content/themes/manrs/assets/images/logo-black.svg)

The aim of this tool is to be able to have the supply chain of an ASN
belonging to a category and a country and to check the routing security
status of each of the ASNs.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Project Overview

The aim of this tool is to be able to have the "supply chain" of an ASN
belonging to a category and a country and to check the routing security
status of each of the ASNs.

## Features

List the key features or functionalities of your project.
- SCRIPT: Script for downloading files to populate the database
- API with FASTAPI
- Web GUI

## Getting Started

Provide instructions on how to set up the project locally. This section should include prerequisites and installation steps.

### Prerequisites Backend and script

List the software, libraries, and tools that need to be installed before setting up your project.

- Prerequisite 1: Python 3.10+
- Prerequisite 2: Install virtualenv for Ubuntu: `apt-get install virtualenv`


### Installation

1. Clone the repository
2. Create a virtualenv: `python3 -m venv {{env}}` and activate your environment.
3. Navigate to the project directory: `cd <project_folder>`
4. Install dependencies: `pip install -r api/requirements.txt` and `pip install -r script/requirements.txt`
5. Navigate to the project directory: `cd backend/api`
6. Run shell: `python -m fastapi_shell`
7. Run: `from load import *`
8. Run: `load_relationship_asn()`, `load_data_as_mapping()`, `load_categorized_asn()`, `load_nro_data()`, `load_manrs_data()`
9. Exit shell: `exit()`
8. Run the API: `python main.py`

## Usage

Go to the documentation at URL: `http://0.0.0.0:8000/docs`

## Contributing

Explain how others can contribute to your project. Include guidelines for submitting issues, pull requests, and any coding standards you'd like contributors to follow.

## License

This project is licensed under the [MIT License](LICENSE).
