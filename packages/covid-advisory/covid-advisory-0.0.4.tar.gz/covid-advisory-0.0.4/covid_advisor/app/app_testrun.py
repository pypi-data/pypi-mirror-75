import requests
from covid_stats import COVID_Data

state = (input("Abbreviation of State: ")).lower()
user_input = ""

while(user_input != 'exit'):
    print("")
    print("1. Number of Cases")
    print("2. Mortality Rate")
    print("3. Hospitalization Rate")
    print("4. Recovery Rate")
    print("5. Travel Adivsory")
    print("6. New State")
    print("7. Exit")

    user_input = input()

    COVID_Tracker = COVID_Data(state)

    if(user_input == '1'):
        data = COVID_Tracker.getCaseGrowthRate()
        print(data)

    if(user_input == '2'):
        data = COVID_Tracker.getMortalityRate()
        print(data)
    
    if(user_input == '3'):
        data = COVID_Tracker.getTotalHospitalizations()
        print(data)

    if(user_input == '4'):
       data = COVID_Tracker.getRecoveryRate()
       print(data)

    if(user_input == '5'):
        data = COVID_Tracker.TravelAdvisory()
        print("data")

    if(user_input == '6'):
        state = (input("Abbreviation of State: ")).lower()
    
    if(user_input == '7'):
        user_input = 'exit'


