import pygame
import random
import os

start_music = (1,2,3)
play_music = (1,2,3,4,5)
end_music = (1,2)
path = os.path.join("..","music")

def music_init():
		pygame.mixer.init()

'''
0 is for starting music
1 is for play music
2 is for ending music
'''
def music_func_thread(music_num):
    global start_music, play_music, end_music
    match(music_num):
        case 0:
            #play starting song
            i = random.choice(start_music)
            pygame.mixer.music.load(f"{path}/start/start{i}.flac")
            pygame.mixer.music.play(loops=-1)
        case 1:
            #play game music
            j = random.choice(play_music)
            pygame.mixer.music.load(f"{path}/play/play{j}.flac")
            pygame.mixer.music.play(loops=-1)
        case 2:
            #play ending music
            k = random.choice(end_music)
            pygame.mixer.music.load(f"{path}/end/end{k}.flac")
            pygame.mixer.music.play(loops=-1)
