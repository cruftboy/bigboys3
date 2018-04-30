vector = [0, 0]
coords = [[-1, -1], [-1, -1]] #2 frames, init state
sim_coords = [0,0]
sim_resp = [0,0]
sim_resp2 = [0,0]
y_goto = 0
chosen_y = False
sim_hit = [0,0]
flipped = False
feature_store = []

table_size = (440, 280)
ball_size = (15, 15)
paddle_bounce = 1.2
wall_bounce = 1.00
dust_error = 0.00
init_speed_mag = 2

enemy_p = [-1,-1]


import operator


import random
import math

import numpy as np

import PongAIvAI as p

def pong_trainerRIGHT(a,b,c,d):
	global vector
	global coords
	global sim_coords
	global sim_resp
	global y_goto
	global chosen_y
	global sim_hit
	global flipped
	global rand

	global table_size
	global ball_size
	global paddle_bounce
	global wall_bounce
	global dust_error
	global init_speed_mag

	global en_pad
	global ball
	global f_pad

	global enemy_p

	if coords[0] == [-1, -1] and coords[1] == [-1, -1]:#if init state
		coords[0] = [c.pos[0], c.pos[1]]


	elif coords[1] == [-1, -1]: #if 2nd state
		coords[1] = [c.pos[0], c.pos[1]]

	else:
		coords[0] = coords[1]
		coords[1] = [c.pos[0], c.pos[1]]
	#generage 2 frames of coords
	vector[0] = coords[1][0] - coords[0][0]
	vector[1] = coords[1][1] - coords[0][1]
	#create vector

	if enemy_p == [-1,-1]:
		enemy_p[0] = b.pos[1]

	elif enemy_p[1] == [-1]:
		enemy_p[1] = b.pos[1]

	else:
		enemy_p[0] = enemy_p[1]
		enemy_p[1] = b.pos[1]

	enemy_dir = enemy_p[1] - enemy_p[0]

	feature_store.append([coords[1][0], coords[1][0], vector[0], vector[1], a.pos[1], b.pos[1]])

	ball = p.Ball(table_size, ball_size, paddle_bounce, wall_bounce, dust_error, init_speed_mag)
	f_pad = p.Paddle(a.pos, a.size, 1, 45,  1, 0.0003)
	if vector[0] > 0:
		
		sim_coords = [c.pos[0], c.pos[1]]
		dx = vector[0]
		dy = vector[1]
		while sim_coords[0] < 420:
			if sim_coords[1] < 0:	
				dy = -dy
			elif sim_coords[1] > 280:
				dy = -dy
			else:
				pass	
			sim_coords[0] += dx
			sim_coords[1] += dy

		if chosen_y == False:
			distances = {}
			sim_hit = sim_coords
			for i in range(round(sim_coords[1])-60,round(sim_coords[1])-10):
				theta = f_pad.get_angle(ball.frect.pos[1]+.5*ball.frect.size[1])
				v = vector
				v = [math.cos(theta)*v[0]-math.sin(theta)*v[1], math.sin(theta)*v[0]+math.cos(theta)*v[1]]
				v[0] = -v[0]
				v = [math.cos(-theta)*v[0]-math.sin(-theta)*v[1], math.cos(-theta)*v[1]+math.sin(-theta)*v[0]]
				dy_s = v[1]
				dx_s = v[0]
				while sim_hit[0] < 0:
					if sim_hit[1] < 0:	
						dy_s = -dy_s
					elif sim_hit[1] > 280:
						dy_s = -dy_s

					sim_hit[0] += dy_s
					sim_hit[1] += dx_s
				dist =  abs(sim_hit[1] - b.pos[1])
				predictable = abs(vector[1]) + abs(vector[0]) < 3
				distances[sim_hit[1]] = [dist, predictable]
			else:
				y_goto = max(distances)

		if a.pos[1] > y_goto:
			return 'up'
		elif a.pos[1] < y_goto:
			return 'down'
		else:
			pass
	else:
		en_pad = p.Paddle(b.pos, b.size, 1, 45,  1, 0.0003)
		sim_resp = [c.pos[0], c.pos[1]]
		dx2 = vector[0]
		dy2 = vector[1]
		while sim_resp[0] > 20:
			if sim_resp[1] <= 0 or sim_resp[1] >= 280:	
				dy2 = -dy2
			else:
				pass	

			sim_resp[0] += dx2
			sim_resp[1] += dy2
		

		sim_resp2 = sim_resp

		
		theta = en_pad.get_angle(sim_resp[1]+.5*ball.frect.size[1])
		v = vector
		v = [math.cos(theta)*v[0]-math.sin(theta)*v[1], math.sin(theta)*v[0]+math.cos(theta)*v[1]]
		v[0] = -v[0]
		v = [math.cos(-theta)*v[0]-math.sin(-theta)*v[1], math.cos(-theta)*v[1]+math.sin(-theta)*v[0]]
		
		vector = v

		dy3 = v[1]
		dx3 = abs(v[0])

		while dx3 <= 0.1:
			dx3 *= 10
			dy3 *= 10
		while sim_resp2[0] < 420:
			if sim_resp2[1] <= 0 or sim_resp2[1] >= 280:	
				dy3 = -dy3
			else:
				pass

			sim_resp2[0] += dx3
			sim_resp2[1] += dy3
		if a.pos[1] > sim_resp2[1]:
			return "up"
		elif a.pos[1] < sim_resp2[1]:
			return "down"
		else:
			pass


def pong_chaser(a,b,c,d):
	if a.pos[1] + a.size[1]/2 < (c.pos[1] + c.size[1]/2):
		return "down"
	else:
		return  "up"

def pong_ai(a,b,c,d):
	pass

def test():
	img = p.getPixels()
	print(img)