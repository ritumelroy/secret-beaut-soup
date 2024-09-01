import requests
from bs4 import BeautifulSoup

def fetch_google_doc(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the document. Status code: {response.status_code}")
    return response.text

def parse_grid_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    table = soup.find('table')
    grid_data = []
    
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            cols = row.find_all('td')
            if len(cols) == 3:
                try:
                    x = int(cols[0].get_text().strip())
                    char = cols[1].get_text().strip()
                    y = int(cols[2].get_text().strip())
                    grid_data.append((char, x, y))
                except ValueError:
                    continue  #assume the data is correct
    # print(grid_data)
    return grid_data

def print_grid(grid_data):
    max_x = max(data[1] for data in grid_data)
    max_y = max(data[2] for data in grid_data)

    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for char, x, y in grid_data:
        grid[max_y - y][x] = char 

    for row in grid:
        print(''.join(row))

# main function
def print_google_doc_grid(url):
    html_content = fetch_google_doc(url)
    grid_data = parse_grid_data(html_content)
    print_grid(grid_data)
    
url = 'https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub'
print_google_doc_grid(url)