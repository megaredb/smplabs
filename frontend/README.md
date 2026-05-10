# Frontend - Local Development Guide

Welcome to the frontend part of our project! This beginner-friendly guide will help you set up and run the project in development mode on your local machine. We are not using Docker at this stage.

## Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js** (version 18 or higher is recommended)
- **pnpm** (a fast package manager, installable via `npm install -g pnpm` if you have Node.js)
- **Git** (for cloning repositories)

---

## Step 1. Clone and Compile Orval (Important!)

Our project uses **Orval** to generate the API client code. Currently, you need to clone it directly from GitHub and compile it locally.

Open your terminal and run the following commands in a directory of your choice (it can be next to our project folder):

```bash
# 1. Clone the Orval repository
git clone https://github.com/anymaniax/orval.git

# 2. Go to the downloaded folder
cd orval

# 3. Install dependencies for Orval itself
bun install

# 4. Compile the project
bun run build
```

> **Note:** After successfully building `orval`, you can use it in the project. If you have any trouble linking the locally built `orval` to our frontend (e.g., using `pnpm link`), please ask the team for help!

---

## Step 2. Install Frontend Dependencies

Now, go back to the `frontend` folder of our project in your terminal and download all the necessary packages:

```bash
pnpm install
```

---

## Step 3. Start the Development Server

Once all packages are installed, you can start the project:

```bash
pnpm dev
```

Your terminal will display a local address (usually `http://localhost:5173`). Open this link in your browser.
Now, whenever you modify files in the `src` folder, the page in the browser will update automatically.

Happy coding! If something isn't working, don't hesitate to ask questions!
