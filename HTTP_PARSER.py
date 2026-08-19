from bs4.element import ResultSet, Tag
import requests
import sys
import requests.exceptions
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    print("Usage:")
    print(f"Python {sys.argv[0]} URL")
    print(f"Example: python {sys.argv[0]} http://example.com ")
    sys.exit(1)

URL = sys.argv[1]
try:
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL,headers = headers, timeout = 10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    links: ResultSet[Tag] = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href:
            print("\n [+] Links: ",href)

    forms: ResultSet[Tag] = soup.find_all('form')
    inputs: ResultSet[Tag] = soup.find_all('input')

    print("\n [+] Forms: ",forms)
    print("\n [+] Inputs: ",inputs)
except requests.exceptions.Timeout:
    print(f"Error occured: Timeout")
    sys.exit(1)
except requests.exceptions.ConnectionError:
    print("Internet veya DNS Sorunu")
    sys.exit(1)
except Exception as e:
    print(f"Beklenmedik Hata{e}")
    sys.exit(1)
finally:
    print("İşlem Sonlandırıldı.")
    sys.exit()






