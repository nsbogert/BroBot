import pandas as pd
import requests
import time
import smtplib, ssl
from datetime import datetime


NotifiedNick = False

# Function to Send email to Nick's Phone
def sendNickNotification(message):
    port = 465  # For SSL
    password = '*************'
    mySMSTarget = '**********@vtext.com'

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("('********@gmail.com", password)
        server.sendmail('********@gmail.com', '**********@vtext.com', message)

        
def checkVulcan(url, position_array):
    # Takes in a url and a set of positions on the grid
    # Outputs "True" If any of the targets are not 'Out of Stock'. Otherwise returns False (still out of stock)
    
    Notify = False
    
    # Get the HTML
    dfs = pd.read_html(url, header=0)

    # Pull out the dataframe corresponding to the table I want. Seems consistant at #5
    mydf = dfs[5]

    # Check the items I want on the page
    for position in position_array:
        if mydf.at[position,'Qty'] != '(Out of Stock)':
            Notify = True

    return Notify


def checkRogue(url, target_text_array):
    # Takes in a Rogue URL and an array of text blurbs to search for on the page
    # Returns "True" if any of the target texts are missing from the page (indicating the item is back in stock.
    #      False indicates the item is still out of stock. 
    
    Notify = False    

    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest",
      "Accept-Encoding": "identity"
    }

    r = requests.get(url, headers=header)

    # Check if target text is present in the HTML doc
    for text in target_text_array:
        if text not in r.content:
            Notify = True

    return Notify


# Check every so often. Biz logic stored here.  
while NotifiedNick == False:
    if ((datetime.now(tz=None).hour >= 6) & (datetime.now(tz=None).hour < 21)): # Starts at 6 and ends at 9pm
        
        # Check Vulcan Steel Plates
        url = 'https://www.vulcanstrength.com/Absolute-Calibrated-Steel-Plates-Vulcan-p/v-apsp.htm'
        positions = [6,7,8]
        if checkVulcan(url, positions):
            message = "Vulcan Steel Plates are available."
            sendNickNotification(message)
            
        # Check Vulcan Bumper Plates
        url = 'http://www.vulcanstrength.com:80/Alpha-Bumper-Plate-Pairs-p/alpha10.htm'
        positions = [3,4]
        if checkVulcan(url, positions):
            message = "Vulcan Bumper Plates are available."
            sendNickNotification(message)            
                  
        # Check Rogue Incine Bench
        url = 'https://www.roguefitness.com/rogue-adjustable-bench-2-0'
        text = b"id=\"product-price-25843\">\n<span class=\"price\">$545.00</span> </span>\n</div>\n</div>\n</div>\n<div class=\"bin-stock-availability\">\n\n<div class=\"bin-out-of-stock bin-out-of-stock-cart\">"
        if checkRogue(url, [text]):
            message = "Rogue Incline Bench 2.0 is available."   
            sendNickNotification(message)
        
        # Check Rogue Six Shooters
        url = 'https://www.roguefitness.com/rogue-6-shooter-olympic-plates'
        text = b"45LB 6-Shooter Olympic Grip Plates - Pair</div>\n<div class=\"item-price\">\n<div class=\"price-box\">\n<span class=\"regular-price\" id=\"product-price-47225\">\n<span class=\"price\">$156.00</span> </span>\n</div>\n</div>\n</div>\n<div class=\"bin-stock-availability\">\n\n<div class=\"bin-out-of-stock bin-out-of-stock-cart\">"
        if checkRogue(url, [text]):
            message = "Rogue Six Shooter Plates are available."
            sendNickNotification(message)
            
        # Check Rogue Steel Calibrated Plates
        url = 'https://www.roguefitness.com/rogue-calibrated-lb-steel-plates'
        text35lb = b"35LB Calibrated Plate - Pair</div>\n<div class=\"item-price\">\n<div class=\"price-box\">\n<span class=\"regular-price\" id=\"product-price-38883\">\n<span class=\"price\">$149.50</span> </span>\n</div>\n</div>\n</div>\n<div class=\"bin-stock-availability\">\n\n<div class=\"bin-out-of-stock bin-out-of-stock-cart\">"
        text45lb = b"45LB Calibrated Plate - Pair</div>\n<div class=\"item-price\">\n<div class=\"price-box\">\n<span class=\"regular-price\" id=\"product-price-38885\">\n<span class=\"price\">$185.00</span> </span>\n</div>\n</div>\n</div>\n<div class=\"bin-stock-availability\">\n\n<div class=\"bin-out-of-stock bin-out-of-stock-cart\">"
        text55lb = b"55LB Calibrated Plate - Pair</div>\n<div class=\"item-price\">\n<div class=\"price-box\">\n<span class=\"regular-price\" id=\"product-price-38887\">\n<span class=\"price\">$225.00</span> </span>\n</div>\n</div>\n</div>\n<div class=\"bin-stock-availability\">\n\n<div class=\"bin-out-of-stock bin-out-of-stock-cart\">"
        
        if checkRogue(url, [text35lb,text45lb,text55lb]):
            message = "Rogue Steel LB Plates are available."
            sendNickNotification(message)
        
        print("Checked at "+str(datetime.now(tz=None)))
        
    time.sleep(300) # delays N seconds
