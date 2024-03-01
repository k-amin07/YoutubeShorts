# YoutubeShorts
Youtube shorts project for Topics in Internet Research Course 

## Currently Working Approaches
### Screen Recording
This is the primary approach since it is easiest to implement and is pretty much device agnostic. Use it if you do not have an Android device or are unable to root your device.
- Enable stats for nerds in general section for YouTube app settings. Navigate to shorts, click the three dot menu and click stats for nerds.
- Switch the phone to 2G network mode, do not use WiFi.
- Screen record youtube shorts MANUALLY. Make sure that the short plays to completion before scrolling. Autoscrolling solutions will be inaccurate as shorts vary in length. An elaborate mechanism can be established to automate this without compromising data quality, but it is easier to just scroll it manually.
- Make sure you have pytesseract installed with the English Language package. Search for distro-specific instructions but generally you need tesseract-ocr and at least one language package before it can be used with python.
- Use the read_frames script to extract frames from the video. The script is currently configured to extract 4 frames per second. The framerate for screenrecording that I used was 60 fps. This is not the framerate at which the shorts are being fetched; this is the framerate at which the phone recorded the screen.
- Run the extract data from frames script. It turns the image to grayscale, extracts the text using OCR, converts it to a dictionary and saves it to a pickle file. Do not commit your recorded video or extracted frames to git, just commit the pickle file but name it appropriately.

### MITM Proxy
This one requires a Rooted Android device. It **may** work with iOS devices (see the bold text in the 7th point below) but I am unable to verify as I do not own an iOS device. This approach requires a WiFi connection, so we would need to figure out a way to throttle the WiFi speed to emulate a 2G connection **OR** enable systemwide HTTP proxy on mobile data.
- Download MITM proxy. Extract the zip and open terminal in the extracted folder.
- Make the mitmweb file executable using
    ```
        chmod +x ./mitmweb
    ```
- Run MITM web.
    ```
        ./mitmweb
    ```
 - Root your device with Magisk. **This is absolutely necessary** for this setup to work. You should be able to find instructions for rooting your device on forum.xda-developers.com
 - Make sure your phone and the computer running the mitm server are on the same WiFi network.
 - Open Wifi settings on Android, select your wifi network and add the IP address of your laptop and MITM's port to the network's proxy settings.
 - Open Chrome on Android, go to mitm.it. If mitm is configured correctly, you would see certificate install instructions. **This page contains instructions for iOS devices as well**, could be worth exploring.
 - In the instructions for Android, choose the Magisk module. Install it in Magisk, and reboot the device. YouTube uses SSL pinning, so without this Magisk module, mitm would not be able to capture the traffic from YouTube.
 - Open `mitmweb` on your laptop and you should be able to see all requests that are made by your phone.
 - This [repo](https://github.com/ddxv/mobile-network-traffic?tab=readme-ov-file#open-source-link-1) also contains instructions on rooting Waydroid and using mitm. It relies on LSPosed for traffic monitoring, however the instructions in this section do not require LSPosed.
----
## Instructions on Using git:

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
