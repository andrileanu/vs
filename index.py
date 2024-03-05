import pygame
import random
import sys

# Initialize Pygame
pygame.init()

image = pygame.image.load('img/main.png')
# Screen setup
states = {
    "happy": pygame.Rect(45, 110, 183, 232),  
    "ecstatic": pygame.Rect(270, 110, 183, 232),  
    "maniac": pygame.Rect(495, 110, 183, 232),  
    "sad": pygame.Rect(45, 489, 183, 232),  
    "depressed": pygame.Rect(270, 489, 183, 232),  
    "miserable": pygame.Rect(495, 489, 183, 232),  
    "angry": pygame.Rect(45, 875, 183, 232),  
    "enraged": pygame.Rect(270, 875, 183, 232),  
    "furious": pygame.Rect(495, 875, 183, 232),  
}
cropped_states = {state: image.subsurface(rect) for state, rect in states.items()}

screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.flip()
pygame.display.set_caption("Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font setup
font = pygame.font.Font(None, 36)

# Function to render text
def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def show_state_at_bottom(screen, state_image):
    screen_height = screen.get_height()
    image_height = state_image.get_height()
    
    y_position = screen_height - image_height
    
    screen_width = screen.get_width()
    image_width = state_image.get_width()
    x_position = (screen_width - image_width) // 2

    screen.blit(state_image, (x_position, y_position))
    pygame.display.flip()  # Update the screen to display changes


class Player:
    def __init__(self, name):
        self.name = name
        self.social_credits = 0
        self.money = 1000

    def choose(self):
        self.potential_credits = random.randint(400, 700)
        if self.name == "AI":
            return random.choice(['yes', 'no'])
        else:
            decision = None
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            decision = 'yes'
                        elif event.key == pygame.K_n:
                            decision = 'no'
                if decision:
                    return decision
                else:
                    screen.fill(BLACK)
                    draw_text(f"{self.name}, ${self.potential_credits}, 'Y' for yes or 'N' for no?", 100, 50)
                    show_state_at_bottom(screen, cropped_states["happy"])
                    pygame.display.flip()

def play_game():
    player1 = Player("You")
    player2 = Player("AI")

    for i in range(1, 11):
        decision1 = player1.choose()
        decision2 = player2.choose()

        if decision1 == 'yes' and decision2 == 'yes':
            player1.money += player1.potential_credits
            player1.social_credits += 3
            player2.money += player1.potential_credits
            player2.social_credits += 3
            show_state_at_bottom(screen, cropped_states["enraged"])
        elif decision1 == 'no' and decision2 == 'no':
            player1.social_credits += 1
            player2.social_credits += 1
            show_state_at_bottom(screen, cropped_states["angry"])
        elif decision1 == 'yes' and decision2 == 'no':
            player1.money += player1.potential_credits
            player2.money -= player1.potential_credits
            player2.social_credits += 5
            show_state_at_bottom(screen, cropped_states["maniac"])
        elif decision1 == 'no' and decision2 == 'yes':
            player1.money -= player2.potential_credits
            player2.money += player2.potential_credits
            player1.social_credits += 5
            show_state_at_bottom(screen, cropped_states["ecstatic"])

        # Inside your game loop
        

        # After processing decisions, display the outcome
        
        draw_text(f"Round {i}: You chose {decision1}, AI chose {decision2}", 100, 100)
        draw_text(f"Your money: {player1.money}, Your credits: {player1.social_credits}", 100, 140)
        draw_text(f"AI money: {player2.money}, AI credits: {player2.social_credits}", 100, 180)
        

        pygame.display.flip()
        waiting_for_user = True
        while waiting_for_user:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_user = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting_for_user = False

    # Final standings display
    screen.fill(BLACK)
    draw_text("Game Over!", 100, 100)
    draw_text(f"Final You: Money - ${player1.money}, Credits - {player1.social_credits}", 100, 140)
    draw_text(f"Final AI: Money - ${player2.money}, Credits - {player2.social_credits}", 100, 180)
    draw_text("Press ESC to exit", 100, 220, color=(255,165,0))  # Orange color for the exit instruction
    pygame.display.flip()

    waiting_for_user = True
    while waiting_for_user:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_user = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting_for_user = False

    pygame.quit()

if __name__ == "__main__":
    play_game()
    pygame.quit()
