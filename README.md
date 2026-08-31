# ResearchMind · Studio Workspace

ResearchMind is an interactive multi-agent workspace built with Streamlit and powered by Groq LLMs and Tavily Search. It coordinates autonomous agents to search, scrape, synthesize, and review research topics in real time.

---

## 🛠️ Step-by-Step Setup & Execution

### 1. Clone the Repository
Clone the project repository to your local machine using Git and navigate into the project directory:

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```

---

### 2. Create a Virtual Environment
Set up an isolated Python virtual environment to manage dependencies:

* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  ```

* **Windows:**
  ```cmd
  python -m venv venv
  ```

---

### 3. Activate the Virtual Environment
Activate the environment prior to installing packages or running the application:

* **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

* **Windows (Command Prompt):**
  ```cmd
  venv\Scripts\activate.bat
  ```

* **Windows (PowerShell):**
  ```powershell
  venv\Scripts\Activate.ps1
  ```

---

### 4. Obtain Required API Keys
You will need API keys from both Groq and Tavily:

* **Groq API Key:** Sign up or log in at the [Groq Console](https://console.groq.com/) to generate an API key.
* **Tavily API Key:** Sign up or log in at [Tavily AI](https://tavily.com/) to retrieve your search API key.

---

### 5. Configure Environment Variables
Set your API keys as environment variables. You can export them in your terminal session or store them in a `.env` file.

#### Option A: Terminal Export (Current Session)

* **macOS / Linux:**
  ```bash
  export GROQ_API_KEY="your_groq_api_key_here"
  export TAVILY_API_KEY="your_tavily_api_key_here"
  ```

* **Windows (Command Prompt):**
  ```cmd
  set GROQ_API_KEY="your_groq_api_key_here"
  set TAVILY_API_KEY="your_tavily_api_key_here"
  ```

* **Windows (PowerShell):**
  ```powershell
  $env:GROQ_API_KEY="your_groq_api_key_here"
  $env:TAVILY_API_KEY="your_tavily_api_key_here"
  ```

#### Option B: Using a `.env` File
Create a `.env` file in the root directory of your project:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

---

### 6. Install Dependencies
Ensure your virtual environment is active, then install the required Python packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 7. Run the Streamlit Application
Launch the application using Streamlit:

```bash
streamlit run app.py
```

*Replace `app.py` with the filename of your main entry point script if named differently.*

Once executed, Streamlit will start a local server and automatically open the application workspace in your browser at `http://localhost:8501`.
