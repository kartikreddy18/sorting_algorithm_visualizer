
import pygame
from random import randint

# initialize pygame
pygame.init()
pygame.font.init()

# global variables
width = 800
height = 700
screen = pygame.display.set_mode((width, height), flags=pygame.NOFRAME)
pygame.mouse.set_visible(False)
background_color = '#293462'
red = '#D61C4E'
golden = '#FEB139'
yellow = '#FFF80A'
min = 10
max = 100
size = 13
padding = 75
bar_width = 50
bar_height = 5
font = pygame.font.SysFont("arial", 27)
clock = pygame.time.Clock()
FPS = 5
color_position = {}
demo_list = []


def generate_random_list(min: int, max: int, size: int) -> list[int]:
    return [randint(a=min, b=max) for _ in range(size)]


class sorting:
    __ascending = True
    __sorting_name = "bubble"
    __l: list[int] = generate_random_list(min, max, size)

    def isAscending(self) -> bool:
        return self.__ascending

    def set_ascending(self, value: bool) -> None:
        self.__ascending = value

    def get_sorting_name(self) -> str:
        return self.__sorting_name

    def set_sorting_name(self, value: str) -> None:
        self.__sorting_name = value

    def get_list(self) -> list[int]:
        return self.__l

    def set_list(self, value: list[int]) -> None:
        self.__l = value


def draw_bars(l: list = demo_list, color_position: dict = color_position) -> None:
    for index, value in enumerate(l):
        x = padding + (index * bar_width)
        y = height - padding - (value * bar_height)
        color = red
        if index in color_position:
            color = color_position[index]
        pygame.draw.rect(
            screen, color, (x, y, bar_width, (value * bar_height)))
        pygame.draw.rect(screen, background_color,
                         (x, y, bar_width, (value * bar_height)), 2)


def control_labels() -> None:
    ascending = sort.isAscending()
    sorting_name = sort.get_sorting_name()
    type = f'w- refresh | a- type(ascending | descending) {"ascending" if ascending else "descending"}'
    method = f's- sorting_method(insertion(iterative | binary_search) | bubble) {sorting_name}'
    control = 'd- start_sorting | esc- exit'
    type_surface = font.render(type, True, golden)
    method_surface = font.render(method, True, golden)
    control_surface = font.render(control, True, golden)
    type_rect = type_surface.get_rect()
    method_rect = method_surface.get_rect()
    control_rect = control_surface.get_rect()
    type_rect.center = (width//2, 20)
    method_rect.center = (width//2, 50)
    control_rect.center = (width//2, 75)
    screen.blit(type_surface, type_rect)
    screen.blit(method_surface, method_rect)
    screen.blit(control_surface, control_rect)
    # pygame.display.update()


def binary_search(l: list[int], num: int, ascending: bool) -> int:
    start = 0
    end = len(l) - 1
    while start <= end:
        mid = (start + end) // 2
        if ((l[mid] > num) and ascending) or ((l[mid] < num) and not ascending):
            end = mid - 1
        else:
            start = mid + 1
    return start


def insertion_sort(l: list[int]):
    global color_position
    ascending = sort.isAscending()
    for i in range(1, len(l)):
        for j in range(0, i):
            if (l[i-j] < l[i-1-j] and ascending) or (l[i-j] > l[i-1-j] and not ascending):
                l[i-j], l[i-1-j] = l[i-1-j], l[i-j]
                color_position = {
                    i-j: golden,
                    i-1-j: yellow
                }
                yield True
            else:
                continue
    color_position = {}
    return l


def binary_insertion_sort(l: list[int]):
    global color_position
    ascending = sort.isAscending()
    for i in range(1, len(l)):
        if (l[i] < l[i-1] and ascending) or (l[i] > l[i-1] and not ascending):
            index = binary_search(l[:i], l[i], ascending=ascending)
            color_position = {
                i: golden,
                index: yellow
            }
            l.insert(index, l.pop(i))
            yield True

    color_position = {}
    return l


def bubble_sort(l: list[int]):
    global color_position
    ascending = sort.isAscending()
    for i in range(len(l) - 1):
        for j in range(len(l) - 1 - i):
            if (l[j] > l[j + 1] and ascending) or (l[j] < l[j + 1] and not ascending):
                l[j], l[j + 1] = l[j + 1], l[j]
                color_position = {
                    j: golden,
                    j + 1: yellow
                }
                yield True
    color_position = {}
    return l


def main_loop() -> None:
    global demo_list
    run = True
    sorting_generator = None
    l = sort.get_list()
    demo_list = l
    sorting = False
    while run:
        clock.tick(FPS)

        if sorting:
            try:
                next(sorting_generator)
            except StopIteration:
                sorting = False

        for event in pygame.event.get():
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_w:
                sorting = False
                l = generate_random_list(min, max, size)
                sort.set_list(l)
                demo_list = l

            elif event.key == pygame.K_a:
                sorting = False
                if sort.isAscending():
                    sort.set_ascending(value=False)
                else:
                    sort.set_ascending(value=True)

            elif event.key == pygame.K_s:
                sorting = False
                sorting_name = sort.get_sorting_name()
                if sorting_name == "bubble":
                    sort.set_sorting_name(value="insertion_iterative")
                elif sorting_name == "insertion_iterative":
                    sort.set_sorting_name("insertion_binary")
                else:
                    sort.set_sorting_name("bubble")

            elif event.key == pygame.K_d:
                sorting = True
                l = sort.get_list()
                sorting_name = sort.get_sorting_name()
                if sorting_name == "bubble":
                    sorting_generator = bubble_sort(l)
                elif sorting_name == "insertion_iterative":
                    sorting_generator = insertion_sort(l)
                else:
                    sorting_generator = binary_insertion_sort(l)

        screen.fill(background_color)
        control_labels()
        draw_bars(l=demo_list, color_position=color_position)
        pygame.display.update()

    pygame.quit()
    exit(0)


if __name__ == '__main__':
    sort = sorting()
    main_loop()
