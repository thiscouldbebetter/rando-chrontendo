Using Rando Chrontendo to Post to Mastodon
==========================================

1. Log in to Mastodon with valid credentials.  Make a note of the URL of the Mastodon instance.

2. On the Mastodon homepage, click "Preferences".

3. On the Preferences page, click the "Development" menu item.

4. On the "Your applications" page, click the "New Application" button.

5. On the "New application" page, in the "Application Name" box, enter the text "rando-chrontendo".

6. Click the Submit button.

7. Back on the "Your applications" page, click the new link for "rando-chrontendo".

8. On the "Application:rando-chrontendo" page, make a note of the value in the field named "Your access token".

9. If you have not already done so, install Git.

10. From any convenient directory, run the following command to download the "Rando Chrontendo" script and its supporting repository.

	git clone https://github.com/thiscouldbebetter/rando-chrontendo

11. Within the newly downloaded repository, locate the file "Source/SetEnvironmentVariablesAndRun.sh" and open it in a text editor.

12. Within the .sh file, substitute the access token obtained in step 8 and the hostname of the Mastodon instance (for example, "mstdn.social") where appropriate, then save the file.

13. Within the rando-chrontendo directory, locate the directory named "Content".

14. Open a web browser and, in the address bar, enter the URL given below to download a sample video file.  Note that this is only the first of many videos; downloading all of them would take many hours.

	https://archive.org/download/chrontendo-yt/Chrontendo/62-Chrontendo%20Episode%201-20130715.mp4

15. Copy the .mp4 video file downloaded in the previous step into the "Content" directory.

16. Make sure that Python 3 is installed, perhaps by running the command "sudo apt install python3".

17. Make sure that Pip (the Python package manager) is installed, perhaps by running the command "sudo apt install pip".

18. Install the necessary python modules by running the command "pip install substitute_modulename_here" multiple times, substituting the module names "opencv-python", "pytumblr", "cohost", "Mastodon.py", and "twitter" where appropriate.

19. Make the SetEnvironmentVariablesAndRun.sh script runnable, perhaps by running the command "sudo chmod +x SetEnvironmentVariablesAndRun.sh".

20. Open a command prompt and run the command "./SetEnvironmentVariablesAndRun.sh".

21. In the web browser, verify that a new post was posted to Mastodon, containing a random frame from the video stored in the Content directory.
