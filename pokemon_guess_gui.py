import PySimpleGUI as sg
import os
import random
from PIL import Image

"""
Plays the Who's That Pokemon game using a GUI
Currently only includes Gen 1 pokemon

All pokemon images taken from Bulbapedia 
Who's that pokemon background from u/CaptainRako

Further expansion: include blurb about pokemon after reveal
"""

def get_guess_composites(path, pkm):
	#Set images for pokemon and silhouette
	pkm_spath = path + '/Silhouette/siloh' + pkm
	siloh_img = Image.open(pkm_spath)
	
	#Create new backgrounds with pokemon and silhouette for GUI
	bg = Image.open('Images/who\'s that pokemon.png')
	w, h = bg.size
	
	#Make silhouette background
	siloh_resized = siloh_img.resize((h-170,h-170))
	bg_siloh = bg.copy()
	
	#Note: need 3rd mask parameter when pasting transparent images
	bg_siloh.paste(siloh_resized, (int(w/7),int(h/4)), siloh_resized)
	bg_siloh.save('Images/guess.png')
	
def get_reveal_composites(path, pkm):
	#Set images for pokemon and silhouette
	pkm_path = path + '/Original/' + pkm
	pkm_img = Image.open(pkm_path)
	
	#Create new backgrounds with pokemon and silhouette for GUI
	bg = Image.open('Images/who\'s that pokemon.png')
	w, h = bg.size
	
	#Make reveal background
	pk_resized = pkm_img.resize((h-170,h-170))
	bg_reveal = bg.copy()
	bg_reveal.paste(pk_resized, (int(w/7),int(h/4)), pk_resized)
	bg_reveal.save('Images/reveal.png')

def main():
	path = 'Images/Pokémon/1st Generation'
	pkm = random.choice(os.listdir('Images/Pokémon/1st Generation/Original'))
	get_guess_composites(path, pkm)
	guess_txt = 'Who\'s that Pokemon? '
	
	layout1 = [
			[sg.Image('Images/guess.png', key = 'guess')],
			[sg.Text(guess_txt, size = (17,1), font = ('Helvetica', 25)), 
			sg.InputText(do_not_clear = False, focus = True),
			sg.Submit()]
	]
	window1 = sg.Window('Who\'s That Pokemon?', size = (800, 500)).Layout(layout1)
	
	while True:
		event, values = window1.Read()

		if event is None or event == 'Exit':
			break
		
		if event == 'Submit':
			#Prepare reveal window image
			get_reveal_composites(path, pkm)
			
			#Hide guess window 
			window1.Hide()
			
			#Outcome of guess
			user_guess = values[0].title()
			pkm_name = pkm[3:].replace('.png','')
			pkm_name = pkm_name.replace('_', ' ')
			if user_guess == pkm_name.title():
				guess_outcome = 'That\'s right! '
			else:
				guess_outcome = ''
			
			#Set up reveal window
			reveal_txt = ' '*15 + guess_outcome + 'It\'s '
			pkm_txt =  pkm_name + '!'
			layout2 = [
			[sg.Image('Images/reveal.png')],
			[sg.Text(reveal_txt, font = ('Helvetica', 25)),
			 sg.Text(pkm_txt, font = ('Helvetica', 25), text_color = 'red')],
			[sg.Text(' '*60),
			sg.Button('Wow, that\'s amazing! Show me another one.', key = 'wow')]
			]
			window2 = sg.Window('It\'s...').Layout(layout2)
			
			#Choose new pokemon for next round and update guess window
			new_pkm = random.choice(os.listdir('Images/Pokémon/1st Generation/Original'))
			get_guess_composites(path, new_pkm)
			window1.Element('guess').Update('Images/guess.png')
			
			while True:
				event2, values2 = window2.Read()
				if event2 is None or event2 == 'Exit' or event2 == 'wow':
					window2.Close()								
					window1.UnHide()
					pkm = new_pkm #Update reveal window for next round
					break
	
if __name__ == '__main__':
	main()



