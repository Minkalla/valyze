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
* **API Documentation:** Built-in Swagger UI for easy API exploration.
* **Unit Tested:** Core API endpoints and valuation logic are covered by comprehensive unit tests.

## Getting Started

### Prerequisites

* Python 3.10+ and Poetry installed.
* (Optional but Recommended for Development): GitHub Codespaces for a pre-configured cloud development environment. A `.devcontainer` configuration is included for easy setup.

### Local Development Setup (Using Codespaces)

If you are using GitHub Codespaces, the environment (Python, Poetry, etc.) will be automatically set up for you based on the `.devcontainer` configuration. The `postCreateCommand` will automatically install Python dependencies (`poetry install`).

1.  **Launch Codespace:**
    Go to your [Valyze GitHub repository](https://github.com/minkalla/valyze), click the green `< > Code` button, select the `Codespaces` tab, and launch your Codespace.
2.  **Verify Setup (Optional):**
    Once the Codespace loads, you can verify installations in the terminal:

    ```bash
    python3 --version
    poetry --version
    ```

    You should see their respective versions.
3.  **Run the FastAPI Application:**
    Navigate to the Valyze repository root directory and start the server:

    ```bash
    poetry run uvicorn app.main:app --reload --port 3002 --app-dir app/
    ```

    You should see output indicating the server is running on `http://127.0.0.1:3002`.
4.  **Access API Documentation:**
    Open your web browser and navigate to `http://localhost:3002/docs` (or the Codespaces forwarded URL ending in `/docs`). You will see the interactive Swagger UI.

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

To run the unit tests for Valyze:

```bash
poetry run pytest
```

## Contribution

We welcome contributions! Please see our central [CONTRIBUTING.md](../.github/CONTRIBUTING.md) guidelines to get started.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Security

For information on reporting security vulnerabilities, please refer to our [SECURITY.md](SECURITY.md) policy.

---

Part of the [Minkalla](https://github.com/minkalla) open-source ecosystem.
