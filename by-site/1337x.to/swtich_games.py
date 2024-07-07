# Fetcher for switch game magnet links from 1337x
# Copyright (C) 2024-present Guoxin "7Ji" Pu

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from bs4 import BeautifulSoup
import requests
import json

site = "https://1337x.to"
url = f"{site}/sub/82/1/"
session = requests.session()
links = []

try:
    while True:
        r = session.get(url)
        if r.status_code != 200:
            raise Exception("Non 200 response")
        soup = BeautifulSoup(r.content, 'html.parser')
        for row in soup.find_all('td', class_="coll-1 name"):
            url_torrent = f"{site}{row.find_all('a')[-1].get('href')}"
            r = session.get(url_torrent)
            if r.status_code != 200:
                raise Exception("Non 200 response")
            soup_torrent = BeautifulSoup(r.content, 'html.parser')
            link = soup_torrent.find('a', id="openPopup").get('href')
            print(link)
            links.append(link)
                
        pages = soup.find('div', class_="pagination").find_all('li')
        break
        if pages[-1].find('a').string == 'Last':
            url = f"{site}{pages[-2].find('a').get('href')}"
        else:
            break

    links.sort()
except:
    pass
with open('1337x.to-magnet-links.list', 'wb') as f:
    for link in links:
        f.write(link.encode('utf-8'))
        f.write(b'\n')