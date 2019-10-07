import sys, logging, os, random, open_color, arcade

version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)




SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Particle Exercise"

PARTICLE_MIN_SCALE = 0.01
PARTICLE_MAX_SCALE = 0.08
PARTICLE_MIN_X = -20
PARTICLE_MAX_X = 20
PARTICLE_VELOCITY_X = 0
PARTICLE_VELOCITY_Y = 4
PARTICLE_MIN_AX = -0.1
PARTICLE_MAX_AX = 0.1
PARTICLE_MIN_AY = -0.1
PARTICLE_MAX_AY = 0.1
PARTICLE_MIN_DECAY = 0.001
PARTICLE_MAX_DECAY = 0.01


class Particle(arcade.Sprite):
    def __init__(self, asset, scale, x, y, dx, dy, ax, ay, decay):
        super().__init__("assets/{}.png".format(asset), scale)
        self.center_x = x
        self.center_y = y
        self.dx = dx
        self.dy = dy
        self.ax = ax
        self.ay = ay
        self.decay = decay
        self.color_pos = 0

        self.particle_colors = [
            (open_color.red_5, 4)
            ,(open_color.red_4, 5)
            ,(open_color.red_3, 6)
            ,(open_color.red_2, 7)
            ,(open_color.red_1, 8)
            ,(open_color.teal_1, 8)
            ,(open_color.teal_2, 7)
            ,(open_color.teal_3, 6)
            ,(open_color.teal_4, 5)
            ,(open_color.teal_5, 4)
        ]
        (self.color, self.lifetime) = self.particle_colors[self.color_pos]
        self.alive = True
        
    
    def update(self):
        self.dx += self.ax
        self.dy += self.ay
        self.center_x += self.dx
        self.center_y += self.dy
        self.scale -= self.decay
        if self.scale < self.decay:
            self.scale = self.decay
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.color_pos += 1
            if self.color_pos >= len(self.particle_colors):
                self.alive = False
            else:
                (self.color, self.lifetime) = self.particle_colors[self.color_pos]




        


class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)

        arcade.set_background_color(open_color.black)

        self.particle_list = arcade.SpriteList()
        self.mouse_down = False
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2

    def setup(self):
        pass

    def update(self, delta_time):
        self.particle_list.update()
        if self.mouse_down:
            #generate a new particle
            x = self.x + random.uniform(PARTICLE_MIN_X, PARTICLE_MAX_X)
            y = self.y
            dx = PARTICLE_VELOCITY_X
            dy = PARTICLE_VELOCITY_Y
            ax = random.uniform(PARTICLE_MIN_AX,PARTICLE_MAX_AX)
            ay = random.uniform(PARTICLE_MIN_AY,PARTICLE_MAX_AY)
            decay = random.uniform(PARTICLE_MIN_DECAY,PARTICLE_MAX_DECAY)
            scale = random.uniform(PARTICLE_MIN_SCALE,PARTICLE_MAX_SCALE)
            #Particle(asset, sprite scale, initial position [x], initial position [y], velocity [x], velocity [y], acceleration [x], acceleration [y], scale decay)
            particle = Particle('circle_05',scale,x,y,dx,dy,ax,ay,decay)

            self.particle_list.append(particle)

        for p in self.particle_list:
            #if the particle is off the edge of the screen, kill it
            if p.center_x < -50 or p.center_x > SCREEN_WIDTH + 50 or p.center_y < -50 or p.center_y > SCREEN_HEIGHT + 50:
                p.kill()
            #if it has reached the end of its life
            if not p.alive:
                p.kill


    def on_draw(self):
        arcade.start_render()
        self.particle_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.x = x
        self.y = y
        self.mouse_down = True

    def on_mouse_release(self, x, y, button, modifiers):
        self.x = x
        self.y = y
        self.mouse_down = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.x = x
        self.y = y


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()