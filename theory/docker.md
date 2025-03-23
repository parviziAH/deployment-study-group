## What's Docker and Why It’s Your New Best Friend
Docker is a tool that wraps your code, libraries, and settings into a **container**—a lightweight, portable box that runs the same way everywhere Docker’s installed. Think of it like shipping a product: you pack it in a standard box, and it arrives intact no matter where it goes.

**Real-world scenario:** You’ve built a sales prediction script that works perfectly on your laptop. Your boss says, “Deploy it!” Without Docker, chaos hits:
- Your Python version (say, 3.9) doesn’t match the server’s (3.7)—crash.
- A library like `pandas` is missing—crash.
- File paths are different—crash.
- Your teammate can’t even run it to double-check your work.

With Docker, you pack everything—code, Python version, libraries—into one container. It runs the same on your laptop, 
the test server, or production. This is how a deployment works.

### Images vs. Containers: The Basics
- **Image:** The blueprint. It’s like a package with your code and tools (e.g., Python, your script, files, dependencies).
You build it once with `docker build`.
- **Container:** The running version of the **image**. It’s what you launch from the image with `docker run`. Stop it or 
run it again.

**Think of it like this:** An image is a cake recipe—mix the ingredients, bake it once. A container is a slice—you cut 
as many as you need, and they’re all identical. You’ll build one image and spin up containers to test or deploy.

### The Docker Daemon: Who's doing the trick?
Docker isn’t magic—it’s powered by the **Docker daemon**, a background process on your machine (or server) that manages 
images, containers, and everything else. When you type a command like `docker run`, you’re telling the daemon, “Hey, do 
this for me.” It’s like a chef in the kitchen—you give the orders, it cooks the meal.

- **Why care?** If Docker’s not working, it’s often because the daemon’s stopped (e.g., Docker Desktop isn’t running for
whatever reason. You can check with `docker info`). Restart it, and you’re good to go again.

### Your First Dockerfile: The Recipe
ADD A PART WHER YOU EXPLAIN THAT DOCKER IS BUILD IN LAYERS, SO YOU WANT TO PUT THE MOST FREQUENTLY CHANGING FILES AT THE 
START

A `Dockerfile` is a text file that tells Docker how to build your image. No `Dockerfile`, no container—it’s that simple. 
Here’s a basic one for a sales predictor:

```
FROM python:3.9-slim
COPY sales_predictor.py /app/
CMD ["python", "/app/sales_predictor.py"]
```

- **Breaking down the instructions:**
  - `FROM`: Picks the base image—like choosing a starter kit. Here, `python:3.9-slim` gives you Python 3.9 with minimal extras (lightweight).
  - `COPY`: Moves files from your machine to the container. `COPY sales_predictor.py /app/` puts your script in the container’s `/app` folder.
  - `CMD`: Sets the default command to run when the container starts. `["python", "/app/sales_predictor.py"]` says, “Run this script with Python.”

Save this as `Dockerfile` (no extension) in a folder with your script.

### More Dockerfile Commands You’ll Use
Here’s the rundown of key `Dockerfile` instructions—think of them as steps in a recipe:
- **WORKDIR**: Sets the “current directory” inside the container, like `cd` in a terminal. Example: `WORKDIR /app` makes `/app` your base folder.
- **RUN**: Executes a command during the build—like installing stuff. Example: `RUN pip install numpy` adds NumPy to your image.
- **COPY**: Copies files from your machine to the container. Example: `COPY . .` grabs everything in your folder (careful with this—only copy what’s needed).
- **ENV**: Sets environment variables, like settings you can tweak. Example: `ENV MY_VAR=value`.
- **ENTRYPOINT**: Locks in a base command (e.g., `ENTRYPOINT ["python"]`), letting `CMD` add arguments.

Why? Each line builds your image layer by layer—miss one, and your container’s toast.

### Building It: What’s the `.` in `docker build`?
Run this in your terminal, in the same folder as your `Dockerfile`:

```
docker build -t sales-predictor .
```

- `-t sales-predictor`: Tags your image with a name so you can reference it later (e.g., `sales-predictor`).
- `.`: The dot means “use this folder as the build context.” It tells Docker where to find the `Dockerfile` and any files it needs (like `sales_predictor.py`).

You’ll see Docker pull Python, copy your file, and build the image. Check it with `docker images`—`sales-predictor` will be there.

### A Working Example: `sales_predictor.py`
SUBSTITUTE THIS WITH THE ALGORITHM.PY IN THE OTHER FOLDER

Here’s a real script—something a junior MLOps engineer might build. It predicts next week’s sales based on the last three weeks:

```
# sales_predictor.py
import sys

# Mock sales data (or pass it in later)
sales = [100, 120, 110]  # Last 3 weeks

# Simple average-based prediction
next_week = sum(sales) / len(sales)
print(f"Predicted sales for next week: {next_week}")
```

Save this as `sales_predictor.py` next to your `Dockerfile`. It’s simple but practical—like a task to “containerize this predictor for the team.”

### Basic Docker Commands: Your Toolkit
Here’s what you’ll type daily to control Docker:
- **docker build**: Builds an image from a `Dockerfile`. Example: `docker build -t my-image .`.
- **docker run**: Starts a container from an image. Example: `docker run my-image`.
  - Add `--rm` to delete it after: `docker run --rm my-image`.
  - Add `-it` for interactive mode (see output): `docker run -it my-image`.
- **docker ps**: Lists running containers. Add `-a` for all containers: `docker ps -a`.
- **docker stop**: Stops a running container. Example: `docker stop <container_id>` (grab the ID from `docker ps`).
- **docker rm**: Deletes a stopped container. Example: `docker rm <container_id>`.
- **docker images**: Lists your images. Example: `docker images`.
- **docker image rm**: Deletes an image. Example: `docker image rm my-image`.


### Running Your Container
Launch it:

```
docker run sales-predictor
```

Output: `Predicted sales for next week: 110.0`. Your first containerized app! Use `--rm` to clean up: `docker run --rm sales-predictor`.

### Adding Libraries
CHANGE THIS PART. YOU HAVE A POETRY FILE, YOU DONT NEED THIS. BUT YOU NEED TO GET THE DEPENDENCIES FORM THE POETRY FILE


Real ML needs libraries. Update the `Dockerfile`:

```
FROM python:3.9-slim
RUN pip install numpy
COPY sales_predictor.py /app/
CMD ["python", "/app/sales_predictor.py"]
```

- `RUN pip install numpy`: Installs NumPy during the build. Without this, `import numpy` fails.

Rebuild: `docker build -t sales-predictor .`. Run it again—now you can use NumPy.

### WORKDIR: Keeping It Organized
Set a working directory:

```
FROM python:3.9-slim
WORKDIR /app
COPY sales_predictor.py .
CMD ["python", "./sales_predictor.py"]
```

- `WORKDIR /app`: Makes `/app` the default folder.
- `COPY sales_predictor.py .`: Copies to `/app` (dot = current directory).
- `CMD`: Uses `./` since we’re in `/app`.

Why? It’s like keeping your desk clean—everything’s where it belongs.

### Passing Data with Arguments
Update the script:

```
# sales_predictor.py
import sys

if len(sys.argv) < 4:
    print("Usage: python sales_predictor.py <week1> <week2> <week3>")
    sys.exit(1)

sales = [float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])]
next_week = sum(sales) / len(sales)
print(f"Predicted sales for next week: {next_week}")
```

Run it:

```
docker run sales-predictor 100 120 110
```

Output: `Predicted sales for next week: 110.0`. Now it’s dynamic—real-world vibes.


### Why Docker Beats Virtual Machines?
ADD TO THIS PART AND PUT IT EARLIER

A VM runs a full OS—slow and heavy. Docker uses your machine’s OS, adding just your app and libs. It’s fast and light—perfect for ML deployments.

## Wrapping Up
You’ve containerized a sales predictor—a real tool for guessing next week’s numbers. The exercises below build on this, giving you job-ready MLOps skills.

### Subchapter 3.1: Introduction to Docker
- **Exercise 1**: Write a `Dockerfile` for `sales_predictor.py` with Python 3.9 and NumPy.
- **Exercise 2**: Build and run it with `docker build -t sales-predictor .` and `docker run sales-predictor`.
- **Exercise 3**: Add a print statement to log the prediction. Rebuild and run.
- **Exercise 4**: Pass sales data (e.g., `100 120 110`) as arguments and test.
- **Exercise 5**: Add `WORKDIR /app` to the `Dockerfile`, adjust paths, rebuild, and test.

### Subchapter 3.2: Managing Dependencies and Data
- **Exercise 1**: Add `RUN pip install pandas` to the `Dockerfile`. Rebuild.
- **Exercise 2**: Use Pandas in `sales_predictor.py` for averaging (e.g., `df.mean()`). Test it.
- **Exercise 3**: Mount a `sales.txt` file as a volume and read it in the script.
- **Exercise 4**: Add `ENV PREDICTION_TYPE=average` and check it with `os.getenv()`. Run with `-e`.
- **Exercise 5**: Save the prediction to `prediction.txt` and mount it back.

### Subchapter 3.3: Scaling Up
- **Exercise 1**: Tag your image (e.g., `sales-predictor:v1.0`) and check with `docker images`.
- **Exercise 2**: Add a NumPy-based linear regression to predict trends.
- **Exercise 3**: Write a `docker-compose.yml` to run with a mounted `sales.txt`.
- **Exercise 4**: Add file logging to the script, rebuild, and test.
- **Exercise 5**: Clean up all containers with `docker ps -a` and `docker rm`.
