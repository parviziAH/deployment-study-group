# Module 2: Building Custom Images Quiz

## Dockerfiles & Image Building

1. **What is a Dockerfile?**
   - [ ] A binary file format for Docker containers
   - [ ] A text file containing instructions for building a Docker image
   - [ ] A log file generated when running containers
   - [ ] A configuration file for Docker Compose

2. **Which Dockerfile instruction copies files from the host into the image?**
   - [ ] `ADD`
   - [ ] `COPY`
   - [ ] `IMPORT`
   - [ ] `INCLUDE`

3. **What is the purpose of the `WORKDIR` instruction in a Dockerfile?**
   - [ ] To specify where Docker should be installed
   - [ ] To set the working directory for any subsequent instructions
   - [ ] To define which directories should be excluded from the image
   - [ ] To create a new directory on the host machine

4. **What does this Dockerfile line do? `ENV OUTPUT_PATH=/app/output_data.json`**
   - [ ] Creates a file named output_data.json
   - [ ] Sets an environment variable named OUTPUT_PATH
   - [ ] Validates that the specified file exists
   - [ ] Outputs the path to the console during build

5. **What is the purpose of a `.dockerignore` file?**
   - [ ] To specify which Docker commands are not allowed
   - [ ] To exclude files and directories from the build context
   - [ ] To document known issues with the Docker image
   - [ ] To prevent certain users from running the container

6. **In our retail inventory system, why do we mount the output directory as a volume?**
   - [ ] To increase the container's storage capacity
   - [ ] To share output data between the host and the container
   - [ ] To improve algorithm performance
   - [ ] To encrypt sensitive inventory data

7. **What command would you use to build a Docker image from a Dockerfile in the current directory with the tag 'inventory-web:latest'?**
   - [ ] `docker create inventory-web:latest .`
   - [ ] `docker image inventory-web:latest`
   - [ ] `docker build -t inventory-web:latest .`
   - [ ] `docker compile -t inventory-web:latest`

8. **What does the `-d` flag do in the command `docker run -d -p 80:80 inventory-web`?**
   - [ ] Debug mode - shows additional container logs
   - [ ] Detached mode - runs the container in the background
   - [ ] Development mode - enables hot reloading
   - [ ] Disable networking

9. **What does the `-p 80:80` flag do in the command `docker run -d -p 80:80 inventory-web`?**
   - [ ] Sets the container priority to 80
   - [ ] Maps port 80 on the host to port 80 in the container
   - [ ] Limits the container to 80% CPU usage
   - [ ] Makes the container persist for 80 seconds

10. **Why is Lazydocker useful in our containerized inventory system?**
    - [ ] It automatically optimizes Docker image sizes
    - [ ] It provides a user-friendly interface for monitoring and managing containers
    - [ ] It generates documentation for Docker containers
    - [ ] It synchronizes inventory data between containers
