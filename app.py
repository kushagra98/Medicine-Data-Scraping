from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.keys import Keys
import requests
import time
import os

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')


@app.route('/index',methods=['POST'])
def getValue():
    name = request.form['name']
    CHROMEDRIVER_PATH = '/Users/kushagra/Downloads/chromedriver'

    options = Options()  
    options.add_argument("--headless")  
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)   

    driver.get("https://www.netmeds.com/catalogsearch/result/?q="+name)
    elm = driver.find_element_by_tag_name('html')
    elm.send_keys(Keys.END)
    time.sleep(8)
    page_source = driver.page_source
    driver.quit()

    soup = bs(page_source, 'lxml')

    divs = soup.find_all("div",attrs = {'class':'drug_list'})
    imgs=[]
    names=[]
    links=[]

    for d in divs:
        img = d.find("img")
        img = img['src']
        drug = d.find("div", attrs={'class':'drug_c'})
        drug = drug.find("a")
        link = 'https://www.netmeds.com'
        link += drug['href']
        title = drug.find("div", attrs={'class':'info'}).getText().strip()

        #a = d.find("a",attrs={'class':'result'},href=True)
        #link = a['href']
        #title = d.find("h3",attrs={'class':'result-title'}).getText().strip()
        
        imgs.append(img)
        links.append(link)
        names.append(title)
    return render_template('pass.html',imgs=imgs,names=names,links=links,len=len(imgs))

@app.route('/pass',methods=['POST'])
def getValu():
    link = request.form['name']
    data = requests.get(link)
    soup = bs(data.text,'lxml')
    
    
    manufacturer = soup.find("span",attrs={'class':'drug-manu'})
    manufacturer = manufacturer.find("a").getText().strip()
    
    drug = soup.find("div",attrs={'class':'drug-manu'})
    drug = drug.find("a").getText().strip()

    uses=[]
    warnings=[]
    interactions=[]
    directions=[]
    side=[]
    more=[]
    data = soup.find("div",attrs={'class':'prescript-txt product_desc_info'})

    if data:
        data1 = data.find("div",attrs={'id':'np_tab1'})
        if data1:
            data1 = data1.find_all(['h2','p','li'])
            for i in data1:
                uses.append(i.getText().strip())

        data1 = data.find("div",attrs={'id':'np_tab2'})
        if data1:
            data1 = data1.find_all(['h2','p','li'])
            for i in data1:
                warnings.append(i.getText().strip())

        data1 = data.find("div",attrs={'id':'np_tab3'})
        if data1:
            data1 = data1.find_all(['h2','p','li'])
            for i in data1:
                interactions.append(i.getText().strip())

        data1 = data.find("div",attrs={'id':'np_tab4'})
        if data1:
            data1 = data1.find_all(['h2','p','li'])
            for i in data1:
                directions.append(i.getText().strip())

        data1 = data.find("div",attrs={'id':'np_tab5'})
        if data1:
            data1 = data1.find_all(['h2','p','li'])
            for i in data1:
                side.append(i.getText().strip())

        data1 = data.find("div",attrs={'id':'np_tab6'})
        if data1:
            data1 = data1.find_all(['h2','p','li'])
            for i in data1:
                more.append(i.getText().strip()) 
    return render_template("pass2.html",uses=uses,warnings=warnings,interactions=interactions,directions=directions,side=side,more=more)


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 4444)))
    