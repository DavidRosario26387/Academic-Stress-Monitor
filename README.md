# Stress Monitoring and Intervention System in Academic Forums

This project implements an **AI-powered stress detection and personalized recommendation system** for academic forums like Discord. It leverages **DistilBERT** for stress classification and a **RAG-based LLM** for personalized recovery suggestions, with all interactions logged in **MongoDB** for analysis and record-keeping.

---

## Features

- Detect stress in forum messages using **DistilBERT**.
- Categorize stress levels as **Low, Medium, or High**.
- Provide **personalized advice** based on forum knowledge using **RAG + LLM**.
- Asynchronous logging of all user interactions in **MongoDB**.
- Easy deployment as a **Discord bot**.

---

## Architecture

<img width="891" height="417" alt="new drawio" src="https://github.com/user-attachments/assets/50732fa0-8959-45f0-9987-569338815ab9" />


**Components:**

- `analyse.py` – Stress prediction using DistilBERT.
- `llm_inference.py` – LLM chain for generating personalized advice.
- `RAG.py` – Retrieval-Augmented Generation database setup and queries.
- `responses.py` – Orchestrates model inference and response formatting.
- `datamodel.py` – MongoDB handler for async logging.
- `main.py` – Discord bot integration and event handling.

---

## Setup

1. **Clone the repository**
    ```bash
    git clone https://github.com/DavidRosario26387/Academic-Stress-Monitor
    cd Academic-Stress-Monitor
    ```

2. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

3. **Environment Variables**

    Create a .env file with:
    ```
    DISCORD_TOKEN=<your_discord_bot_token>
    MONGO_URI=<your_mongodb_uri>
    GROQ_API_KEY=<your_groq_api_key>
    ```

4. **Prepare Models**
    
    - Download and place your DistilBERT stress model and quantized weights as per analyse.py paths.
    - Prepare rags.csv for RAG recommendations.
---

## Usage

Run the Discord bot:

```
python main.py
```

- The bot listens to messages in Discord channels.

- If stress is detected, it sends a direct message with personalized advice.

- All messages and responses are logged to MongoDB.

## Dashboard Setup

### Backend Setup

- Navigate to the backend folder & Install dependencies::

```
cd UIdashboard/backend
npm install
```

- Create a .env file with your MongoDB connection:
  
```
MONGO_URI=<your_mongodb_uri>
PORT=5000
```
Start the backend server:
```
node server.js
```

You should see:
- MongoDB connected
- Server running on port 5000
- Backend API endpoint: http://localhost:5000/api/logs

### Frontend Setup

Navigate to the frontend folder & Install dependencies::
```
cd UIdashboard/frontend
npm install
```

Update API URL in app.js if needed:
```
axios.get("http://localhost:5000/api/logs")
```
Start the frontend:
```
npm start
```
- Dashboard opens in your browser at: http://localhost:3000
