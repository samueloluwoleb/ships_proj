from operator import itemgetter
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap
from load_data_4_web_generator import load_data

all_data = load_data()
list_of_countries = []
check_for_top_countries_list = []


def display_choice_menu():
    menu = """
    Available commands:\n
    help
    show_countries
    top_countries <num_countries> Example: top_countries 10 (number should be less than 43)
    ships_by_types
    search_ship
    speed_histogram
    draw_map
           """
    print(f"{menu}")


def to_continue():
    print('')
    input("Press Enter key to continue")


def helps():
    """
    Gets called when the user types 'help' a menu function
    """
    pass


def show_countries():
    """
    Iterates through the dictionary values of 'data' key to get a list of all
    the countries with ships, remove duplicate countries and print
    """

    for count, value_dictionary in enumerate(all_data['data']):
        list_of_countries.append(value_dictionary['COUNTRY'])
    no_duplicate_list = list(set(list_of_countries))
    no_duplicate_list.sort()
    for country in no_duplicate_list:
        print(country)
    to_continue()


def top_countries_n():
    """
    Iterates through the dictionary values of 'data' key to get a list of all
    the countries with the most ships and print the number of top countries
    the user requested
    """
    dictionary_for_country_count = {}
    number = int(check_for_top_countries_list[1])
    for list_values in all_data['data']:
        if list_values['COUNTRY'] not in dictionary_for_country_count:
            dictionary_for_country_count[list_values['COUNTRY']] = 0
        dictionary_for_country_count[list_values['COUNTRY']] += 1
    sort_dict = dict(sorted(dictionary_for_country_count.items(), key=itemgetter(1), reverse=True))
    for count, (key, value) in enumerate(sort_dict.items()):
        print(f"{key} : {value}")
        if count == number - 1:
            break
    to_continue()


def ships_by_types():
    """
    Iterates through the dictionary values of 'data' key to get a list of all
    the ship types and print the ship type with its number of occurence in the data
    """
    dictionary_for_ship_type = {}
    for list_values in all_data['data']:
        if list_values['TYPE_SUMMARY'] not in dictionary_for_ship_type:
            dictionary_for_ship_type[list_values['TYPE_SUMMARY']] = 0
        dictionary_for_ship_type[list_values['TYPE_SUMMARY']] += 1
    for key, value in dictionary_for_ship_type.items():
        print(f'{key} : {value}')
    to_continue()


def search_ships():
    """
    Gets a search query from user and Iterates through the dictionary values of 'data' key to get a list of all
    shipname, prints out a list of shipname that contains the searched queries
    """
    shipnames_dict = []
    search_input = input('Enter your search query: ')
    search_input = search_input.upper()
    for value_dictionary in all_data['data']:
        if value_dictionary['SHIPNAME'].startswith(search_input):
            print(value_dictionary['SHIPNAME'])
            shipnames_dict.append(value_dictionary['SHIPNAME'])
    if not shipnames_dict:
        print("There is no shipname that matches your query")
    to_continue()


def speed_histogram():
    """
    Creates a histogram of all the ships speed and generates the png file displaying the visula data.
    """
    speed_list = []
    for list_values in all_data['data']:
        speed_list.append(list_values['SPEED'])
    plt.hist(speed_list)
    file_name = input("Enter a name for your histogram file: ")
    plt.savefig(file_name + '.png')
    plt.show()
    to_continue()


def draw_map():
    """
    Creates a real-world geographical representation of countries in the data that has ships and marking
    the countries with a black dot on the map.
    """
    longitude_list = []
    latitude_list = []
    for value_dictionary in all_data['data']:
        longitude_list.append(float(value_dictionary['LON']))
        latitude_list.append(float(value_dictionary['LAT']))
    df = pd.DataFrame(list(zip(longitude_list, latitude_list)), columns=['longitude', 'latitude'])
    longitude = df['longitude'].values
    latitude = df['latitude'].values
    fig = plt.figure(figsize=(12, 12))
    m = Basemap()
    m.drawcoastlines(linewidth=1, linestyle='dotted', color='green')
    m.drawcountries(linewidth=.5, linestyle='solid', color='white')
    m.fillcontinents(color='gray')
    plt.title("Titanic Ship Map ", fontsize=20)
    m.scatter(longitude, latitude, latlon=True, alpha=0.5, c='black', s=10)
    plt.show()
    to_continue()


func_dictionary = {
    'help': helps,
    'show_countries': show_countries,
    'top_countries_number': top_countries_n,
    'ships_by_types': ships_by_types,
    'search_ship': search_ships,
    'speed_histogram': speed_histogram,
    'draw_map': draw_map
}


def main():
    print("Welcome to the Ships CLI! Enter 'help' to view available commands.")
    help_input = input('')
    while help_input != 'help':
        help_input = input('Unknown command, type "help" to continue ')
        if help_input == 'help':
            break
    while True:
        global check_for_top_countries_list
        display_choice_menu()
        print('Type in your choice to continue:')
        choice_check = True
        while choice_check:
            try:
                choice_input = input('')
                check_for_top_countries = choice_input
                check_for_top_countries_list = check_for_top_countries.split(' ')
                if choice_input in ['help', 'show_countries', 'ships_by_types', 'search_ship', 'speed_histogram',
                                    'draw_map']:
                    break
                elif len(check_for_top_countries_list) == 2 and check_for_top_countries_list[1].isnumeric() and int(
                        check_for_top_countries_list[1]) <= 42:
                    break
                else:
                    choice_check = True
                    print('Type the correct choice from the menu to continue')
            except IndexError:
                choice_check = True
                print('Type the correct choice from the menu to continue')

        if len(check_for_top_countries_list) == 2 and check_for_top_countries_list[1].isnumeric() and int(
                check_for_top_countries_list[1]) <= 42:
            choice_input = 'top_countries_number'
        func_dictionary[choice_input]()


main()
