# Импортируем необходимые библиотеки
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

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

    def __init__(self, body_color=None):
        """Инициализирует игровой объект."""
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на экране.
        Должен быть переопределён в дочерних классах.
        """
        raise NotImplementedError(
            'Метод draw должен быть реализован в дочернем классе'
        )


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self, body_color=APPLE_COLOR, occupied_positions=SCREEN_CENTER):
        """Инициализирует яблоко."""
        super().__init__(body_color)
        self.occupied = occupied_positions or []
        self.randomize_position()

    def randomize_position(self, occupied_positions=SCREEN_CENTER):
        """Генерирует случайную позицию для яблока."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                   randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует змейку."""
        super().__init__(body_color)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]

    def get_head_position(self):
        """Вычисляет позицию головы змейки после следующего шага
        с учётом границ экрана.
        """
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        return (new_x, new_y)

    def move(self):
        """Перемещает змейку на один шаг вперёд."""
        new_head = self.get_head_position()
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает все сегменты змейки на игровом поле."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """При столкновении змейки с собой, начинает игру с начала."""
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


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
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        new_head = snake.get_head_position()

        if new_head == apple.position:
            snake.length += 1
            apple.occupied = snake.positions
            apple.randomize_position()

        snake.move()

        if snake.positions[0] in snake.positions[1:]:
            snake.reset()
            apple.occupied = snake.positions
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
