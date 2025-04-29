## What's Docker and Why It's Your New Best Friend
Docker is a tool that wraps your code, libraries, and settings into a **container**—a lightweight, portable box that runs the same way everywhere Docker's installed. Think of it like shipping a product: you pack it in a standard box, and it arrives intact no matter where it goes.

**Real-world scenario:** You've built a restock calculator that works perfectly on your laptop. Your boss says, "Deploy it!" Without Docker, chaos hits:
- Your Python version (say, 3.10) doesn't match the server's (3.7)—crash.
- Libraries like `json` might have version conflicts—crash.
- File paths are different—crash.
- Your colleague can't even run it to double-check your work.

With Docker, you pack everything—code, Python version, libraries—into one container. It runs the same on your laptop, 
the test server, or production. This is how a deployment works.

### Images vs. Containers: The Basics
When working with deployments, you'll hear two key terms: **images** and **containers**.
- **Image:** The blueprint. It's like a package with your code and tools (e.g., Python, your script, files, dependencies).
You build it once with `docker build`.
- **Container:** The running version of the **image**. It's what you launch from the image with `docker run`. Stop it or 
run it again (this is also why it's called "Docker" and the logo is a whale that carries a container)

**Think of it like this:**  An image is your company's standard workstation setup - carefully configured once by IT. 
Containers are like individual employees' workstations - all starting from the same setup, but each running independently. 
When a project needs more workers, you don't rebuild the setup - you just bring in more pre-configured workstations 
(containers) from your template (image).

### The Docker Daemon: Who's doing the trick?
Docker isn't magic—it's powered by the **Docker daemon**, a background process on your machine (or server) that manages 
images, containers, and everything else. When you type a command like `docker run`, you're telling the daemon, "Hey, do 
this for me". You give the orders, it obeys.

- **Why care?** If Docker's not working, it's often because the daemon's stopped (e.g., Docker Desktop isn't running for
whatever reason. You can check with `docker info`). Restart it, and you're good to go again.

### Docker is Built in Layers
Docker builds images in layers, with each instruction in your Dockerfile creating a new layer. Each layer is practically a 
file system snapshot. Think of it as a snapshot of file changes - similar to how you might save versions of your analysis at different stages:

- Layer 1: Base Python installation (like setting up your initial environment)
- Layer 2: Added dependencies (like installing pandas, numpy, etc.)
- Layer 3: Added your application code (like adding your analysis scripts)
Each layer doesn't just track the individual files that changed (like Git would) - it captures the entire file system state for those changes. When you run a container, Docker stacks these read-only file system snapshots on top of each other to create the complete environment.



This is important because:

1. Layers are cached - if nothing changes in a layer, Docker reuses it in subsequent builds
2. The order matters - put frequently changing files later in your Dockerfile
3. Each layer adds to the image size (since a layer == a file)

For the restock calculator, you'd want to put your Python dependencies first, then copy your code files. This way, 
if you update your code but not your dependencies, Docker only rebuilds from the code layer, saving time.

### Your First Dockerfile: The Recipe
A `Dockerfile` is a text file that tells Docker how to build your image. No `Dockerfile`, no container—it's that simple. 
Here's a basic one for our restock calculator:

```
FROM python:3.10-slim
WORKDIR /app
COPY restock_calculator/lib/algorithm.py /app/
COPY restock_calculator/lib/utils.py /app/
CMD ["python", "algorithm.py"]
```

- **Breaking down the instructions:**
  - `FROM`: Picks the base image—like choosing a starter kit. Yes, a layer can also be **another image**. Here, 
  `python:3.10-slim` gives you Python 3.10 with minimal extras (the "slim" part).
  - `WORKDIR`: Sets the working directory inside the container to `/app`. The container can be explored like a file system.
  - `COPY`: Moves files from your machine to the container. We copy both the algorithm and utils files.
  - `CMD`: Sets the default command to run when the container starts. `["python", "algorithm.py"]` it's like typing in the
  terminal `python algorithm.py`

Save this as `Dockerfile` (no extension) in your project's root folder.

### More Dockerfile Commands You'll Use
Here's the rundown of key `Dockerfile` instructions. Each line corresponds to a layer:
- **WORKDIR**: Sets the "current directory" inside the container, like `cd` in a terminal. Example: `WORKDIR /app` makes `/app` your base folder.
- **RUN**: Executes a command during the build—like installing stuff. Example: `RUN pip install numpy` adds NumPy to your image.
- **COPY**: Copies files from your machine to the container. Example: `COPY . .` grabs everything in your folder (careful with this—only copy what's needed).
- **ENV**: Sets environment variables, like settings you can tweak. Example: `ENV MY_VAR=value`.
- **ENTRYPOINT**: Locks in a base command (e.g., `ENTRYPOINT ["python"]`), letting `CMD` add arguments.


### Building It: What's the `.` in `docker build`?
Run this in your terminal, in the same folder as your `Dockerfile`:

```
docker build -t restock-calculator .
```

- `-t restock-calculator`: Tags your image with a name so you can reference it later (e.g., `restock-calculator`).
- `.`: The dot means "use this folder as the build context." It tells Docker where to find the `Dockerfile` and any files it needs.

You'll see Docker pull Python, copy your files, and build the image. Check it with `docker images`—`restock-calculator` will be there.

### A Working Example: `algorithm.py`
Here's the restock calculator script we're containerizing:

```python
import json
from utils import load_json, save_json


def calculate_restock_needs():
    """
    Calculates which inventory items need restocking based on current stock and sales data.
    Restock rule: if stock < sales * 2, item needs restocking
    """
    # Load inventory data
    data = load_json("input_data.json")

    # Process each item to determine restock needs
    results = []
    for item in data:
        needs_restock = item["stock"] < item["sales"] * 2
        results.append({
            "item": item["item"],
            "current_stock": item["stock"],
            "recent_sales": item["sales"],
            "restock": needs_restock,
            "recommended_order": (item["sales"] * 2 - item["stock"]) if needs_restock else 0
        })

    # Save results to output file
    save_json("output_data.json", results)
    print(f"Processed {len(data)} inventory items. Results saved to output_data.json")


if __name__ == "__main__":
    calculate_restock_needs()
```

This script calculates which inventory items need restocking based on current stock and sales data, using a simple rule: 
if stock is less than twice the sales, the item needs restocking.

### Basic Docker Commands: The Toolkit
Here's what you'll type daily to control Docker:
- **docker build**: Builds an image from a `Dockerfile`. Example: `docker build -t my-image .`.
- **docker run**: Starts a container from an image. Example: `docker run my-image`.
  - Add `--rm` to delete it after: `docker run --rm my-image`.
  - Add `-it` for interactive mode (accessing it as it was a folder): `docker run -it my-image`.
- **docker ps**: List of running containers. Add `-a` for all containers: `docker ps -a`.
- **docker stop**: Stops a running container. Example: `docker stop <container_id>` (grab the ID from `docker ps`).
- **docker rm**: Deletes a stopped container. Example: `docker rm <container_id>`.
- **docker images**: Lists your images. Example: `docker images`.
- **docker image rm**: Deletes an image. Example: `docker image rm my-image`.

### Running Your Container
Launch it:

```
docker run restock-calculator
```

However, you'll notice an error because the container can't find `input_data.json`. Let's fix that by mounting a volume.

### Handling Data Files with Volumes
Our restock calculator needs input and output files. We can use Docker volumes to mount these:

#TO CHECK
```
docker run -v $(pwd)/data:/app/data restock-calculator
```

But first, we need to update our Dockerfile to look for files in the data directory:

```
FROM python:3.10-slim
WORKDIR /app
COPY restock_calculator/lib/algorithm.py /app/
COPY restock_calculator/lib/utils.py /app/
RUN mkdir -p /app/data
ENV INPUT_FILE=/app/data/input_data.json
ENV OUTPUT_FILE=/app/data/output_data.json
CMD ["python", "algorithm.py"]
```

And modify our algorithm.py to use environment variables:

```python
import json
import os
from utils import load_json, save_json

def calculate_restock_needs():
    """
    Calculates which inventory items need restocking based on current stock and sales data.
    Restock rule: if stock < sales * 2, item needs restocking
    """
    # Load inventory data
    input_file = os.getenv("INPUT_FILE", "input_data.json")
    output_file = os.getenv("OUTPUT_FILE", "output_data.json")
    
    data = load_json(input_file)

    # Process each item to determine restock needs
    results = []
    for item in data:
        needs_restock = item["stock"] < item["sales"] * 2
        results.append({
            "item": item["item"],
            "current_stock": item["stock"],
            "recent_sales": item["sales"],
            "restock": needs_restock,
            "recommended_order": (item["sales"] * 2 - item["stock"]) if needs_restock else 0
        })

    # Save results to output file
    save_json(output_file, results)
    print(f"Processed {len(data)} inventory items. Results saved to {output_file}")


if __name__ == "__main__":
    calculate_restock_needs()
```

### WORKDIR: Keeping It Organized
Set a working directory:

```
FROM python:3.10-slim
WORKDIR /app
COPY sales_predictor.py .
CMD ["python", "./sales_predictor.py"]
```

- `WORKDIR /app`: Makes `/app` the default folder.
- `COPY sales_predictor.py .`: Copies to `/app` (dot = current directory).
- `CMD`: Uses `./` since we’re in `/app`.

Why? For structure, readability and debugging.

### Passing Data with Arguments

```
MAKE THE RUN FOR THE ALGORITHM.py. SO THAT THEY'RE FED TO THE PYTHON FILE AND AN OUTPUT FILE IS CREATED.
```


### Managing Dependencies with Poetry
If your project uses Poetry for dependency management, you can incorporate it into your Dockerfile:

```
FROM python:3.9-slim

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy only pyproject.toml and poetry.lock first to leverage Docker cache
COPY pyproject.toml poetry.lock* /app/

# Configure poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev

# Now copy the rest of the application
COPY restock_calculator /app/restock_calculator

# Create data directory
RUN mkdir -p /app/data

# Set environment variables
ENV INPUT_FILE=/app/data/input_data.json
ENV OUTPUT_FILE=/app/data/output_data.json

# Run the application
CMD ["python", "restock_calculator/lib/algorithm.py"]
```

This approach installs dependencies first (which change less frequently) before copying your code (which changes more often), making better use of Docker's layer caching.


### Why Docker Beats Virtual Machines
Docker containers share the host OS kernel, making them much lighter than VMs. For our restock calculator:
- A VM would need a full OS (gigabytes) just to run a simple Python script
- A Docker container only needs Python and your code (megabytes)
- Containers start in seconds, VMs take minutes
- You can run many containers on one machine, but only a few VMs

This makes Docker perfect for deploying applications in production environments.

## Wrapping Up
You've containerized a restock calculator, a real tool for inventory management. But just now business contacted you and
image need to have 50MB less in size. 
- How much currently is the image? 
- What is contributing the most?
- If you had to guess, what do you think could reduce the size (without touching the python code)?


## The exercises below are build on the previous container
### Exercise 1: Create Another Container

**Goal**: Build a SIMPLE python file `order_generator.py` that processes JSON output from `algorithm.py` to generate purchase orders, calculate costs, and integrate with Docker.

**Steps**:
1. Implement `order_generator.py`:
  * Create a function to read JSON output from `algorithm.py` identifying items needing restocking.
  * Generate purchase orders with fields: item name, quantity, supplier, and timestamp.
  * Calculate total order cost using a hardcoded price list (e.g., `{"item1": 10.0, "item2": 15.0}`).
  * Save orders to a JSON file (e.g., `orders.json`).
2. Update Dockerfile:
  * Base image: `python:3.10-slim`.
  * Make it depend on `algorithm.py`'s **output**.
3. Run the container

---


### Exercise 2: Implement Environment Variable Configuration

**Objective**: Enhance `order_generator.py` to use environment variables for configuration, updating Docker files accordingly.

**Steps**:
* Modify `order_generator.py`:
  * Read `DEFAULT_SUPPLIER` environment variable to set supplier (default: "SupplierA").
  * Apply pricing tiers using `BULK_DISCOUNT_THRESHOLD` (e.g., 10% discount if quantity > threshold).
  * Use `ORDER_API_ENDPOINT` for a mock order submission (print endpoint for now).
* Update Dockerfile:
  * Add `ENV` instructions or allow passing environment variables.
* Update `docker-compose.yml`:
  * Add environment variables to `order-generator` service:
    * `DEFAULT_SUPPLIER=SupplierA`
    * `BULK_DISCOUNT_THRESHOLD=100`
* Test configuration:
  * Run with different environment variable values to verify behavior.
