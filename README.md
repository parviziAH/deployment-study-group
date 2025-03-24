# Deployment & APIs Training Roadmap
## A Beginner's Guide to Containerization and Deployment


### Overview
This roadmap equips participants with the skills to deploy and manage a realistic retail store inventory system using containerization and orchestration. Designed for complete beginners, it features hands-on exercises that build a functional application step-by-step, simulating real-world workflows. Starting with Docker basics, you'll create a Python-based inventory algorithm, a web frontend to display results, and scale it with Kubernetes.

### Setup
Running this file prevents direct pushes to the main branch
After cloning the repository, please run the following command to set up the Git hooks:
```
./.githooks/setup_githooks.sh
```

### Scenario: Retail Store Inventory System
You’re a DevOps engineer for a retail chain tasked with deploying an inventory management system:
- **Core Component**: A Python script (`algorithm.py`) calculates stock reorder points based on sales data.
- **Input**: `input_data.json` (e.g., item sales and stock levels).
- **Output**: `output_data.json` (e.g., items needing restock).
- **Evolution**: Add a web frontend, API, and production scaling over modules.

### Repository Structure
- **`theory/`**: Markdown files with quizzes to test theoretical knowledge.
- **`exercises/`**: Jupyter notebooks with practical, retail-focused tasks.
- **`study_material/`**: Books.
- **`restock_calculator/`**: Sample files (e.g., `algorithm.py`, `utils.py`, `input_data.json`).
- Clone this repo: `git clone <repo-url> && cd docker-kubernetes-training`

### Prerequisites
- **Docker Desktop** (Windows/Mac) or **Docker Engine + Compose** (Linux).
- **Minikube** (for Kubernetes modules).
- **Jupyter Notebook**: `poetry add notebook`.
- **Lazydocker**: Install after Module 2 (instructions provided).
- Basic terminal familiarity.

### Module Structure
| Module | Topic | Focus | Retail Use Case |
|--------|-------|-------|-----------------|
| 1 | Git & GitHub Basics | Version control fundamentals | Set up project repository |
| 2 | Understanding Docker Basics | Core concepts and basic Docker commands | Run a stock algorithm in a container |
| 3 | Building Custom Images | Dockerfiles and declarative configuration | Add a web frontend for stock results |
| 4 | Multi-Container Applications | Docker Compose for multi-container apps | Link algorithm and frontend |
| 5 | RESTful APIs | Building and containerizing APIs | Create inventory API endpoints |
| 6 | API Integration | Connecting frontend to backend API | Complete inventory management system |

---

### Module 1: Git & GitHub Basics
**Goal**: Set up version control and understand Git workflow.

| Topic | Content |
|-------|---------|
| **Concepts** | • Git vs. GitHub<br>• Branches and commits<br>• Pull requests |
| **Exercise 1: Git Setup** | • Configure Git<br>• Create feature branch<br>• Make changes and commit |
| **Exercise 2: GitHub Workflow** | • Push changes to GitHub<br>• Create pull request<br>• Review and merge changes |

---

### Module 2: Understanding Docker Basics
**Goal**: Launch a Python container running `algorithm.py` to process inventory data.

| Topic | Content |
|-------|---------|
| **Concepts** | • Traditional vs. containerized deployments<br>• Containerization: Isolation + Shared Kernel<br>• Benefits: Portability, Consistency, Efficiency |
| **Exercise 1: Setup** | • Install Docker<br>• Verify: `docker version`, `docker ps` |
| **Exercise 2: Run Algorithm** | • Create `algorithm.py`: Calculate reorder points (e.g., `if stock < sales * 2: restock`)<br>• Create `utils.py`: Helper functions (e.g., load/save JSON)<br>• Create `input_data.json`: `[{"item": "shirt", "stock": 10, "sales": 7}]`<br>• Run: `docker run -v $(pwd):/app python:3.9 python /app/algorithm.py`<br>• Output: `output_data.json` |
| **Exercise 3: Explore Layers** | • Build a minimal image: `FROM python:3.9; COPY algorithm.py utils.py /app/`<br>• Inspect: `docker inspect <container_id>`<br>• View layers: `docker image history inventory-algorithm` |

---

### Module 3: Building Custom Images
**Goal**: Containerize the algorithm and add a web frontend, monitor with Lazydocker.

| Topic | Content |
|-------|---------|
| **Concepts** | • Dockerfiles: Syntax, instructions<br>• `.dockerignore`: Optimize builds<br>• Build context and versioning |
| **Exercise 4: Algorithm Image** | • Dockerfile: `FROM python:3.9; COPY algorithm.py utils.py input_data.json /app/; WORKDIR /app`<br>• Build: `docker build -t inventory-algorithm .`<br>• Run: `docker run -v $(pwd)/output:/app/output inventory-algorithm python algorithm.py` |
| **Exercise 5: Web Frontend** | • Create `index.html`: `<h1>Restock: <span id="restock"></span></h1>`<br>• Dockerfile: `FROM nginx:latest; COPY index.html /usr/share/nginx/html/; ENV OUTPUT_PATH=/app/output_data.json`<br>• Build: `docker build -t inventory-web .`<br>• Run: `docker run -d -p 80:80 -v $(pwd)/output:/app inventory-web` |
| **Monitoring with Lazydocker** | • Run: `lazydocker`<br>• Monitor `inventory-algorithm` and `inventory-web` |

---

### Module 4: Multi-Container Applications
**Goal**: Orchestrate the algorithm and frontend with Docker Compose.

| Topic | Content |
|-------|---------|
| **Concepts** | • Orchestration basics<br>• Docker Compose: YAML, services, networks |
| **Exercise 6: Compose File** | • Create `docker-compose.yml`:<br>"""
version: '3'
services:
  algorithm:
    image: inventory-algorithm
    volumes:
      - ./output:/app/output
    command: python algorithm.py
  web:
    image: inventory-web
    ports:
      - "80:80"
    volumes:
      - ./output:/app
networks:
  default:
""" |
| **Exercise 7: Manage App** | • Start: `docker compose up -d`<br>• Check: `docker compose ps`<br>• Logs: `docker compose logs algorithm`<br>• Stop: `docker compose down` |

---

### Module 5: RESTful APIs
**Goal**: Build and containerize a RESTful API for inventory management.

| Topic | Content |
|-------|---------|
| **Concepts** | • RESTful API principles<br>• FastAPI basics<br>• Containerizing APIs |
| **Exercise 8: Build API** | • Create FastAPI endpoints for inventory<br>• Test locally with Swagger UI<br>• Containerize the API |
| **Exercise 9: API Testing** | • Test API endpoints with curl and Postman<br>• Handle error cases<br>• Implement data validation |

---

### Module 6: API Integration
**Goal**: Connect frontend to backend API for a complete system.

| Topic | Content |
|-------|---------|
| **Concepts** | • Frontend-backend integration<br>• Asynchronous requests<br>• Error handling |
| **Exercise 10: Frontend Integration** | • Update frontend to call API endpoints<br>• Implement loading states<br>• Handle API errors gracefully |
| **Exercise 11: Complete System** | • Compose all services together<br>• Test end-to-end workflow<br>• Implement improvements |

---

### Key Training Emphases
| Emphasis | Description |
|----------|-------------|
| **Practical Application** | Process retail inventory data with a custom algorithm |
| **Version Control** | Use Git and GitHub for collaborative development |
| **Containerization** | Package applications with Docker for consistency |
| **API Development** | Build RESTful services for inventory management |
| **Integration** | Connect frontend and backend components |
| **Monitoring** | Use Lazydocker for container observability |

### Getting Started
1. Install prerequisites as described above.
2. Open `exercises/module1_exercises.ipynb` in Jupyter: `jupyter notebook`.
3. Follow quizzes and exercises in order.
4. For each module, create a new feature branch: `git checkout -b feature/module-1-exercises`.
5. Commit your work and create pull requests to track your progress.
6. Ask questions in our study group!
