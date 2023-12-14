from tkinter import *
import time
import tkinter
import random
import tkinter.messagebox
import pygame
from pygame.locals import *

root = tkinter.Tk()
root.resizable(0, 0)
canvas = Canvas(root, width=1200, height=800, bg="black")

class Obstacle:
    def __init__(self, canvas, color, size):
        self.canvas = canvas
        self.color = color
        self.size = size
        self.speed = random.uniform(1, 4)
        initial_positions = [(0, random.randint(0, 800), 1, 0),
                             (1200, random.randint(0, 800), -1, 0),
                             (random.randint(0, 1200), 0, 0, 1),
                             (random.randint(0, 1200), 800, 0, -1)]
        self.x, self.y, self.x_direction, self.y_direction = random.choice(initial_positions)
        self.obstacle_id = canvas.create_oval(self.x, self.y, self.x + size, self.y + size, fill=color)

    def move(self):
        self.x += self.x_direction * self.speed
        self.y += self.y_direction * self.speed
        if self.x > 1200 or self.x + self.size < 0 or self.y > 800 or self.y + self.size < 0:
            self.reset_position()
        self.canvas.coords(self.obstacle_id, self.x, self.y, self.x + self.size, self.y + self.size)

    def reset_position(self):
        initial_positions = [(0, random.randint(0, 800), 1, 0),
                             (1200, random.randint(0, 800), -1, 0),
                             (random.randint(0, 1200), 0, 0, 1),
                             (random.randint(0, 1200), 800, 0, -1)]
        self.x, self.y, self.x_direction, self.y_direction = random.choice(initial_positions)

class things:
    def __init__(self, x, y, size_x, size_y, color):
        self.x, self.y = x, y
        self.size_x, self.size_y = size_x, size_y
        self.color = color
        self.x_accel, self.y_accel = 0, 0
        players.add(self)
        self.id = canvas.create_rectangle(x, y, x + self.size_x, y + self.size_y, fill=self.color, width=0)

    def move(self):
        x_value, y_value = self.x_accel, self.y_accel
        if x_value != 0 or y_value != 0:
            if canvas.coords(self.id)[0] + x_value < 0:
                x_value = -canvas.coords(self.id)[0]
                self.x_accel = -self.x_accel

            if canvas.coords(self.id)[1] + y_value < 0:
                y_value = -canvas.coords(self.id)[1]
                self.y_accel = -self.y_accel

            if canvas.coords(self.id)[2] + x_value > 1200:
                x_value = 1200 - canvas.coords(self.id)[2]
                self.x_accel = -self.x_accel

            if canvas.coords(self.id)[3] + y_value > 800:
                y_value = 800 - canvas.coords(self.id)[3]
                self.y_accel = -self.y_accel

            canvas.move(self.id, x_value, y_value)
            self.x_accel -= self.x_accel / 100
            self.y_accel -= self.y_accel / 100

    def check_collision(self):
        player_coords = canvas.coords(self.id)
        for obstacle in obstacles:
            obstacle_coords = canvas.coords(obstacle.obstacle_id)

            if (
                player_coords[0] < obstacle_coords[2]
                and player_coords[2] > obstacle_coords[0]
                and player_coords[1] < obstacle_coords[3]
                and player_coords[3] > obstacle_coords[1]
            ):
                global current_width
                current_width -= 5
                canvas.coords(rectangle, 0, 0, current_width, 50)
                collision_sound.play()
                break

        if random_rectangle:
            random_rectangle_coords = canvas.coords(random_rectangle)

            if (
                len(random_rectangle_coords) == 4  
                and player_coords[0] < random_rectangle_coords[2]
                and player_coords[2] > random_rectangle_coords[0]
                and player_coords[1] < random_rectangle_coords[3]
                and player_coords[3] > random_rectangle_coords[1]
            ):
                current_width += 30
                canvas.coords(rectangle, 0, 0, current_width, 50)
                canvas.delete(random_rectangle)
                collision_sound1.play()
                
class Game:
    global players
    players = set()
    def __init__(self):
        self.keys = set()
        self.timer_seconds = 25
        self.timer_label = Label(root, text=f"Time: {self.timer_seconds}s", font=("Helvetica", 16), fg="white", bg="black")
        self.timer_label.place(x=1000, y=10)
        self.stage_count = 2
        self.update_timer()
        self.clock = pygame.time.Clock()
        self.stage1_show()
        
        player = things(320, 320, 20, 20, "white")
        root.bind("<KeyPress>", self.keyPress)
        root.bind("<KeyRelease>", self.keyRelease)
        self.show_start_message()
        while True:
            for key in self.keys:
                if key == "Left" and player.x_accel > -10:
                    player.x_accel -= 1
                if key == "Right" and player.x_accel < 10:
                    player.x_accel += 1
                if key == "Up" and player.y_accel > -10:
                    player.y_accel -= 1
                if key == "Down" and player.y_accel < 10:
                    player.y_accel += 1
                    
            for obj in players.copy():
                obj.move()
                obj.check_collision()
            self.clock.tick(60) 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            root.update()
            time.sleep(0.0001)

    def keyPress(self, event):
        self.keys.add(event.keysym)

    def keyRelease(self, event):
        if event.keysym in self.keys:
            self.keys.remove(event.keysym)

    def update_timer(self):
        self.timer_seconds -= 1
        self.timer_label.config(text=f"Time: {self.timer_seconds}s")
        if self.timer_seconds > 0:
            root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time's up!")
            self.pause_game()
    def pause_game(self):
        if self.stage_count <4:
            root.after(1000, self.show_message_box)
        elif self.stage_count == 4:
            self.end_game()
    
    def stage1_show(self):
        self.stage_label = tkinter.Label(root, text = 'STAGE : 1' , font=("Helvetica", 16), fg="white",bg="black")
        self.stage_label.place(x=400,y=10)

    def stage_show(self):
        self.stage_label = tkinter.Label(root, text = 'STAGE : {}'.format(self.stage_count) , font=("Helvetica", 16), fg="white",bg="black")
        self.stage_label.place(x=400,y=10)

    def show_message_box(self):
        result = tkinter.messagebox.showinfo("Game Paused", f"{self.stage_count} 스테이지로 넘어갑니다.\n 난이도가 올라갑니다")
        if result == "ok":
            if self.stage_count < 4:
                self.stage_show()  
                self.stage_count += 1
                self.restart_game()

    def end_game(self):
        result = tkinter.messagebox.showinfo('알림',"모든 스테이지를 클리어 했습니다.")
        if result == "ok":
            root.destroy() 

    def restart_game(self):
        self.timer_seconds = 25
        self.timer_label.config(text=f"Time: {self.timer_seconds}s")
        self.update_timer()

    def show_start_message(self):
        message = "방향키를 통해 장애물로부터 살아 남으세요!!\n tip) 노란 사각형은 도움이 될겁니다."
        result = tkinter.messagebox.showinfo("게임 시작 안내", message)

def fade_out():
    global current_width
    current_width = canvas.coords(rectangle)[2] - canvas.coords(rectangle)[0]
    new_width = current_width - 1

    if new_width > 0:
        canvas.coords(rectangle, 0, 0, new_width, 50)
        label_text = f'HP: {new_width}'
        label.config(text=label_text)
        root.after(250, fade_out)
    else:
        result = tkinter.messagebox.showinfo('알림',"게임 클리어에 실패했습니다.")
        if result == "ok":
            root.destroy()

def create_random_rectangle():
    global random_rectangle
    x1 = random.randint(0, 1100)
    y1 = random.randint(0, 700)
    x2 = x1 + random.randint(50, 100)
    y2 = y1 + random.randint(50, 100)
    random_rectangle = canvas.create_rectangle(x1, y1, x2, y2, fill="yellow")
    root.after(1500, lambda: canvas.delete(random_rectangle))
    root.after(5000, create_random_rectangle)

def create_obstacles():
    obstacle = Obstacle(canvas, "red", 15)
    obstacles.append(obstacle)
    root.after(2500, create_obstacles)

def move_obstacles():
    for obstacle in obstacles.copy():
        obstacle.move()
    root.after(10, move_obstacles)

label = tkinter.Label(root, text = 'HP', font=("Helvetica", 16), fg="yellow",bg="black")
obstacles = []
random_rectangle = None  
current_width = 150 
root.update()
img=tkinter.PhotoImage(file="space.png")
canvas.create_image(600,400,image = img)
create_random_rectangle()
rectangle = canvas.create_rectangle(5, 5, 150, 50, fill="green")
fade_out()
create_obstacles()
move_obstacles()
canvas.pack()
pygame.init()
bgm_file_path = "your_bgm_file.ogg"
collision_sound_path = "8bit_shoot4.mp3"
collision_sound_path1 = "powerup05.mp3"
collision_sound = pygame.mixer.Sound(collision_sound_path)
collision_sound1 = pygame.mixer.Sound(collision_sound_path1)
pygame.mixer.music.load(bgm_file_path)
pygame.mixer.music.play(-1)
label.place(x=151,y=5)
Game()






















