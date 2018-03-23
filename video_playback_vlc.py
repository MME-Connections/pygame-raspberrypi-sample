import os
import sys
import vlc
import pygame
import time

# GPIO
import RPi.GPIO as GPIO

#
movie = "test3.mp4"
movie_1 = "test3.mp4"
movie_2 = "test10.mp4"
movie_3 = "test11.divx"


button_1 = 23
button_2 = 24
button_3 = 25
led_green = 16
led_red = 12
led_blue = 20

btn_led_green = 17
btn_led_red = 27
btn_led_blue = 22

GPIO.setmode(GPIO.BCM)
#initialize gpio pin #s
GPIO.setwarnings(False)


GPIO.setup(button_1, GPIO.IN, pull_up_down=GPIO.PUD_UP) ## Tells it that pinNumBTN will be giving input
GPIO.setup(button_2, GPIO.IN, pull_up_down=GPIO.PUD_UP) ## Tells it that pinNumBTN will be giving input
GPIO.setup(button_3, GPIO.IN, pull_up_down=GPIO.PUD_UP) ## Tells it that pinNumBTN will be giving input
#GPIO.setup(button_1, GPIO.IN)
#GPIO.setup(button_2, GPIO.IN)
#GPIO.setup(button_3, GPIO.IN)

GPIO.setup(led_green, GPIO.OUT)
GPIO.setup(led_red, GPIO.OUT)
GPIO.setup(led_blue, GPIO.OUT)

GPIO.setup(btn_led_green, GPIO.OUT)
GPIO.setup(btn_led_red, GPIO.OUT)
GPIO.setup(btn_led_blue, GPIO.OUT)

#pwm setup
#pwm_green = GPIO.PWM(led_green, 50)
#pwm_red = GPIO.PWM(led_red, 50)
#pwm_blue = GPIO.PWM(led_blue, 50)
dc = 95 # duty cycle (0-100)


#This means you are catching a rising detection - so your button press
GPIO.add_event_detect(button_1, GPIO.RISING)
GPIO.add_event_detect(button_2, GPIO.RISING)
GPIO.add_event_detect(button_3, GPIO.RISING)

#initialize
#pwm_green.start(dc)
#pwm_red.start(dc)
#pwm_blue.start(dc)

flag_fullscreen = pygame.FULLSCREEN|pygame.OPENGL|pygame.HWSURFACE|pygame.DOUBLEBUF
flag_normalscreen = pygame.RESIZABLE|pygame.OPENGL|pygame.HWSURFACE|pygame.DOUBLEBUF

#must be the same as monitor and video resolution
#size_screen = (1024,600) #screen size of 7 inch monitor dispaly for raspberrypi
size_screen = (800,600)



def callback(self, player):

	print
	print 'FPS =',  player.get_fps()
	print 'time =', player.get_time(), '(ms)'
	print 'FRAME =', .001 * player.get_time() * player.get_fps()

if len( sys.argv )< 3 or len( sys.argv )> 5:
	print 'Usage: vlctest <file_name> <file_name> <file_name>'
else:
	# Enable in Windows to use directx renderer instead of windib
	#os.environ["SDL_VIDEODRIVER"] = "directx"

	pygame.init()
	screen = pygame.display.set_mode(size_screen,pygame.RESIZABLE|pygame.FULLSCREEN|pygame.OPENGL|pygame.HWSURFACE|pygame.DOUBLEBUF)
	pygame.display.get_wm_info()

	print "Using %s renderer" % pygame.display.get_driver()
	print 'Playing: %s' % sys.argv[1]

	# Get path to movie specified as command line argument
	movie_1 = os.path.expanduser(sys.argv[1])
	movie_2 = os.path.expanduser(sys.argv[2])
	movie_3 = os.path.expanduser(sys.argv[3])

	# Check if movie is accessible
	if not os.access(movie, os.R_OK):
		print('Error: %s file not readable' % movie)
		sys.exit(1)

	# Create instane of VLC
	vlcInstance = vlc.Instance('--input-repeat=-1', '--no-video-title-show', '--fullscreen', '--mouse-hide-timeout=0', '--no-xlib')
	

	# Create new instance of vlc player
	player = vlcInstance.media_player_new()
	#player = vlc.MediaPlayer(movie)

	# Add a callback
	em = player.event_manager()
	em.event_attach(vlc.EventType.MediaPlayerTimeChanged, \
		callback, player)

	# Pass pygame window id to vlc player, so it can render its contents there.
	win_id = pygame.display.get_wm_info()['window']
	if sys.platform == "linux2": # for Linux using the X Server
		player.set_xwindow(win_id)
	elif sys.platform == "win32": # for Windows
		player.set_hwnd(win_id)
	elif sys.platform == "darwin": # for MacOS
		player.set_agl(win_id)

	

	# Quit pygame mixer to allow vlc full access to audio device (REINIT AFTER MOVIE PLAYBACK IS FINISHED!)
	pygame.mixer.quit()

	#create reference to movie.
	media = vlcInstance.media_new(movie)
	# Load movie into vlc player instance
	player.set_media(media)
	# Start movie playback
	#player.play() # dont start at this point

	playing = False
	movie_playing = 0
	game = True
	while game:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(2)
			if event.type == pygame.MOUSEBUTTONDOWN:
				print "we got a mouse button down!"
			if (event.type is pygame.KEYDOWN and event.key == pygame.K_F11):
			    if screen.get_flags() & pygame.FULLSCREEN:
				pygame.display.set_mode(size_screen, flag_normalscreen)
			    else:
				pygame.display.set_mode(size_screen, flag_fullscreen)

		if GPIO.event_detected(button_1):
			if  not movie_playing == 1:
				player.stop()
				media = vlcInstance.media_new(movie_1)
				player.set_media(media)
				player.play()
			playing = True
			movie_playing = 1

			GPIO.output(btn_led_red,GPIO.HIGH)
			time.sleep(1)
			GPIO.output(btn_led_red,GPIO.LOW)

		if GPIO.event_detected(button_2):
			if  not movie_playing == 2:
				player.stop()
				media = vlcInstance.media_new(movie_2)
				player.set_media(media)
				player.play()

			playing = True
			movie_playing = 2
			GPIO.output(btn_led_green,GPIO.HIGH)
			time.sleep(1)
			GPIO.output(btn_led_green,GPIO.LOW)

		if GPIO.event_detected(button_3):
			if  not movie_playing == 3:
				player.stop()
				media = vlcInstance.media_new(movie_3)
				player.set_media(media)
				player.play()
			playing = True
			movie_playing = 3
			GPIO.output(btn_led_blue, GPIO.HIGH)
			time.sleep(1)
			GPIO.output(btn_led_blue,GPIO.LOW)
		
		if movie_playing == 1 and playing == True :
			#pwm_blue.ChangeDutyCycle(100-dc)
			GPIO.output(led_red, GPIO.HIGH)
			time.sleep(0.075)
			GPIO.output(led_red, GPIO.LOW)
			time.sleep(0.075)
		if movie_playing == 2 and playing == True :
			#pwm_blue.ChangeDutyCycle(100-dc)
			GPIO.output(led_green, GPIO.HIGH)
			time.sleep(0.075)
			GPIO.output(led_green, GPIO.LOW)
			time.sleep(0.075)	
		if movie_playing == 3 and playing == True :
			#pwm_blue.ChangeDutyCycle(100-dc)
			GPIO.output(led_blue, GPIO.HIGH)
			time.sleep(0.075)
			GPIO.output(led_blue, GPIO.LOW)
			time.sleep(0.075)
