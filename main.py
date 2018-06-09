from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView
from kivy.config import Config
import os, webbrowser, re, random

Builder.load_file("mymain.kv")
phoneDirectory = os.path.join(os.path.dirname(__file__), "data_book")

query = ''

class HomeScreen(Screen):
    def updateQuery(self):
        global query
        query = self.ids.queryText.text
        sm.get_screen("user_asks").results()

    def show_stdcodes(self):
        sm.get_screen("stdcodes").make_std_list()

    def clear_text(self):
        self.ids.queryText.text = ""

class AboutAppScreen(Screen):
    def about(self):
        f = open("about.txt", "r")
        content = f.read()
        f.close()

        return content

class AllNumbersScreen(Screen):
    def numofrows(self):
        f = open(os.path.join(phoneDirectory, "phone_numbers.txt"))
        l = f.readlines()
        f.close()

        d = {}
        for i in range(0, len(l), 2):
            d.update({l[i]:l[i+1]})
            
        return len(d)
        
    def load_phone_numbers(self):
        f = open(os.path.join(phoneDirectory, "phone_numbers.txt"))
        l = f.readlines()
        f.close()

        up_data_mark = len(l)/2 - 4

        # copy the list in L
        count = 1
        L = ['']
        for i in range(len(l)):
            if i % 2 != 0:
                L.append("Ph.: "+l[i])
                #L.append(("-"*1000)+"\n")
                L.append("")
                L.append("")
            else:
                if count == up_data_mark:
                    L.append("~~~~~~~~~~~UTTAR PRADESH (NCR)~~~~~~~~~~~~~~\n\n")
                    #L.append("____________________________________________")
               # L.append("({}.)".format(count))
                L.append(l[i])
                count+=1

        d = {}
        for i in range(0, len(l), 2):
            d.update({l[i]:l[i+1]})

        names = d.keys()
        phones = d.values()

        return L

class SearchResults(Screen):
    def results(self):
        global query
        f = open(os.path.join(phoneDirectory, "phone_numbers.txt"), "r")
        l = f.readlines()
        f.close()

        d = {}
        for i in range(0, len(l), 2):
            d.update({l[i]:l[i+1]})

        names = d.keys()
        phones = d.values()

        indexes = []
        queries = query.split(" ")

        if query != "":
            for q in queries:
                for i in range(len(names)):
                    checked = re.findall(q.upper(), names[i].upper())
                    if q.upper() in checked and i not in indexes:
                        indexes.append(i)

            L = ["",]
            for i in indexes:
                L.append(names[i])
                L.append(phones[i])
                #L.append('-'*1000 +"\n")
                L.append("")
                L.append("")

            if L == ["",]:
                L = ["", "Sorry, found nothing! :("]
        else:
            L = ["", "Please enter a query to get some results."]

        self.ids.main_grid.clear_widgets()
        self.ids.main_grid.add_widget(ListView(item_strings=L))

class STDCodesScreen(Screen):
    def make_std_list(self):
        f = open(os.path.join(phoneDirectory, "state_codes.txt"), "r")
        SC = f.readlines()
        f.close()

        f = open(os.path.join(phoneDirectory, "other_states_codes.txt"), "r")
        OSC = f.readlines()
        f.close()

        d1, d2 = {}, {}
        for i in range(0, len(SC), 2):
            d1.update({SC[i]:SC[i+1]})

        for i in range(0, len(OSC), 2):
            d2.update({OSC[i]:OSC[i+1]})

        main_state_names, other_state_names = d1.keys(), d2.keys()
        main_state_phones, other_state_phones = d1.values(), d2.values()

        count = 1
        L = ['', "\n\n\n\n----------Main STD Codes-----------\n\n\n\n\n"]
        
        for i in range(len(main_state_names)):
            L.append(main_state_names[i])
            L.append("Ph.: "+main_state_phones[i])
            #L.append(("-"*1000)+"\n")
            L.append("")
            L.append("")
            count += 1

        count = 1
        L.append("\n\n-------------Other STD Codes-------------\n\n\n\n")

        for i in range(len(other_state_names)):
            L.append(other_state_names[i])
            L.append("Ph.: "+other_state_phones[i])
            #L.append(("-"*1000)+"\n")
            count += 1
            L.append("")
            L.append("")

        self.ids.std_grid.clear_widgets()
        self.ids.std_grid.add_widget(ListView(item_strings=L))

class STDCodeSearchScreen(Screen):
    def search_std_code_by_city(self):
        std_city = self.ids.std_query.text
        sm.get_screen("user_std_query_results_by_city").query_results_for_std(std_city)

    def clear_it(self):
        self.ids.std_query.text = ""

class STDCodeResultsScreen(Screen):
    def query_results_for_std(self, city_name_s):
        f = open(os.path.join(phoneDirectory, "state_codes.txt"), "r")
        SC = f.readlines()
        f.close()

        f = open(os.path.join(phoneDirectory, "other_states_codes.txt"), "r")
        OSC = f.readlines()
        f.close()

        d1, d2 = {}, {}
        for i in range(0, len(SC), 2):
            d1.update({SC[i]:SC[i+1]})

        for i in range(0, len(OSC), 2):
            d2.update({OSC[i]:OSC[i+1]})

        main_state_names, other_state_names = d1.keys(), d2.keys()
        main_state_phones, other_state_phones = d1.values(), d2.values()

        cities = city_name_s.split(" ")

        main_city_indexes = []
        other_city_indexes = []
        
        if city_name_s != "":
            for a_city in cities:
                
                for i in range(len(main_state_names)):
                    checked = re.findall(a_city.upper(), main_state_names[i].upper())
                    if a_city.upper() in checked and i not in main_city_indexes:
                        main_city_indexes.append(i)

                for i in range(len(other_state_names)):
                    checked = re.findall(a_city.upper(), other_state_names[i].upper())
                    if a_city.upper() in checked and i not in other_city_indexes:
                        other_city_indexes.append(i)

            L = ["","\n\n\n\n-----------Main Cities Founded---------------\n\n\n\n\n",]
            
            for i in main_city_indexes:
                L.append(main_state_names[i])
                L.append(main_state_phones[i])
                #L.append("-"*1000 + "\n")
                L.append("")
                L.append("")

            aLabel = "\n-------------Other Citites Founded-----------------\n\n"
            L.append(aLabel)
            
            for i in other_city_indexes:
                L.append(other_state_names[i])
                L.append(other_state_phones[i])
                #L.append("-"*1000 + "\n")
                L.append("")
                L.append("")

            if L[0] == "" and L[1] == "\n\n\n\n-----------Main Cities Founded---------------\n\n\n\n\n" and L[2] == aLabel and L[-1] == aLabel:
                L = ["\n\nSorry, nothing found! :("]
            elif L[-1] == aLabel:
                L.remove(L[-1])
            elif L[2] == aLabel:
                L.remove(L[1])
        else:
            L = ["\n\nPlease enter a query to get some results."]

        self.ids.std_query_grid.clear_widgets()
        self.ids.std_query_grid.add_widget(ListView(item_strings=L))
        
sm = ScreenManager()
sm.add_widget(HomeScreen(name="Home"))
sm.add_widget(AboutAppScreen(name="about"))
sm.add_widget(AllNumbersScreen(name="allphones"))
sm.add_widget(SearchResults(name="user_asks"))
sm.add_widget(STDCodesScreen(name="stdcodes"))
sm.add_widget(STDCodeSearchScreen(name="search_std_code_screen"))
sm.add_widget(STDCodeResultsScreen(name="user_std_query_results_by_city"))

class HelplineApp(App):
    def build(self):
        return sm

HelplineApp().run()
