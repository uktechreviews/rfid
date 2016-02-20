#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import mcpi.minecraft as minecraft
import mcpi.block as block
import random
import time
mc = minecraft.Minecraft.create()


continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

        if uid[0]==75 and uid[1]==53:
                x,y,z = mc.player.getPos()
                mc.player.setPos(x,y+500,z)
                mc.postToChat("Welcome to RFid Minecraft on the Raspberry Pi")
                time.sleep(0.5)
                mc.postToChat(" ")
                time.sleep(0.5)
                mc.postToChat("Select a RFiD card and place it in front of the reader")
                

	if uid[0]==91 and uid[1]==113:
		print "house activated"
		mc.postToChat("House")
		x, y, z = mc.player.getPos()
		x+=1
		b_name = 5
		mc.setBlocks(x,y,z,x+6, y+3, z+3, b_name)
		b_name = 35
		colour = 3
		mc.setBlocks(x,y-1,z,x+6, y-1, z+3, b_name,colour)
		b_name = 0
		mc.setBlocks(x+1,y,z+1,x+5,y+2,z+2,b_name)
		mc.setBlock(x+2,y,z,b_name)
		mc.setBlock(x+2,y+1,z,b_name)
		b_name = 102
		mc.setBlock(x+4,y+1,z,b_name)
		mc.setBlock(x+5,y+1,z,b_name)
		b_name = 64
		mc.setBlock(x+2,y,z,b_name)
        	mc.setBlock(x+2,y+1,z,b_name)

        if uid[0]==105 and uid[1]==141:
                mc.postToChat("Let it snow")
                x,y,z = mc.player.getPos()
                x+=2
                ice = 79
                snow_b = 80
                weather = [ice,snow_b]
                variation_list = [0,1,2,3]
                for distance_x in range (0,10,1):
                    variation=random.choice(variation_list)
                    for distance_z in range(0,(10-variation),1):
                        weather_rnd=random.choice(weather)
                        mc.setBlock(x+distance_x,y-1,z+distance_z,weather_rnd)
                        time.sleep(0.1)

	if uid[0]==75 and uid[1]==84:
		mc.postToChat("Lava falls") 
		x,y,z = mc.player.getPos()
		x+=2
		z+=2
		hill = 1
		lava_flowing = 10
		dirt  = 3
		grass = 2
		mc.setBlocks(x,y,z,x+2,y+20,z+1,hill)
		mc.setBlocks(x,y,z,x+3,y+10,z+1,hill)               
                mc.setBlocks(x,y,z,x+1,y+15,z+2,dirt)
		mc.setBlocks(x,y,z,x,y+6,z-1,grass)
		mc.setBlock(x,y+19,z,lava_flowing)

	if uid[0]==91 and uid[1]==2:
		mc.postToChat("Water falls") 
		x,y,z = mc.player.getPos()
		x+=2
		z+=2
		water_flowing = 8
		dirt  = 3
		grass = 2
		mc.setBlocks(x,y,z,x+2,y+10,z+1,dirt)
		mc.setBlocks(x,y,z,x+3,y+7,z+1,dirt)               
                mc.setBlocks(x,y,z,x+1,y+8,z+2,dirt)
		mc.setBlocks(x,y,z,x,y+6,z-1,grass)
		mc.setBlock(x,y+10,z,water_flowing)

	if uid[0]==75 and uid[1]==89:
		mc.postToChat("Build a farm")
		x,y,z=mc.player.getPos()
		x+=1
		mc.setBlocks(x,y,z,x+5,y+1,z+5,49)
		mc.setBlocks(x+1,y,z+1,x+4,y+1,z+4,60)
		mc.setBlocks(x+1,y+2,z+1,x+4,y+2,z+4,103)		

	if uid[0]==91 and uid[1]==8:
		mc.postToChat("TNT mini game")
		mc.postToChat("Beware 2 of the TNT blocks are active")
		mc.postToChat("Hit with an iron sword")
		mc.postToChat("You will need to reload the world after due to lag!")
		x,y,z=mc.player.getPos()
		x+=1
		y+=10
		mc.setBlocks(x,y,z,x+5,y+5,z+5,41)
		mc.setBlocks(x+1,y+1,z+1,x+4,y+5,z+4,0)
		mc.setBlocks(x+1,y+1,z+1,x+4,y+1,z+4,46)
		x_list=[2,3,4]
		z_list=[2,3,4]
		for bomb in range (1,3,1):
			x_rand=random.choice(x_list)
			z_rand=random.choice(z_list)
			mc.setBlock(x+(x_rand),y+1,z+(z_rand),46,1)
		mc.player.setPos(x+2,y+5,z+2)

        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"

