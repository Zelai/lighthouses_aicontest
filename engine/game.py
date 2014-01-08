#!/usr/bin/python
# -*- coding: utf-8 -*

import sys, time
import engine, botplayer
import view

cfg_file = sys.argv[1]
bots = sys.argv[2:]
DEBUG = False

config = engine.GameConfig(cfg_file)
game = engine.Game(config, len(bots))
actors = [botplayer.BotPlayer(game, i, cmdline, debug=DEBUG) for i, cmdline in enumerate(bots)]

for actor in actors:
    actor.initialize()

view = view.GameView(game)

# Para parametrizar número de jugadas 
# y si se ejecuta de continuo o hay pausas entre jugadas
# Creado con las siguientes lineas:
	# v={"rounds":10, "pausa":1}
	# f=open("modo.txt","w")
	# f.write(str(v))
	# f.close()
# modo.txt variables:
#  rounds = numero de rondas (-1 = infinito)
#  pausa = 1 para pausa, 0 para no.

f = open('modo.txt','r')
modo= eval(f.read())
f.close()

round = 0
#while True:
while round < modo['rounds'] or modo['rounds'] == -1:
    game.pre_round()
    view.update()
    for actor in actors:
        actor.turn()
        view.update()
    game.post_round()
    print "########### ROUND %d SCORE:" % round,
    for i in range(len(bots)):
        print "P%d: %d" % (i, game.players[i].score),
    print
    round += 1
    if modo['pausa'] == 1:
	print "Pulsa intro para continuar\n"
	sys.stdin.read(1)

view.update()
