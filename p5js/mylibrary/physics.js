class Surface {
    constructor(vecs) {
        this.surface = vecs;

        for (let i = 0; i < this.surface.length; i++) {
            this.surface[i] = scaleToWorld(this.surface[i]);
        }

        //定义shape
        let chain = new box2d.b2ChainShape();
        chain.CreateChain(this.surface, this.surface.length);

        //定义body
        let bd = new box2d.b2BodyDef();
        this.body = world.CreateBody(bd);

        //定义fixture
        let fd = new box2d.b2FixtureDef();
        fd.shape = chain;

        //定义物理属性
        fd.density = 1.0;
        fd.friction = 0.1;
        fd.restitution = 0.3;

        //
        this.body.CreateFixture(fd);
    }

    //绘制
    display() {
        strokeWeight(1);
        stroke(200);
        fill(200);
        beginShape();
        for (let i = 0; i < this.surface.length; i++) {
            let v = scaleToPixels(this.surface[i]);
            vertex(v.x, v.y);
        }
        vertex(width, height);
        vertex(0, height);
        endShape(CLOSE);
    }
}

//定义一个草图星形多边形
class CustomShape {
    constructor(x, y) {

        //定义一个body
        let bd = new box2d.b2BodyDef();
        bd.type = box2d.b2BodyType.b2_dynamicBody;
        bd.position = scaleToWorld(x, y);

        //定义一个fixture
        let fd = new box2d.b2FixtureDef();

        let vertices = [];
        vertices[3] = scaleToWorld(-15, 25);
        vertices[2] = scaleToWorld(15, 0);
        vertices[1] = scaleToWorld(20, -15);
        vertices[0] = scaleToWorld(-10, -10);

        fd.shape = new box2d.b2PolygonShape();
        fd.shape.SetAsArray(vertices, vertices.length);

        //设置物理属性
        fd.density = 1.0;
        fd.friction = 0.05;
        fd.restitution = 0.1;

        this.body = world.CreateBody(bd);
        this.body.CreateFixture(fd);

        colorMode(HSB, 100);
        this.color = color(55, 65, random(30, 100));
    }

    killBody() {
        world.DestroyBody(this.body);
    }

    done() {
        let pos = scaleToWorld(this.body.GetPosition());

        if (pos.y > height + this.w * this.h) {
            this.killBody();
            return true;
        }
        return false;
    }

    //绘制customShape
    display() {
        let pos = scaleToPixels(this.body.GetPosition());
        let a = this.body.GetAngleRadians();

        let f = this.body.GetFixtureList();
        let ps = f.GetShape();

        rectMode(CENTER);
        push();
        translate(pos.x, pos.y);
        rotate(a);

        stroke(this.color);
        strokeWeight(2);

        // beginShape();
        // for (let i = 0; i < ps.m_count; i++) {
        //     let v = scaleToPixels(ps.m_vertices[i]);
        //     vertex(v.x, v.y);
        // }
        // endShape();

        let xCoords = [];
        let yCoords = [];

        for (let i = 0; i < ps.m_count; i++) {
            let v = scaleToPixels(ps.m_vertices[i]);
            xCoords.push(v.x);
            yCoords.push(v.y);
        }

        scribble.scribbleFilling(xCoords, yCoords, 3.5, 315);

        stroke(127);
        for (let i = 0; i < ps.m_count - 1; i++) {
            let v1 = scaleToPixels(ps.m_vertices[i]);
            let v2 = scaleToPixels(ps.m_vertices[i + 1]);
            scribble.scribbleLine(v1.x, v1.y, v2.x, v2.y);
        }
        let count = ps.m_count;
        let v1 = scaleToPixels(ps.m_vertices[count - 1]);
        let v2 = scaleToPixels(ps.m_vertices[0]);
        scribble.scribbleLine(v1.x, v1.y, v2.x, v2.y);

        pop();
    }
}
