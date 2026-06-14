# Импортируем необходимые библиотеки
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    def __init__(self, position, body_color):
        """Инициализирует игровой объект."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на экране.
        Должен быть переопределён в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        """Инициализирует яблоко."""
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Генерирует случайную позицию для яблока."""
        position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return position_x, position_y

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(
            self,
            position,
            body_color=SNAKE_COLOR,
            length=1,
            direction=RIGHT,
            next_direction=None,
            last=None
    ):
        """Инициализирует змейку."""
        super().__init__(position, body_color)
        self.length = length
        self.direction = direction
        self.next_direction = next_direction
        self.last = last
        self.positions = [position]

    def get_head_position(self):
        """Вычисляет позицию головы змейки после следующего шага
        с учётом границ экрана.
        """
        position_x, position_y = self.position
        if self.direction == RIGHT:
            position_x += GRID_SIZE
            if position_x >= SCREEN_WIDTH:
                position_x = 0
        elif self.direction == LEFT:
            position_x -= GRID_SIZE
            if position_x < 0:
                position_x = SCREEN_WIDTH - GRID_SIZE
        elif self.direction == UP:
            position_y -= GRID_SIZE
            if position_y < 0:
                position_y = SCREEN_HEIGHT - GRID_SIZE
        elif self.direction == DOWN:
            position_y += GRID_SIZE
            if position_y >= SCREEN_HEIGHT:
                position_y = 0
        return (position_x, position_y)

    def move(self):
        """Перемещает змейку на один шаг вперёд."""
        new_head_position = self.get_head_position()
        self.positions.insert(0, new_head_position)
        self.position = new_head_position
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает все сегменты змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """При столкновении змейки с собой, начинает игру с начала."""
        start_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = start_position
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions = [start_position]


def handle_keys(game_object):
    """Обрабатывает события клавиатуры и
    возвращает запрошенное направление движения.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Основная функция игры — запускает игровой цикл.

    Включает:
    - Инициализацию Pygame.
    - Создание объектов змейки и яблока.
    - Игровой цикл с обработкой ввода, движением, проверкой столкновений.
    """
    pygame.init()
    apple = Apple()
    snake = Snake(position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

        if snake.positions[0] in snake.positions[1:]:
            snake.reset()
            apple.position = apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
