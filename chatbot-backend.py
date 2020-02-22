TOKEN = "<YOUR TOKEN>"
# TOKEN = "1097961899:AAEJh8vH0Eqcd5TJaCFC8DMLFiEX1h-eXNQ"

import botogram
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
bot = botogram.create(TOKEN)
from datetime import datetime

@bot.command("hello")
def hello_command(chat, message, args):
    """Say hello to the world!"""
    chat.send("Hello world from bala's bot..")

@bot.command("time")
def time_command(chat, message, args):
    print("Sender:", message.sender.name)
    """Print the current time: from the machine"""
    chat.send(f"Time : {datetime.now()}")

@bot.command("setinputfile")
def inputfile(chat, message, args):
    """Set the inputfile for processing.."""
    print(args)
    if len(args) == 1:
        save_json(key=message.sender.name, value=args[0])
        chat.send("Ok Noted.")
    else:
        chat.send("Usage: /setinputfile <filename or filepath>")

@bot.command("stats")
def stats(chat, message, args):
    """Returns the current inputfile stats"""
    fname = load_json().get(message.sender.name, None)
    if fname:
        df = pd.read_csv(fname)
        chat.send("Columns: ")
        chat.send(" , ".join(df.columns))
        chat.send("Info:")
        chat.send(f"{df.info()}")
        chat.send("Dtypes:")
        chat.send(f"{df.dtypes}")
    else:
        chat.send("Please set an inputfile before calling this.. /setinputfile for more info")

    
@bot.command("plot")
def plot(chat, message, args):
    """Plot the graph based on a column"""
    
    if len(args) == 2:
        col = args[0]
        kind = args[1]
        fname = load_json().get(message.sender.name, None)
        if fname:
            df = pd.read_csv(fname)
            series = df[col]
            try:
                fig = plt.figure(figsize=(10,7))
                series.plot(kind=kind)
                output_filename = f"C:/Users/balap/Desktop/outputs/{message.sender.name}-output.png"
                plt.savefig(output_filename)
                chat.send("Uploading....")
                chat.send_photo(output_filename)
            except Exception as e:
                print(e)
                #chat.send("Sorry. something went wrong.. Please call...")
                #chat.send("Please check your graph_type : kind")
        else:
            chat.send("Please set an inputfile before calling this.. /setinputfile for more info")
    else:
        chat.send("Usage /plot <col1> <plot_type>")
        return
    

@bot.command("plotxy")
def plotxy(chat, message, args):
    """Plot the graph based on a column"""
    
    if len(args) >= 2:
        cols = args[0].split(",") #['Date','AdjColse']
        kind = args[1]
        if len(args) >2:
            hue = args[2]
            print(f"Value of -> {hue}")
        else:
            hue = None
            print(f"Value of -> {hue}")

        fname = load_json().get(message.sender.name, None)
        if fname:
            df = pd.read_csv(fname)
            smalldf = df
            try:
                fig, ax = plt.subplots(1,1,figsize=(10,7))

                if kind == "categorical":
                    pass
                elif kind == "scatter":
                    if hue:
                        sns.scatterplot(x=cols[0], y=cols[1], data=smalldf, hue=hue)
                    else:
                        sns.scatterplot(x=cols[0], y=cols[1], data=smalldf)
                #plot_from_seaborn(smalldf, x=cols[0], y=cols[1], kind=kind, ax=ax, hue=hue)
                #smalldf.plot(x=cols[0], y=cols[1], kind=kind)
                output_filename = f"C:/Users/balap/Desktop/outputs/{message.sender.name}-outputxy1.png"
                plt.savefig(output_filename)
                chat.send("Uploading....")
                chat.send("Please wait....")
                chat.send_photo(output_filename)
            except Exception as e:
                print(e)
                #chat.send("Sorry. something went wrong.. Please call...")
                #chat.send("Please check your graph_type : kind")
        else:
            chat.send("Please set an inputfile before calling this.. /setinputfile for more info")
    else:
        chat.send("Usage /plot <col1>,<col2> <plot_type>")
        return
        

@bot.command("currentfile")
def current(chat, message, args):
    """Returns the current inputfile"""
    chat.send(  load_json().get(message.sender.name, "Not set for this user."))
        
import json
def save_json(key, value):
    fname="data.json"
    current_dct = load_json()
    current_dct[key] = value
    with open(fname, "w") as f:
        f.write( json.dumps(current_dct) )

def load_json():
    fname="data.json"
    try:
        with open(fname, "r") as f:
            return json.loads(f.read())
    except:
        return {} 

def plot_from_seaborn(df,x,y,kind,ax, hue=None):
    if kind == "bar":
        pass
    elif kind == "scatter":
        if hue: sns.scatterplot(x=x, y=y, data=df, hue=hue, ax=ax)
        else: sns.scatterplot(x=x, y=y, data=df, ax=ax)


if __name__ == "__main__":
    bot.run()