# AI Data Analyst

A full-stack application that provides an interactive interface for data analysis and visualization, powered by AI.

## Overview

This application combines a modern React frontend with a Python backend to create an intelligent data analysis platform. It features real-time data visualization, interactive charts, and AI-powered insights.

## Features

- Interactive data visualization with multiple chart types:
  - Line charts (single and multiple series)
  - Bar charts (vertical and horizontal)
  - Stacked bar charts with tooltips
  - Area charts with gradients
- Real-time data analysis
- AI-powered insights and recommendations
- Responsive and modern UI
- Redux state management
- RESTful API integration

## Tech Stack

### Frontend
- React.js
- Redux Toolkit for state management
- Recharts for data visualization
- Tailwind CSS for styling
- Shadcn UI components

### Backend
- Python
- FastAPI
- SQLAlchemy (for database operations)
- Docker for containerization

## Project Structure
```
ai_data_analyst/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── components/
│   │   │   │   ├── BarChart.jsx
│   │   │   │   ├── LineChart.jsx
│   │   │   │   ├── LineChartMultiple.jsx
│   │   │   │   ├── Tooltip.jsx
│   │   │   │   ├── Message.jsx
│   │   │   │   ├── InputBox.jsx
│   │   │   │   ├── ChatArea.jsx
│   │   │   │   └── ...
│   │   │   └── ...
│   │   ├── store/
│   │   │   └── store.js
│   │   ├── http/
│   │   │   └── http.js
│   │   └── ...
│   └── ...
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── agents/
│   │   │   ├── orchestrator.py
│   │   │   ├── sql_agent.py
│   │   │   ├── formatter_agent.py
│   │   │   └── analyst_agent.py
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   └── ...
└── docker-compose.yaml
```

## Component Functionality

### Frontend Components

#### http.js
- Handles all HTTP communication with the backend
- Provides functions for sending user input and receiving responses
- Manages API endpoints for data analysis requests
- Integrates with Redux store for state management

#### InputBox.jsx
- Provides the user input interface
- Manages text input state
- Handles message submission
- Integrates with Redux for message dispatch
- Maintains conversation context

#### ChatArea.jsx
- Displays the conversation history
- Renders different types of messages (text, charts, tables)
- Manages message layout and styling
- Integrates with Redux for message state

#### Redux Store (store.js)
- Manages application state
- Handles message history
- Provides selectors for message access
- Manages chart and visualization data
- Implements message dispatch actions

### Backend Components

#### Server (server.py)
- FastAPI application entry point
- Handles CORS configuration
- Manages API endpoints
- Routes requests to appropriate agents
- Processes user input and returns responses

#### Orchestrator Agent (orchestrator.py)
- Coordinates the flow between different agents
- Manages the conversation pipeline
- Handles database connections
- Routes queries to appropriate agents
- Formats and returns final responses

#### SQL Agent (sql_agent.py)
- Generates SQL queries from natural language
- Interacts with the database
- Handles query execution
- Manages error handling and retries
- Validates query results

#### Formatter Agent (formatter_agent.py)
- Evaluates user questions
- Determines if SQL generation is needed
- Provides direct answers for simple queries
- Formats responses for better understanding
- Manages conversation context

#### Analyst Agent (analyst_agent.py)
- Analyzes query results
- Generates visualizations
- Creates natural language explanations
- Determines appropriate chart types
- Formats data for frontend display

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8+
- Docker and Docker Compose

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd ai_data_analyst
```

2. Start the application using Docker Compose:
```bash
docker-compose up
```

Or run frontend and backend separately:

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. The application will present a chat-like interface where you can:
   - Ask questions about your data
   - View visualizations
   - Get AI-powered insights

## API Endpoints

- `GET /`: Health check endpoint
- `POST /input`: Process user input and return analysis
- Additional endpoints for specific data operations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
