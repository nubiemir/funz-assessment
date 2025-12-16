# Funz App Documentation

Welcome to the documentation for **Funz App**, a modern game management application built with Python. This system provides a robust backend API featuring both RESTful endpoints for authentication/administration and a flexible GraphQL API for game data management.

## 📋 Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
- [API Reference](#api-reference)
  - [REST API](#rest-api)
  - [GraphQL API](#graphql-api)
- [Data Models](#data-models)

---

## 🔍 Overview

Funz App is a backend service designed to handle:
- **User Authentication**: Secure signup and login for normal users and admins.
- **Game Management**: Create, read, update, and delete (CRUD) operations for games.
- **Social Features**: Ability for users to "like" games.

It leverages synchronous and asynchronous patterns, utilizing MongoDB for high-performance data storage.

## 🛠 Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance web framework for APIs.
- **GraphQL**: [Strawberry](https://strawberry.rocks/) - Python GraphQL library based on dataclasses.
- **Database**: [MongoDB](https://www.mongodb.com/) - NoSQL database.
- **Driver**: [Motor](https://motor.readthedocs.io/) - Asynchronous Python driver for MongoDB.
- **Validation**: [Pydantic](https://docs.pydantic.dev/) - Data validation and settings management.
- **Authentication**: [PyJWT](https://pyjwt.readthedocs.io/) - JSON Web Token implementation.

## 📂 Project Structure

The project follows a modular structure within the `app` directory:

```text
app/
├── api/                            # REST API Routes
│   └── routes/                     # Endpoint definitions (auth)
│   └── └──auth.py                  # Auth endpoint (signup, login)
├── core/                           # Core application configuration
│   ├── config.py                   # Pydantic settings
│   ├── database.py                 # MongoDB connection logic
│   └── loader.py                   # App factory and middleware
├── enums/                          # Enumerations (e.g., UserType)
│   ├── user_type.py                # User type enum
├── graphql/                        # GraphQL Schema & Resolvers
│   ├── mutations.py                # Write operations
│   ├── queries.py                  # Read operations
│   ├── schema.py                   # Main schema definition
│   └── types.py                    # GraphQL types
├── models/                         # Pydantic Data Models (DB schema)
├── services/                       # Business Logic Layer
│   ├── mongodb_service/            # MongoDB service layer
│   ├── └──mdb_user_service.py      # User service layer
│   └── graphql_service/            # GraphQL service layer
│   └── └──graphql_service/         # GraphQL service layer
└── main.py                         # Application Entry Point
└── Dockerfile                      # Application Docker File
└── docker-compose.yml              # Docker Compose File for (Funz App, Mongodb)
└── doc.md                          # This Documentation
└── requirement.txt                 # Application Requirements
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **MongoDB** running locally on port `27017` (default) or accessible via URI.

### Installation

1.  **Clone the repository** (if applicable).

### Configuration

The application uses `pydantic-settings` to manage configuration. Default values are set in `app/core/config.py`. You can override these using environment variables.

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `APP_NAME` | `Funz App` | Name of the application. |
| `MONGO_URI` | `mongodb://localhost:27017` | Connection string for MongoDB. |
| `MONGO_DB` | `funz` | Database name. |
| `JWT_SECRET` | `appsecret` | Secret key for signing JWT tokens. |
| `JWT_APP_ID` | `appid` | App ID identifier. |

### Running the Application

To start the development server with hot reload enabled:

```bash
docker compose up --build
```

The server will start at `http://127.0.0.1:8000`.

## 📡 API Reference

### REST API

The REST API handles authentication and administrative tasks.

#### Authentication (`/api/auth`)

- **POST** `/api/auth/signup/{user_type}`
  - **Description**: Register a new user.
  - **Parameters**: `user_type` (Enum: `admin`, `user`).
  - **Body**: JSON object with `email` and `password`.
  - **Returns**: Created user object.

- **POST** `/api/auth/login`
  - **Description**: Authenticate a user and receive a token.
  - **Body**: JSON object with `email` and `password`.
  - **Returns**: Access token (JWT).

### GraphQL API

The GraphQL API is available at `/api/graphql`. It is used for all game-related data operations.

#### Queries

- **`game(gameId: String!)`**: Fetch a single game by its unique ID.
- **`games`**: List all available games.

#### Mutations

- **`createGame(gameInput: GameInput!)`**: Create a new game entry.
- **`updateGame(gameId: String!, gameInput: GameInput!)`**: Update an existing game's details.
- **`deleteGame(gameId: String!)`**: Remove a game from the system.
- **`toggleLikeGame(gameId: String!, userId: String!)`**: Toggle a "like" for a game by a specific user.

## 💾 Data Models

### User
Represents a user in the system.
- **Fields**: `id`, `email`, `password` (hashed), `is_admin`.

### Game
Represents a game entity.
- **Fields**:
  - `id`: Unique Identifier (UUID).
  - `name`: Title of the game.
  - `type`: Genre or category.
  - `publisher_name`: Name of the publisher.
  - `external_game_id`: ID from an external system.
  - `description`: Optional text description.
  - `is_featured`: Boolean flag.
  - `cover_image_url`: HTTP URL to the cover art.
  - `trailer`: Optional HTTP URL to the trailer.
  - `collage`: List of image URLs.
  - `likes`: List of User IDs who liked the game.
  - `created_at` / `updated_at`: Timestamps.


