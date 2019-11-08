#!/usr/bin/python3

# Kunal Mukherjee
# audio to speech using google speech api
# 11/7/19

# Mac speech_recognition library installation
# pip3 install SpeechRecognition
# brew install portaudio
# pip3 install pyaudio

# Testing speech_recognization
# python3 -m speech_recognition

#Program usage
#usage: python3 ./audio2text.py audio.wav 

#import library
import speech_recognition as sr
import sys

# the main driver program
def main():
	r = sr.Recognizer()

	audio = sys.argv[1]

	with sr.AudioFile(audio) as source:
	    audio = r.record(source)
	    print ('Conversion Done!')

	try:
	    text = r.recognize_google(audio)
	    
	    f = open("text.txt","w+")
	    f.write(text)
	    f.close()
	    
	    print (text)
	    
	except Exception as e:
	    print (e)

if __name__ == '__main__':
    main()
