#!/usr/bin/python
import requests, json, random
from qhue import Bridge
from gpiozero import Button
from time import sleep, time

#############
# Variables #
#############
debug       = True
brip        = '' # Your Hue bridge's IP
bruser      = '' # Your hue API key
hue         = Bridge(brip, bruser)
lights      = hue.lights
groups      = hue.groups

# GPIO Pin settings
b1 = Button(23) #17 
b2 = Button(22) #27
b3 = Button(27) #22
b4 = Button(17) #23

# Quick variables.
lOne       = hue.lights[1]
lTwo        = hue.lights[2]
lThree      = hue.lights[3]

############
if debug:
    print "Debugging enabled, some general code info:"
    print "Bridge: " + hue.url
    print "Lights: " + lights.url
    print "Groups: " + groups.url
    print "\nExecuting real code:"
    sleep(0.5)
    #lThree.state(sat=254, bri=254, hue=9000) < It works kinda like this
    #lThree.state(sat=12, bri=254, hue=2000)

##########
# Actual #
##########

# Read the current light status from the API
def status(light):
    state = lights[light]()['state']['on']
    if state is True:
        return True
    elif state is False:
        return False
    else:
        return "Error"

# If it is off, switch it on. And vice versa. While loop just in case
def lToggle(light):
    initstate = status(light)
    url = 'http://' + brip + '/api/' + bruser + '/lights/' + str(light) + '/state'
    if debug: print "\tState of light "+ str(light) +" returned: " + str(initstate)
    switch = 'true' if initstate is False else 'false'
    while status(light) == initstate:
        put = requests.put(url, "{\"on\": "+switch+"}")
        if debug: print "\tToggle action of light ("+str(light)+") returned: " + put.text
    return

# Brightness loop 20, 40, 60, 80, 100% (of 254 max)
def briToggle(light):
    if status(light) is False: lToggle(light)
    cur = lights[light]()['state']['bri']
    new = 0
    if debug: print "\tCurrent brightness of light ("+str(light)+"): " + str(cur)
    if cur < 51:
        new = 51 # 20%
    elif cur < 102:
        new = 102 # 40%
    elif cur < 152:
        new = 152 # 60%
    elif cur < 203:
        new = 203 # 80%
    elif cur < 254:
        new = 254 # 100%
    else:
        new = 51 # Back to 20%
    lights[light].state(bri=new)
    if debug: print "\tLight ("+str(light)+") adjusted to: " + str(new)

# A color loop of 5 colors
def colToggle(light):
    if status(light) is False: lToggle(light)
    cur = lights[light]()['state']['bri']

def lRandom(light):
    if status(light) is False: lToggle(light)
    rcolor = random.randrange(0,65280)
    bright = random.randrange(20,254)
    lights[light].state(hue=rcolor, bri=bright)
    if debug: print "\tColor of light ("+str(light)+") changed to: " + str(rcolor) + " (brightness: " + str(bright) +")"

def main():
    menu = 0
    while True:
        if menu == 0:
            # Button 1
            if b1.is_pressed:
                if debug: print("\tButton 1 is pressed")
                lToggle(1)
                b1.wait_for_release()
                if debug: print("\t- Button released. Continue execution.")
            # Button 2
            if b2.is_pressed:
                if debug: print("\tButton 2 is pressed")
                lToggle(3)
                b2.wait_for_release()
                if debug: print("\t- Button released. Continue execution.")
            # Button 3
            if b3.is_pressed:
                if debug: print("\tButton 3 is pressed")
                lToggle(2)
                b3.wait_for_release()
                if debug: print("\t- Button released. Continue execution.")
            # Button 4 - Menu
            if b4.is_pressed:
                if debug: print("\tButton 4 is pressed")
                menu = 1
                b4.wait_for_release()
                if debug: print("\n\tMenu 1 entered")
        # Menu 1 - Brightness
        elif menu == 1:
            if b1.is_pressed: #B1-M1
                if debug: print("\tB1-M1 - Adjust brightness")
                briToggle(1)
                b1.wait_for_release()
                if debug: print("\t- Button released. Continue execution.")
            if b2.is_pressed: #B2-M1
                if debug: print("\tB2-M1 - Adjust brightness")
                briToggle(3)
                b2.wait_for_release()
                if debug: print("\t- Button released. Continue execution.")
            if b3.is_pressed: #B3-M1
                if debug: print("\tB3-M1 - Adjust brightness")
                briToggle(2)
                b3.wait_for_release()
                if debug: print("\t- Button released. Continue execution.")
            if b4.is_pressed: #B4-M1
                if debug: print("\tB4-M1 - Menu up")
                menu = 2
                b4.wait_for_release()
                if debug: print("\n\tMenu 2 entered")
        # Menu 2 - Color 
        elif menu == 2:
            if b1.is_pressed: #B1-M2
                if debug: print("\tB1-M2 - Change color")
                colToggle(1)
                b1.wait_for_release()
                if debug: print("\t- Button released. Continue execution.")
            if b2.is_pressed: #B2-M2
                if debug: print("\tB2-M2 - Change color")
                colToggle(3)
                b2.wait_for_release()
                if debug: print("\t- Button released. Continue execution.")
            if b3.is_pressed: #B3-M2
                if debug: print("\tB3-M2 - Change color")
                colToggle(2)
                b3.wait_for_release()
                if debug: print("\t- Button released. Continue execution.")
            if b4.is_pressed: #B4-M2
                if debug: print("\tB4-M2 - To disco")
                menu = 3
                b4.wait_for_release()
                if debug: print("\n\tStarting disco!")
        # Menu 3 == DISCO!
        elif menu == 3:
            lRandom(1)   
            lRandom(2)   
            lRandom(3)
            sleep(0.2)
            if b1.is_pressed: #B1-M2
                if debug: print("\tB1-M3 - ?")
                b1.wait_for_release()
                if debug: print("\t- Button released. Continue execution.")
            if b2.is_pressed: #B2-M2
                if debug: print("\tB2-M3 - ?")
                b2.wait_for_release()
                if debug: print("\t- Button released. Continue execution.")
            if b3.is_pressed: #B3-M2
                if debug: print("\tB3-M3 - ?")
                b3.wait_for_release()
                if debug: print("\t- Button released. Continue execution.")
            if b4.is_pressed: #B4-M2
                if debug: print("\tB4-M3 - To main")
                menu = 0
                b4.wait_for_release()
                if debug: print("\n\tMenu back to main.")

if __name__ == '__main__':
    main()
