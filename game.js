const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const welcomeScreen = document.getElementById('welcomeScreen');
const scoreElement = document.getElementById('score');
const highScoreElement = document.getElementById('highScore');

// Constants
const GRID_SIZE = 20;
const GRID_COUNT = 30;
canvas.width = GRID_SIZE * GRID_COUNT;
canvas.height = GRID_SIZE * GRID_COUNT;

// Colors
const COLORS = {
    snake: ['#00ff00', '#0000ff', '#00ffff', '#800080', '#ffff00'],
    food: ['#ff0000', '#0000ff', '#800080', '#ffff00', '#00ffff'],
    background: '#000000',
    grid: '#282828'
};

class Snake {
    constructor() {
        this.reset();
    }

    reset() {
        this.positions = Array.from({length: 5}, (_, i) => ({
            x: Math.floor(GRID_COUNT / 2) - i,
            y: Math.floor(GRID_COUNT / 2)
        }));
        this.direction = { x: 1, y: 0 };
        this.length = 5;
    }

    update() {
        const head = { 
            x: (this.positions[0].x + this.direction.x + GRID_COUNT) % GRID_COUNT,
            y: (this.positions[0].y + this.direction.y + GRID_COUNT) % GRID_COUNT
        };

        if (this.positions.some(pos => pos.x === head.x && pos.y === head.y)) {
            return false;
        }

        this.positions.unshift(head);
        if (this.positions.length > this.length) {
            this.positions.pop();
        }
        return true;
    }

    draw() {
        this.positions.forEach((pos, index) => {
            ctx.fillStyle = COLORS.snake[index % COLORS.snake.length];
            ctx.fillRect(pos.x * GRID_SIZE, pos.y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1);
        });
    }
}

class Food {
    constructor() {
        this.position = { x: 0, y: 0 };
        this.color = COLORS.food[0];
        this.randomize();
    }

    randomize() {
        this.position.x = Math.floor(Math.random() * GRID_COUNT);
        this.position.y = Math.floor(Math.random() * GRID_COUNT);
        this.color = COLORS.food[Math.floor(Math.random() * COLORS.food.length)];
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.fillRect(
            this.position.x * GRID_SIZE,
            this.position.y * GRID_SIZE,
            GRID_SIZE - 1,
            GRID_SIZE - 1
        );
    }
}

// Game state
let snake = new Snake();
let food = new Food();
let score = 0;
let gameStarted = false;
let gameLoop;

function drawGrid() {
    ctx.strokeStyle = COLORS.grid;
    for (let i = 0; i <= GRID_COUNT; i++) {
        ctx.beginPath();
        ctx.moveTo(i * GRID_SIZE, 0);
        ctx.lineTo(i * GRID_SIZE, canvas.height);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, i * GRID_SIZE);
        ctx.lineTo(canvas.width, i * GRID_SIZE);
        ctx.stroke();
    }
}

function update() {
    if (!snake.update()) {
        snake.reset();
        food.randomize();
        score = 0;
        scoreElement.textContent = score;
    }

    if (snake.positions[0].x === food.position.x && 
        snake.positions[0].y === food.position.y) {
        snake.length++;
        score++;
        scoreElement.textContent = score;
        food.randomize();
    }
}

function draw() {
    ctx.fillStyle = COLORS.background;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    drawGrid();
    snake.draw();
    food.draw();
}

function gameStep() {
    update();
    draw();
}

document.addEventListener('keydown', (event) => {
    if (!gameStarted && event.code === 'Space') {
        gameStarted = true;
        welcomeScreen.classList.add('hidden');
        gameLoop = setInterval(gameStep, 100);
        return;
    }

    if (!gameStarted) return;

    const directions = {
        'ArrowUp': { x: 0, y: -1 },
        'ArrowDown': { x: 0, y: 1 },
        'ArrowLeft': { x: -1, y: 0 },
        'ArrowRight': { x: 1, y: 0 }
    };

    if (directions[event.code]) {
        const newDir = directions[event.code];
        if (snake.direction.x !== -newDir.x || snake.direction.y !== -newDir.y) {
            snake.direction = newDir;
        }
    }
});

// Initial draw
draw(); 