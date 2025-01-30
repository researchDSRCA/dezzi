# Dezzi - Your AI-Powered Research Assistant

Welcome to **Dezzi**, an AI-powered tool designed to assist researchers in enhancing their understanding for DSR.
## 🚀 Getting Started

Follow these steps to set up Dezzi on your local machine.

### 1️⃣ Clone the Repository
```bash
git clone NAME OF THE REPO
```

### 2️⃣ Create and Activate a Virtual Environment
```bash
python -m venv .venv
```

Activate the virtual environment:
- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 3️⃣ Install Dependencies
Some packages require a specific pip version due to metadata issues. Ensure you use a version below 24.1 before installing these:
```bash
pip install --upgrade "pip<24.1"
pip install six==1.16.0 unstructured-client==0.24.1
```
```bash
pip install -r requirements.txt
```

### 4️⃣ Install LIGHTRAG & SWARM
Dezzi uses [LIGHTRAG](https://github.com/HKUDS/LightRAG) for enhanced document retrieval. Install it in your project:
```bash
git clone https://github.com/HKUDS/LightRAG.git
cd LightRAG
pip install .
cd ..
```

Additionally, install [SWARM](https://github.com/openai/swarm.git):
```bash
git clone https://github.com/openai/swarm.git
cd swarm
pip install .
cd ..
```

### 5️⃣ Setup Directories
Create the following folders inside your project:
```bash
mkdir lightrag_files
mkdir proceeding_publications
```
Place the **PDF documents** that Dezzi should process inside `proceeding_publications`.

### 6️⃣ Configure Environment Variables
Create a `.env` file in the root directory and add your API keys:
```plaintext
OPENAI_API_KEY="INSERT_YOUR_OPENAI_API_KEY_HERE"
UNSTRUCTURED_API_KEY="INSERT_YOUR_UNSTRUCTURED_API_KEY_HERE"
```

### 7️⃣ Updating the Knowledge Base
To add new PDF files to the knowledge base, uncomment the relevant code in `agent_pool.py` and start the application as written in section 8. Once processing is done, comment it out again to avoid redundant updates.

### 8️⃣ Start Dezzi
Run the application using:
```bash
streamlit run app.py
```
A new browser window should open where you can interact with Dezzi.

### ❌ Stopping Dezzi
To stop the application, press:
```bash
CTRL + C
```

---

## 🏆 Credits
This project is based on [GilGPT](https://github.com/GilGPT/GilGPT_2025/tree/main).

---

Enjoy using Dezzi and feel free to contribute! 🚀
