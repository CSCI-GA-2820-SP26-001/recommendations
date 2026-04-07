# Recommendations Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![CI Build](https://github.com/CSCI-GA-2820-SP26-001/recommendations/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP26-001/recommendations/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP26-001/recommendations/branch/master/graph/badge.svg)](https://codecov.io/gh/CSCI-GA-2820-SP26-001/recommendations)

## Squad: Recommendations

| Name | Email | GitHub |
|------|-------|--------|
| Rasmika Billa | rb5719@nyu.edu | [@Rasmika-b](https://github.com/Rasmika-b) |
| Tess Fairbanks | tmf8970@stern.nyu.edu | [@tess-fair](https://github.com/tess-fair) |
| Johnny O'Keefe | jmo7754@stern.nyu.edu | [@Javvns](https://github.com/Javvns) |
| Drew Adler | da3978@stern.nyu.edu | [@Dadler27](https://github.com/Dadler27) |
| Jenny Lim | jjl10010@stern.nyu.edu | [@jjl10010-cmd](https://github.com/jjl10010-cmd) |

---

## Overview

The **Recommendations Service** is a REST API that represents a product recommendation based on another product. In essence it is a relationship between two products that "go together" (e.g., radio and batteries, printers and ink, shirts and pants, etc.). It can also recommend based on what other customers have purchased — for example, "customers who bought item A usually buy item B".

Recommendations have a **recommendation type** such as cross-sell, up-sell, or accessory, allowing a product page to request all up-sells or cross-sells for a given product:

- **Up-sell** — a more full-featured and expensive product recommended instead of the one initially selected
- **Cross-sell** — other items similar to the selected product in features and price
- **Accessory** — complementary items that go with the selected product

Recommendation types are represented using **Python enumerations**.

**Service URL:** `/recommendations`

---

## Data Model

### Recommendation

| Field                    | Type               | Description                                       |
|--------------------------|--------------------|---------------------------------------------------|
| `id`                     | Integer (PK)       | Auto-generated unique identifier                  |
| `source_product_id`      | Integer            | The product being viewed / origin product         |
| `recommended_product_id` | Integer            | The product being recommended                     |
| `recommendation_type`    | Enum               | Type of recommendation (see below)                |
| `created_at`             | DateTime           | Timestamp when the record was created             |
| `updated_at`             | DateTime           | Timestamp when the record was last updated        |

### RecommendationType Enum

| Value        | Description                                       |
|--------------|---------------------------------------------------|
| `CROSS_SELL` | Recommend a related product from another category |
| `UP_SELL`    | Recommend a higher-end version of the product     |
| `ACCESSORY`  | Recommend an accessory for the product            |

### Constraints

- A product **cannot recommend itself** (`source_product_id != recommended_product_id`)
- The combination of `source_product_id`, `recommended_product_id`, and `recommendation_type` must be **unique**

---

## API Endpoints

**Base URL:** `http://localhost:8080`

| Method   | Endpoint                    | Description                        | Status Code      |
|----------|-----------------------------|------------------------------------|------------------|
| `GET`    | `/`                         | Root URL — service metadata        | `200 OK`         |
| `GET`    | `/recommendations`          | List all recommendations           | `200 OK`         |
| `GET`    | `/recommendations/<id>`     | Read a single recommendation       | `200 OK`         |
| `POST`   | `/recommendations`          | Create a new recommendation        | `201 CREATED`    |
| `PUT`    | `/recommendations/<id>`     | Update an existing recommendation  | `200 OK`         |
| `DELETE` | `/recommendations/<id>`     | Delete a recommendation            | `204 NO CONTENT` |

### Query Parameters for LIST

| Parameter              | Description                                   | Example                           |
|------------------------|-----------------------------------------------|-----------------------------------|
| `recommendation_type`  | Filter by type (`CROSS_SELL`, `UP_SELL`, etc) | `?recommendation_type=CROSS_SELL` |
| `source_product_id`    | Filter by source product id                   | `?source_product_id=1`            |

---

## Contents

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to fix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - Recommendation model and DB logic
├── routes.py              - REST API endpoints
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - RecommendationFactory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for the Recommendation model
└── test_routes.py         - test suite for service routes
```

---

## Automatic Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
cp .gitignore  ../<your_repo_folder>/
cp .flaskenv ../<your_repo_folder>/
cp .gitattributes ../<your_repo_folder>/
```

---

## Running the Tests

```bash
make test
```

This runs all unit and integration tests with coverage reporting. The minimum coverage we achieved is **96.49%**.

---

## License

Copyright (c) 2016, 2025 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
