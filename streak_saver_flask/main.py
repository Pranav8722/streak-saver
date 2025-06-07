import streamlit as st
import requests
import os
import random
import string
import base64
import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# GitHub credentials
GITHUB_USER = "Pranav8722"
REPO_NAME = "streak-saver"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

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

    responses = []

    for filename, content in generate_dummy_files():
        api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{filename}"
        data = {
            "message": f"Auto commit {filename}",
            "content": base64.b64encode(content.encode()).decode()
        }
        response = requests.put(api_url, headers=headers, json=data)
        responses.append((filename, response.status_code, response.json()))

    return responses

# Streamlit App
st.set_page_config(page_title="Streak Saver", page_icon="🔥")
st.title("🔥 GitHub Streak Saver")

st.markdown("""
This app commits dummy files to your GitHub repo to help keep your contribution streak alive.
""")

if st.button("Commit to GitHub"):
    st.info("Committing files...")
    result = commit_to_github()
    for filename, status, resp in result:
        if status == 201:
            st.success(f"✅ {filename} committed successfully.")
        else:
            st.error(f"❌ Failed to commit {filename}: {resp.get('message')}")

st.markdown("---")
st.caption("Developed by Pranav8722")
