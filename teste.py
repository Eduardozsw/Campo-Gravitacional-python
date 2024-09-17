import pygame
import numpy as np

# Inicializa o pygame
pygame.init()

# Define as dimensões da janela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simulação Gravitacional')

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Constantes físicas
G = 6.67430e-11  # Constante gravitacional
FPS = 240

# Classe para as esferas
class Sphere:
    def __init__(self, x, y, mass, radius, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.vx = 0
        self.vy = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def apply_gravity(self, spheres):
        ax, ay = 0, 0
        for sphere in spheres:
            if sphere != self:
                dx = sphere.x - self.x
                dy = sphere.y - self.y
                dist_sq = dx**2 + dy**2
                dist = np.sqrt(dist_sq)
                if dist > self.radius + sphere.radius:  # Evita colapsos
                    force = G * self.mass * sphere.mass / dist_sq
                    ax += force * (dx / dist)
                    ay += force * (dy / dist)
        
        # Atualiza a velocidade
        self.vx += ax
        self.vy += ay

    def update_position(self):
        # Atualiza a posição com base na velocidade
        self.x += self.vx
        self.y += self.vy

# Esferas iniciais
sphere1 = Sphere(WIDTH // 4, HEIGHT // 2, 5e5, 20, BLUE)
sphere2 = Sphere(3 * WIDTH // 4, HEIGHT // 2, 5e5, 20, RED)
sphere3 = Sphere(WIDTH // 2, HEIGHT // 4, 5e5, 20, GREEN)

spheres = [sphere1, sphere2, sphere3]

# Loop principal
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Calcula e aplica a gravidade entre as esferas
    for sphere in spheres:
        sphere.apply_gravity(spheres)

    # Atualiza as posições e desenha as esferas
    for sphere in spheres:
        sphere.update_position()
        sphere.draw(screen)

    # Controle de FPS
    clock.tick(FPS)

    # Atualiza a tela
    pygame.display.flip()

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Encerra o pygame
pygame.quit()
