# Docker & Kubernetes Training Roadmap
## A Beginner's Guide to Containerization and Deployment

### Overview
This roadmap equips participants with the ability to understand and execute deployments using containerization as the foundation. It's designed for complete beginners and features practical exercises that build upon each other.

### Module Structure

| Module | Topic | Focus |
|--------|-------|-------|
| 1 | Understanding the Basics (Containerization & Docker) | Core concepts of containerization and basic Docker commands |
| 2 | Building Custom Images | Creating custom images using Dockerfiles and understanding declarative configuration |
| 3 | Multi-Container Applications & Orchestration | Using Docker Compose for defining and managing multi-container applications |
| 4 | Towards Production: Kubernetes Basics | Introduction to Kubernetes as a production-grade container orchestration system |
| 5 | Deployment and Versioning for Production-Readiness | Understanding real-life deployments, versioning, and rollback strategies |
| 6 | Monitoring and Troubleshooting with k9s | Using k9s to monitor and manage Kubernetes clusters |

### Module 1: Understanding the Basics

| Topic | Content |
|-------|---------|
| **Theoretical Concepts** | • What is a Deployment? (Traditional vs. Containerized)<br>• Problems with traditional deployments<br>• What is Containerization? (Definition: Isolation + Shared Kernel)<br>• Benefits: Portability, Consistency, Resource Efficiency |
| **Exercise 1:<br>Setting up a Basic Environment** | • Install Docker Desktop (or Docker Engine + Docker Compose on Linux)<br>• Verify installation with `docker version` and `docker ps`<br>• Reference: "Docker Up and Running 2023" - Chapter 3 |
| **Exercise 2:<br>Running a Simple Container** | • Run "hello-world" container using `docker run hello-world`<br>• Explain image pulling, container creation, execution, and termination<br>• Run interactive Ubuntu container with `docker run -it ubuntu bash`<br>• Practice basic Linux commands inside the container |
| **Exercise 3:<br>Exploring Container Layers** | • Run `docker inspect hello-world` and analyze the output<br>• Discuss images, immutability, and importance of layers<br>• Run `docker image history` commands to compare layer structures |

### Module 2: Building Custom Images

| Topic | Content |
|-------|---------|
| **Theoretical Concepts** | • Introduction to Dockerfiles: syntax and common instructions<br>• Dockerignore: reducing image size<br>• Build Context: importance of directory and files used<br>• Images as instructions: versioning and compatibility |
| **Exercise 4:<br>Creating a Basic Dockerfile** | • Create directory with simple index.html file<br>• Create Dockerfile using nginx:latest base image<br>• Build image using `docker build -t my-nginx .`<br>• Run container mapping port 80 to host port<br>• Access website in browser |
| **Exercise 5:<br>Adding Configuration with Environment Variables** | • Modify index.html to include variable message<br>• Update Dockerfile to set default value for MESSAGE<br>• Rebuild image and run container with custom message<br>• Demonstrate environment variables for configuration |

### Module 3: Multi-Container Applications & Orchestration

| Topic | Content |
|-------|---------|
| **Theoretical Concepts** | • What is Orchestration?<br>• Introduction to Docker Compose: YAML structure, services, networks, volumes<br>• Benefits of Compose: Simplicity, repeatability, dependency management<br>• Difference between Docker Compose and Kubernetes |
| **Exercise 6:<br>Creating a Simple Docker Compose File** | • Create docker-compose.yml for web and db services<br>• Define shared network for container communication<br>• Link web service to database using environment variables<br>• Reference: Buelta's Book - Chapter 8 |
| **Exercise 7:<br>Managing the Multi-Container Application** | • Use `docker compose up -d` to start the application<br>• Use `docker compose ps` to check container status<br>• Use `docker compose logs web` to view service logs<br>• Use `docker compose down` to stop and remove the application |

### Module 4: Towards Production: Kubernetes Basics

| Topic | Content |
|-------|---------|
| **Theoretical Concepts** | • Need for Orchestration at Scale: Resource Management, Scheduling, HA<br>• Kubernetes Architecture: Control Plane, Nodes, Pods, Services, Deployments<br>• Key Kubernetes Concepts: Declarative Configuration, Health Checks, Auto-Scaling<br>• Tools: kubectl |
| **Exercise 8:<br>Setting up a Local Kubernetes Cluster** | • Install Minikube (or Kind/k3s)<br>• Start Minikube using `minikube start`<br>• Verify installation with `kubectl cluster-info` and `kubectl get nodes`<br>• Reference: "Docker Up and Running 2023" - Chapter 3 |
| **Exercise 9:<br>Deploying a Simple Application to Kubernetes** | • Create a Deployment for nginx image<br>• Expose the Deployment using a Service of type NodePort<br>• Find service URL and access application in browser<br>• Reference: Buelta's Book - Chapter 5 |

### Module 5: Deployment and Versioning for Production-Readiness

| Topic | Content |
|-------|---------|
| **Theoretical Concepts** | • Testing images in production: Versioning and Rollback<br>• Docker workflow: Ensuring data and code correctness<br>• Versioning: Tags and semantic versioning<br>• CI/CD integration |
| **Exercise 10:<br>Setting deployment strategy** | • Replicate nginx deployment with different strategies<br>• Compare rollingUpdate and Recreate deployment types<br>• Create a faulty deployment to test k8s rollback functionality<br>• Practice troubleshooting techniques |

### Module 6: Monitoring and Troubleshooting with k9s

| Topic | Content |
|-------|---------|
| **Theoretical Concepts** | • Introduction to k9s and its benefits<br>• Monitoring Kubernetes resources in real-time<br>• Understanding resource utilization and performance metrics<br>• Troubleshooting patterns and best practices |
| **Exercise 11:<br>Installing and Configuring k9s** | • Install k9s on your local machine<br>• Configure k9s to connect to your Minikube cluster<br>• Explore the k9s interface and basic navigation<br>• Customize k9s view to show relevant information |
| **Exercise 12:<br>Monitoring Cluster Resources** | • Use k9s to monitor pods, deployments, and services<br>• View logs of running containers directly in k9s<br>• Monitor resource usage (CPU, memory) of pods<br>• Set up custom views for different resource types |
| **Exercise 13:<br>Troubleshooting with k9s** | • Identify and diagnose pod failures<br>• Investigate resource constraints and limits<br>• Execute commands within pods using k9s<br>• Practice rolling restarts and scaling operations |

### Key Training Emphases

| Emphasis | Description |
|----------|-------------|
| **Practical Application** | Tie each concept to real-world use cases participants will encounter |
| **Troubleshooting** | Encourage experimentation and guide through common issues using diagnostic tools |
| **Security** | Continuously mention security best practices (non-root users, minimizing privileges, secret management) |
| **Questions** | Allocate plenty of time for questions and discussion |
| **Monitoring** | Emphasize the importance of observability in containerized environments |

### Notable Quotes

| Source | Quote |
|--------|-------|
| Buelta's Book | "...containers are extremely portable, as they are detached from the underlying hardware and the platform that runs them; they are very lightweight, as a minimal amount of data needs to be included, and they are secure, as the exposed attack surface of a container is extremely small." |
| "Docker Up and Running 2023" | "Docker single-handedly made Linux containers, which have been publicly available since 2008, approachable and useful for all computer engineers. Docker fits containers relatively easily into the existing workflow and processes of real companies." |
| Buelta's Book | "As you may already have noticed, this is a hassle to read, is not very flexible, will be a pain to edit, and might fail unexpectedly in several places." (comparing shell scripts to Docker Compose) |
| Buelta's Book | "...there's an overhead in creating microservices, as there's some work that gets replicated on each service. That overhead gets compensated by allowing independent and parallel development." |
| Buelta's Book | "It is highly recommended that you tag your CI/CD builds with something that uniquely identifies the exact source code commit that was used to build them. In a git workflow, this could be the git hash related to the commit." |