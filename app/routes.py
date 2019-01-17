from flask import render_template
from app import app
from urllib import request
import bs4

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/linux/')
def linux():
    info = crawler('5')
    return render_template('mytable.html', products=info)

@app.route('/windows/')
def windows():
    info = crawler('4')
    return render_template('mytable.html', products=info)

def crawler(page):
    page = request.urlopen("https://caensoftware.engin.umich.edu/" + page)
    byte = page.read()
    html = byte.decode("utf8")
    soup = bs4.BeautifulSoup(html, 'html.parser')
    parsing = []
    rows = soup.find_all('tr')
    for idx,row in enumerate(rows):
        if idx > 8:
            break
        singular = row.find_all('td')
        row = dict()
        for i,el in enumerate(singular):
            if i == 0:
                software = el.find('a').get_text()
                text = software.replace("\n", "")
                row["software"] = text
            elif i == 1:
                row["version"] = el.get_text().replace("\n", "")
            elif i == 3:
                row["product"] = el.get_text().replace("\n", "")
        if(row != {}):
            parsing.append(row)
    return parsing