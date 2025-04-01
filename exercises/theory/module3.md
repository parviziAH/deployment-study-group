# Module 3: Multi-Container Applications & Orchestration Quiz

## Docker Compose & Container Orchestration

1. **What is Docker Compose primarily used for?**
   - [ ] Creating complex Dockerfiles
   - [ ] Hosting Docker images
   - [ ] Converting traditional applications to containers
   - [ ] Managing multi-container applications

2. **Which file format is used for Docker Compose configurations?**
   - [ ] JSON
   - [ ] XML
   - [ ] YAML
   - [ ] INI

3. **In a Docker Compose file, what does the `services` section define?**
   - [ ] External APIs the application can access
   - [ ] The containers that make up your application
   - [ ] Background tasks to be executed
   - [ ] User access permissions

4. **What does the following Docker Compose snippet do?**
   ```yaml
   volumes:
     - ./output:/app/output
   ```
   - [ ] Creates a new volume called "output"
   - [ ] Mounts the host's ./output directory to /app/output in the container
   - [ ] Copies files from ./output to /app/output
   - [ ] Sets the output log directory

5. **Which command starts all services defined in a docker-compose.yml file in detached mode?**
   - [ ] `docker compose start -d`
   - [ ] `docker compose run -d`
   - [ ] `docker compose up -d`
   - [ ] `docker compose launch -d`

6. **In our retail inventory system, why do we use Docker Compose instead of running each container separately?**
   - [ ] Docker Compose provides better security
   - [ ] Docker Compose automatically optimizes inventory algorithms
   - [ ] Docker Compose simplifies managing the relationship between the algorithm and web frontend
   - [ ] Docker Compose is required to connect to external databases

7. **Which command shows the logs for a specific service in a Docker Compose application?**
   - [ ] `docker compose logs <service-name>`
   - [ ] `docker compose show-logs <service-name>`
   - [ ] `docker compose output <service-name>`
   - [ ] `docker compose console <service-name>`

8. **What does the `depends_on` directive in Docker Compose do?**
   - [ ] Creates shared storage between containers
   - [ ] Controls the order in which services are started
   - [ ] Shares environment variables between containers
   - [ ] Limits resource usage for dependent containers

9. **What network is created by default when you use Docker Compose?**
   - [ ] No network is created by default
   - [ ] A bridge network with the project name as prefix
   - [ ] The host network
   - [ ] A global Docker network

10. **What command stops and removes all containers, networks, and volumes defined in the Docker Compose file?**
    - [ ] `docker compose delete`
    - [ ] `docker compose stop`
    - [ ] `docker compose down`
    - [ ] `docker compose remove`

