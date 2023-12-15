from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


print('-'*22)
# Initialize the webdriver
driver = webdriver.Chrome()

trending_skills = {}
trends = []
jobs = 0

def readResults(page_number):
    global jobs
    # Navigate to the webpage
    driver.get("https://www.upwork.com/nx/jobs/search/?sort=recency&t=1&duration_v3=weeks&page=" + str(page_number) + "&per_page=50")

    # Find all divisions with the class "up-skill"
    divisions = driver.find_elements(By.CLASS_NAME, "up-skill-wrapper")
    while len(divisions) != 50:
        sleep(1)
        divisions = driver.find_elements(By.CLASS_NAME, "up-skill-wrapper")
    jobs += 50
    print(len(divisions), "jobs in page", page_number)

    # Loop through each division
    for division in divisions:
        # Find all anchor elements inside the current division
        anchors = division.find_elements(By.TAG_NAME, "a")
        
        # Loop through each anchor element
        for anchor in anchors:
            # Get the text inside the anchor element
            text = anchor.text
            
            # Store the text in a list
            if (text not in trending_skills):
                trending_skills[text] = 0
            trending_skills[text] += 1

for page in range(1, 100):
    readResults(page)

# Close the webdriver
driver.quit()
print("TOTAL OF", jobs, "JOBS")

for skill in trending_skills:
    repeats = trending_skills[skill]
    if repeats not in trends:
        trends.append(repeats)
trends.sort()
trends.reverse()
file_content = f"CURRENTLY ON DEMAND SKILLS FROM {jobs} JOB REQUESTS ON UpWork\n\n"
for rank in trends:
    if rank < 10:
        continue
    for skill in trending_skills:
        if trending_skills[skill] == rank:
            file_content += f"{skill} {rank}\n"

with open("trending UpWork skills.txt", 'w') as f:
    f.write(file_content)

print('-'*22)
