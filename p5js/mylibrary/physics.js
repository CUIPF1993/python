
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
