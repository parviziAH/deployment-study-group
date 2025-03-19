# Module 6: Monitoring and Troubleshooting with k9s Quiz

## Kubernetes Monitoring & Debugging

1. **What is k9s?**
   - [ ] A Kubernetes deployment strategy
   - [ ] A terminal-based UI for managing Kubernetes clusters
   - [ ] A container orchestration alternative to Kubernetes
   - [ ] A backup solution for Kubernetes clusters

2. **Which of these is NOT something you can do with k9s?**
   - [ ] View pod logs
   - [ ] Delete resources
   - [ ] Monitor resource usage
   - [ ] Create new Docker images

3. **What keyboard shortcut typically accesses the k9s command mode?**
   - [ ] Alt+C
   - [ ] Tab
   - [ ] Shift+Space
   - [ ] :

4. **How do you view logs for a specific pod in k9s?**
   - [ ] Select the pod and press L
   - [ ] Type "logs" in command mode
   - [ ] Right-click on the pod and select "logs"
   - [ ] Press the F1 key

5. **What command scales a Kubernetes deployment to have 3 replicas?**
   - [ ] `kubectl scale --count=3 deployment/algorithm`
   - [ ] `kubectl replicate deployment/algorithm --copies=3`
   - [ ] `kubectl scale deployment/algorithm --replicas=3`
   - [ ] `kubectl deployment/algorithm scale 3`

6. **In our retail inventory system, why might you need to scale the algorithm deployment?**
   - [ ] To handle increased inventory processing during busy retail periods
   - [ ] To comply with licensing requirements
   - [ ] To reduce security vulnerabilities
   - [ ] To simplify the application architecture

7. **How can you check the resource usage (CPU/memory) of pods in k9s?**
   - [ ] Press U when viewing pods
   - [ ] Select the pod and press R
   - [ ] Type "top" in command mode
   - [ ] Press Ctrl+M

8. **What is a common indicator that a pod is experiencing problems in Kubernetes?**
   - [ ] The pod status shows "CrashLoopBackOff"
   - [ ] The pod has a green status indicator
   - [ ] The pod has multiple IP addresses
   - [ ] The pod appears at the top of the list

9. **What command would you use to describe a pod to get detailed information about its status?**
   - [ ] `kubectl info pod/algorithm-5d4f8b9c7-xyz12`
   - [ ] `kubectl describe pod/algorithm-5d4f8b9c7-xyz12`
   - [ ] `kubectl status pod/algorithm-5d4f8b9c7-xyz12`
   - [ ] `kubectl details pod/algorithm-5d4f8b9c7-xyz12`

10. **What's a benefit of using k9s over standard kubectl commands for troubleshooting?**
    - [ ] k9s can modify Docker images directly
    - [ ] k9s automatically fixes common Kubernetes issues
    - [ ] k9s provides real-time visual feedback and interactive navigation of cluster resources
    - [ ] k9s bypasses Kubernetes security controls for faster debugging

## Answer Key
1. A terminal-based UI for managing Kubernetes clusters
2. Create new Docker images
3. :
4. Select the pod and press L
5. `kubectl scale deployment/algorithm --replicas=3`
6. To handle increased inventory processing during busy retail periods
7. Press U when viewing pods
8. The pod status shows "CrashLoopBackOff"
9. `kubectl describe pod/algorithm-5d4f8b9c7-xyz12`
10. k9s provides real-time visual feedback and interactive navigation of cluster resources