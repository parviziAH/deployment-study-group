# Module 5: Deployment and Versioning Quiz

## Kubernetes Deployment Strategies & Version Management

1. **What is semantic versioning?**
   - [ ] Using descriptive words for version names
   - [ ] Using a MAJOR.MINOR.PATCH format where each number has specific meaning
   - [ ] Using dates as version numbers
   - [ ] Using random numbers for versions to improve security

2. **In the tag `inventory-algorithm:v2.3.5`, what does the `2` typically represent in semantic versioning?**
   - [ ] The patch version
   - [ ] The minor version
   - [ ] The major version
   - [ ] The build number

3. **What is a rolling update in Kubernetes?**
   - [ ] Updating all Pods simultaneously
   - [ ] Gradually replacing Pods with new versions to avoid downtime
   - [ ] Renaming Pods while they continue running
   - [ ] Scheduling updates to occur at specific times

4. **Which Kubernetes deployment strategy replaces all instances at once?**
   - [ ] Rolling update
   - [ ] Blue/Green deployment
   - [ ] Recreate
   - [ ] Canary deployment

5. **What command would you use to update a Kubernetes deployment to use a new image version?**
   - [ ] `kubectl upgrade deployment/algorithm`
   - [ ] `kubectl set image deployment/algorithm algorithm=inventory-algorithm:v2`
   - [ ] `kubectl deployment version --set=v2`
   - [ ] `kubectl change-image algorithm to inventory-algorithm:v2`

6. **In our retail inventory system, why is versioning important for the algorithm container?**
   - [ ] To make the application run faster
   - [ ] To track changes in restock logic and enable rollbacks if needed
   - [ ] To reduce storage requirements
   - [ ] To comply with retail industry regulations

7. **What does the following command do? `kubectl rollout status deployment/algorithm`**
   - [ ] Shows the deployment's current status and progress of any ongoing rollout
   - [ ] Changes the deployment's current status
   - [ ] Starts a new deployment rollout
   - [ ] Rolls back to the previous deployment version

8. **What command would you use to undo a problematic deployment and revert to the previous version?**
   - [ ] `kubectl deployment previous`
   - [ ] `kubectl rollout undo deployment/algorithm`
   - [ ] `kubectl revert algorithm`
   - [ ] `kubectl set version=previous deployment/algorithm`

9. **What is a Kubernetes ReplicaSet?**
   - [ ] A backup copy of the cluster's data
   - [ ] A controller that ensures a specified number of pod replicas are running
   - [ ] A set of replica Kubernetes clusters
   - [ ] A database replication mechanism

10. **Which deployment strategy would be best for testing a major change to the inventory algorithm with minimal risk?**
    - [ ] Recreate deployment
    - [ ] Rolling update
    - [ ] Canary deployment
    - [ ] All-at-once deployment
