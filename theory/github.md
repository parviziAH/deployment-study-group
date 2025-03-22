# Git and GitHub Practical Guide

## What is Git and Why is it FUNDAMENTAL?

Git is a distributed version control system that tracks changes to your code. Unlike older systems, Git stores complete snapshots of your project, not just the changes.

### Why Git is Absolutely Essential:

1. **History Tracking**: Like a videogame it allows you to save your progress, if you want revert them, test something and
go back, and check who does what
2. **Parallel Development**: Multiple people can work on the same project simultaneously, without interfering with each other
3. **Experimentation**: Create branches to try new features without affecting the main code
4. **Disaster Recovery**: Roll back to any previous version when things break

**Without Git, professional software development is practically impossible.**

## Git vs. GitHub

- **Git**: The version control system that runs locally on your machine
- **GitHub**: The web-interface service for Git repositories

## Essential Git Commands for the Training

### It's written cloning, it means copying 

```bash
# Clone literally means copying
git clone https://github.com/username/docker-kubernetes-training.git

# Navigate into the repository
cd docker-kubernetes-training
```

### Checking Repository Status

```bash
# Shows which files are modified, staged, or untracked
git status
```

### Working with Branches

```bash
# List all branches (* indicates current branch)
git branch

# Create a new branch
git branch feature/new-algorithm

# Switch to a branch
git checkout feature/new-algorithm

# Create and switch to a new branch in one command
git checkout -b feature/web-dashboard

# Switch back to main branch
git checkout main
```

### Making Changes

```bash
# Stage modified files (prepare them for commit)
git add algorithm.py

# Stage all modified files
git add .

# Commit staged changes with a message
git commit -m "Improve restock algorithm logic"

# See commit history
git log
```

### Syncing with GitHub

```bash
# Download changes from GitHub
git pull

# Upload your local commits to GitHub
git push

# Push a new branch to GitHub
git push -u origin feature/new-algorithm
```

### Merging Changes

```bash
# First, switch to the destination branch
git checkout main

# Merge another branch into current branch
git merge feature/new-algorithm

# If there are conflicts, resolve them and then:
git add <resolved-files>
git commit -m "Merge feature/new-algorithm"
```

## Pull Requests (PRs)

A Pull Request is a GitHub feature (not a Git command) that allows you to propose changes to a repository.

### Why Pull Requests Matter:

1. **Code Review**: Team members can review your code before it's merged
2. **Discussion**: Provides a space to discuss the implementation
3. **CI/CD Integration**: Automated tests can run on your PR
4. **Documentation**: Creates a record of why changes were made

### Creating a Pull Request:

1. Push your branch to GitHub: `git push -u origin feature/new-algorithm`
2. Go to the repository on GitHub
3. Click "Pull requests" > "New pull request"
4. Select your branch as the compare branch
5. Add description, reviewers, and create the PR

### PR Workflow for the Training:

1. Create a feature branch for each exercise
2. Commit your changes to that branch
3. Push the branch to GitHub
4. Create a PR when you're ready for feedback
5. After approval, merge the PR on GitHub
6. Pull the updated main branch locally: `git pull`

## Practical Git Workflow for Our Training

1. **Start each module**:
   ```bash
   git checkout main
   git pull
   git checkout -b module-1/exercise-1
   ```

2. **During development**:
   ```bash
   # Check what you've changed
   git status
   
   # Stage and commit frequently
   git add .
   git commit -m "Implement restock calculation logic"
   ```

3. **Before submitting for review**:
   ```bash
   # Push your branch
   git push -u origin module-1/exercise-1
   
   # Create PR on GitHub
   ```

4. **After PR is approved and merged**:
   ```bash
   git checkout main
   git pull  # Get the latest main, including your merged changes
   ```

## Git Tips for Containerization Training

1. **Ignore Docker artifacts**: Add appropriate entries to `.gitignore`:
   ```
   .DS_Store
   __pycache__/
   output_data.json
   ```

2. **Commit Dockerfiles and configs**: Always commit your Dockerfiles, docker-compose.yml, and Kubernetes YAML files.

3. **Meaningful commit messages**: "Fix algorithm bug" is not as helpful as "Fix restock calculation for zero-stock items"

4. **Branch per feature**: Create a new branch for each distinct feature or exercise.