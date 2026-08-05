import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import json
import time
import random

def human_scroll(driver, total_height):
    current_height = 0
    while current_height < total_height:
        scroll_step = random.randint(150, 400)
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        current_height += scroll_step
        time.sleep(random.uniform(0.3, 1.2))
        if random.random() < 0.25:
            driver.execute_script(f"window.scrollBy(0, {-random.randint(50, 150)});")
            time.sleep(random.uniform(0.3, 0.7))


options = uc.ChromeOptions()
options.add_argument("--window-size=1366,1068")
options.add_argument("--disable-notifications")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=options)

total_hotels = 3300
start_urls = [f"https://www.tripadvisor.com/Hotels-g293921{'-oa' + str(i) if i != 0 else ''}-Vietnam-Hotels.html" for i in range(0, total_hotels, 30)]

unique_hotels = {}
actions = ActionChains(driver)

for index, current_url in enumerate(start_urls):
    print(f"\n[{index + 1}/{len(start_urls)}] Đang xử lý URL: {current_url}")

    try:
        driver.get(current_url)
    except Exception as e:
        print(f"Lỗi khi tải trang: {e}")
        continue

    time.sleep(random.uniform(7.0, 12.0))

    scroll_height = 2500 if index == 0 else 3500
    human_scroll(driver, scroll_height)
    time.sleep(random.uniform(3.0, 6.0))

    if index == 0:
        try:
            actions.move_by_offset(150, 150).click().perform()
            time.sleep(random.uniform(1.0, 2.0))
        except:
            pass

        try:
            button_xpath = "//button[.//span[contains(text(), 'See all')]]"
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, button_xpath)))

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(random.uniform(1.5, 3.0))

            driver.execute_script("arguments[0].click();", button)
            print("-> Đã nhấp vào 'See all'")

            print("-> Đang chờ các khách sạn mới tải...")
            time.sleep(random.uniform(8.0, 12.0))

            human_scroll(driver, 2000)

        except Exception as e:
            print("-> Không tìm thấy nút 'See All'")

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")

    hotel_cards = soup.find_all('div', class_='eCDPE')

    print(f"-> Tìm thấy {len(hotel_cards)} thẻ khách sạn trên trang này.")

    for card in hotel_cards:
        h3_tag = card.find('h3')
        if not h3_tag:
            continue

        raw_name = h3_tag.get_text(strip=True)
        if '.' in raw_name:
            parts = raw_name.split('.', 1)
            if parts[0].strip().isdigit():
                hotel_name = parts[1].strip()
            else:
                hotel_name = raw_name
        else:
            hotel_name = raw_name

        title_div = card.find('div', attrs={'data-automation': 'hotel-card-title'})
        base_url = "N/A"

        if title_div:
            a_tag = title_div.find('a', href=True)
            if a_tag:
                href = a_tag.get("href")
                raw_url = href if href.startswith('http') else 'https://www.tripadvisor.com' + href
                base_url = raw_url.split('?')[0]

        if base_url == "N/A":
            continue

        review_div = card.find('div', attrs={'data-automation': 'bubbleReviewCount'})
        if review_div:
            review_text = review_div.get_text(strip=True)
            current_reviews = "".join(filter(str.isdigit, review_text))
        else:
            current_reviews = "0"

        if base_url not in unique_hotels:
            unique_hotels[base_url] = {
                'hotel_name': hotel_name,
                'number_of_reviews': int(current_reviews) if current_reviews else 0,
                'hotel_url': base_url
            }
            print(f"   + Đã cào: {hotel_name} | {current_reviews} review")
        else:
            print(f"   - [Trùng lặp]: {hotel_name}")

    sleep_time = random.uniform(8.0, 15.0)
    time.sleep(sleep_time)

driver.quit()

total_hotel_list = list(unique_hotels.values())

output_filename = "vietnam_hotels_link.json"
with open(output_filename, 'w', encoding='utf-8') as file:
    json.dump(total_hotel_list, file, indent=4, ensure_ascii=False)

print(f"Hoàn tất! Đã thu thập được {len(total_hotel_list)} khách sạn duy nhất.")
print(f"Dữ liệu đã được lưu vào file: {output_filename}")
