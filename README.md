# Contract Advisor RAG: Towards Building A High-Precision Legal Expert LLM APP

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [Key Features](#key-features) 
- [License](#license)


## Project Overview

The primary goal of this project is to build, evaluate, and improve a Retrieval-Augmented Generation (RAG) system for Contract Q&A. This system will enable users to interact with contracts by asking questions and receiving precise, relevant answers. The ultimate aim is to enhance the capabilities of our contract assistant, contributing to our vision of creating a fully autonomous contract bot.



## Tech Stack

- **Programming Languages:** Python,
- **Backend Frameworks:** Flask
- **Frontend Framework:** React

## Setup Instructions

### Prerequisites

- Python 3.x

### Installation

1. **Clone the Repository**
   ```sh
   git clone git@github.com:jadmassu/contract_advisor_rag.git
   cd contract_advisor_rag
   ```
2. **Set Up Virtual Environment**

   ```sh
      python3 -m venv .venv
   . .venv/bin/activate
   ```

3. **Install Backend Requirements**

   ```sh
   pip install -r requirements.txt
   ```

4. **Install Frontend Modules**
   ```sh
   npm i
   ```
5. **SetUP environments**
   ```sh
   OPENAI_API_KEY = Your_open_api_key
   PATH_TO_PDF = Your_file_Path
   ```

## API Development

**Run Flask Application**

```sh
cd backend
flask --app main run
```

## Frontend Development

**Run Next Application**

```sh
cd frontend
npm run dev
```

**Open with your browser to see the result.**

[http://localhost:3000](http://localhost:3000)

## Project Structure

    ├── backend
    │   ├── main.py               # API entry point
    │   ├── controller            # All the controllers
    │   └── service               # All service that interact with outside
    ├── data
    │   ├── data       		      # Raw data files
    │   └──...
    ├── frontend
    │   ├── public               # Static resource
    │   ├── src                  # Contains all the components pages and styles
    │   └── ...
    ├── requirements.txt          # Python dependencies
    ├── README.md                 # Project documentation
    └── ...

## Key Features

* Pre-Retrieval Optimization: Efficiently load, chunk, and embed data for streamlined processing.
* Retrieval Optimization: Implemented Expansion Query Analysis to enhance retrieval performance.
* Post-Retrieval Optimization: Refined results using Cohere Rerank to improve output quality.
* Ragas Framework: Evaluates Retrieval Augmented Generation (RAG) pipelines for performance assessment.
* AutoGen Agents: Developed multi-agent system with Assistant for initialization, Worker for RAG pipeline and Ragas evaluation, and User Proxy for user interactions.

### License

This project is licensed under the MIT License. See the LICENSE file for details.
