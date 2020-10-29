import pandas as pd #import pandas
import datetime #import datetime
import tkinter as tk
from tkinter import filedialog

#Function that executes DATE input
#Also specifies the format of the date input
#Validates input with a try except and if it fails
#it repeats the DATE input request
#date HAS to be entered as [YYYY-MM-DD]
#or it won't be able to match it with the dates in file
def booking_date():
    
    #func to take in date from user
    def getDate():
        input_date = input("\nEnter the date of booking [YYYY-MM-DD]: ")
        return input_date


    global bDate    #accesses global bDate var outside of func
    bDate = getDate()   #executes date input function and populates the global date variable
    

    dateformat = "%Y-%m-%d"     #specifies required format of date input
    try:
        datetime.datetime.strptime(bDate, dateformat)       #checks if inputted date matches the specified format
        print("Booking results for ", bDate, "\n")          #presents the inputted date
        global success      #accesses global var out of func
        success = True      #if input data matches the specified format, returns True
    except ValueError:
        print("Invalid format")     #Prints error message
        pass



#create dataframe of requested dates
def readDates():
    #displays the data file and parses dates
    #parsing is required to match date in csv
    df = pd.read_csv(file_path, parse_dates=['reservation_status_date'])


    pd.set_option('display.max_rows', None) #removes view limit so all rows are displayed


    #accesses global bDate variable
    #and populates it with date in the format
    #of datetime - converts from str to datetime
    global bDate
    bDate = datetime.datetime.strptime(bDate, '%Y-%m-%d') #convert input date from str to datetime

    #Retrieves the data for a range of 7 days
    #This range is from the inputted date + 6 days
    enddate = bDate + datetime.timedelta(days = 7) #gets date 7 days from input date
    global dfDate
    dfDate = df.copy()  #copy dataframe to a new variable
    dfDate = dfDate.loc[(dfDate['reservation_status_date'] >= bDate) & (dfDate['reservation_status_date'] < enddate)] #returns dataframe of input date + 6 days (7 days total)

    #exclude rows with cancelled bookings
    areCancelled = dfDate[dfDate['is_canceled'] == 1].index
    dfDate.drop(areCancelled, inplace = True)


    #Displays dataframe of the requested dates
    #input date + 6 days (7 days total)
    print("\nBookings from ", bDate, "to ", enddate,"---------------------------------------------\n")
    print(dfDate)



#Create dataframe representing the amount of
#adults, children and babies within the requested dates
def resCount():

    #gets the total number of adults, children and kids respectively
    global dfDate
    df_adults = int(dfDate['adults'].sum())
    df_children = int(dfDate['children'].sum())
    df_babies = int(dfDate['babies'].sum())

    #Creates a dictionary of the amount of
    #residents in each category
    total_res = {'adults' : [df_adults],
                 'children' : [df_children],
                 'babies' : [df_babies]}

    #Accesses global variable and populates it
    #with a dataframe with the columns 'adults'
    #'children' and 'babies' and their values
    global df_totals
    df_totals = pd.DataFrame.from_dict(total_res) #converts dictionary to a dataframe to be saved as .csv

    print("\nTotal number of residents---------------------------------------------")
    print(df_totals)
    


#save to csv
def exportCSV(e):
    save = input("\nDo you want to save the above as .csv? [Y/N] ") 
    
    if save == "Y" or save == "y" or save == "Yes" or save == "yes":        
        try:
            export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
            (e).to_csv(export_file_path, index = True, header=True)
        except Exception:
            pass
        
    

#main program loop

#opens dialog to select data file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
    
while True:
    
    bDate = ""          #empty variable will be populated in the bookingdate() func

    success = False     #var to check if input data has been entered in the right format
    while success == False:     #loop to continue requesting date input until format is correct
        booking_date()



    #prints out table of 7 days from and including input date
    dfDate = ""     #7 days dataframe to be populated by readDates()
    readDates()

    
    #save the table of 7 days
    exportCSV(dfDate)

    #presents dataframe of amounts of residents
    df_totals = ""
    resCount()

    #save dataframe of amount of adults, kids and babies
    exportCSV(df_totals)

    

    input("press ENTER to search another date")
