import xml.etree.ElementTree as ET
import sqlite3
import json
import numpy as np
import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt


class Business:

    def __init__(self):
        self.json_string = ""
        self.elem_list = []
        self.temp = []
        self.country_year_value = []
        self.multiple_country_list = []
        self.individual_country_list = []
        self.country_as_dict = []
        self.years = []
        self.values = []
        self.count = 0
        root = ET.parse('UNData.xml').getroot()
        for elem in root.iter():
            self.elem_list.append(elem.text.strip())
        for val in self.elem_list:
            if val != "":
                self.temp.append(val)
        self.country_year_value = [self.temp[i:i + 3] for i in range(0, len(self.temp), 3)]
        for l in self.country_year_value:
            self.multiple_country_list.append(l[0])
        for c in range(len(self.multiple_country_list)):
            if self.multiple_country_list[c] == self.multiple_country_list[c - 1]:
                pass
            else:
                self.individual_country_list.append(self.multiple_country_list[c])
        self.np_years = np.array([])
        self.np_values = np.array([])

        self.conn = sqlite3.connect('UNData.db')
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS UNData(Country TEXT, Year TEXT, Value TEXT UNIQUE)')
        for record in self.country_year_value:
            self.cur.execute(
                '''INSERT OR IGNORE INTO UNData (Country, Year, Value) VALUES (?, ?, ?)''', (record[0], record[1], record[2]))
        self.conn.commit()

    def getJson(self, userInput):
        countryNum = int(userInput)
        self.cur.execute("""SELECT * FROM UNData WHERE country='%s'""" % self.individual_country_list[countryNum])
        records = self.cur.fetchall()
        with open('UNData.json', 'w') as fh:
            self.np_years = np.array([])
            self.np_values = np.array([])
            self.years = []
            self.values = []
            self.country_as_dict = [
                {'Country': records[country][0], 'Year': records[country][1], 'Value': records[country][2]} for country in range(len(records))]
            for c in self.country_as_dict:
                country = c['Country']
                country2 = self.individual_country_list[countryNum]
                if country == country2:
                    f_val = float(c['Value'])
                    self.years.append(c['Year'])
                    self.values.append(int(f_val))

            self.np_years = np.array(self.years)
            self.np_values = np.array(self.values)
            json.dump(self.country_as_dict, fh, indent=3)
        with open('UNData.json', 'r') as fh:
            self.json_string = json.load(fh)
            self.np_years = self.np_years[::-1]
            self.np_values = self.np_values[::-1]

            plt.title(self.individual_country_list[countryNum])
            plt.xlabel('Years')
            plt.ylabel('Values')
            plt.grid(True)
            plt.tight_layout()
            plt.xticks(rotation='vertical')
            plt.plot(self.np_years, self.np_values, marker='.', linewidth=2)
            plt.tick_params(labelsize=6)
            plt.xticks(rotation=45)
        return self.json_string

