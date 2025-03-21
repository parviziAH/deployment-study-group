# Docker & Kubernetes Training Roadmap
## A Beginner's Guide to Containerization and Deployment

### Overview
This roadmap equips participants with the skills to deploy and manage a realistic retail store inventory system using containerization and orchestration. Designed for complete beginners, it features hands-on exercises that build a functional application step-by-step, simulating real-world workflows. Starting with Docker basics, you'll create a Python-based inventory algorithm, a web frontend to display results, and scale it with Kubernetes.

### Scenario: Retail Store Inventory System
You’re a DevOps engineer for a retail chain tasked with deploying an inventory management system:
- **Core Component**: A Python script (`algorithm.py`) calculates stock reorder points based on sales data.
- **Input**: `input_data.json` (e.g., item sales and stock levels).
- **Output**: `output_data.json` (e.g., items needing restock).
- **Evolution**: Add a web frontend, API, and production scaling over modules.

### Repository Structure
- **`theory/`**: Markdown files with quizzes to test theoretical knowledge.
- **`exercises/`**: Jupyter notebooks with practical, retail-focused tasks.
- **`resources/`**: Sample files (e.g., `algorithm.py`, `utils.py`, `input_data.json`).
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
| 1 | Understanding the Basics (Containerization & Docker) | Core concepts and basic Docker commands | Run a stock algorithm in a container |
| 2 | Building Custom Images | Dockerfiles and declarative configuration | Add a web frontend for stock results |
| 3 | Multi-Container Applications & Orchestration | Docker Compose for multi-container apps | Link algorithm and frontend |
| 4 | Towards Production: Kubernetes Basics | Intro to Kubernetes orchestration | Deploy the system to a cluster |
| 5 | Deployment and Versioning | Production strategies and rollbacks | Update algorithm with versioning |
| 6 | Monitoring and Troubleshooting with k9s | Real-time monitoring and debugging | Monitor and fix inventory processing |

---

### Module 1: Understanding the Basics
**Goal**: Launch a Python container running `algorithm.py` to process inventory data.

| Topic | Content |
|-------|---------|
| **Concepts** | • Traditional vs. containerized deployments<br>• Containerization: Isolation + Shared Kernel<br>• Benefits: Portability, Consistency, Efficiency |
| **Exercise 1: Setup** | • Install Docker<br>• Verify: `docker version`, `docker ps` |
| **Exercise 2: Run Algorithm** | • Create `algorithm.py`: Calculate reorder points (e.g., `if stock < sales * 2: restock`)<br>• Create `utils.py`: Helper functions (e.g., load/save JSON)<br>• Create `input_data.json`: `[{"item": "shirt", "stock": 10, "sales": 7}]`<br>• Run: `docker run -v $(pwd):/app python:3.9 python /app/algorithm.py`<br>• Output: `output_data.json` |
| **Exercise 3: Explore Layers** | • Build a minimal image: `FROM python:3.9; COPY algorithm.py utils.py /app/`<br>• Inspect: `docker inspect <container_id>`<br>• View layers: `docker image history inventory-algorithm` |

**Sample `algorithm.py`:**
"""
import json
from utils import load_json, save_json

data = load_json("input_data.json")
results = [{"item": item["item"], "restock": item["stock"] < item["sales"] * 2} for item in data]
save_json("output_data.json", results)
"""

**Sample `utils.py`:**
"""
import json

def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)
"""

---

### Module 2: Building Custom Images
**Goal**: Containerize the algorithm and add a web frontend, monitor with Lazydocker.

| Topic | Content |
|-------|---------|
| **Concepts** | • Dockerfiles: Syntax, instructions<br>• `.dockerignore`: Optimize builds<br>• Build context and versioning |
| **Exercise 4: Algorithm Image** | • Dockerfile: `FROM python:3.9; COPY algorithm.py utils.py input_data.json /app/; WORKDIR /app`<br>• Build: `docker build -t inventory-algorithm .`<br>• Run: `docker run -v $(pwd)/output:/app/output inventory-algorithm python algorithm.py` |
| **Exercise 5: Web Frontend** | • Create `index.html`: `<h1>Restock: <span id="restock"></span></h1>`<br>• Dockerfile: `FROM nginx:latest; COPY index.html /usr/share/nginx/html/; ENV OUTPUT_PATH=/app/output_data.json`<br>• Build: `docker build -t inventory-web .`<br>• Run: `docker run -d -p 80:80 -v $(pwd)/output:/app inventory-web` |
| **Monitoring with Lazydocker** | • Install Lazydocker: [Instructions](https://github.com/jesseduffield/lazydocker#installation)<br>• Run: `lazydocker`<br>• Monitor `inventory-algorithm` and `inventory-web` |

---

### Module 3: Multi-Container Applications & Orchestration
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

### Module 4: Towards Production: Kubernetes Basics
**Goal**: Deploy the inventory system to Kubernetes.

| Topic | Content |
|-------|---------|
| **Concepts** | • Kubernetes: Control Plane, Pods, Services<br>• Declarative config, health checks |
| **Exercise 8: Setup Cluster** | • Install Minikube: `minikube start`<br>• Verify: `kubectl cluster-info`, `kubectl get nodes` |
| **Exercise 9: Deploy App** | • Create `algorithm-deployment.yaml` and `web-deployment.yaml`<br>• Expose: `kubectl expose deployment web --type=NodePort --port=80`<br>• Access: `minikube service web --url` |

---

### Module 5: Deployment and Versioning
**Goal**: Update the algorithm with new logic and test rollbacks.

| Topic | Content |
|-------|---------|
| **Concepts** | • Versioning: Tags, semantic versioning<br>• Deployment strategies: RollingUpdate, Recreate |
| **Exercise 10: Strategy & Rollback** | • Update `algorithm.py` (e.g., stricter restock logic)<br>• Build: `docker build -t inventory-algorithm:v2 .`<br>• Update: `kubectl set image deployment/algorithm algorithm=inventory-algorithm:v2`<br>• Rollback: `kubectl rollout undo deployment/algorithm` |

---

### Module 6: Monitoring and Troubleshooting with k9s
**Goal**: Monitor and debug the inventory system.

| Topic | Content |
|-------|---------|
| **Concepts** | • k9s benefits<br>• Real-time monitoring, troubleshooting |
| **Exercise 11: Setup k9s** | • Install k9s: [Instructions](https://k9scli.io/topics/install/)<br>• Run: `k9s` |
| **Exercise 12: Monitor** | • View pods, logs, CPU/memory usage<br>• Customize views |
| **Exercise 13: Troubleshoot** | • Diagnose algorithm failures<br>• Scale: `kubectl scale deployment/algorithm --replicas=3` |

---

### Key Training Emphases
| Emphasis | Description |
|----------|-------------|
| **Practical Application** | Process retail inventory data with a custom algorithm |
| **Troubleshooting** | Fix algorithm errors, handle bad input data |
| **Security** | Use non-root users, secure file mounts |
| **Realism** | Simulate stock analysis, updates, and scaling |
| **Monitoring** | Use Lazydocker and k9s for observability |

### Notable Quotes
- **Buelta's Book**: "Containers are extremely portable… lightweight… and secure."
- **Docker Up and Running 2023**: "Docker made Linux containers approachable for all engineers."

### Getting Started
1. Install prerequisites.
2. Open `exercises/module1_exercises.ipynb` in Jupyter: `jupyter notebook`.
3. Follow quizzes and exercises in order.
4. Ask questions in our study group!

Happy deploying!