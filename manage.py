import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_practo_clinics(city):
    url = f"https://www.practo.com/{city}/clinics"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    clinics = []
    for clinic in soup.find_all('div', class_='u-border-general--bottom'):
        name = clinic.find('h2').text.strip()
        address = clinic.find('div', class_='c-listing__address').text.strip()
        clinics.append({'Name': name, 'Address': address})

    return pd.DataFrame(clinics)

def scrape_justdial_clinics(city):
    url = f"https://www.justdial.com/{city}/Clinics"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    clinics = []
    for clinic in soup.find_all('li', class_='cntanr'):
        name = clinic.find('span', class_='lng_cont_name').text.strip()
        try:
            address = clinic.find('span', class_='cont_fl_addr').text.strip()
        except AttributeError:
            address = None
        clinics.append({'Name': name, 'Address': address})

    return pd.DataFrame(clinics)

def scrape_linkedin_groups():
    url = "https://www.linkedin.com/search/results/groups/?keywords=clinic%20management%20software"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    groups = []
    for group in soup.find_all('div', class_='search-result__info'):
        name = group.find('span', class_='name').text.strip()
        try:
            description = group.find('p', class_='subline-level-1').text.strip()
        except AttributeError:
            description = None
        groups.append({'Name': name, 'Description': description})

    return pd.DataFrame(groups)

def analyze_data():
    try:
        practo_df = pd.read_csv('practo_clinics.csv')
        justdial_df = pd.read_csv('justdial_clinics.csv')
        linkedin_df = pd.read_csv('linkedin_groups.csv')

        total_clinics = pd.concat([practo_df, justdial_df]).drop_duplicates().reset_index(drop=True)
        total_clinics.to_csv('total_clinics.csv', index=False)

        print(f"Total unique clinics: {len(total_clinics)}")
        print(f"LinkedIn groups related to clinic management: {len(linkedin_df)}")
    except pd.errors.EmptyDataError:
        print("One or more CSV files are empty or do not exist.")
    except FileNotFoundError:
        print("One or more CSV files are not found.")

# Example usage
city = "chennai"
practo_clinics = scrape_practo_clinics(city)
if not practo_clinics.empty:
    practo_clinics.to_csv('practo_clinics.csv', index=False)
else:
    print("No data found for Practo clinics.")

city = "delhi"  # Specify a valid city for Justdial
justdial_clinics = scrape_justdial_clinics(city)
if not justdial_clinics.empty:
    justdial_clinics.to_csv('justdial_clinics.csv', index=False)
else:
    print("No data found for Justdial clinics.")

linkedin_groups = scrape_linkedin_groups()
if not linkedin_groups.empty:
    linkedin_groups.to_csv('linkedin_groups.csv', index=False)
else:
    print("No data found for LinkedIn groups.")

analyze_data()
