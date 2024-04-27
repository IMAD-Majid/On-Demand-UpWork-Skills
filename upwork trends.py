from time import sleep
from json import dumps as JSONstringify, loads as JSONparse
import cv2
import pyperclip as clipboard
from pyautogui import moveTo, click, press, hotkey, typewrite, position, screenshot

parentPath = "C:/Users/HP/Documents/projects/bin/"

def locateElement(targetName, timeout):
    while True:
        print(f"{str(timeout).zfill(2)} : cursor on \"{targetName}\"", end="\r")
        sleep(1)
        timeout -= 1
        if (timeout < 0):
            print('\n')
            return position()


def locatedImage(snapshotName):
    template = cv2.imread(parentPath + snapshotName + ".png")
    screenshotPath = parentPath + "screenshot.png"
    screenshot().save(screenshotPath)
    screen = cv2.imread(screenshotPath)

    # Convert to grayscale if images are in color
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= 0.9:  # Example confidence threshold: 0.9
        return max_loc;
    else:
        return ();

def mouseTo(x, y):
    moveTo(x=x, y=y)
    pause(0.2)
    click()
     # - - - -


def enter():
    press("Enter")

def pause(duration=0.5):
    sleep(duration)

def waitFor(snapshotName: str) -> None:
    while not locatedImage(snapshotName):
        print(f"...waiting for: {snapshotName}", end="\r")
        pause(1)
    print()

def clickOn(snapshotName: str) -> None:
    x, y = locatedImage(snapshotName)
    # Load the PNG image
    image = cv2.imread(parentPath + snapshotName + ".png")

    # Get the dimensions of the image
    h, w, channels = image.shape
    mouseTo(x + (w//2), y + int(h//2))

def waitThenClick(snapshotName: str) -> None:
    waitFor(snapshotName)
    clickOn(snapshotName)

def visitURL(urlToVisit: str) -> None:
    typewrite(f"location.href = '{urlToVisit}'")
    pause(1)
    enter()

# CONFIGURATION

trend = {}
priceSkillset = {}
pages = 20

# CONFIGURATION

print("started")
for i in range(5):
    print(5-i)
    pause(1)
hotkey("f12")
pause(1)
for p in range(1, pages+1):
    visitURL(f"https://www.upwork.com/nx/search/jobs/?client_hires=1-9,10-&duration_v3=week&per_page=50&sort=recency&page={p}")
    waitFor("upwork")
    pause(3)
    script = """
        function main(){
            let extracted = {};
            document.querySelectorAll('article').forEach((a) => {
                const fadedtext = a.querySelector('ul').textContent;
                let price = -1;
                if (fadedtext.indexOf('$') != -1) {
                    price = fadedtext.slice(fadedtext.indexOf('$') + 1, fadedtext.indexOf('.00'));
                }
                let skills = '';
                a.querySelectorAll('span.air3-token').forEach((s) => {
                    if (!s.textContent.includes('+')) {
                        skills += s.textContent + ', ';
                    }
                });
                if (extracted[price] == undefined) {
                    extracted[price] = [];
                }
                extracted[price].push(skills);
            })
            let elm = document.createElement('span');
            elm.textContent = JSON.stringify(extracted);
            document.body.appendChild(elm);
            document.getSelection().selectAllChildren(elm);
            document.execCommand('copy');
        }
        """
    clipboard.copy(script)
    hotkey("ctrl", 'v')
    enter()
    pause(2.5)
    typewrite("main();")
    enter()
    pause(1)

    extracted = JSONparse(clipboard.paste())

    for p in extracted:
        if p not in priceSkillset:
            priceSkillset[p] = extracted[p][::]
        priceSkillset[p].extend(extracted[p])

    skills = ''
    for price in extracted:
        skills += ''.join(extracted[price])
    skills = skills[:-4]
    
    for skill in skills.split(", "):
        if skill in trend:
            trend[skill] += 1
        else:
            trend[skill] = 1

with open("upwork trends.txt", 'w') as f:
    scores = set()
    for skill in trend:
        scores.add(trend[skill])
    for rank in sorted(scores)[::-1]:
        for skill in trend:
            if trend[skill] == rank:
                f.write(f"{skill}: {rank}\n")

with open("upwork skillsets price.json", 'w') as f:
    f.write(JSONstringify(priceSkillset))

with open("upwork top 30 most high paying skillsets.txt", 'w') as f:
    prices = []
    for p in priceSkillset:
        prices.append(int(p.replace(',', '')))
    for p in sorted(prices)[::-1][:30]: # top 30
        for ps in priceSkillset:
            if int(ps.replace(',', '')) == p:
                f.write(f"{p}$ ({len(priceSkillset[ps])}): [{"] - [".join(priceSkillset[ps])[:-2]}]\n")
