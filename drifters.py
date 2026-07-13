

import pygame

import drifters_core


pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
world = pygame.Surface((7000, 7000))
car_image = pygame.image.load("car2.xcf").convert_alpha()
car_image = pygame.transform.rotozoom(car_image, 0, 0.1)
car_image0 = car_image
car_image1 = pygame.transform.rotate(car_image, 90)
car_image2 = pygame.transform.rotate(car_image, 180)
car_image3 = pygame.transform.rotate(car_image, 270)
l_car_image = [car_image0, car_image1, car_image2, car_image3]

state = drifters_core.GameState()
clock = pygame.time.Clock()
inputs = {"z": False, "s": False, "q": False, "d": False}

while state.running:
    clock.tick(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z: inputs["z"] = True
            if event.key == pygame.K_s: inputs["s"] = True
            if event.key == pygame.K_q: inputs["q"] = True
            if event.key == pygame.K_d: inputs["d"] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z: inputs["z"] = False
            if event.key == pygame.K_s: inputs["s"] = False
            if event.key == pygame.K_q: inputs["q"] = False
            if event.key == pygame.K_d: inputs["d"] = False
    
    
    state.update(inputs)

    world.fill((0, 0, 0))
    pygame.draw.rect(world, (100, 100, 100), (10, 10, 6980, 6980))
    for enemie in state.enemies:
        pygame.draw.circle(world, (0, 0, 0), enemie.position, 10)
        vect = drifters_core.VecteurForce(enemie.norme_inertie,
                                         enemie.direction).coordonnees()
        pygame.draw.line(world,
                         (200, 200, 200),
                         enemie.position,
                         (enemie.position[0]
                          + vect[0],
                         enemie.position[1]
                         + vect[1]),
                         3)
    
    coef = (state.car.direction // 90) % 4
    rest = state.car.direction % 90
    car_image = pygame.transform.rotate(l_car_image[int(coef)], rest)
    rect = car_image.get_rect(center=(state.car.position[0], state.car.position[1]))

    cam_x = int(state.car.position[0]) - screen.get_width() // 2
    cam_y = int(state.car.position[1]) - screen.get_height() // 2
    world.blit(car_image, rect.topleft)
    screen.blit(world, (0, 0),
                area=pygame.Rect(cam_x, cam_y, screen.get_width(),
                                 screen.get_height()))

    pygame.display.update()

pygame.quit()
