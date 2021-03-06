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
        
        #P1.6
        if self.thrust:
            canvas.draw_image(self.image, [135, 45], self.image_size, self.pos, self.image_size, self.angle)
        else:
            #P1.1
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle) 
        
        
    def update(self):
        #P1.2
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        #P1.3
        self.angle += self.angle_vel
        
        if self.thrust:
            #P1.8
            forward_vect = angle_to_vector(self.angle)
            
            #P1.9
            self.vel[0] += THRUST_FRACT*forward_vect[0]
            self.vel[1] += THRUST_FRACT*forward_vect[1]
        
        #P1.10
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        
        #P1.11
        self.vel[0] *= FRICTION
        self.vel[1] *= FRICTION
        
    
    def shoot(self):
        #P3.1
        global a_missile
        
        forward = angle_to_vector(self.angle)
        pos = [self.pos[0] + self.radius*forward[0], self.pos[1] + self.radius*forward[1]]
        vel = [self.vel[0] + 4*forward[0], self.vel[1] + 4*forward[1]]
        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)


            

        

            
            
    
    #P1.4
    def incr_angle_vel(self):
        self.angle_vel += 0.05
    
    #P1.4
    def decr_angle_vel(self):
        self.angle_vel -= 0.05
    
    #P1.5    
    def thrusters(self):
        if self.thrust:
            self.thrust = False
            
            #P1.7
            ship_thrust_sound.rewind()
        else:
            self.thrust = True
            
            #P1.7
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
   
    #P2.1
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle) 
    
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]       

           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Score: "+str(score), [150, 50], 30, 'White', 'monospace')
    canvas.draw_text("Lives: "+str(lives), [WIDTH - 275, 50], 30, 'White', 'monospace')

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
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
    #P2.2
    global a_rock
    
    pos = [random.randrange(50, WIDTH - 50),random.randrange(50, HEIGHT - 50)]
    vel = [random.randrange(-100, 100)/100.0,random.randrange(-100, 100)/100.0]
    angle_vel = random.randrange(0, 100)/1000.0
    
    a_rock = Sprite(pos,vel, 0, angle_vel, asteroid_image, asteroid_info)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.025, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
                          
                          
# Testing

