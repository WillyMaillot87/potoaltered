# PotoAltered
This project is a work in progress. Contributions and feedback are welcome.

## **Features**
This app offers a comprehensive solution for tracking your **Altered** collection. Key features include :

- Detailed inventory of your collection
- Automated card consolidation by name
- Identification of missing and excess cards
- Easy comparison of your collection with a friend's

## **How to use**
There are two ways to use this application:

### 1. Web App

For a quick and easy experience, access the web app directly through this link:

[https://potoaltered.streamlit.app/](https://potoaltered.streamlit.app/)

### 2. Desktop App (Windows Only)

For offline use, download the desktop app:

- Download the application ([download file](https://drive.google.com/drive/folders/1Xughs42UaLViGV5dEk2X3UrRpGelHhxO?usp=sharing)).
- Unzip the downloaded file to a directory of your choice.
- Double-click on the potoaltered.exe file to launch the application.

### 3. Pull from github repo:

**Prerequisites:**
   - Ensure you have Git installed on your system. You can download it from https://git-scm.com/downloads.
   - Python 3.11 is also required. You can check your version by running `python --version` in your terminal. If you need Python, download it from https://www.python.org/downloads/.

**Clone the Repository:**
   - Open a terminal window and navigate to your desired working directory.
   - Run the following command to clone the repository:

     `git clone https://github.com/WillyMaillot87/PotoAltered`

   - This will create a new directory named *PotoAltered* in your current working directory.

**Install Dependencies:**
   - Navigate to the cloned directory:

     `cd PotoAltered`

   - Install the required dependencies listed in *requirements.txt* :

     `pip install -r requirements.txt`

     This command will download and install all the necessary libraries needed for your application to run.

**Run the Application:**
   - Start the Streamlit app using the following command:

     `streamlit run app.py`

   - This will launch your application in a web browser at `http://localhost:8501`. You can now interact with the app's features and functionalities.

## **Get your token**

In order to access your cards collection, you'll need to get your own token from altered.gg website. Here is how to proceed : 
- Connect to altered.gg with your account
- Press F12 to access to the browser developer tool
- go to the "network" section
- Press F5 to refresh the page
- in the browser developer tool look for the line showing the *api.altered.gg/me* request
- copy the Bearer token in the header "Authorization"
- Paste it in your PotoAltered app
- That's it !


