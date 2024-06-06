# Save the following script to a file named setup_project.ps1

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install Python from https://www.python.org/downloads/."
    exit 1
}

# Set up a virtual environment
Write-Host "Setting up a virtual environment..."
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Create .env file for environment variables
Write-Host "Setting up environment variables..."
$envFilePath = ".env"
if (-Not (Test-Path $envFilePath)) {
    New-Item -Path $envFilePath -ItemType File -Force
}
Add-Content -Path $envFilePath -Value "OPENAI_API_KEY=your_openai_api_key"

# Run the application
Write-Host "Running the application..."
python app.py
