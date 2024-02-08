# YoutubeShorts
Youtube shorts project for Topics in Internet Research Course 

Using git:

- You would first need to add an ssh keypair to your github account, refer to [github docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) for that.
- Add your username and email to the git command line. For example:
    ```
    git config user.name "Khizar Amin"
    git config user.email "khizaramin95@gmail.com"
    ```
- Clone the repo: go to the git repo, click clone, choose SSH, copy link and then in your terminal, do git clone <copied-url-goes-here>. For this particular repo, just copy paste this in your terminal
    ```
    git clone git@github.com:k-amin07/YoutubeShorts.git
    ```
- If you are not comfortable with the command line, VSCode provides an extension for git. Feel free to use that.
- For every new thing that you do, create a new branch. First do 
    ```
    git switch main
    ```
    then do git checkout -b yourusername/date/what-you-are-doing. For example
    ```
    git checkout -b kamin/2024-02-08/update-instructions-in-readme
    ```
- For newly created branches, the git extension will give an option to publish the branch.
- Do your work, commit frequently. Once you are satisfied, push your committed changes.
- Ideally, you should do
    ```
    git pull origin main
    ```
    after committing and **before pushing** your code.
- Sometimes, you will get merge conflicts when pulling code from github as multiple people are working on it, VSCode provides an interactable way to resolve these merge conflicts. 
    - For each line that conflicts, it will give an option to keep your changes or keep remote changes or keep both.
    - At each conflicting line, choose the suitable option. Sometimes it may require a bit of code reorganizing.
    - Once done, commit your changes and push them to your branch.
- Make sure everything is working in your branch before proceeding.
- Go to github and create a pull request for the main branch. 
- Avoid committing directly to the main branch, even for small changes. It will help avoid merge conflicts later.
- One person must be in charge of merging code to the main branch. If merginge one person's code creates conflicts in another persons code, the person who's code is affected must resolve the conflicts locally and update the pull request.