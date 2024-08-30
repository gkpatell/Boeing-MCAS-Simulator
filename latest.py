import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen object
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption('2D Flight Simulator')

# Load airplane image
airplane_image = pygame.image.load('airplane.png')
airplane_image = pygame.transform.scale(airplane_image, (500, 500))  # Resize the airplane image

# Load RCEL logo image
rcel_logo = pygame.image.load('RCEL.png')
rcel_logo = pygame.transform.scale(rcel_logo, (275,65))
rcel_logo_rect = rcel_logo.get_rect()
rcel_logo_rect.topleft = (10, 10)  # Position the logo at the top left corner

# Get the rectangle object for the resized image
airplane_rect = airplane_image.get_rect()
airplane_rect.center = (screen_width // 2, screen_height // 2)

# Clock object to control the frame rate
clock = pygame.time.Clock()

# Font for text
font = pygame.font.SysFont(None, 24)

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

#Function to draw rotated text on screen
def draw_text_rotated(text, font, color, surface, x, y, angle):
    text_obj = font.render(text, True, color)
    rotated_text = pygame.transform.rotate(text_obj, angle)
    text_rect = rotated_text.get_rect(center=(x, y))
    surface.blit(rotated_text, text_rect)

# Function to rotate the airplane
def rotate(surface, angle):
    rotated_surface = pygame.transform.rotate(surface, angle)
    rotated_rect = rotated_surface.get_rect(center=(airplane_rect.centerx, airplane_rect.centery))
    return rotated_surface, rotated_rect

# Initial angle of the airplane
angle = 0

# Slide bar dimensions and position for AoA control
slider_width = 20
slider_height = 175
slider_handle_height = 17.5
slider_min_angle = -45
slider_max_angle = 45

# Position sliders in the bottom right corner
slider_x_aoa = screen_width - 50
slider_y_aoa = screen_height - slider_height - 50

slider_width_trim = 20
slider_height_trim = 175
slider_x_trim = screen_width - 110
slider_y_trim = screen_height - slider_height_trim - 50

# Initial slider handle position
slider_handle_y_aoa = slider_y_aoa + (slider_height // 2)
slider_handle_y_trim = slider_y_trim + (slider_height_trim // 2)
trim_angle = 0

# Control sliders dimensions and position
control_slider_width = 20
control_slider_height = 150
control_slider_handle_height = 20
control_slider_x1 = screen_width - 200
control_slider_y1 = 50
control_slider_x2 = screen_width - 150
control_slider_y2 = 50
control_slider_x3 = screen_width - 100
control_slider_y3 = 50
control_slider_x4 = screen_width - 50 
control_slider_y4 = 50

# Initial control slider handle positions
control_slider_handle_y1 = control_slider_y1 + control_slider_height // 2
control_slider_handle_y2 = control_slider_y2 + control_slider_height // 2
control_slider_handle_y3 = control_slider_y3 + control_slider_height // 2
control_slider_handle_y4 = control_slider_y4 + control_slider_height // 2

# Function to draw the slide bar
def draw_slider(surface, x, y, width, height, handle_y):
    pygame.draw.rect(surface, (100, 100, 100), (x, y, width, height))  # Slider bar
    pygame.draw.rect(surface, (200, 200, 200), (x, handle_y - slider_handle_height // 2, width, slider_handle_height))  # Handle

# Function to draw the AoA indicator
def draw_aoa_indicator(surface, x, y, angle):
    radius = 50
    pygame.draw.circle(surface, (200, 200, 200), (x, y), radius)
    pygame.draw.line(surface, (0, 0, 0), (x, y), 
                     (x + radius * math.cos(math.radians(-angle - 0)), 
                      y + radius * math.sin(math.radians(-angle - 0))), 4)
    draw_text(f'AoA: {angle:.2f}°', font, (0, 0, 0), surface, x - 40, y + 60)

# Automation system class
class AutomationSystem:
    def __init__(self):
        self.control_mode = 0  # Starting with manual control

    def control_sliders(self, aoa_handle_y, trim_handle_y):
        if self.control_mode == 0:  # Top position: Control AoA (MCAS) only, freeze (Pilot) Trim
            trim_handle_y = slider_y_trim + slider_height_trim // 2
        elif self.control_mode == 1:  # Middle position: Synchronize both
            trim_handle_y = aoa_handle_y
        elif self.control_mode == 2:  # Bottom position: Control Trim (Pilot) only, freeze AoA (MCAS)
            aoa_handle_y = slider_y_aoa + slider_height // 2
        return aoa_handle_y, trim_handle_y

# Create the automation system
automation_system = AutomationSystem()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                if slider_x_aoa <= event.pos[0] <= slider_x_aoa + slider_width and slider_y_aoa <= event.pos[1] <= slider_y_aoa + slider_height:
                    slider_handle_y_aoa = event.pos[1]
                elif slider_x_trim <= event.pos[0] <= slider_x_trim + slider_width_trim and slider_y_trim <= event.pos[1] <= slider_y_trim + slider_height_trim:
                    slider_handle_y_trim = event.pos[1]
                if control_slider_x1 <= event.pos[0] <= control_slider_x1 + control_slider_width and control_slider_y1 <= event.pos[1] <= control_slider_y1 + control_slider_height:
                    control_slider_handle_y1 = event.pos[1]
                    automation_system.control_mode = (control_slider_handle_y1 - control_slider_y1) // (control_slider_height // 3)
                elif control_slider_x2 <= event.pos[0] <= control_slider_x2 + control_slider_width and control_slider_y2 <= event.pos[1] <= control_slider_y2 + control_slider_height:
                    control_slider_handle_y2 = event.pos[1]
                    automation_system.control_mode = (control_slider_handle_y2 - control_slider_y2) // (control_slider_height // 3)
                elif control_slider_x3 <= event.pos[0] <= control_slider_x3 + control_slider_width and control_slider_y3 <= event.pos[1] <= control_slider_y3 + control_slider_height:
                    control_slider_handle_y3 = event.pos[1]
                    automation_system.control_mode = (control_slider_handle_y3 - control_slider_y3) // (control_slider_height // 3)
                elif control_slider_x4 <= event.pos[0] <= control_slider_x4 + control_slider_width and control_slider_y4 <= event.pos[1] <= control_slider_y4 + control_slider_height:
                    control_slider_handle_y4 = event.pos[1]
                    automation_system.control_mode = (control_slider_handle_y4 - control_slider_y4) // (control_slider_height // 3)

    # Apply automation control to the AoA and Trim sliders
    slider_handle_y_aoa, slider_handle_y_trim = automation_system.control_sliders(slider_handle_y_aoa, slider_handle_y_trim)

    # Calculate the angle from the AoA slider position
    relative_position_aoa = (slider_handle_y_aoa - slider_y_aoa) / slider_height
    angle = slider_min_angle + relative_position_aoa * (slider_max_angle - slider_min_angle)

    # Calculate the trim angle from the trim slider position
    relative_position_trim = (slider_handle_y_trim - slider_y_trim) / slider_height_trim
    trim_angle = -15 + relative_position_trim * 30  # Trim range from -45 to 45 degrees

    # Apply the trim to the airplane's angle
    adjusted_angle = angle + trim_angle

    # Rotate the airplane image
    rotated_airplane_image, rotated_airplane_rect = rotate(airplane_image, adjusted_angle)

    # Fill the screen with a light grey color
    screen.fill((177, 175, 167))

    # Draw the airplane on the screen
    screen.blit(rotated_airplane_image, rotated_airplane_rect.topleft)

    #Draw the RCEL logo at top left of the window
    screen.blit(rcel_logo, rcel_logo_rect.topleft)

    # Draw the AoA slider
    draw_slider(screen, slider_x_aoa, slider_y_aoa, slider_width, slider_height, slider_handle_y_aoa)
    draw_text('MCAS', font, (0, 0, 0), screen, slider_x_aoa - 20, slider_y_aoa + slider_height +10)

    # Draw the stabilizer trim slider
    draw_slider(screen, slider_x_trim, slider_y_trim, slider_width_trim, slider_height_trim, slider_handle_y_trim)
    draw_text('Pilot', font, (0, 0, 0), screen, slider_x_trim - 20, slider_y_trim + slider_height +10)

    # Draw the AoA indicator at the bottom left, using adjusted_angle for the current AoA
    draw_aoa_indicator(screen, 100, screen_height - 100, adjusted_angle)

    # Draw the control sliders at the top right
    draw_slider(screen, control_slider_x1, control_slider_y1, control_slider_width, control_slider_height, control_slider_handle_y1)
    draw_slider(screen, control_slider_x2, control_slider_y2, control_slider_width, control_slider_height, control_slider_handle_y2)
    draw_slider(screen, control_slider_x3, control_slider_y3, control_slider_width, control_slider_height, control_slider_handle_y3)
    draw_slider(screen, control_slider_x4, control_slider_y4, control_slider_width, control_slider_height, control_slider_handle_y4)

   # Label the control sliders
    draw_text('DAq', font, (0, 0, 0), screen, control_slider_x1, control_slider_y1 - 30)
    draw_text('DAn', font, (0, 0, 0), screen, control_slider_x2, control_slider_y2 - 30)
    draw_text('Dec', font, (0, 0, 0), screen, control_slider_x3, control_slider_y3 - 30)
    draw_text('Act', font, (0, 0, 0), screen, control_slider_x4, control_slider_y4 - 30)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()