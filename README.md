# Introduction
This project was developed to automate data recording recieved by the ARL WAM-V's Operator Control Unit (OCU) GUI. The OCU does not allow exporting or reviewing recieved data, hence the need to scrape it from the screen using computer vision! This program can also act as a standalone screen recorder and screen scraper, and will output both a video and txt file.

# Getting Started
## Installation
Python 3.6 or later and pip required.
1. Install tesseract using your device's dependency manager (brew, etc) or manually install.
    - After installation:
        - On Windows, open your terminal, run `where tesseract`, copy the PATH, and set it as a PATH using `set PATH=%PATH%;C:\your\path\here\`
        - On MacOS / Linux, open your terminal, run `which tesseract`, copy the PATH, and set it as a PATH using `export PATH=$PATH:/path/to/your/directory`
        - These are temporary changes to your path and will need to be done during every terminal session unless set permanently or handled by your global dependency manager.
2. Clone the repository in your desired directory using `git clone https://github.com/MatthewLabasan/cv-project.git`
3. Navigate to this directory and create a Python virtual environment (optional)
    - Create your virtual environment using `python -m venv <env_name>`, replacing <env_name> with your environment name.
    - Activate it using
        Windows: `<env_name>\Scripts\activate`
        Mac: `source <env_name>/bin/activate`
4. Install requirements.txt using `pip install -r requirements.txt`
    - Note: This may take a couple minutes.
5. Run `python main.py()` to run the program. This will begin screen capture and data recognition.
6. Press the escape key to exit the program. A CSV file and video recording should now be saved in the data_recordings and screen_recordings folder.
7. Deactivate the virtual environment by running `deactivate` 
8. For future use, utilize the same virtual envionment unless your dependencies are installed to your system. In that case, just run `main.py`.
## Modifications
- You can modify the video's fps by changing the cv2.waitKey, though this will cause performance issues. 
- Screen size can be modified by changing the height and width in the `ImageGrab.grab()` function.

# Future Work
- Categorize OCR data by relative coordinates to ensure scalability and standardized data collection (begun implementation in `alternative_processing,py`)
- Implement of CSV file creation 
