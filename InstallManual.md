# Installation Guide

This guide provides instructions for both manual and automatic installation using PowerShell scripts.

## **Manual Installation**

Before you begin, ensure you have the following software installed:

- **Python 3**

### Step 1: Extract the Project

Extract the project to the desired location on your system.

### Step 2: Set Up a Virtual Environment (Optional)

Setting up a virtual environment is optional but recommended to avoid impacting other programs or packages and to maintain stability. You can read more about [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html).

1. Open Command Prompt (cmd) and navigate to the project folder.
2. Run the following commands:

    ```bash
    # Create a virtual environment
    python -m venv venv
    
    # Activate the virtual environment
    .\venv\Scripts\Activate
    ```

3. With the virtual environment activated, install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Step 3: Configure the API Key

Ensure that the API key is available in the `.env` file:

1. Create a file named `.env` in the project folder.
2. Add your OpenAI API key as follows:

    ```bash
    OPENAI_API_KEY=your_openai_api_key
    ```

3. Save the `.env` file in the root of your project. This step is required to run the application in the virtual environment.

### Step 4: Run the Application

After completing the above steps, you can run the program:


python app.py

### **Without Virtual Environment**

As an alternative, you can install the dependencies without setting up a virtual environment:

1. Open Command Prompt (cmd) and run:

    ```bash
    pip install -r requirements.txt
    ```

2. Set the API key in the system environment variables:

    ```bash
    setx OPENAI_API_KEY "YOUR_API_KEY_HERE"
    ```

3. Restart Command Prompt and navigate to your project directory.

4. Run the Flask server:

    ```bash
    python app.py
    ```

5. Open a browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## **Automatic Installation with PowerShell Script**

> **Note:** For security reasons, the script only installs the application in a virtual environment. If you wish to install it outside of a virtual environment, either follow the manual installation steps or modify the script to avoid entering the virtual environment at the beginning.

### Step 1: Run PowerShell as Administrator

Press `Win + X` and select **PowerShell (Admin)**.

### Step 2: Navigate to the Project Directory

Use the `cd` command to navigate to the project folder.

### Step 3: Execute the Script

Run the setup script:

```bash
.\setup.ps1
```


The script will handle the installation and will attempt to run the program if everything goes smoothly.

Step 4: API Key Configuration
The API key is not included in the script. After running the script, add your API key to the .env file as described in the manual installation steps.

Step 5: Handling Execution Policies
If you encounter errors related to execution policies, you may need to adjust them temporarily:

Change the execution policy:

```bash
Set-ExecutionPolicy RemoteSigned
```
After running the script, you can restore the original execution policy:

```bash
Set-ExecutionPolicy Restricted
```
### Key Points:

1. **Indentation:** Ensure that any sub-items or code blocks are indented correctly under their respective list items or headings.
2. **Code Blocks:** Use triple backticks (\`\`\`) to denote code blocks, followed by the language identifier (e.g., `bash`).
3. **Links:** Ensure that URLs are enclosed in square brackets with a descriptive text, followed by the actual URL in parentheses.
