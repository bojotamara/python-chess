#!/usr/bin/python3

if __name__ == "__main__":
    import pygame

    # from assets import *
    from modules.board import *

    pygame.init()

    screen = pygame.display.set_mode((800, 60 * 8))
    pygame.display.set_caption('Boss Ass Chess Game')

    # load background image
    bg = pygame.image.load("assets/chessboard.png").convert()
    # blit like puts the image on there

    # board matrix
    b = Board()

    all_sprites_list = pygame.sprite.Group()
    sprites = [piece for row in b.array for piece in row if piece]
    all_sprites_list.add(sprites)

    screen.blit(bg, (0, 0))
    all_sprites_list.draw(screen)
    # all_sprites_list = pygame.sprite.LayeredDirty(
    #     piece for row in b.array for piece in row if piece)

    clock = pygame.time.Clock()
    crashed = False

    while not crashed:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # get a list of all sprites that are under the mouse cursor
                clicked_sprites = [
                    s for s in sprites if s.rect.collidepoint(pos)]

                if len(clicked_sprites) == 1:
                    # clicked_sprites[0].highlight(screen)
                    clicked_sprites[0].highlight()

            # elif event.type == pygame.MOUSEBUTTONUP:
            #     pos = pygame.mouse.get_pos()
            #     # get a list of all sprites that are under the mouse cursor
            #     clicked_sprites = [
            #         s for s in sprites if s.rect.collidepoint(pos)]
            #     if len(clicked_sprites) == 1:
            #         # clicked_sprites[0].highlight(screen)
            #         clicked_sprites[0].unhighlight()
            #         # clicked_sprites[0].unhighlight()
            #         # elif:
            #         #     crashed = True
            #         #     print('SOMETHING DEADASS BROKE')

            print(event)

        screen.blit(bg, (0, 0))
        all_sprites_list.draw(screen)
        pygame.display.update()
        clock.tick(60)
