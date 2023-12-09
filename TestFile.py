import requests
from bs4 import BeautifulSoup

def make_homepage(title, url, button_text, button_url):
    soup = BeautifulSoup("", 'html.parser')

    head = soup.new_tag("head")
    title_tag = soup.new_tag("title")
    title_tag.string = title
    head.append(title_tag)
    soup.append(head)

    body = soup.new_tag("body")

    h1 = soup.new_tag("h1")
    h1.string = title
    body.append(h1)

    form = soup.new_tag("form")
    form['action'] = button_url
    form['method'] = 'get'

    button = soup.new_tag("button")
    button.string = button_text
    button['type'] = 'submit'
    form.append(button)

    body.append(form)
    soup.append(body)

    with open("index.html", "w") as f:
        f.write(str(soup))

    return soup

soup = make_homepage("                     Fremind", "https://myhpython -m SimpleHTTPServeromepage.com", "Login", "https://myhomepage.com/login")
print(soup.prettify())