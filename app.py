"""
Created by: Gagan Nayyar
Date: 20/Sept/2021
Task: Remove emojies and punctuations from a pandas dataframe 

"""

#Libraries 
import pandas as pd
import re
import emoji
from pywebio.input import *
from pywebio.output import *
from pywebio.platform import tornado
from pywebio import start_server
import datetime as dt
import random
pd.options.mode.chained_assignment = None

#Input to import the excel file
file_path = file_upload("Please upload the file to predict NPS")

#Input to get the folder path where user want to save file
path_to_save = input("Please enter the path where you want to save the file")



def remove_emoji(string):

    """This function remomove emojis"""
    return emoji.get_emoji_regexp().sub(u'', string)

def get_file():

    df = pd.read_excel(file_path['content']) #Load the file to pandas dataframe
    df.dropna(inplace=True) # Drop the empty rows
    df.reset_index(inplace=True) #Reset the index for for loop
    df["Cleaned_Comment"] = " " #Create a new column for cleaned comments

    #Create rows with the cleaned data in the dataframe
    for i in range(0,len(df["Comment"])):     
        res = re.sub(r'[^\w\s]', '', df["Comment"][i])
        res_emoji = remove_emoji(res)
        df["Cleaned_Comment"][i] = random.randint(1,5)
    #Drop the index created by Python    
    df = df.drop(columns='index', axis=1)
    return df

now = dt.datetime.now()

def export_excel():
    df = get_file()
    put_processbar('bar') # Process Bar
    for i in range(1,11):
        set_processbar('bar', i/10)
    #Export the data tp .xlsx format in the user specified folder    
    df.to_excel(path_to_save+"/"+"processed.xlsx")
    put_text(f"Completed. The file is saved at {path_to_save} as processed.xlsx. You may now close the browser.")
    
try:
    if __name__ == "__main__":
        start_server(export_excel())

except Exception as e:
    print(e)

