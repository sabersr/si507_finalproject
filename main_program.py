from itertools import count
import json

import plotly.express as px
from data_tree import Tree
import webbrowser
import pandas as pd

# Const
RANK_YEAR = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
TYPE = ['s', 'c', 'p', 'e']
SELECTIONS = ['genre', 'release year', 'chart year', 'rank', 'length', 'explicit', 'e']
SEARCH_TYPE = ['c', 'e']
INTERACTION = ['i', 'v', 'e']
PREVIEW = ['p', 'a', 'u', 'e']
GRAPH = ['p', 'h', 'e']

def main():
    data = json.load(open("billboard.json"))
    
    current_tree = None
    selections = []
    print("Welcome to the recommendation of songs from Billboard Year-end Hot 100 Singles of 2012-2021!")

    while True:
        search = input("Enter \"s\" to start the new search, \"c\" to continue the previous search, \"p\" to interact with the current search, \"e\" to quit: ")
        while (search not in TYPE):
            print("Sorry, I cannot recognize this answer. I can only recognize \"s\", \"c\", \"p\", and \"e\".")
            search = input("Enter \"s\" to start the new search, \"c\" to continue the previous search, \"p\" to interact with the current search, \"e\" to quit: ")

        if search == 's':
            print("Load the full song lists...")
            newSearchTree = Tree(data=data)
            current_tree = query(newSearchTree)

        elif search == 'c':
            # Check and load previous search
            if current_tree is None:
                print("There is no previous search. Please try again.")
                continue
            print("Load the previous search.")
            current_tree.traverse()

            current_tree = query(current_tree)

        elif search == 'p':
            if current_tree is None:
                print("There is no previous search. Please try again.")
                continue

            print("Load current search.")
            current_tree.traverse()
            if len(current_tree.access()) == 0:
                print("There is no recommended song based on your filters.")
                continue

            length = len(current_tree.access())
            if length > 50: length = 50

            print()
            print("Here is the list of Top", length, "recommended songs based on your filters.")
            print("Due to the limited space, we could only present at most 50 songs information here.")
            print("The songs are sorted by the descending order of the rank year and the ascending order of the rank.")
            print()

            while True:
                song_info = current_tree.access()
                for index, song in enumerate(song_info):
                    print(index+1, song["Title"].replace('"', ''), "-", song["Artist(s)"])
                    if (index+1 >= 50): break

                print()
                visual = input("Please enter \"i\" to interactive with the listed song, \"v\" to visualize the current search or \"e\" to exit: ")
                while (visual not in INTERACTION):
                    print("Sorry, I cannot recognize this answer. I can only recognize \"i\", \"v\", and \"e\".")
                    visual = input("Please enter \"i\" to interactive with the listed song, \"v\" to visualize the current search or \"e\" to exit: ")

                if visual == "e": break

                if visual == "i":
                    # Small interaction
                    number = input("Please enter the index for more information of the song: ")
                    while (not number.isdecimal()) | ((int(number) > length) | (int(number) <= 0)):
                        print("Sorry, please enter a valid number")
                        number = input("Please enter the index for more information of the song: ")

                    index = int(number)-1
                    print()
                    print("Detailed song data:")
                    print("Song name:", song_info[index]["Title"].replace('"', ''))
                    print("Artist(s):", song_info[index]["Artist(s)"])
                    print("Rank Year:", song_info[index]["Year"])
                    print("Rank:", song_info[index]["No."])
                    print("Release date:", song_info[index]["release_date"])
                    print("Genre:", song_info[index]["genre"])
                    print("Explicit", song_info[index]["explicit"])
                    print("Track time:", int((song_info[index]["trackTime"]/(1000*60))%60), "minutes", int((song_info[index]["trackTime"]/1000)%60) ,"seconds")
                    print()

                    # interaction mode
                    mode = input("Please enter \"p\" to see the image of the song, \"a\" to have the audio preview, \"u\" to see the song in Apple Music, or \"e\" to exit: ")
                    while (mode not in PREVIEW):
                        print("Sorry, I cannot recognize this answer. I can only recognize \"p\", \"a\", \"u\" and \"e\".")
                        visual = input("Please enter \"p\" to see the image of the song, \"a\" to have the audio preview, \"u\" to see the song in Apple Music, or \"e\" to exit: ")

                    if mode == "p":
                        if song_info[index]["images"] is not None:
                            print("Launching the image in the web brower...")
                            webbrowser.open(song_info[index]["images"])
                        else:
                            print("Sorry, there is no image for this song.")
                    elif mode == "a":
                        if song_info[index]["preview_url"] is not None:
                            print("Launching the audio preview in the web brower...")
                            webbrowser.open(song_info[index]["preview_url"])
                        else:
                            print("Sorry, there is no audio preview for this song.")
                    elif mode == "u":
                        if song_info[index]["trackView"] is not None:
                            print("Launching the Apple Music link in the web brower...")
                            webbrowser.open(song_info[index]["trackView"])
                        else:
                            print("Sorry, there is no Apple Music link for this song.")
                    elif mode == "e":
                        print("Go back to recommended song lists")
                        print()
                        continue
                
                    print("Go back to recommended song lists")
                    print()
                    continue

                elif visual == "v":
                    # Visualization
                    mode = input("Please choose a filter from 'Genre', 'Release Year', 'Chart Year', 'Rank', 'Length', and 'Explicit' to visualize or 'E/e' to exit: ").lower()
                    while (mode not in SELECTIONS):
                        print("Sorry, I cannot recognize this filter. I can only recognize 'Genre', 'Release Year', 'Chart Year', 'Rank', 'Length', 'Explicit'.")
                        mode = input("Please choose a filter from 'Genre', 'Release Year', 'Chart Year', 'Rank', 'Length', and 'Explicit' to visualize or 'E/e' to exit: ").lower()

                    if mode == "e": 
                        print("Go back to recommended song lists")
                        print()
                        continue
                    
                    dfItem = pd.DataFrame.from_records(song_info)
                    dfItem["release_date"] = pd.to_datetime(dfItem["release_date"])
                    dfItem["release_year"] = dfItem["release_date"].dt.year
                    dfItem["length"] = dfItem["trackTime"]/60000

                    filter_label = mode
                    if mode == 'release year': 
                        filter_label = 'release_year'
                    if mode == "rank":
                        filter_label = 'No.'
                    if mode == "chart year":
                        filter_label = 'Year'

                    graph = input("Please enter \"p\" for pie chart, \"h\" for histogram or \"e\" to exit: ")
                    while (graph not in GRAPH):
                        print("Sorry, I cannot recognize this answer. I can only recognize \"p\", \"h\" and \"e\".")
                        graph = input("Please enter \"p\" for pie chart, \"h\" for histogram or \"e\" to exit: ")
                    
                    if graph == "e":
                        print("Go back to recommended song lists")
                        print()
                        continue

                    if  graph == "p":
                        fig = px.pie(dfItem, names=filter_label)
                    elif graph == "h":
                        fig = px.histogram(dfItem, x=filter_label)
                    fig.show()

                    print("Go back to recommended song lists")
                    print()
                    continue

        elif search == 'e':
            print("Thank you! Bye!")
            break
    
def query(currentTree):
    while True:
        search = input("Please choose a filter from 'Genre', 'Release Year', 'Chart Year', 'Rank', 'Length', and 'Explicit' or 'E/e' to exit: ").lower()
        
        while (search not in SELECTIONS):
            print("Sorry, I cannot recognize this filter. I can only recognize 'Genre', 'Release Year', 'Chart Year', 'Rank', 'Length', 'Explicit'.")
            search = input("Please choose a filter from 'Genre', 'Release Year', 'Chart Year', 'Rank', 'Length', and 'Explicit' or 'E/e' to exit: : ").lower()

        if search == 'e': break

        print("Please enter the value you would like to find according to the filter:")
        print("For release year and chart year, please enter a year from 2012 to 2021.")
        print("For rank, please enter a number from 1 to 100.")
        print("For length, we will provide all songs that their length is less than the value.")
        print("For explicitness, please enter whether 'True' or 'False'.")
        print("Please use each filter once since the selection is irreversible.")
        print("If you do not follow the insruction above, the program may not provide proper result.")

        value = input()

        search_label = search
        if search == 'release year': 
            search_label = 'release_date'
            value = int(value)
        if search == 'chart year': 
            search_label = 'Year'
            value = int(value)
        if search == 'length': 
            search_label = 'TrackTime'
            value = int(value)
        if search == 'rank': 
            search_label = 'No.'
            value = int(value)
        if search == 'explicit':
            if value.lower() == "true": value = True
            if value.lower() == "false": value = False

        currentTree.insert(search_label, value)

        exit = input("Enter \"c\" to continue filtering or \"e\" to exit current search to see the result: ")

        while (exit not in SEARCH_TYPE):
            print("Sorry, I cannot recognize this answer. I can only recognize \"c\" and \"e\".")
            exit = input("Enter \"c\" to continue filtering or \"e\" to exit current search to see the result: ")

        if exit == "e":
            break
    return currentTree


if __name__ == '__main__':
    main()