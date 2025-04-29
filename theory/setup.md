# Python Environment Setup Guide
## Setting Up pyenv and Poetry for Docker & Kubernetes Training (MacOS)

### Why Use pyenv and Poetry?

The first step is to set up the Python environment. You'll use `pyevn` for Python version management and `Poetry` for 
dependency management. Together, they create a robust setup where pyenv manages the basic Python version available
on your machine, and Poetry adapts it per each project you have.

#### pyenv allows you to:
- Install and manage multiple Python versions on your Macbook
- Switch between Python versions per project
- Avoid conflicts with the system Python version

#### Poetry lets you:
- Have a dependency management (alternative to pip/requirements.txt)
- Handles virtual environments automatically
- Lock files ensure reproducible environments
- You can package projects
- Builds on the Python version set by pyenv, linking it to each project

### Installing pyenv on MacOS

```bash
# Install with Homebrew
brew update
brew install pyenv

# Make your shell (terminal) able to find and execute the pyenv command.
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc

# Reload your profile
source ~/.zshrc
```

### Installing Python 3.12 with pyenv

```bash
# List available Python versions
pyenv install 3.12

# Verify installation
python --version  # Should show Python 3.12
```

### Installing Poetry on MacOS

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to your PATH (if not automatically added)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify installation
poetry --version
```

### Setting Up Your Project

```bash
# Navigate to your project directory
cd deployment-study-group

# Set local Python version for this project
pyenv local 3.12

# Create and activate virtual environment
poetry shell

# Check the (just spawned) virtual environment to verify everything is correct:
poetry env info

# Install dependencies
poetry install
```