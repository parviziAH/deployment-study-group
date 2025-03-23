# Module 4: Towards Production: Kubernetes Basics Quiz

## Kubernetes Fundamentals & Architecture

1. **What is Kubernetes?**
   - [ ] A container runtime that replaces Docker
   - [ ] A containerization technology
   - [ ] A container orchestration platform
   - [ ] A virtual machine management system

2. **What is the relationship between Docker and Kubernetes?**
   - [ ] Kubernetes is a subset of Docker
   - [ ] Docker can be used to create containers that Kubernetes then orchestrates
   - [ ] They are competing technologies that cannot be used together
   - [ ] Kubernetes can only manage Docker containers

3. **Which of these is NOT a component of the Kubernetes control plane?**
   - [ ] API Server
   - [ ] Scheduler
   - [ ] Docker Engine
   - [ ] Controller Manager

4. **What is a Kubernetes Pod?**
   - [ ] A group of nodes in a Kubernetes cluster
   - [ ] A management interface for Kubernetes
   - [ ] The smallest deployable unit that can contain one or more containers
   - [ ] A storage volume for container data

5. **What command starts a local Kubernetes cluster using Minikube?**
   - [ ] `minikube init`
   - [ ] `minikube begin`
   - [ ] `minikube launch`
   - [ ] `minikube start`

6. **What command would you use to verify your connection to a Kubernetes cluster?**
   - [ ] `kubectl status`
   - [ ] `kubectl check`
   - [ ] `kubectl cluster-info`
   - [ ] `kubectl verify`

7. **In our retail inventory system, why might you want to move from Docker Compose to Kubernetes?**
   - [ ] To reduce the application's memory footprint
   - [ ] To enable container orchestration features like scaling, self-healing, and rolling updates
   - [ ] To improve algorithm calculation speed
   - [ ] To eliminate the need for containerization

8. **What Kubernetes resource type would you use to define how to create multiple identical Pods?**
   - [ ] Service
   - [ ] ConfigMap
   - [ ] Pod
   - [ ] Deployment

9. **What does a Kubernetes Service do?**
   - [ ] Runs background maintenance tasks
   - [ ] Provides persistent storage for Pods
   - [ ] Provides a way to access Pods through a stable network endpoint
   - [ ] Manages container images

10. **What command exposes a Kubernetes deployment as a service accessible from outside the cluster?**
    - [ ] `kubectl publish deployment/web --port=80`
    - [ ] `kubectl expose deployment/web --type=NodePort --port=80`
    - [ ] `kubectl service create web --external`
    - [ ] `kubectl network expose web:80`
