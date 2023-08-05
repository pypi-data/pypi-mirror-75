import requests
import datetime
import numpy as np

class COVID_Data():
    def __init__(self, state):
        self.state = state

    def get_StateData(self):
        url = f"https://covidtracking.com/api/v1/states/{self.state}/daily.json"
        COVID_Data = requests.get(url = url)
        if COVID_Data.status_code == 200:
            COVID_Data = COVID_Data.json()
            return COVID_Data, 200
        else:
            return COVID_Data, COVID_Data.status_code
   

    def getCaseGrowthRate(self):
        try:
            max_cases = 0
            case_dict = {}
            COVID_Data,status = self.get_StateData()
            amount_of_new_cases = COVID_Data[0]['positiveIncrease']
            total_cases = COVID_Data[0]['positive']
            total_pastweek_cases = COVID_Data[14]['positive']
            percent_change_cases = ((total_cases - total_pastweek_cases)/(total_cases)) * 100
            for record in COVID_Data:
                if(record['positiveIncrease'] > max_cases):
                    max_cases = record['positiveIncrease']
                    max_cases_date = str(record['date'])
            max_date =  str(max_cases_date[0:4]) + '-' + str(max_cases_date[4:6]) + '-' + str(max_cases_date[6:8])
            case_dict['Total Amount of Cases:'] = total_cases
            case_dict['New Daily Cases:'] = amount_of_new_cases
            case_dict['Percent Increase in Cases From Past 2 Weeks(%):'] = percent_change_cases
            case_dict['Date of Maximum New Cases:'] = max_date
            case_dict['Maximum Cases'] = max_cases
            return case_dict 
        except TypeError as e:
            raise e      

    def getMortalityRate(self):
        try:
            max_deaths = 0
            mort_dict = {}
            COVID_Data, status = self.get_StateData()
            amount_of_new_deaths = COVID_Data[0]['deathIncrease']
            total_dead = COVID_Data[0]['death']
            total_cases = COVID_Data[0]['positive']
            total_pastweek_dead = COVID_Data[14]['death']
            death_rate = (total_dead/total_cases) * 100
            percent_change_dead = ((total_dead - total_pastweek_dead)/(total_dead)) * 100
            for record in COVID_Data:
                if(record['deathIncrease'] > max_deaths):
                    max_deaths = record['deathIncrease']
                    max_deaths_date = str(record['date'])
            max_date =  str(max_deaths_date[0:4]) + '-' + str(max_deaths_date[4:6]) + '-' + str(max_deaths_date[6:8])
            mort_dict['Total Amount of Deaths:'] = total_dead
            mort_dict['New Daily Deaths:'] = amount_of_new_deaths
            mort_dict['Moratality Rate(%):'] = death_rate
            mort_dict['Percent Increase in Deaths From Past 2 Weeks(%):'] = percent_change_dead
            mort_dict['Date of Maximum Rise in Deaths:'] = max_date
            mort_dict['Maximum Rise in Deaths'] = max_deaths
            return mort_dict
        except TypeError as e:
            print("")
            print('Not Enough Data Provided')
        except Exception as e:
            raise(e)

    def getTotalHospitalizations(self):
        try:
            hosp_dict = {}
            COVID_Data, status = self.get_StateData()
            total_hospitalized = COVID_Data[0]['hospitalizedCurrently']
            amount_recovered = COVID_Data[0]['recovered']
            total_cases = COVID_Data[0]['positive']
            current_cases = total_cases - amount_recovered
            hospitalized_rate = (total_hospitalized / current_cases) * 100
            hosp_dict['Current Hospitalizations:'] = total_hospitalized
            hosp_dict['Hospitalization Rate for Infected(%):'] = hospitalized_rate
            return hosp_dict
        except TypeError as e:
            print("")
            print('Wrong Data Provided')
        except Exception as e:
            raise(e)

    def getRecoveryRate(self):
        try:
            rec_dict = {}
            COVID_Data, status = self.get_StateData()
            amount_recovered = COVID_Data[0]['recovered']
            total_cases = COVID_Data[0]['positive']
            percent_recovered = (amount_recovered / total_cases) * 100
            rec_dict['Amount Recovered:'] = amount_recovered
            rec_dict['Percent of Cases Recovered(%):'] = percent_recovered
            return rec_dict
        except TypeError as e:
            print("")
            print('Wrong Data Provided')
        except Exception as e:
            raise(e)

    def getSlope(self):
        COVID_Data, status = self.get_StateData()
        cases_list = []
        dates_list = []
        for record in COVID_Data[:30]:
            cases_list.append(record['positiveIncrease'])
            dates_list.append(record['date'])
        x_axis = np.array(dates_list)
        y_axis = np.array(cases_list)
        slope, intercept = np.polyfit(x_axis, y_axis, 1)
        return slope
    
    def getScore(self):
        score = 0
        COVID_Data, status = self.get_StateData()
        slope = self.getSlope()
        total_cases = COVID_Data[0]['positive']
        total_pastweek_cases = COVID_Data[14]['positive']
        percent_change_cases = ((total_cases - total_pastweek_cases)/(total_cases)) * 100
        if(total_cases > 60000):
            score += 1
        if(slope >= 1):
            score += 2
        if(percent_change_cases >= 20):
            score +=1
        return score
    
    def TravelAdvisory(self):
        result_dict = {}
        score = self.getScore()
        if(score == 1 or score == 0):
            result_dict[self.state] = "Travel allowed, but still maintain social distancing protocals"
        if(score > 1 and score < 4):
            result_dict[self.state] = "Travel at own risk, COVID-19 cases are yet to be fully explored and a second wave may be avoked without effective social distancing policies"
        if(score == 4):
            result_dict[self.state] = "Avoid travel to this state, COVID-19 cases are on the rise which is coupled with an already high rate of infections"
        return result_dict
        
        

        

            



    
        




    
