# Fixing Git Remote Configuration

The deployment failed because your git remote is pointing to a placeholder URL:
`https://github.com/YOUR_USERNAME/computer-lab-monitoring.git/`

## Steps to Fix

1.  **Create a Repository on GitHub**
    *   Go to [GitHub.com/new](https://github.com/new).
    *   Name it `computer-lab-monitoring` (or whatever you prefer).
    *   Do **not** add a README, .gitignore, or License (keep it empty).

2.  **Update the Remote URL**
    Copy the URL of your new repository and run the following command in your terminal:
    
    ```powershell
    git remote set-url origin https://github.com/<YOUR-ACTUAL-USERNAME>/<YOUR-REPO-NAME>.git
    ```
    *(Replace `<YOUR-ACTUAL-USERNAME>` and `<YOUR-REPO-NAME>` with your actual details)*

3.  **Push the Code**
    Once updated, retry the push command:
    
    ```powershell
    git push --set-upstream origin main
    ```
