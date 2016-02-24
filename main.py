import vlc
import string

#Define the queue of the player.
queue = []

#Define some prefixes for certain types of URLs
samba_prefix = "smb://bla;bla:bla@"
local_file = "file:///"

def pause():
	#Pause the player.
	p.pause()

def addToQueue(fileName):
	#Add a song to the queue.
	queue.append(fileName)
	print(fileName + " has been added to the queue!")

def clearQueue():
	#Clear the contents of the queue.
	del queue[:]
	print("Queue cleared.")

def printQueue():
	#Print the contents of the queue in a semi user-friendly way.
	i = 1
	print("The queue consists of the following tracks:")
	for song in queue:
		print("#" + str(i) + ": " + song)
		i = i + 1


def nextTrack():
	#Go the the next track.
	print("Moving on to the next track!")
	if(p.is_playing()):
		queue.pop(0)
	play()

def getCurrentlyPlaying():
	#Gets the track thats currently supposed to be played.
	if len(queue) > 0:
		return queue[0]
	return "fail"

def play():
	#Play some music!
	if(getCurrentlyPlaying == "fail"):
		print("I failed in playing your music...")
	else:
		media = inst.media_new(getCurrentlyPlaying())
		p.set_media(media)
		p.play()
		print("We are now playing: ", getCurrentlyPlaying())

def addLocal(path):
	#Handle an add command with a local url (windows only??)
	addToQueue(local_file + path)

def addSamba(path):
	#Handle an add command with a samba url
	addToQueue(samba_prefix + path)

def addUnc(path):
	#Handle an add command with a unc url
	path = '/'.join(path.split('\\'))
	path = path[2:]
	addToQueue(samba_prefix + path)

#Initialize
inst = vlc.Instance()
p = inst.media_player_new()

#listen to input
while True:
	cmd = input(">")
	cmd = cmd.split(' ')
	
	if(cmd[0] == 'next'):
		nextTrack()

	if(cmd[0] == 'clear'):
		clearQueue()

	if(cmd[0] == 'queue'):
		printQueue()

	if len(cmd)>2:
		if(cmd[0] == 'add'):
			#rebuild song path, because it was exploded by cmd.split()
			path = ""
			for i in range(2, len(cmd)):
				path += (cmd[i]) + " "
			#Trim the path.
			path.strip()

			if(cmd[1] == 'local'):
				#Here you should type something like 
				#seaoftime.mp3
				addLocal(path)

			if(cmd[1] == 'smb'):
				#Here you should type something like:
				#datamonster/Music/MP3/Soundtracks/Kill Bill/01 - Bang Bang.mp3
				addSamba(path)

			if(cmd[1] == 'unc'):
				#Here you should type something like
				#\\cheeseburger.student.utwente.nl\Music\P\Pendulum\Pendulum [2005] Hold Your Colour (FLAC)\14 - Pendulum - Still Grey.flac
				addUnc(path)