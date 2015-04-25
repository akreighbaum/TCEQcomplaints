import csv
from mechanize import Browser
from bs4 import BeautifulSoup

########## STEP 1: Open and read the URL ##########

url = 'http://www2.tceq.texas.gov/oce/waci/index.cfm?fuseaction=home.main'

# Create a new browser object and open the URL
br = Browser()
br.set_handle_robots(False)
br.open(url)

########## STEP 2: Select and fill out the appropriate form ##########

# Select the appropriate form, which we'll find by looking in Chrome
br.select_form("county_search_form")

# Each control can be set. Dropdown lists are handled as lists, text fields take text
br.form['county_select'] = ['111111111111180']
br.form['start_date_month'] = ['1']
br.form['start_date_day'] = ['1']
br.form['start_date_year'] = ['2014']
br.form['end_date_month'] = ['1']
br.form['end_date_day'] = ['30']
br.form['end_date_year'] = ['2014']

# Submit the form
br.submit()

########## STEP 3: Grab and parse the HTML ##########

soup = BeautifulSoup(br.response())

complaints = soup.find('table', class_='waciList')


# ########## STEP 4: Iterate through the results and write to an output list ##########

output = []
print 'page 1'
for tr in complaints.findAll('tr'):
    print tr

    output_row = []
    for td in tr.findAll('td'):
        output_row.append(td.text.strip())

    output.append(output_row)

# url2 = 'http://www2.tceq.texas.gov/oce/waci/index.cfm?fuseaction=home.search&pageNumber=2'

br.open(url)
print 'page 2'
complaints = soup.find('table', class_='waciList')

for tr in complaints.findAll('tr'):
    print tr

# ########## STEP 5: Write results to file ##########

# print output

with open('out-tceq.csv', 'w') as csvfile:
    my_writer = csv.writer(csvfile, delimiter='|')
    my_writer.writerows(output)