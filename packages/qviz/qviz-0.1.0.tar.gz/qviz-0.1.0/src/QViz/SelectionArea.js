import {
    //Frustum,
    //Vector3,
    Vector2
} from "three";

class SelectionArea {


    constructor(selectionBox, renderer, cssClassName) {

        this.element = document.createElement('div');
        this.element.classList.add(cssClassName);
        this.element.style.pointerEvents = 'none';

        this.renderer = renderer;

        this.startPoint = new Vector2();
        this.pointTopLeft = new Vector2();
        this.pointBottomRight = new Vector2();

        this.isDown = false;
        this.mdown = (event) => {
            this.isDown = true;
            this.onSelectStart(event);
        };
        this.mmove = (event) => {
            if (this.isDown) {
                this.onSelectMove(event);
            }
        };
        this.mup = (event) => {
            this.isDown = false;
            this.onSelectOver(event);
        };

    }

    enable() {
        this.renderer.domElement.addEventListener('mousedown', this.mdown, false);

        this.renderer.domElement.addEventListener('mousemove', this.mmove, false);

        this.renderer.domElement.addEventListener('mouseup', this.mup, false);
    }

    disable() {
        this.renderer.domElement.removeEventListener('mousedown', this.mdown);

        this.renderer.domElement.removeEventListener('mousemove', this.mmove);

        this.renderer.domElement.removeEventListener('mouseup', this.mup);
    }

    onSelectStart(event) {

        const parent = this.renderer.domElement.parentElement;
        parent.appendChild(this.element);
        //const {top, left} = parent.getBoundingClientRect();
        this.element.style.left = (event.offsetX) + 'px';
        this.element.style.top = (event.offsetY) + 'px';
        this.element.style.width = '10px';
        this.element.style.height = '10px';

        this.startPoint.x = event.offsetX;
        this.startPoint.y = event.offsetY;

    };

    onSelectMove(event) {

        this.pointBottomRight.x = Math.max(this.startPoint.x, event.offsetX);
        this.pointBottomRight.y = Math.max(this.startPoint.y, event.offsetY);
        this.pointTopLeft.x = Math.min(this.startPoint.x, event.offsetX);
        this.pointTopLeft.y = Math.min(this.startPoint.y, event.offsetY);

        this.element.style.left = this.pointTopLeft.x + 'px';
        this.element.style.top = this.pointTopLeft.y + 'px';
        this.element.style.width = (this.pointBottomRight.x - this.pointTopLeft.x) + 'px';
        this.element.style.height = (this.pointBottomRight.y - this.pointTopLeft.y) + 'px';

    };

    onSelectOver() {

        this.element.parentElement.removeChild(this.element);
    }

}

export default SelectionArea;