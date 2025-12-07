from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import re


columns = [ "Rank", "Brand Name", "Model Name", "Launch Date", "Launch Price", "Overall Camera Score","Chipset",
           "Camera MP", "Aperture","Number of Cameras", "Photo Score", "Bokeh Score", "Video Score","Exposure", "Color","Auto Focus", 
           "Texture", "Noise", "Artifacts", "Stabilization" ]


def get_phone_details(rank, row):
    driver2 = webdriver.Chrome()
    wait2 = WebDriverWait(driver2, 10)

    try:
        details = row.text.split('\n')
        contents = {}

        contents["Rank"] =              (rank + 1)
        contents["Brand Name"] =        (details[1].split(" "))[0]
        contents["Model Name"] =        (details[1])
        contents["Launch Date"] =       (details[3].split(" "))[-1]
        contents["Launch Price"] =      int(details[2].replace("$",""))


        link = row.find_element(By.TAG_NAME, 'a').get_attribute('href')
        driver2.get(link)
        try:

            camera_element = driver2.find_element(
                By.XPATH, "//div[@class='protocol-name']//div[@class='name' and normalize-space()='Camera']"
            )
            
        except NoSuchElementException:
            return -1

        contents["Overall Camera Score"] = driver2.find_element(By.CLASS_NAME, 'scoreBadgeValue').text


        try:
            show_more = wait2.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#show-more-specs span"))
            )
            driver2.execute_script("arguments[0].click();", show_more)
        except:
            print("No 'Show more' section found for:", contents["Model Name"])

        spec_values = driver2.find_elements(By.CSS_SELECTOR, ".spec-value")
        if len(spec_values) > 2:
            temp = spec_values[2].text
            contents['Chipset'] = re.sub(r"\s*\d+(?:/\d+)*GB(?:\s*RAM)?", "", temp).strip()
        else:
            contents['Chipset'] = "N/A"

        camera_infos = (spec_values[-1].text if spec_values else "N/A").split("\n")
        specific_info = [i for i in camera_infos if i.startswith("Wide: ")]

        try:
            contents['Camera MP'] =(specific_info[0].split(" ")[1]).replace("MP,","") 
        except:
            contents['Camera MP'] = 'N/A'

        try:
            contents['Aperture'] = (specific_info[0].split("/")[1]).strip()
            contents['Number of Cameras'] = len(camera_infos)
        except:
            contents['Aperture'] = 'N/A'
            contents['Number of Cameras'] = 'N/A'


        
        link2_elements = driver2.find_elements(By.CLASS_NAME, 'mr-half')

        if link2_elements and "camera-test" in (link2_elements[0].get_attribute('href')):
            link2 = link2_elements[0].get_attribute('href')
            driver2.get(link2)


            all_score = driver2.find_elements(By.CLASS_NAME, 'currentScore')
            if len(all_score) <= 20:
                try: 

                    product_details = driver2.find_elements(By.CLASS_NAME, 'bars-graph')
                    main_scores = product_details[0].find_elements(By.CLASS_NAME, 'large-4')
                    sub_scores = product_details[0].find_elements(By.CLASS_NAME, 'large-8')

                    photo_score = sub_scores[0].find_elements(By.CLASS_NAME, 'currentScore')
                    video_score = sub_scores[-1].find_elements(By.CLASS_NAME, 'currentScore')

                    contents['Photo Score'] =   int((main_scores[0].text.split("\n"))[0])
                    contents['Bokeh Score'] =   int((main_scores[1].text.split("\n"))[0])
                    contents['Video Score'] =   int((main_scores[4].text.split("\n"))[0])

                    contents['Exposure'] =      int(photo_score[0].text)
                    contents['Color'] =         int(photo_score[1].text)
                    contents['Auto Focus'] =    int(photo_score[2].text)
                    contents['Texture'] =       int(photo_score[3].text)
                    contents['Noise'] =         int(photo_score[4].text)
                    contents['Artifacts'] =     int(photo_score[5].text)
                    contents['Stabilization'] = int(video_score[-1].text)
                except:
                    print(f"{contents["Model Name"]} is showing error in else")                


            else:
                try: 
                    contents['Photo Score'] =   int( all_score[-22].text )
                    contents['Bokeh Score'] =   int( all_score[-14].text )
                    contents['Video Score'] =   int( all_score[-11].text )
                    contents['Exposure'] =      int( all_score[-20].text )
                    contents['Color'] =         int( all_score[-19].text )
                    contents['Auto Focus'] =    int( all_score[-18].text )
                    contents['Texture'] =       int( all_score[-17].text )
                    contents['Noise'] =         int( all_score[-16].text ) 
                    contents['Artifacts'] =     int( all_score[-15].text )
                    contents['Stabilization'] = int( all_score[-4].text )
                except:
                    print(f"{contents["Model Name"]} is showing error")


        else:
            # No link2 → fallback scoring
            score_current = driver2.find_elements(By.CSS_SELECTOR, ".score-current")
            clean_scores = [s.text.strip() for s in score_current if s.text.strip() != ""]

            contents["Photo Score"] = int(clean_scores[1]) if len(clean_scores) > 1 else 0
            contents["Bokeh Score"] =   0
            contents["Video Score"] = int(clean_scores[2]) if len(clean_scores) > 2 else 0

            contents['Exposure'] =      0
            contents['Color'] =         0
            contents['Auto Focus'] =    0
            contents['Texture'] =       0
            contents['Noise'] =         0
            contents['Artifacts'] =     0
            contents['Stabilization'] = 0

        return contents

    finally:
        
        driver2.quit()



def main():
    url = "https://www.dxomark.com/smartphones/"

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    driver.get(url)
    time.sleep(2)

    date_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "date-filter")))
    driver.execute_script("arguments[0].click();", date_btn)
    time.sleep(2)

    min_year_select = wait.until(EC.element_to_be_clickable((By.ID, "launch_date_min")))
    select = Select(min_year_select)
    select.select_by_value("2020")

    apply_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".filter-launch-date button.primary.small"))
    )
    driver.execute_script("arguments[0].click();", apply_btn)
    time.sleep(5)


    while True:
        try:
            load_more_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Load more')]")))
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_btn)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", load_more_btn)
            
        except:
            break

    product_card = driver.find_element(By.CLASS_NAME, 'ranking-overflow-inner')
    products = product_card.find_elements(By.CLASS_NAME, 'list')

    phones_data = []

    for num, product in enumerate(products):
        phone_info = get_phone_details(num, product)
        if phone_info == -1:
            break
        if phone_info: 
            phones_data.append(phone_info)



    df = pd.DataFrame(data=phones_data, columns=columns)
    df.to_csv("dxomark_phones.csv", index=False)

    print("\nSaved as dxomark_phones.csv")




if __name__ == "__main__":
    main()
