# Module 1: Understanding the Basics Quiz

## Containerization & Docker Fundamentals

1. **What is the main difference between traditional deployments and containerized deployments?**
   - [x] Containerized deployments are always faster than traditional deployments
   - [ ] Traditional deployments use virtual machines while containerized deployments don't use any virtualization
   - [ ] Containerized deployments package the application with its dependencies, ensuring consistency across environments
   - [ ] Traditional deployments are more secure by default

2. **Which of these is NOT a key benefit of containerization?**
   - [x] Portability across different environments
   - [ ] Isolation of application dependencies
   - [ ] Efficient resource utilization
   - [ ] Elimination of the need for operating systems

3. **What does it mean when we say containers share the host kernel?**
   - [x] All containers run the same application code
   - [ ] Containers use the host operating system's kernel rather than virtualizing an entire OS
   - [ ] Container images must be built on the same system where they'll be deployed
   - [ ] Multiple users can access the same container simultaneously

4. **In the context of our retail store inventory system, why is containerization beneficial?**
   - [x] It allows the algorithm to access the store's physical inventory directly
   - [ ] It ensures the inventory algorithm will run consistently regardless of the deployment environment
   - [ ] It automatically optimizes the algorithm to process inventory data faster
   - [ ] It prevents competitors from seeing your inventory levels

5. **Which command will show you all running containers on your system?**
   - [ ] `docker ls`
   - [ ] `docker images`
   - [ ] `docker ps`
   - [ ] `docker list`

6. **What does the following command do? `docker run -v $(pwd):/app python:3.9 python /app/algorithm.py`**
   - [ ] Creates a new Python image named algorithm.py
   - [ ] Runs algorithm.py on the host machine using Python 3.9
   - [ ] Mounts the current directory to /app in the container and runs algorithm.py
   - [ ] Downloads algorithm.py from a remote repository and runs it

7. **What are Docker layers?**
   - [ ] Different security permission levels within a container
   - [ ] Read-only filesystem components that make up a Docker image
   - [ ] Network interfaces that connect containers
   - [ ] User access levels for Docker Hub

8. **Why is understanding Docker layers important?**
   - [ ] Layers determine how quickly a container starts up
   - [ ] Each layer requires a separate license
   - [ ] Efficient layer management can reduce image size and improve build performance
   - [ ] Layers determine which users can access container resources
