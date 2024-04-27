# On-Demand-UpWork-Skills
A trend finder

## Dependencies
before usage, open the command prompt and type to download the necessary modules:
- `pip install pillow`
- `pip install opencv-python`
- `pip install pyautogui`
- `pip install pyperclip`

## Configuration
Go to [upwork.com](https://upwork.com) and screenshot but cut and save the logo part, name the image file "upwork" and place it under the same directory as the python script, make sure you minimize the cut.

You can change the number of pages the program can read, by editing the intial value of the variable `pages`.

## Running
After the 5 seconds countdown the program will do after running it, you will open a new broswer tab with a closed console window, then you will see the program automatically writing on the console window, **while the program is running it is forbidden to click or press a key.**

## Output
the program will create 3 files:
- `upwork trends.txt` -> each line contains a skill name followed by its number of demands
- `upwork skillsets price.json` -> a JSON file where the keys are the prices and values are the skillsets
- `upwork top 30 most high paying skillsets.txt` -> each line contains a payment amount followed by a list of skillsets, ordered from the highest top 30
