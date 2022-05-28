from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import options
import json

pygame.init()
pygame.mixer.init()
pygame.key.set_repeat()

window = pygame.display.set_mode((options.screen_width, options.screen_height))
clock = pygame.time.Clock()

receptorimg = pygame.image.load("receptor.png").convert_alpha()
receptorimg = pygame.transform.scale(receptorimg, (options.columnwidth, options.columnwidth))
receptorDimg = pygame.image.load("receptorD.png").convert_alpha()
receptorDimg = pygame.transform.scale(receptorDimg, (options.columnwidth, options.columnwidth))

noteimg = pygame.image.load("note.png").convert_alpha()
noteimg = pygame.transform.scale(noteimg, (options.columnwidth, options.columnwidth))

lnheadimg = pygame.image.load("lnhead.png").convert_alpha()
lnheadimg = pygame.transform.scale(lnheadimg, (options.columnwidth, options.columnwidth))
lnbodyimg = pygame.image.load("lnbody.png").convert_alpha()
lntailimg = pygame.image.load("lntail.png").convert_alpha()
lntailimg = pygame.transform.scale(lntailimg, (options.columnwidth / 1.5, options.columnwidth / 2))

font = pygame.font.Font(None, 30)

class Receptor():
    def __init__(self,a,b,c,d):
        self.x = a
        self.y = b
        self.keybind = c
        self.track = d
        self.held = False
        self.heldafter = False

receptors = [
    Receptor((0 * options.columnwidth + options.columnoffset),options.hitpos,options.keybinds[0],0),
    Receptor((1 * options.columnwidth + options.columnoffset),options.hitpos,options.keybinds[1],1),
    Receptor((2 * options.columnwidth + options.columnoffset),options.hitpos,options.keybinds[2],2),
    Receptor((3 * options.columnwidth + options.columnoffset),options.hitpos,options.keybinds[3],3),
]

def load(map):
    data = json.load(open(map, encoding="utf8"))
    
    for note in data["hitObjects"]:
        if note["x"] == 64: note["x"] = 0
        elif note["x"] == 192: note["x"] = 1
        elif note["x"] == 320: note["x"] = 2
        elif note["x"] == 448: note["x"] = 3
    
    return data["hitObjects"]

map = load("./beatmap.json")
pygame.mixer.music.load("audio.mp3")
pygame.mixer.music.set_volume(options.volume)
pygame.mixer.music.play()
currenttime = options.hitpos / options.scrollspeed + options.audiooffset

while 1:
    window.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    keys = pygame.key.get_pressed()    
                            
    for key in receptors:
        if keys[key.keybind]:
            window.blit(receptorDimg, (key.x, key.y))
            key.held = True
        else:
            window.blit(receptorimg, (key.x, key.y))
            key.held = False
            key.heldafter = False
    
    for note in map:

        if note["endTime"] <= currenttime - (1250 / options.scrollspeed):
            map.pop(map.index(note))
        else:
            if note["time"] <= currenttime + (1250 / options.scrollspeed) and not note["endTime"] < currenttime - (1250 / options.scrollspeed):
            
                y = (currenttime - (note["time"] - 1)) / (note["time"] - (note["time"] - 1)) * options.scrollspeed
                yLN = (currenttime - (note["endTime"] - 1)) / (note["time"] - (note["time"] - 1)) * options.scrollspeed + ((options.columnwidth/2) / options.scrollspeed)
                lnobj = pygame.transform.scale(lnbodyimg, ((options.columnwidth/1.5), (note["endTime"] - note["time"]) * options.scrollspeed))
                    
                '''if note["type"] == "hold":
                    window.blit(lnobj, (receptors[note["x"]].x + (options.columnwidth/6), yLN))
                    window.blit(lntailimg, (receptors[note["x"]].x + (options.columnwidth/6), yLN))
                    window.blit(lnheadimg, (receptors[note["x"]].x, y))
                else:'''
                window.blit(noteimg, (receptors[note["x"]].x, y))
        
        
        if note["time"] <= currenttime - (options.hitpos - 200) + 150 and note["time"] >= currenttime - (options.hitpos - 200) - 150:
            if note["type"] == "note" and not receptors[note["x"]].heldafter:
                if receptors[note["x"]].held:
                    if map[map.index(note)]:
                        map.pop(map.index(note))
                    receptors[note["x"]].heldafter = True
            elif note["type"] == "hold":
                if receptors[note["x"]].held:
                    
                    window.blit(lnobj, (receptors[note["x"]].x + (options.columnwidth/6), options.hitpos))
                    #window.blit(lntailimg, (receptors[note["x"]].x + (options.columnwidth/6), yLN - options.hitpos))
                    window.blit(lnheadimg, (receptors[note["x"]].x, options.hitpos))
                    
                    
                    
                    
                    
        
    if len(map) == 0:
        mapend = font.render("MAP COMPLETED", True, pygame.Color('green'))
        window.blit(mapend, (options.columnoffset, options.screen_height/2))
    
    fps = font.render("FPS: " + str(int(clock.get_fps())), True, pygame.Color('white'))
    objects = font.render("OBJECTS LEFT: " + str(len(map)), True, pygame.Color('white'))
    window.blit(fps, (50, 50))
    window.blit(objects, (50, 100))  
    
    pygame.display.update()
    dt = clock.tick(options.fps)
    currenttime += dt