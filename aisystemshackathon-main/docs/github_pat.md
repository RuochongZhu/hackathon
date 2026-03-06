![](images/banner_thin.png)
---

# Getting Your Github Personal Access Token to Commit, Pull, and Push to Repos

🕒 *Estimated Time: 10 minutes*

In this activity, you will follow the steps to allow you to commit, pull, and push changes on GitHub repositories. Please be sure to create a GitHub Repository first.

## Prerequisites
- Must have already made a GitHub Account
- Must have already made or been added to a GitHub Repository
- Must have the complete URL of the GitHub Repository. For example, our Hackathon repo is https://github.com/timothyfraser/aisystemshackathon.git

## Tasks
- Navigate to GitHub.com and click on your profile icon in the upper right hand corner.
- Click on Profile
- In the left hand menu, navigate to Developer Settings
- Select Create a Personal Access Token. You can either make a fine-grained token (specify the repository) or a standard token (access to all your GitHub repositories). Either is fine; a standard token is often easier for new users.
- Create a name for the token
- Create an expiration date for the token. Pick one after the end of this term.
- Under scopes, select what powers to give to the token. Please select the **public_repo** scope and **repo** scope.
- Copy the token and store it in a secure location (e.g., password manager or note-taking app).
- Open Posit Cloud / RStudio / Positron / Cursor / VSCode
- Create a new project from GitHub using your repository URL (should end in .git)
- Install: `install.packages(c("gert", "credentials"))`
- Create one new file, then run the script below and check the output in your R console and terminal.

```r
library(gert)
library(credentials)

credentials::set_github_pat()
# This will prompt you to enter your GitHub Personal Access Token.

gert::git_pull()   # pull most recent changes from GitHub
gert::git_add(dir(all.files = TRUE))   # stage new or edited files
gert::git_commit_all("my first commit")   # commit
gert::git_push()   # push your commit to GitHub
```

---

![](images/banner_icons.png)

<p align="center">
  <b><a href="https://github.com/timothyfraser/aisystemshackathon/tree/main">🏠 Return to Home Page</a></b>
</p>
