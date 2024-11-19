# Django Channels Demo: Pybites Helpdesk App

This is an experimental project demonstrating Django Channels by building a Pybites Helpdesk app.

The app allows users to:

- Create tickets for support.
- Chat with the support team in dedicated real-time chat rooms.

## Features

- Real-time WebSocket-powered chat using Django Channels.
- Ticket-based support system with dedicated chat rooms.

## Getting Started

### Prerequisites

- Python 3.12+ (what I used, >= 3.10 should also work I think)
- Docker (for running Redis)

### Installation

1. Clone this repo and cd into it.

2. Install dependencies in venv: `uv sync`

3. Migrate db: `uv run python manage.py migrate`

4. Start the server: `uv run python manage.py runserver` (daphne controls the websocket server)

5. Run Redis: `docker run -it --rm --name redis -p 6379:6379 redis`

6. Access the app: [http://localhost:8000](http://localhost:8000)

## Possible Enhancements

- Add user authentication for role-based access (e.g., Support vs. Customers).

- Implement login and sign-up functionality.

- Improve styling with Tailwind CSS or similar frameworks.
