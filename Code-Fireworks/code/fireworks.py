import pygame
import random
import math

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Code-Fireworks Deluxe - Snowman & Muñeco")

clock = pygame.time.Clock()

# Colores foquitos
LIGHT_COLORS = [(255,0,0),(255,255,0),(0,255,0),(0,0,255),(255,165,0),(255,20,147)]

# Fuegos artificiales
def create_firework():
    particles = []
    for _ in range(50):
        angle = random.uniform(0, 2*math.pi)
        speed = random.uniform(3, 7)
        color = random.choice(LIGHT_COLORS)
        particles.append({
            "x": random.randint(200,600),
            "y": random.randint(50,250),
            "dx": math.cos(angle)*speed,
            "dy": math.sin(angle)*speed,
            "color": color,
            "life": random.randint(30,60)
        })
    return particles

fireworks = []

# Estrellas fugaces
stars = [{"x": random.randint(0,800), "y": random.randint(0,200), "dx": random.uniform(-3,-1), "dy": random.uniform(2,4)} for _ in range(20)]

# Pelota animada que rebota en el piso
ball = {"x": 100, "y": 100, "radius": 15, "dx": 6, "dy": 0}  # dx=horizontal, dy=vertical
gravity = 0.5  # gravedad para simular rebote
bounce = -0.7   # factor de rebote

# Árbol de navidad con foquitos
def draw_tree():
    lights = []
    for i in range(0,120,6):
        for j in range(0,100,6):
            tx = 550 + i
            ty = 520 - j
            if j > abs(i-60)/1.5:
                lights.append({"x":tx,"y":ty,"color":random.choice(LIGHT_COLORS)})
    for light in lights:
        if random.random() > 0.2:
            pygame.draw.circle(screen, light["color"], (light["x"], light["y"]), 4)

# Estrella de Belén
def draw_bethlehem_star():
    cx, cy = 400, 150
    points = []
    for i in range(5):
        angle = i * (2*math.pi/5) - math.pi/2
        x = cx + 40 * math.cos(angle)
        y = cy + 40 * math.sin(angle)
        points.append((x, y))
    for i in range(5):
        x1, y1 = points[i]
        x2, y2 = points[(i+2)%5]
        steps = 10
        for s in range(steps+1):
            fx = int(x1 + (x2-x1)*s/steps)
            fy = int(y1 + (y2-y1)*s/steps)
            pygame.draw.circle(screen, random.choice(LIGHT_COLORS), (fx, fy), 4)

# Muñeco estilo "quema de años viejos"
def draw_old_year_effigy():
    x, y = 300, 480
    pygame.draw.circle(screen, (139,69,19), (x, y), 25)
    pygame.draw.circle(screen, (160,82,45), (x, y-35), 20)
    pygame.draw.circle(screen, (205,133,63), (x, y-60), 15)
    pygame.draw.circle(screen, (0,0,0), (x-5, y-62), 3)
    pygame.draw.circle(screen, (0,0,0), (x+5, y-62), 3)
    pygame.draw.arc(screen, (0,0,0), (x-7, y-58, 14, 10), math.pi, 2*math.pi, 2)
    pygame.draw.rect(screen, (255,0,0), (x-10, y-75, 20, 5))
    pygame.draw.polygon(screen, (255,0,0), [(x-10, y-75),(x+10, y-75),(x, y-90)])
    for i in range(-20,21,10):
        for j in range(-30,1,10):
            if random.random() > 0.5:
                pygame.draw.circle(screen, random.choice(LIGHT_COLORS), (x+i, y+j), 3)

# Muñeco de nieve
snowman = {"x":150, "y":480}

running = True
while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fireworks.append(create_firework())

    # Actualizar pelota
    ball["x"] += ball["dx"]
    ball["dy"] += gravity
    ball["y"] += ball["dy"]

    # Rebote en los bordes horizontal
    if ball["x"] - ball["radius"] <= 0 or ball["x"] + ball["radius"] >= 800:
        ball["dx"] *= -1

    # Rebote en el piso
    if ball["y"] + ball["radius"] >= 580:  # piso aproximado
        ball["y"] = 580 - ball["radius"]
        ball["dy"] *= bounce

    # Rebote techo (opcional)
    if ball["y"] - ball["radius"] <= 0:
        ball["y"] = ball["radius"]
        ball["dy"] *= bounce

    # Dibujar elementos
    draw_tree()
    draw_bethlehem_star()
    draw_old_year_effigy()

    # Frase Happy New Year
    font_large = pygame.font.SysFont(None, 60)
    text_large = font_large.render("Happy New Year!", True, (255,255,0))
    screen.blit(text_large, (250, 50))

    # Muñeco de nieve
    pygame.draw.circle(screen, (255,255,255), (snowman["x"], snowman["y"]), 30)
    pygame.draw.circle(screen, (255,255,255), (snowman["x"], snowman["y"]-40), 25)
    pygame.draw.circle(screen, (255,255,255), (snowman["x"], snowman["y"]-70), 20)
    pygame.draw.circle(screen, (0,0,0), (snowman["x"]-7, snowman["y"]-72), 3)
    pygame.draw.circle(screen, (0,0,0), (snowman["x"]+7, snowman["y"]-72), 3)
    pygame.draw.polygon(screen, (255,165,0), [(snowman["x"], snowman["y"]-70),(snowman["x"], snowman["y"]-65),(snowman["x"]+15, snowman["y"]-68)])
    pygame.draw.circle(screen, (0,0,0), (snowman["x"], snowman["y"]-40), 3)
    pygame.draw.circle(screen, (0,0,0), (snowman["x"], snowman["y"]-20), 3)
    pygame.draw.rect(screen, (255,0,0), (snowman["x"]-15, snowman["y"]-85, 30, 10))
    pygame.draw.polygon(screen, (255,0,0), [(snowman["x"]-15, snowman["y"]-85),(snowman["x"]+15, snowman["y"]-85),(snowman["x"], snowman["y"]-110)])
    pygame.draw.circle(screen, (255,255,255), (snowman["x"], snowman["y"]-110), 5)

    # Estrellas fugaces
    for star in stars:
        pygame.draw.circle(screen, (255,255,255), (int(star["x"]), int(star["y"])), 2)
        star["x"] += star["dx"]
        star["y"] += star["dy"]
        if star["y"] > 600 or star["x"] < 0:
            star["x"], star["y"] = 800, random.randint(0,200)

    # Fuegos artificiales
    for firework in fireworks:
        for p in firework:
            pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), 3)
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            p["dy"] += 0.1
            p["life"] -= 1
        firework[:] = [p for p in firework if p["life"] > 0]
    fireworks[:] = [f for f in fireworks if len(f) > 0]

    # Dibujar pelota
    pygame.draw.circle(screen, (0,255,255), (int(ball["x"]), int(ball["y"])), ball["radius"])

    # Firma
    font = pygame.font.SysFont(None,24)
    text = font.render("Created by Jorge Paez - LinkedIn", True, (255,255,255))
    screen.blit(text, (10,10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
