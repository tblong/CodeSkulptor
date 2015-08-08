# @author TBLong
# @creation Jul 26, 2015
# @version Aug 2, 2015
#
# Rice rocks implementation with explosions

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
game_in_progress = False
MAX_ROCKS = 12

# Ship constants
SHIP_DIM = [90, 90]
SHIP_CEN = [SHIP_DIM[0] / 2, SHIP_DIM[1] / 2]
SHIP_RADUIS = 35
SHIP_ROCK_MIN_DISTANCE = SHIP_RADUIS * 4 # min rock spawn distance to ship allowed
SHIP_TURN_SPEED = 0.08 # in radians



class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo(SHIP_CEN, SHIP_DIM, SHIP_RADUIS)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrusting = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
		self.c = 0.02 # friction constant
		
	def turn(self, radians):
		self.angle_vel += radians
		
	def thrust(self, pressed):
		self.thrusting = pressed
		if self.thrusting:
			ship_thrust_sound.play()
		else:
			ship_thrust_sound.rewind()
			
	def shoot(self):
		mx = (self.pos[0] + (SHIP_CEN[0] * math.cos(self.angle))) % WIDTH   # missile x initial position
		my = (self.pos[1] + (SHIP_CEN[0] * math.sin(self.angle))) % HEIGHT   # missile y initial position
		forward = angle_to_vector(self.angle)
		mvx = self.vel[0] + (forward[0] * 8) # missile x velocity
		mvy = self.vel[1] + (forward[1] * 8) # missile y velocity
		
		missile_group.add(Sprite((mx, my), (mvx, mvy), 0, 0, missile_image, missile_info, missile_sound))
		
	def get_position(self):
		return self.pos
			
	def get_radius(self):
		return self.radius		

    def draw(self,canvas):
		if self.thrusting:
			canvas.draw_image(self.image, [SHIP_CEN[0] + SHIP_DIM[0], SHIP_CEN[0]], SHIP_DIM, self.pos, SHIP_DIM, self.angle)
		else:
			canvas.draw_image(self.image, SHIP_CEN, SHIP_DIM, self.pos, SHIP_DIM, self.angle)

    def update(self):
		# angle update
		self.angle += self.angle_vel
		# position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
		self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
		#friction update
		self.vel[0] *= (1 - self.c)
		self.vel[1] *= (1 - self.c)
		# acceleration update
		if self.thrusting:
			forward = angle_to_vector(self.angle)
			self.vel[0] += (forward[0] * .4)
			self.vel[1] += (forward[1] * .4)
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
			
	def get_position(self):
		return self.pos
			
	def get_radius(self):
		return self.radius
		
	def collide(self, obj):
		return dist(self.get_position(), obj.get_position()) < (self.get_radius() + obj.get_radius())
		
	def group_collide(sprites, obj):
		for s in set(sprites):
			if s.collide(obj):
				explosion_group.add(Sprite(s.get_position(), (0, 0), 0, 0, explosion_image, explosion_info, explosion_sound))
				sprites.remove(s)
				return True
		return False
		
	def group_group_collide(g1, g2):
		num_collisions = 0
		for s in set(g1):
			hit = Sprite.group_collide(g2, s)
			if hit:
				num_collisions += 1
				g1.discard(s)
		return num_collisions
		
   
    def draw(self, canvas):
		if self.animated:
			canvas.draw_image(self.image, [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
		else:
			canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
		# angle update
		self.angle += self.angle_vel
		# position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
		self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
		
		self.age += 1
		return self.age >= self.lifespan
        

           
def draw(canvas):
    global time, lives, score, game_in_progress, rock_group, missile_group, explosion_group
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship
	if game_in_progress:
		my_ship.draw(canvas)
		my_ship.update()
		
	# draw and update rocks
	process_sprite_group(canvas, rock_group)
	
	# draw missiles
	process_sprite_group(canvas, missile_group)
	
	# process explosions
	process_sprite_group(canvas, explosion_group)
		
	# did ship hit any rocks
	if Sprite.group_collide(rock_group, my_ship):
		lives -= 1
		
	# still alive?
	if lives <= 0:
		timer.stop()
		game_in_progress = False
		rock_group = set([])
		missile_group = set([])
		explosion_group = set([])
		my_ship.thrust(False)
		soundtrack.rewind()
		
	# missile/rock collisions
	score += Sprite.group_group_collide(missile_group, rock_group)
	
	# draw splash screen
	if not game_in_progress:
		canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), (WIDTH / 2, HEIGHT / 2), splash_info.get_size())
	
	# update score and lives
	canvas.draw_text("Lives", (40, 30), 20, "White", "sans-serif")
	canvas.draw_text(str(lives), (40, 50), 20, "White", "sans-serif")
	canvas.draw_text("Score", (WIDTH - 80, 30), 20, "White", "sans-serif")
	canvas.draw_text(str(score), (WIDTH - 80, 50), 20, "White", "sans-serif")
	
#
# draw then update all Sprite instances
#
def process_sprite_group(canvas, sprites):
	for s in set(sprites):
		s.draw(canvas)
		remove = s.update()
		if remove:
			sprites.remove(s)
		
# timer handler that spawns a rock
def rock_spawner():
	if game_in_progress and len(rock_group) < MAX_ROCKS:
		rock = make_rock()
		
		# only add rocks that are far enough away from the ship's position
		distance = dist(my_ship.get_position(), rock.get_position())
		if distance >= SHIP_ROCK_MIN_DISTANCE:
			rock_group.add(rock)
	
#
# rock maker, generates a random rock
#
def make_rock():
	# generate random position
	pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
	# generate random velocity
	vel_x = (random.randrange(5, 40) / 10.0) * random.choice([-1, 1])
	vel_y = (random.randrange(5, 40) / 10.0) * random.choice([-1, 1])
	# generate random angular velocity
	ang_vel = (random.randrange(3, 16) / 100.0) * random.choice([-1, 1])
		
	return Sprite(pos, (vel_x, vel_y), 0, ang_vel, asteroid_image, asteroid_info)
	
# 
# key handlers
#
def key_up(key):
	if my_ship == None or not game_in_progress:
		return
	
	if key in SHIP_KEYUP_CTRL:
		SHIP_KEYUP_CTRL[key](my_ship, False)
	
		
def key_down(key):
	if my_ship == None or not game_in_progress:
		return
		
	if key in SHIP_KEYDN_CTRL:
		SHIP_KEYDN_CTRL[key](my_ship, True)

		
#
# mouse handler
#
def mouse_handler(pos):
	global game_in_progress, score, lives, my_ship
	
	if not game_in_progress:
		if abs( (WIDTH / 2) - pos[0]) < splash_info.get_center()[0]: # test x position
			if abs((HEIGHT / 2) - pos[1]) < splash_info.get_center()[1]: # test y position
				# init new game
				my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
				game_in_progress = True
				score = 0
				lives = 3
				timer.start()
				soundtrack.play()
		
# 
# ship controls, these called by appropriate key handler
#
def turn_left(ship, pressed):
	if pressed:
		ship.turn(-SHIP_TURN_SPEED)
	else:
		ship.turn(SHIP_TURN_SPEED)
	
def turn_right(ship, pressed):
	if pressed:
		ship.turn(SHIP_TURN_SPEED)
	else:
		ship.turn(-SHIP_TURN_SPEED)
		
def ship_thrust(ship, pressed):
	ship.thrust(pressed)
	
def fire_missile(ship, pressed):
	ship.shoot() 
	
#
# ship control maps
#
SHIP_KEYDN_CTRL = {simplegui.KEY_MAP["left"]: turn_left, 
									simplegui.KEY_MAP["right"]: turn_right, 
									simplegui.KEY_MAP["up"]: ship_thrust, 
									simplegui.KEY_MAP["space"]: fire_missile}
SHIP_KEYUP_CTRL = {simplegui.KEY_MAP["left"]: turn_left, 
									simplegui.KEY_MAP["right"]: turn_right, 
									simplegui.KEY_MAP["up"]: ship_thrust}
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register key up/down handlers
frame.set_keyup_handler(key_up)
frame.set_keydown_handler(key_down)

# mouse handler to start game
frame.set_mouseclick_handler(mouse_handler)

# initialize ship and sprite groups
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()