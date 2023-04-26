# Roborigger-Dashboard PDF Maker guide

## Development

Feature development should happen on dividual feature branches for larger features/fixes or the **develop** branch for minor features/fixes.

### Requirements:

- [Docker](https://www.docker.com/)
- [Visual Studio Code](https://code.visualstudio.com/)

### To start development:

1. Clone this repository to your computer
2. Open Docker and keep it running
3. Open Visual Studio Code (VS Code)
4. Open the cloned folder from VS Code (File > Open folder... > cloned_folder)
5. Open Terminal in VS Code (Terminal > New Terminal)
6. Checkout to the develop branch in Terminal `git checkout develop` 
7. Build docker image for developing environment `docker-compose up` or `docker-compose up --build` if last time install package during the development
8. Open a new terminal in VS Code (Terminal > Split Terminal)
9. Access backend container `docker exec -it backend bash` in a new terminal to install packages `pip install <packages name>` then update requirements.txt `pip freeze > requirements.txt` then type `exit` to exit backend container
10. Access frontend container `docker exec -it frontend bash` to install packages `yard add <packages name>` then package.json will update automatically then type `exit` to exit frontend container
11. View Roborigger PDF Maker in the browser : http://localhost:3000
12. View Roborigger PDF Maker Admin in the browser: http://localhost:8000/admin/
13. Stop development environment crtl/Cmd+C, then `docker-compose down`

## Building and Running

### Requirements:

- [Docker](https://www.docker.com/)

### To running:

1. Clone this repository to your computer
2. Open Docker and keep it running
3. Open cloned folder in Terminal
4. Checkout to the develop branch in Terminal `git checkout develop` 
5. Build docker image `docker-compose up`
6. View Roborigger PDF Maker in the browser: http://localhost:3000
7. Create an account in Register page then login in Login page

### Admin account:

- [Admin Login link](http://localhost:8000/admin)

Email: admin@local.test <br>
Password: admintest!

## User Manual

**Step One: Register** <br>

Input the First Name & Last Name & Email and Password  <br>
Password must be at least 8 characters, can not be fully digits <br>
Then the user gets their account. <br>

**Step Two: Login** <br>

Use the email and password to sign in to the Roborigger Report Maker.<br>
Users can tick the Remember Me to record their account information on the website. <br>

**Step Three: Generate Monthly report** <br>

Download the CSV file from Roborigger Dashboard (message data) <br>
If you cannot access the Roborigger Dashboard. <br>
The sample data can be found in the repo: <br>
[Testing data](./backend/reportdata/CSVFILE/1666252048149/Unit_Message_Log.csv)<br>
which is a real data from AR10-010 1 Jul - 30 Sep. <br>
<br>
Click the file upload box to select file from computer. <br>
Click the **Upload Data File** button to upload the file. <br>
Click **Create Plots** button to create plots. <br>
After the plots are created, click **Create PDF** button to generate PDF. <br>
Input basic information about the unit. <br>
Preview the generated report. <br>
Click the 'Save PDF' button to save report to the device. <br>

## Documents
- [Development Guide](README.md)
- [System Dashboard Runtime Code Process](./doc/System%20Dashboard%20Runtime%20Code%20Process.docx)
- [Report layout and content customization guide](./doc/Report%20layout%20and%20content%20customization%20guide.docx)
- [Backend structure](./backend/README.md)
