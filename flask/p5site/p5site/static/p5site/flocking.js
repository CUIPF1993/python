var flock;

function setup() {
    let canvasWidth = $("#paint").width();
    let canvasHeight = canvasWidth / 2;
    let myCanvas = createCanvas(canvasWidth, canvasHeight);
    myCanvas.parent('paint');


    flock = new Flock();
    for (var i = 0; i < 1; i++) {
        var b = new Boid(width / 2, height / 2);
        flock.addBoid(b)
    }
}

function draw() {
    background(240);
    flock.run();
}

//鼠标拖动生成新的
function mouseDragged() {
    flock.addBoid(new Boid(mouseX, mouseY));
}

class Flock {
    //构造函数
    constructor() {
        this.boids = []
    }

    // 驱动
    run() {
        for (var i = 0; i < this.boids.length; i++) {
            this.boids[i].run(this.boids);
        }
    }

    // 在群集中增加新的
    addBoid(b) {
        this.boids.push(b)

    }
}

class Boid {
    constructor(x, y) {
        this.acceleration = createVector(0, 0);
        this.velocity = createVector(random(-1, 1), random(-1, 1));
        this.position = createVector(x, y);
        this.r = 3.0;
        //最大速度
        this.maxspeed = 3;
        //最大转向力
        this.maxforce = 0.05;
        colorMode(HSB);
        this.color = color(45, 36, random(50, 100));
    }

    //驱动
    run(boids) {
        this.flock(boids);
        this.update();
        this.borders();
        this.render();
    }

    //施加力
    applyForce(force) {
        this.acceleration.add(force);
    }

    //受到的影响
    flock(boids) {
        var sep = this.separate(boids);
        var ali = this.align(boids);
        var coh = this.cohesion(boids);


        sep.mult(1.5);
        ali.mult(1.0);
        coh.mult(1.0);

        this.applyForce(sep);
        this.applyForce(ali);
        this.applyForce(coh);
    }

    //更新位置
    update() {
        this.velocity.add(this.acceleration);
        this.velocity.limit(this.maxspeed);
        this.position.add(this.velocity);
        this.acceleration.mult(0);
    }

    //计算转向力
    seek(target) {
        var desired = p5.Vector.sub(target, this.position);
        desired.normalize();
        desired.mult(this.maxspeed);
        var steer = p5.Vector.sub(desired, this.velocity);
        steer.limit(this.maxforce);
        return steer;
    }

    // 渲染
    render() {
        var theta = this.velocity.heading() + radians(90);
        noStroke();
        fill(this.color);
        push();
        translate(this.position.x, this.position.y);
        rotate(theta);
        beginShape();
        vertex(0, -this.r * 2);
        vertex(-this.r, this.r * 2);
        vertex(this.r, this.r * 2);
        endShape(CLOSE);
        pop();
    }


    //边界检测
    borders() {
        if (this.position.x < -this.r) this.position.x = width + this.r;
        if (this.position.y < -this.r) this.position.y = height + this.r;
        if (this.position.x > width + this.r) this.position.x = -this.r;
        if (this.position.y > height + this.r) this.position.y = -this.r;
    }

    //排斥
    separate(boids) {
        var desiredSeparation = 25.0;
        var steer = createVector(0, 0);
        var count = 0;
        //距离太近施加排斥力
        for (var i = 0; i < boids.length; i++) {
            var d = p5.Vector.dist(this.position, boids[i].position);
            if ((d > 0) && (d < desiredSeparation)) {
                var diff = p5.Vector.sub(this.position, boids[i].position);
                diff.normalize();
                diff.div(d);
                steer.add(diff);
                count++;
            }
        }

        if (count > 0) {
            steer.div(count);
        }

        if (steer.mag() > 0) {
            steer.normalize();
            steer.mult(this.maxspeed);
            steer.sub(this.velocity);
            steer.limit(this.maxforce);
        }
        return steer;
    }

    // 对于系统中的每一个物体计算平均转向力
    align(boids) {
        var neighborDist = 50;
        var sum = createVector(0, 0);
        var count = 0;
        for (var i = 0; i < boids.length; i++) {
            var d = p5.Vector.dist(this.position, boids[i].position);
            if ((d > 0) && (d < neighborDist)) {
                sum.add(boids[i].velocity);
                count++;
            }
        }
        if (count > 0) {
            sum.div(count);
            sum.normalize();
            sum.mult(this.maxspeed);
            var steer = p5.Vector.sub(sum, this.velocity);
            steer.limit(this.maxforce);
            return steer
        } else {
            return createVector(0, 0);
        }

    }

    // 计算凝聚力
    cohesion(boids) {
        var neighborDist = 50;
        var sum = createVector(0, 0);
        var count = 0;
        for (var i = 0; i < boids.length; i++) {
            var d = p5.Vector.dist(this.position, boids[i].position)
            if ((d > 0) && (d < neighborDist)) {
                sum.add(boids[i].position);
                count++;
            }
        }
        if (count > 0) {
            sum.div(count);
            return this.seek(sum);
        } else {
            return createVector(0, 0)
        }
    }
}


