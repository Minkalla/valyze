# Minkalla Valyze

AI-Powered Data Valuation Microservice (Python FastAPI)

## Project Status

[![Under Active Development](https://img.shields.io/badge/status-under%20active%20development-orange)](https://github.com/minkalla/valyze)

This project is currently under active development as part of the Minkalla MVP.

## Overview

Valyze is a foundational component of the Minkalla ecosystem, focused on providing AI-powered insights into the economic value of data. This MVP version implements a pluggable ML model interface to demonstrate basic data valuation and includes minimal provenance logging.

## Features (MVP)

* **Data Valuation API:** `POST /valyze/data` to submit arbitrary data for valuation by a configured ML model.
* **Pluggable ML Model Interface:** Designed to easily swap out different Machine Learning models (e.g., Graph Neural Networks, Recurrent Neural Networks) for valuation.
* **Basic Data Provenance Logging:** Minimal logging of valuation events for auditability.
* **Minimal Schema Registration:** Basic Pydantic schema validation for input data to the valuation API.
* **Health Check:** `GET /health` to verify service operational status.
* **API Documentation:** Built-in Swagger UI for easy API exploration, automatically redirecting from the root URL.
* **Unit Tested:** Core API endpoints and valuation logic are covered by comprehensive unit tests.

## Getting Started

### Prerequisites

* Python 3.10+ and Poetry installed.
* **Recommended for Development:** GitHub Codespaces for a consistent, pre-configured cloud development environment. A `.devcontainer` configuration is included for easy setup.

### Local Development Setup (Using Codespaces)

This project is optimized for development within **GitHub Codespaces**. Your Codespace environment (including Python, `pipx`, and `Poetry`) will be automatically set up for you based on the `.devcontainer` configuration.

**Recommended Codespace Machine Type:**
Due to the size of Python dependencies and the build process, we highly recommend using a **4-core (or higher)** Codespace machine type (e.g., "4-core, 16GB RAM + 32GB Storage") to ensure smooth environment provisioning and avoid "no space left on device" errors. Select this option when creating your Codespace.

**Initial Setup (After Codespace Launches):**

After your Codespace has successfully launched and you see the terminal prompt, you need to install the project-specific Python dependencies. This is a crucial one-time manual step:

1.  **Install Python Dependencies:**
    Navigate to the repository root in your terminal (`/workspaces/valyze`) and run:
    ```bash
    poetry install --no-root
    ```
    This command will install all required packages into your Poetry virtual environment.

### Running the Valyze API Locally

Once your development environment is fully set up (after running `poetry install --no-root`), you can start the FastAPI application:

1.  **Start the Uvicorn Server:**
    From the repository root in your terminal, run:
    ```bash
    PYTHONPATH=. poetry run uvicorn app.main:app --reload --port 3002
    ```
    You should see output indicating the server is running on `http://127.0.0.1:3002`.

2.  **Access the API Documentation (Swagger UI):**
    Open your web browser (via Codespaces Port Forwarding) and navigate to:
    `http://localhost:3002/`

    The API will now automatically redirect you to the interactive Swagger UI at `http://localhost:3002/docs`.

### API Endpoints

All API endpoints are documented in the Swagger UI. Here's a quick overview:

#### `POST /valyze/data`

Submits data for AI-powered valuation.

* **Method:** `POST`
* **URL:** `/valyze/data`
* **Request Body (JSON):**

    ```json
    {
      "input_data": {
        "data_id": "string",
        "category": "string",
        "value_points": {
          "property1": "any",
          "property2": "any"
        },
        "is_sensitive": "boolean",
        "source": "string"
      }
    }
    ```

* **Example Request (using `curl`):**

    ```bash
    curl -X POST http://localhost:3002/valyze/data \
    -H "Content-Type: application/json" \
    -d '{
      "input_data": {
        "data_id": "customer_record_42",
        "category": "sales_lead",
        "value_points": {
          "customer_segment": "enterprise",
          "engagement_score": 95,
          "region": "NA"
        },
        "is_sensitive": true,
        "source": "CRM"
      }
    }'
    ```

    *The response will contain `valuation_score`, `confidence_score`, and other model details.*

#### `GET /health`

Checks the health of the service.

* **Method:** `GET`
* **URL:** `/health`
* **Example Request (using `curl`):**

    ```bash
    curl http://localhost:3002/health
    ```

## Running Tests

To execute the unit tests for Valyze:

1.  **Run Pytest:**
    From the repository root in your terminal, run:
    ```bash
    PYTHONPATH=. poetry run pytest
    ```
    All tests should pass, and you will see a summary of the test results.

## Contribution

We welcome contributions! Please see our central [CONTRIBUTING.md](../.github/CONTRIBUTING.md) guidelines to get started.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Security

For information on reporting security vulnerabilities, please refer to our [SECURITY.md](SECURITY.md) policy.

---

Part of the [Minkalla](https://github.com/minkalla) open-source ecosystem.
