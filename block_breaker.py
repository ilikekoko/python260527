import random
import tkinter as tk

WIDTH = 600
HEIGHT = 500
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_SIZE = 14
BRICK_ROWS = 5
BRICK_COLUMNS = 8
BRICK_WIDTH = 65
BRICK_HEIGHT = 20
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 50
BRICK_OFFSET_LEFT = 30

class l:
    def __init__(self, root):
        self.root = root
        self.root.title("Block Breaker")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#111")
        self.canvas.pack()

        self.score = 0
        self.lives = 3
        self.game_over = False
        self.ball_speed = 5

        self.create_paddle()
        self.create_ball()
        self.create_bricks()
        self.create_text()

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<KeyRelease-Left>", self.stop_moving)
        self.root.bind("<KeyRelease-Right>", self.stop_moving)

        self.paddle_move_x = 0
        self.update()

    def create_paddle(self):
        start_x = (WIDTH - PADDLE_WIDTH) / 2
        start_y = HEIGHT - 40
        self.paddle = self.canvas.create_rectangle(
            start_x, start_y, start_x + PADDLE_WIDTH, start_y + PADDLE_HEIGHT,
            fill="#45aaf2", outline="#89c4f4"
        )

    def create_ball(self):
        center_x = WIDTH / 2
        center_y = HEIGHT / 2
        self.ball = self.canvas.create_oval(
            center_x - BALL_SIZE / 2, center_y - BALL_SIZE / 2,
            center_x + BALL_SIZE / 2, center_y + BALL_SIZE / 2,
            fill="#feca57", outline="#ff9f43"
        )
        self.ball_dx = random.choice([-self.ball_speed, self.ball_speed])
        self.ball_dy = -self.ball_speed

    def create_bricks(self):
        self.bricks = []
        colors = ["#ff6b6b", "#ff9f1a", "#54a0ff", "#1dd1a1", "#f368e0"]

        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLUMNS):
                x1 = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
                y1 = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
                x2 = x1 + BRICK_WIDTH
                y2 = y1 + BRICK_HEIGHT
                brick = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=colors[row % len(colors)], outline="#222"
                )
                self.bricks.append(brick)

    def create_text(self):
        self.score_text = self.canvas.create_text(
            70, 20, text=f"Score: {self.score}", fill="#fff", font=("Arial", 14, "bold")
        )
        self.lives_text = self.canvas.create_text(
            WIDTH - 90, 20, text=f"Lives: {self.lives}", fill="#fff", font=("Arial", 14, "bold")
        )
        self.message_text = self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2, text="", fill="#ffffff", font=("Arial", 24, "bold")
        )

    def move_left(self, event):
        self.paddle_move_x = -8

    def move_right(self, event):
        self.paddle_move_x = 8

    def stop_moving(self, event):
        self.paddle_move_x = 0

    def update(self):
        if not self.game_over:
            self.move_paddle()
            self.move_ball()
            self.check_collisions()
            self.update_text()

        self.root.after(16, self.update)

    def move_paddle(self):
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)
        new_x1 = x1 + self.paddle_move_x
        new_x2 = x2 + self.paddle_move_x

        if new_x1 < 0:
            new_x1 = 0
            new_x2 = PADDLE_WIDTH
        elif new_x2 > WIDTH:
            new_x2 = WIDTH
            new_x1 = WIDTH - PADDLE_WIDTH

        self.canvas.coords(self.paddle, new_x1, y1, new_x2, y2)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        x1, y1, x2, y2 = self.canvas.coords(self.ball)

        if x1 <= 0 or x2 >= WIDTH:
            self.ball_dx *= -1
        if y1 <= 0:
            self.ball_dy *= -1

        if y2 >= HEIGHT:
            self.lose_life()

    def check_collisions(self):
        ball_coords = self.canvas.coords(self.ball)
        overlapping = self.canvas.find_overlapping(*ball_coords)

        for item in overlapping:
            if item == self.paddle:
                self.ball_dy = -abs(self.ball_dy)
                paddle_coords = self.canvas.coords(self.paddle)
                paddle_center = (paddle_coords[0] + paddle_coords[2]) / 2
                ball_center = (ball_coords[0] + ball_coords[2]) / 2
                offset = (ball_center - paddle_center) / (PADDLE_WIDTH / 2)
                self.ball_dx = self.ball_speed * offset
                break

        for brick in list(self.bricks):
            if brick in overlapping:
                self.bricks.remove(brick)
                self.canvas.delete(brick)
                self.ball_dy *= -1
                self.score += 10
                break

        if not self.bricks:
            self.win_game()

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.end_game("Game Over")
        else:
            self.reset_ball()

    def reset_ball(self):
        self.canvas.coords(
            self.ball,
            WIDTH / 2 - BALL_SIZE / 2,
            HEIGHT / 2 - BALL_SIZE / 2,
            WIDTH / 2 + BALL_SIZE / 2,
            HEIGHT / 2 + BALL_SIZE / 2,
        )
        self.ball_dx = random.choice([-self.ball_speed, self.ball_speed])
        self.ball_dy = -self.ball_speed

    def win_game(self):
        self.end_game("You Win!")

    def end_game(self, text):
        self.game_over = True
        self.canvas.itemconfig(self.message_text, text=text)

    def update_text(self):
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    BrickBreakerGame(root)
    root.mainloop()
