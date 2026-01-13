"""
Script to initialize Git repository and push to GitHub
Run this script after installing Git for Windows
"""

import os
import subprocess
import sys

def run_command(cmd, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=cwd
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def setup_git_repo():
    # Change to your project directory
    project_dir = r"c:\Users\swati\Documents\Food ordering\Food ordering"
    
    print(f"Working in directory: {project_dir}")
    
    # Check if git is available
    returncode, stdout, stderr = run_command("git --version", project_dir)
    if returncode != 0:
        print("Git is not installed or not in PATH.")
        print("Please install Git from https://git-scm.com/download/win")
        print("Make sure to restart your terminal after installing Git.")
        return False
    
    print(f"Git version: {stdout.strip()}")
    
    # Initialize git repository
    print("\nInitializing Git repository...")
    returncode, stdout, stderr = run_command("git init", project_dir)
    if returncode != 0:
        print(f"Error initializing git: {stderr}")
        return False
    print("Repository initialized successfully.")
    
    # Check if remote origin already exists
    returncode, stdout, stderr = run_command("git remote get-url origin", project_dir)
    if returncode == 0:
        print("Remote origin already exists:", stdout.strip())
    else:
        # Add remote origin
        print("Adding remote origin...")
        remote_url = "https://github.com/swativerma08/Food_Ordering-system.git"
        returncode, stdout, stderr = run_command(f'git remote add origin "{remote_url}"', project_dir)
        if returncode != 0:
            print(f"Error adding remote: {stderr}")
            return False
        print("Remote origin added successfully.")
    
    # Add all files
    print("Adding all files...")
    returncode, stdout, stderr = run_command("git add .", project_dir)
    if returncode != 0:
        print(f"Error adding files: {stderr}")
        return False
    print("Files added successfully.")
    
    # Commit files
    print("Committing files...")
    returncode, stdout, stderr = run_command('git commit -m "Initial commit: Food ordering system"', project_dir)
    if returncode != 0:
        # If no changes to commit (maybe files were already committed), that's fine
        if "nothing to commit" in stderr or returncode == 0:
            print("Files committed successfully or no new changes to commit.")
        else:
            print(f"Error committing files: {stderr}")
            return False
    else:
        print("Files committed successfully.")
    
    # Set main branch and push
    print("Setting main branch and pushing to GitHub...")
    returncode, stdout, stderr = run_command("git branch -M main", project_dir)
    if returncode != 0:
        print(f"Error renaming branch: {stderr}")
        return False
    
    # Try to push
    returncode, stdout, stderr = run_command("git push -u origin main", project_dir)
    if returncode != 0:
        print(f"Push failed: {stderr}")
        print("\nPossible reasons:")
        print("- Remote repository may already have content (try git pull first)")
        print("- Authentication required (you may need to set up GitHub credentials)")
        print("- Network issues")
        return False
    
    print("Successfully pushed to GitHub!")
    return True

if __name__ == "__main__":
    print("Git Repository Setup Script")
    print("="*30)
    
    success = setup_git_repo()
    
    if success:
        print("\nYour code has been successfully pushed to GitHub!")
    else:
        print("\nSetup failed. Please follow the manual steps in GIT_SETUP_GUIDE.txt")