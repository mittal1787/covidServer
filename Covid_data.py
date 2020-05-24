import pycountry_convert as pc
import requests
import json
from flask import Flask, jsonify
app = Flask(__name__)


# In[17]:

@app.route('/')
def assignCases():
    continent_cases = {"NA": {"Deaths": 0, "Recovered": 0, "Ongoing":0, "Total": 0, "Country data": []},
                   "SA": {"Deaths": 0, "Recovered": 0, "Ongoing":0, "Total": 0, "Country data": []}, 
                   "Antarctica": {"Deaths": 0, "Recovered": 0, "Ongoing":0, "Total": 0, "Country data": []},
                   "EU": {"Deaths": 0, "Recovered": 0, "Ongoing":0, "Total": 0, "Country data": []},
                   'AF': {"Deaths": 0, "Recovered": 0, "Ongoing":0, "Total": 0, "Country data": []},
                   "AS": {"Deaths": 0, "Recovered": 0, "Ongoing":0, "Total": 0, "Country data": []}, 
                   "OC": {"Deaths": 0, "Recovered": 0, "Ongoing":0, "Total": 0, "Country data": []},
                   "Cruises": {"Deaths": 0, "Recovered": 0, "Ongoing":0, "Total": 0, "Cruise data":[]},
                  "World": {"Deaths": 0, "Recovered": 0, "Ongoing":0, "Total": 0}}
    url = "https://coronavirus-19-api.herokuapp.com/countries"

    payload = {}
    headers= {}

    response = requests.get(url)
    country_cases = json.loads(response.text)
    continent_cases["World"]["Deaths"] = country_cases[0]['deaths']
    continent_cases["World"]["Recovered"] = country_cases[0]['recovered']
    continent_cases["World"]["Ongoing"] = country_cases[0]['active']
    continent_cases["World"]["Total"] = country_cases[0]['cases']
    for i in range(1, len(country_cases)):
        if country_cases[i]["country"] == "Diamond Princess" or country_cases[i]["country"] == "MS Zaandam":
            continent_cases["Cruises"]["Deaths"] += country_cases[i]['deaths']
            continent_cases["Cruises"]["Recovered"] += country_cases[i]['recovered']
            continent_cases["Cruises"]["Ongoing"] += country_cases[i]['active']
            continent_cases["Cruises"]["Total"] += country_cases[i]['cases']
            continent_cases["Cruises"]["Cruise data"].append(country_cases[i])
        else:
            if (country_cases[i]["country"] == "UK"):
                country_name = "United Kingdom"
            elif country_cases[i]["country"] == "UAE":
                country_name = "United Arab Emirates"
            elif country_cases[i]["country"] == "S. Korea":
                country_name = "South Korea"
            elif country_cases[i]["country"] == "DRC":
                country_name = "Democratic Republic of the Congo"
            elif country_cases[i]["country"] == "Channel Islands" or country_cases[i]["country"] == "Faeroe Islands" or country_cases[i]["country"] == "Sint Maarten":
                country_name = "United Kingdom"
            elif country_cases[i]["country"] == "CAR":
                country_name = "Central African Republic"
            elif country_cases[i]["country"] == "St. Vincent Grenadines" or country_cases[i]["country"] == "Caribbean Netherlands" or country_cases[i]["country"] == "St. Barth":
                country_name = "USA"
            elif country_cases[i]["country"] == "Vatican City":
                country_name = "Italy"
            elif country_cases[i]["country"] == "Western Sahara":
                country_name = "Egypt"
            elif country_cases[i]["country"] == "Saint Pierre Miquelon":
                country_name = "France"
            else:
                country_name = country_cases[i]["country"]
            country_code = pc.country_name_to_country_alpha2(country_name, cn_name_format="default")
            if (country_code == "TL"):
                continent_name = "AS"
            else:
                continent_name = pc.country_alpha2_to_continent_code(country_code)
            if country_cases[i]['deaths'] is None:
                continent_cases[continent_name]["Deaths"] += 0
            else:
                continent_cases[continent_name]["Deaths"] += country_cases[i]['deaths']
            if country_cases[i]["recovered"] is None:
                continent_cases[continent_name]["Recovered"] += 0
            else:
                continent_cases[continent_name]["Recovered"] += country_cases[i]['recovered']
            if country_cases[i]['active'] is not None:
                continent_cases[continent_name]["Ongoing"] += country_cases[i]['active']
            else:
                continent_cases[continent_name]["Ongoing"] += 0
            continent_cases[continent_name]["Total"] += country_cases[i]['cases']
            continent_cases[continent_name]["Country data"].append(country_cases[i])
    return jsonify(continent_cases)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)


