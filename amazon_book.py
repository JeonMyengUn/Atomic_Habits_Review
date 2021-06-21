import os, warnings
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 

warnings.filterwarnings(action='ignore')
driver = webdriver.Chrome('/Users/jeonmyeong-un/Desktop/chromedriver')
## https://www.amazon.com/
url = 'https://www.amazon.com/-/en/dp/0735211299/ref=zg_bsar_books_25?_encoding=UTF8&psc=1&refRID=1X9BZNKK2N0PXM5H2MS2'
driver.get(url)

sel_rate = driver.find_element_by_xpath('//*[@id="acrCustomerReviewLink"]')
sel_rate.click()

sel_review = driver.find_element_by_xpath('//*[@id="cr-pagination-footer-0"]/a')
sel_review.click()

page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')
all_r = soup.find_all("div", class_="a-section celwidget")
all_user = []    # 사용자
all_ratings = [] # 평점
all_dates = []   # 날짜
all_reviews = [] # 리뷰
all_title = []
for one in all_r:
    #사용자 추가
    user_one = one.find("span", class_="a-profile-name").text
    all_user.append(user_one) 

    # 평점 추가
    rating_one = one.find("span", class_="a-icon-alt").text
    nums = re.findall("\d+", rating_one)[0]
    all_ratings.append(nums) 
    
    #날짜
    date_one = one.find("span", class_="a-size-base a-color-secondary review-date")
    texts = date_one.text.split("on")
    data = texts[1].strip() 
    all_dates.append(data)

    #리뷰
    review_one = one.find("div",
                class_="a-row a-spacing-small review-data")
    tmp = review_one.text
    review = tmp.strip()
    all_reviews.append(review)

    #제목
    review_title = one.find("a", class_="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold")
    title_str = review_title.get_text(strip=True)
    all_title.append(title_str)
    
dat = pd.DataFrame({'User':all_user, 'Rating':all_ratings, "Date":all_dates, "Title":all_title, "Review":all_reviews})
dat.to_csv("Atomic_Habits_Review.csv", index=False, encoding="UTF-8")
print(dat)

