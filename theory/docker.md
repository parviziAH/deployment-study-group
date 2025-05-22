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

### Why Docker Beats Virtual Machines
Docker containers share the host OS kernel, making them much lighter than VMs. For our restock calculator:
- A VM would need a full OS (gigabytes) just to run a simple Python script
- A Docker container only needs Python and your code (megabytes)
- Containers start in seconds, VMs take minutes
- You can run many containers on one machine, but only a few VMs

This makes Docker perfect for deploying applications in production environments.

### Your First Dockerfile: The Recipe
A `Dockerfile` is a text file that tells Docker how to build your image. No `Dockerfile`, no container—it's that simple. 
Here's a basic one for our restock calculator:

```
FROM python:3.10-slim
WORKDIR /app
COPY restock_calculator/lib/algorithm.py /app/
COPY restock_calculator/lib/utils.py /app/
COPY restock_calculator/files/input_data.json /app/

RUN mkdir -p /app/data
CMD ["python", "algorithm.py"]
```

- **Breaking down the instructions:**
  - `FROM`: Picks the base image—like choosing a starter kit. Yes, a layer can also be **another image**. Here, 
  `python:3.10-slim` gives you Python 3.10 with minimal extras (the "slim" part).
  - `WORKDIR`: Sets the working directory inside the container to `/app`. The container can be explored like a file system.
  - `COPY`: Moves files from your machine to the container. We copy the algorithm, utils files, and the input that we need
generate the output.
  - `CMD`: Sets the default command to run when the container starts. `["python", "algorithm.py"]` it's like typing in the
  terminal `python algorithm.py`

Save this as `Dockerfile` (no extension) in your project's root folder.

### More Dockerfile Commands You'll Use
Here's the rundown of key `Dockerfile` instructions. Each line corresponds to a layer:
- **WORKDIR**: Sets the "current directory" inside the container, like `cd` in a terminal. Example: `WORKDIR /app` makes `/app` your base folder. Why? For structure, readability and debugging.
- **RUN**: Executes a command during the build—like installing stuff. Example: `RUN pip install numpy` adds NumPy to your image.
- **COPY**: Copies files from your machine to the container. Example: `COPY . .` grabs everything in your folder (careful with this—only copy what's needed).
- **ENV**: Sets environment variables, like settings you can tweak. Example: `ENV MY_VAR=value`.
- **ENTRYPOINT**: Locks in a base command (e.g., `ENTRYPOINT ["python"]`), letting `CMD` add arguments.
- **VOLUME**: Shares a folder with the host machine. Example: `VOLUME /data` makes `/data` accessible from both the 
container and your machine.


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

However, you'll notice that while the application runs, there's no way to retrieve the output file after the container 
exits. The output is generated inside the container but is lost when the container stops.

### Handling Data Files with Volumes
What just happened is because Docker containers are temporary by design: when they stop running, any data created inside 
them is lost unless specifically saved. This approach might be sufficient for applications that don't need to save 
data or for simple testing, but it's not practical for data processing applications like our restock calculator.


To solve this problem, we can use Docker volumes which are dedicated storage locations that exist outside the 
container's filesystem. Think of them as bridges connecting your container to the host (or cloud) machine's storage. 
They allow data to still exists outside the container's lifecycle.

To implement, we need to modify our Dockerfile to:
1. Adjust `algorithm.py` so that it accept an output path as argument
2. Create a local folder for the data
3. Declare the volume in the Dockerfile
4. Run the container with the tag `-v` followed by the directory you just created + ":" + the path inside the container
   (e.g. my/local/path:/container/path)
5. Check that the application actually writes to this directory

Try to do it!

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

### Exercise 2: Implement Environment Variables for Output Configuration

**Goal**: Configure your application to use environment variables for specifying output locations, allowing flexible file paths without code changes.
**Steps**:

1. Modify algorithm.py to read environment variables:
   * Use `OUTPUT_PATH` to determine where to save the output file
   * Add fallback to a default location if variable isn't set
2. Update Dockerfile:
   * Add `ENV` command
   * Keep the simple `CMD ["python", "algorithm.py"]` structure
3. Test your implementation:
   * Build and run with default settings
   * Verify output appears in the mounted volume with expected filename
   * Verify output appears in the local directory with expected filename



### Exercise 3: Build step and installing the whl 

**Goal**: Create a Docker image with a build step to install a Python wheel file.


##### What is Poetry build?
`poetry build` is a command that packages your Python project into distribution formats (wheel (`.whl` for example). 
It handles dependency resolution and metadata generation automatically based on your `pyproject.toml` configuration.

##### What is a wheel?
A wheel (.whl) is a built package format for Python that contains all ready-to-install components of a project. 
Unlike source distributions, wheels are pre-built, making installation faster and more reliable as they don't require 
a compilation step.

##### Why use wheels in production containers?
Production containers typically use wheels because:
  * Faster deployment - no compilation needed during container startup
  * Smaller images - build dependencies aren't required in the final container
  * Better security - reduces attack surface by excluding development tools
  * Simplified dependency management - all dependencies are resolved ahead of time

**Steps**:

1. First, build your wheel file locally using Poetry:
   ```
    poetry build
    ```
2. Create a Dockerfile that installs this wheel:
 * Copy the wheel file
 * Install the wheel
 * Set up volume and environment
3. Test your implementation


