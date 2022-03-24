# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
THRUST_FRACT = 0.5
FRICTION = 0.95
score = 0
lives = 3
time = 0
started = False
rock_group = set([])
missile_group = set([])
explosion_group = set([])
started = False

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
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

#Process Sprite Group Helper Function
def process_sprite_group(sprite_set, canvas):
    for sprite in set(sprite_set):
        sprite.draw(canvas)
        if sprite.update():
            sprite_set.remove(sprite)
        else:
            sprite.update()
        
#Group Collide Helper Function
def group_collide(sprite_set, other_object):
    for sprite in set(sprite_set):
        if sprite.collide(other_object):
            sprite_set.remove(sprite)
            new_explosion = Sprite(sprite.get_position(), [0, 0], 0, 0.025, explosion_image, explosion_info) 
            explosion_group.add(new_explosion)
            explosion_sound.rewind()
            explosion_sound.play()
            return True
        else:
            return False
        
# Group Group Collide Helper Function
def group_group_collide(sprite_set1, sprite_set2):
    score_num = 0
    for sprite1 in set(sprite_set1):
        if group_collide(sprite_set2, sprite1):
            score_num += 1
            sprite_set1.remove(sprite1)
        
    return score_num

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        
        if self.thrust:
            canvas.draw_image(self.image, [135, 45], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle) 
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        self.angle += self.angle_vel
        
        if self.thrust:
            forward_vect = angle_to_vector(self.angle)
            
            self.vel[0] += THRUST_FRACT*forward_vect[0]
            self.vel[1] += THRUST_FRACT*forward_vect[1]
        
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        
        self.vel[0] *= FRICTION
        self.vel[1] *= FRICTION
        
    
    def shoot(self):
        global missile_group
        
        forward = angle_to_vector(self.angle)
        pos = [self.pos[0] + self.radius*forward[0], self.pos[1] + self.radius*forward[1]]
        vel = [self.vel[0] + 4*forward[0], self.vel[1] + 4*forward[1]]
        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)
        
        missile_group.add(a_missile)

    def incr_angle_vel(self):
        self.angle_vel += 0.05
    
    def decr_angle_vel(self):
        self.angle_vel -= 0.05
       
    def thrusters(self):
        if self.thrust:
            self.thrust = False
            ship_thrust_sound.rewind()
        else:
            self.thrust = True
            ship_thrust_sound.play()
            
        
    
    
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
   
    def draw(self, canvas):
        if self.animated:
            change = self.age * self.image_center[0]
            new_center = [self.image_center[0] + change, self.image_center[1]]
            canvas.draw_image(self.image, new_center, self.image_size, self.pos, self.image_size, self.angle) 
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle) 
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def update(self):
        self.age += 1
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]  
        
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        
        if self.age < self.lifespan:
            return False
        else:
            return True
        
    def collide(self, other_object):
        self_pos = self.get_position()
        self_rad = self.radius
        other_pos = other_object.get_position()
        other_rad = other_object.radius
        
        distance = dist(self_pos, other_pos)
        if distance < (self_rad + other_rad):
            return True
        else:
            return False
        
        


# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.rewind()
        soundtrack.play()

def draw(canvas):
    global time, collision, lives, score, started, missile_group, rock_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    #a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    #a_missile.update()
    
    #draw and update sprite sets
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    #Update Score
    score += group_group_collide(missile_group, rock_group)
    
    #Draw Ship-Sprite Collisions
    if group_collide(rock_group, my_ship):
        lives -= 1
        
    if lives <= 0:
        started = False
        lives = 3
        score = 0
        rock_group = set([])
        missile_group = set([])
        soundtrack.pause()
    
        
        
    # Draw Lives and Score AFTER Sprites/Ship so that Lives/Score is always viewable
    canvas.draw_text("Lives", [50, 50], 22, "White", 'monospace')
    canvas.draw_text("Score", [680, 50], 22, "White", 'monospace')
    canvas.draw_text(str(lives), [50, 80], 22, "White", 'monospace')
    canvas.draw_text(str(score), [680, 80], 22, "White", 'monospace')
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
#Key Up/Down Handlers
def keydown(key):
    global my_ship
    
    if key == simplegui.KEY_MAP["left"]:
        my_ship.decr_angle_vel()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.incr_angle_vel()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrusters()
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    


def keyup(key):
    global my_ship
    
    if key == simplegui.KEY_MAP["left"]:
        my_ship.incr_angle_vel()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.decr_angle_vel()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrusters()
        

        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, my_ship
    
    if started and len(rock_group) < 12:
        pos = [random.randrange(50, WIDTH - 50),random.randrange(50, HEIGHT - 50)]
        vel = [random.randrange(-100, 100)/100.0,random.randrange(-100, 100)/100.0]
        angle_vel = random.randrange(0, 100)/1000.0

        a_rock = Sprite(pos,vel, 0, angle_vel, asteroid_image, asteroid_info)
        distance = dist(pos, my_ship.get_position())
        
        #Make sure rock doesn't spawn on top of ship
        if distance > 2*(my_ship.get_radius() + a_rock.get_radius()):
            rock_group.add(a_rock)
        


# initialize frame
frame = simplegui.create_frame("RiceRocks", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.025, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [0,0], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
                          
                          
# Testing
