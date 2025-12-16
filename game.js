const gameArea = document.getElementById("gameArea");
const road = document.getElementById("road");
const car = document.getElementById("playerCar");

const scoreEl = document.getElementById("score");
const levelEl = document.getElementById("level");

const lanes = [120, 260, 400];
let carLane = 1;

let score = 0;
let level = 1;
let speed = 5;
let gameRunning = true;

/* FOOD DATA */
const foods = [
    { img: "assets/images/curd.png", type: "healthy" },
    { img: "assets/images/spinach.png", type: "healthy" },
    { img: "assets/images/egg.png", type: "healthy" },
    { img: "assets/images/maggi.png", type: "unhealthy" },
    { img: "assets/images/chicken.png", type: "unhealthy" },
    { img: "assets/images/panipuri.png", type: "unhealthy" }
];

let enemies = [];

/* ROAD MOVE */
function moveRoad() {
    let top = parseInt(road.style.top || -700);
    top += speed;
    if (top >= 0) top = -700;
    road.style.top = top + "px";
}

/* SPAWN FOOD */
function spawnFood() {
    if (!gameRunning) return;

    const food = document.createElement("img");
    const f = foods[Math.floor(Math.random() * foods.length)];

    food.src = f.img;
    food.dataset.type = f.type;
    food.className = "food";

    food.style.left = lanes[Math.floor(Math.random() * lanes.length)] + "px";
    food.style.top = "-60px";

    gameArea.appendChild(food);
}

/* MOVE FOOD */
function moveFoods() {
    document.querySelectorAll(".food").forEach(food => {
        food.style.top = parseInt(food.style.top) + speed + "px";

        if (isColliding(food, car)) {
            score += food.dataset.type === "healthy" ? 1 : -1;
            scoreEl.innerText = score;
            food.remove();
        }

        if (parseInt(food.style.top) > 700) {
            food.remove();
        }
    });
}

/* ENEMY */
function spawnEnemy() {
    if (!gameRunning) return;

    const enemy = document.createElement("img");
    enemy.src = "assets/images/enemy_car.png";
    enemy.className = "enemy";

    enemy.style.left = lanes[Math.floor(Math.random() * lanes.length)] + "px";
    enemy.style.top = "-150px";

    gameArea.appendChild(enemy);
    enemies.push(enemy);
}

function moveEnemies() {
    enemies.forEach((enemy, index) => {
        enemy.style.top = parseInt(enemy.style.top) + speed + 2 + "px";

        if (isColliding(enemy, car)) {
            gameOver();
        }

        if (parseInt(enemy.style.top) > 800) {
            enemy.remove();
            enemies.splice(index, 1);
        }
    });
}

/* COLLISION */
function isColliding(a, b) {
    const r1 = a.getBoundingClientRect();
    const r2 = b.getBoundingClientRect();

    return !(
        r1.bottom < r2.top ||
        r1.top > r2.bottom ||
        r1.right < r2.left ||
        r1.left > r2.right
    );
}

/* CONTROLS */
document.addEventListener("keydown", e => {
    if (e.key === "ArrowLeft" && carLane > 0) carLane--;
    if (e.key === "ArrowRight" && carLane < 2) carLane++;
    car.style.left = lanes[carLane] + "px";
});

/* LEVEL SYSTEM */
setInterval(() => {
    level++;
    speed += 1;
    levelEl.innerText = level;
}, 15000);

/* GAME OVER */
function gameOver() {
    gameRunning = false;
    alert("💥 GAME OVER!\nScore: " + score);
    location.reload();
}

/* GAME LOOP */
function gameLoop() {
    if (!gameRunning) return;
    moveRoad();
    moveFoods();
    moveEnemies();
    requestAnimationFrame(gameLoop);
}

/* START */
setInterval(spawnFood, 1200);
setInterval(spawnEnemy, 3000);
gameLoop();
