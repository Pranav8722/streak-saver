from flask import Flask, render_template, redirect, url_for
import requests, os, random, string, base64, datetime

app = Flask(__name__)

# GitHub credentials
GITHUB_USER = "Pranav8722"
REPO_NAME = "streak-saver"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set this environment variable

# Function to generate dummy text files
def generate_dummy_files(n=5):
    files = []
    for _ in range(n):
        name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        filename = f"file_{name}.txt"
        content = f"Auto-generated on {datetime.datetime.now()} with file: {filename}"
        files.append((filename, content))
    return files

# GitHub commit function
def commit_to_github():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    for filename, content in generate_dummy_files():
        api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{filename}"
        data = {
            "message": f"Auto commit {filename}",
            "content": base64.b64encode(content.encode()).decode()
        }
        response = requests.put(api_url, headers=headers, json=data)
        print(response.status_code, response.json())

# Routes
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/commit')
def commit():
    commit_to_github()
    return redirect(url_for("home"))

# Run Flask server
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)


