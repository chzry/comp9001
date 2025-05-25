import json
import os
import time
import random
from datetime import datetime

datafile = "crow_data.json"

def load_crowdata():
    if os.path.exists(datafile):
        with open(datafile, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return None
    
def save_crowdata(crow_data):
    with open(datafile,"w", encoding="utf-8") as f:
        json.dump(crow_data, f)

def remind_drinkwater(crow_data):
        def remind():
            while crow_data.get("drinkwater", False):
                print(f"⏰ It's time for water! Let's drink water, have a rest!")
                time.sleep(1800)    #半个钟提醒一次



#游戏开始
def gamestart():
    crow_data = load_crowdata()

    if crow_data is None:    #第一次打开游戏
        print("""Welcome to the game!

You get a crow egg ...""")
        crowname = input("Now, please give your crow a name:")

        crow_data = {"name": crowname,
                 "stage": "egg",
                 "feed": 0,
                 "hatch": 0,
                 "drinkwater": False,
                 "lastfeeddate": None}
        save_crowdata(crow_data)

        print()
        print("   _____  ")
        print("  /     \\ ")
        print(" /       \\")
        print("|         |")
        print(" \\       /")
        print("  \\_____/ ")
        print()
        
        print(f"""Hooray! 
Now {crowname} is still in the egg, you can choose "pet" to make him hatch faster!""")
    
        #comm = input("What do you want to do now?")

    else:    #有游戏记录了，不是第一次打开了
        print(f"Welcome back!{crow_data["name"]} misses you so much.")
    return crow_data

def viewcrow(crow_data):
    stage = crow_data["stage"]
    if stage == "egg":
        print("   _____  ")
        print("  /     \\ ")
        print(" /       \\")
        print("|         |")
        print(" \\       /")
        print("  \\_____/ ")
    elif stage == "litte_crow":
        print("   \\   /")
        print("   (o o)")
        print("  /  V  \\")
        print(" /(  _  )\\")
        print("   ^^ ^^")
    elif stage == "big_crow":
        print("   \\  ^  /")
        print("   ( o o )")
        print("   /  V  \\")
        print("  /( === )\\")
        print(" /__|:::|__\\")
        print("   ||   ||")
        print("   ^^   ^^")

def feeding(crow_data):
    if crow_data["stage"] == "little_crow":
        today = datetime.now().strftime("%Y-%m-%d")
        lastfeed = crow_data.get("lastfeeddate")
        if lastfeed == today:
            print(f"You already fed {crow_data["name"]} today. Try again tomorrow.")
            return
            
        crow_data["feed"] += 1
        crow_data["last_feed_date"] = today
        print(f"{crow_data["name"]}: Thank you for feeding me. I'm full now!")

        if crow_data["feed"] >= 10:
            crow_data["stage"] = "big_crow"
            print(f"WOW! {crow_data["name"]} has grown up!")
    elif crow_data["stage"] == "big_crow":
        print(f"{crow_data["name"]} is already fully grown.")
    else:    #stage==egg
        print("Oops! You can't feed an egg.")
    save_crowdata(crow_data)

def playgame(crow_data):
    if crow_data["stage"] == "egg":
        print("Your crow hasn't hatched yet. It cannot interact with you in the game.")
    else:
        num = random.randint(1,200)
        print(f"{crow_data["name"]}: I came up with a number within the range of 0-200! Let's guess!")
        
        while True:
            guess = int(input("Your guess: "))
            if 0 <= guess and guess <= 200:
                if guess < num:
                    print("Too low!")
                elif guess > num:
                    print("Too high!")
                elif guess == num:
                    print("Correct!")
                    break
            else:
                print("Out of range!")

def pet(crow_data):
    if crow_data["stage"] == "egg":
        today = datetime.now().strftime("%Y-%m-%d")
        lastfeed = crow_data.get("lastfeeddate")
        if lastfeed == today:
            print(f"You already pet {crow_data["name"]} today. Try again tomorrow.")
            return
        
        crow_data["hatch"] += 1
        crow_data["lastfeeddate"] = today
        print("You pet the egg... it wiggles slightly.")

        if int(crow_data["hatch"]) == 10:
            crow_data["stage"] = "little_crow"
            print(f"Crack! {crow_data["name"]} has broken out of its shell!")
    else:
        print("Your crow is already hatched.")
    save_crowdata(crow_data)

def main():
    crow_data = gamestart()

    while True:
        comm = input("\nHi! What would you like to do?  view|pet|feed|game|wateron|wateroff|quit :  ").strip().lower()
        if comm == "view":
            viewcrow(crow_data)
        elif comm == "pet":
            pet(crow_data)
        elif comm == "feed":
            feeding(crow_data)
        elif comm == "game":
            playgame(crow_data)
        elif comm == "wateron":
            crow_data["drinkwater"] = True
            print("Reminder to drink water function is ready.")
            save_crowdata(crow_data)
        elif comm == "wateroff":
            crow_data["drinkwater"] = False
            print("Reminder to drink water function is off.")
            save_crowdata(crow_data)
        elif comm == "quit":
            print("Saving...please wait...")
            time.sleep(2)
            save_crowdata(crow_data)
            print("Bye!")
            break
        else:
            print("Unknown command. Please re-enter.")

if __name__ == "__main__":
    main()
            