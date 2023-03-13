import pygame
import random
import time

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Set up the game window
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")
clock = pygame.time.Clock()

#car size and scalling korci....
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 80))
        self.image = pygame.image.load("car.png")
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed



# sprite groups create korci...
all_sprites_group = pygame.sprite.Group()
car_sprites_group = pygame.sprite.Group()

track_img = pygame.image.load("track.png")



#  primary car re declear korci
primary_car = Car(SCREEN_WIDTH/2-25, SCREEN_HEIGHT-100, GREEN, 0)
all_sprites_group.add(primary_car)


#  other cars re decelear korci....
for i in range(50):
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    car = Car(random.randint(0, SCREEN_WIDTH-50), -i*150, color, random.randint(3, 6))
    all_sprites_group.add(car)
    car_sprites_group.add(car)


# Game ta re auto run korci....
running = True
all_cars_passed_primary_car = False
track_y = -SCREEN_HEIGHT
looppostion = {'x':50, 'y':50}



speed_breaker_y = -500
speed_breaker_triggered = False


while running:
    # Handle events , akhane car bame dane jabe...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        primary_car.rect.y -= 5
    if keys[pygame.K_DOWN]:
        primary_car.rect.y += 5
    if keys[pygame.K_LEFT]:
        primary_car.rect.x -= 10
    if keys[pygame.K_RIGHT]:
        primary_car.rect.x += 10

    # Check for collisions between the primary car and the other cars
    collided_cars = pygame.sprite.spritecollide(primary_car, car_sprites_group, False, pygame.sprite.collide_mask)
    if len(collided_cars) == 1:
        if collided_cars and collided_cars[0] != primary_car:
            if primary_car.rect.x < collided_cars[0].rect.x:
                primary_car.rect.x -= 10
            elif primary_car.rect.x > collided_cars[0].rect.x:
                primary_car.rect.x += 10
    elif len(collided_cars) > 1:
        primary_car.rect.x -= 10

    # Check for collision with speed breaker
    if primary_car.rect.y <= speed_breaker_y + 50 and primary_car.rect.y + 80 >= speed_breaker_y:
        if not speed_breaker_triggered:
            speed_breaker_triggered = True
            primary_car.speed -= 1
    else:
        speed_breaker_triggered = False
        primary_car.speed = 0

    # Update the sprites
    all_sprites_group.update()

    # Draw the track image
    screen.blit(track_img, (0, track_y))
    screen.blit(track_img, (0, track_y + SCREEN_HEIGHT))

    # Update the track position
    track_y += 5
    if track_y > 0:
        track_y = -SCREEN_HEIGHT


    # Update the speed breaker position
    speed_breaker_y += 5
    if speed_breaker_y > SCREEN_HEIGHT:
        speed_breaker_y = -SCREEN_HEIGHT * 0

       
    if primary_car.rect.y <= SCREEN_HEIGHT:
        speed_breaker_rect = pygame.Rect(SCREEN_WIDTH/2 - looppostion['x'], track_y + SCREEN_HEIGHT - looppostion['y'], 50, 50)
        pygame.draw.rect(screen, BLACK, speed_breaker_rect)
        pygame.draw.rect(screen, YELLOW, speed_breaker_rect.inflate(50, -5))

        # Check if the primary car is colliding with the speed breaker
        if primary_car.rect.colliderect(speed_breaker_rect):
            
            primary_car.rect.y += 1
        else:
            primary_car.rect.y -= 1
    
    # Draw the sprites
    all_sprites_group.draw(screen)

    # Update the screen
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

    # Check if all cars have passed the primary car
    if all_cars_passed_primary_car == False and len(car_sprites_group) > 0 and car_sprites_group.sprites()[-1].rect.y > primary_car.rect.y:
        all_cars_passed_primary_car = True
        time.sleep(2)
        pygame.time.wait(1000) # Wait for 2 seconds before showing popup
        popup_font = pygame.font.SysFont('Arial', 50)
        popup_text = popup_font.render('All cars Passed!', True, WHITE)
        popup_rect = popup_text.get_rect()
        popup_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        screen.blit(popup_text, popup_rect)
        pygame.display.flip()
        pygame.time.wait(2000) # Wait for 2 seconds before closing window
        running = False

# Clean up the pygame library
pygame.quit()
