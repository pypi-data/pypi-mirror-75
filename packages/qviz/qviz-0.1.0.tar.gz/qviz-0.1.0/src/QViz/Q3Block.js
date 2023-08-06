import React, {PureComponent} from "react";
import * as THREE from "three";
import QDashBlock from "./QDashBlock";
import {SelectionBox} from "three/examples/jsm/interactive/SelectionBox";
import SelectionArea from "./SelectionArea";
import chroma from "chroma-js";
import {TrackballControls} from "three/examples/jsm/controls/TrackballControls";
import CircularProgress from "@material-ui/core/CircularProgress";
import Axios from "axios";

const UNSELECTED_OPACITY = 0.4;
const SELECTED_OPACITY = 1.0;
export default class Q3Block extends PureComponent {
    constructor(props) {
        super(props);
        const server = props.apiURL;
        console.log("LOADING Q3BLOCK", props);
        this.state = {ready: false};
        this.scene = new THREE.Scene();
        this.renderer = new THREE.WebGLRenderer({alpha: true});
        this.configCanvas = this.configCanvas.bind(this);
        this.colorMinMax = {};
        this.shouldRecolor = (force) => {
            const {color} = this.props;
            const colorScale = chroma.scale(['green', 'red', 'navy']).mode('hsl');

            if (force || this.previousColor !== color) {
                this.previousColor = color;
                const points = this.scene.children.filter(i => i.userData.isQdata);
                if (points.length > 0) {
                    if (!this.colorMinMax[color]) {
                        this.colorMinMax[color] = points.reduce((mm, item) => {
                            return {
                                min: Math.min(mm.min, item.userData[color]),
                                max: Math.max(mm.max, item.userData[color])
                            }
                        }, {min: Number.MAX_VALUE, max: Number.MIN_VALUE});
                    }
                    const {min, max} = this.colorMinMax[color];
                    const scale = 1.0 / (max - min);
                    points.forEach(i =>
                        i.material.color = new THREE.Color(colorScale((i.userData[color] - min) * scale).toString())
                    );
                }

            }
        };
        this.shouldReloadSample = () => {
            const {model, schema, space} = this.props;
            if (this.previousModel !== model) {
                this.colorMinMax = {};
                Axios.get(`${server}${model}/point/`)
                    .then(
                        (res) => {
                            const points = res.data;
                            const geometry = new THREE.SphereGeometry(.3);
                            //remove the old ones
                            this.scene.children.filter(i => i.userData.isQdata).forEach(i => this.scene.remove(i));
                            const [xname, yname, zname] = schema.spaces[space];
                            points.forEach(point => {
                                const x = point[xname];
                                const y = point[yname];
                                const z = point[zname];
                                const material = new THREE.MeshBasicMaterial({
                                    opacity: UNSELECTED_OPACITY,
                                    transparent: true
                                });
                                point.isQdata = true;
                                const cube = new THREE.Mesh(geometry, material);
                                cube.userData = point;
                                cube.position.set(x, y, z);
                                this.scene.add(cube);
                            });
                            this.shouldRecolor(true);
                            const [targetX, targetY, targetZ] = points.map(a => [a.x, a.y, a.z]).reduce(
                                (totals, elem) => totals.map((v, i) => elem[i] + v)
                            ).map(a => Math.abs(a / points.length));

                            //sthis.center.position.set(targetX, targetY, targetZ);
                            console.log(targetX, targetY, targetZ);
                            this.setState({loading: false});


                        }
                        ,

                        (error) => {
                            this.setState({
                                isLoaded: true,
                                msg: error
                            });
                        }
                    );

                this.previousModel = model;
                this.setState({loading: true});
                return true;
            }
            return false;
        };
    }


    componentDidMount() {
        const {scene, renderer} = this;
        const canvas = renderer.domElement;
        const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
        const axesHelper = new THREE.AxesHelper(100);
        scene.add(axesHelper);


        console.log(camera);
        this.camera = camera;
        camera.position.z = 20;

        function resizeRendererToDisplaySize() {

            const pixelRatio = window.devicePixelRatio;
            const width = canvas.clientWidth * pixelRatio | 0;
            const height = canvas.clientHeight * pixelRatio | 0;
            const needResize = canvas.width !== width || canvas.height !== height;
            if (needResize) {
                renderer.setSize(width, height, false);
                camera.aspect = canvas.clientWidth / canvas.clientHeight;
                camera.updateProjectionMatrix();
            }

        }

        const animate = () => {
            resizeRendererToDisplaySize();
            requestAnimationFrame(animate);
            if (this.controls) {
                this.controls.update();
            }
            renderer.render(scene, camera);
        };
        animate();
        this.selectionBox = new SelectionBox(camera, scene);
        this.helper = new SelectionArea(this.selectionBox, renderer, 'selectBox');
        const raycaster = new THREE.Raycaster();

        const onDocumentMouseClick = (event) => {
            event.preventDefault();
            const mouse = new THREE.Vector2();
            mouse.x = (event.clientX / renderer.domElement.clientWidth) * 2 - 1;
            mouse.y = -(event.clientY / renderer.domElement.clientHeight) * 2 + 1;
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(scene.children);
            if (intersects.length > 0) {
                console.log(intersects);
                this.props.updateSelection(intersects);
            }
        };

        document.addEventListener('dblclick', onDocumentMouseClick, false);
        this.setState({ready: true})


    }

    shouldSwitchMode() {
        const {inSelectMode, updateSelection} = this.props;
        const {controls, selectionBox, helper, camera, renderer, previousMode} = this;
        if (previousMode !== inSelectMode) {
            this.previousMode = inSelectMode;
            if (inSelectMode) {
                if (controls) {
                    controls.dispose();
                    delete this.controls;
                }
                helper.enable();
                this.eventsToRemove = [
                    ['mousedown', (event) => {
                        selectionBox.startPoint.set(
                            (event.layerX / renderer.domElement.clientWidth) * 2 - 1,
                            -(event.layerY / renderer.domElement.clientHeight) * 2 + 1,
                            0.5);
                    }],
                    ['mousemove', (event) => {
                        if (helper.isDown) {
                            selectionBox.endPoint.set(
                                (event.layerX / renderer.domElement.clientWidth) * 2 - 1,
                                -(event.layerY / renderer.domElement.clientHeight) * 2 + 1,
                                0.5);

                            selectionBox.select().forEach(item =>
                                item.material.opacity = SELECTED_OPACITY
                            );

                        }
                    }],
                    ['mouseup', (event) => {
                        selectionBox.endPoint.set(
                            (event.layerX / renderer.domElement.clientWidth) * 2 - 1,
                            -(event.layerY / renderer.domElement.clientHeight) * 2 + 1,
                            0.5);
                        const allSelected = selectionBox.select();
                        console.log("mouseup,upload selection");
                        updateSelection(allSelected);

                        allSelected.forEach(item =>
                            item.material.opacity = SELECTED_OPACITY
                        );
                    }]
                ]
                ;
                this.eventsToRemove.forEach(a => {
                    const [eventName, listener] = a;
                    document.addEventListener(eventName, listener);
                });


            } else {
                helper.disable();
                const controls = new TrackballControls(camera, renderer.domElement);
                controls.rotateSpeed = 1.2;
                controls.zoomSpeed = 1.2;
                controls.panSpeed = 1.2;
                controls.noZoom = false;
                controls.noPan = false;
                controls.staticMoving = true;
                controls.dynamicDampingFactor = 0.3;
                controls.keys = [65, 83, 68];

                this.controls = controls;
                if (this.eventsToRemove) {
                    this.eventsToRemove.forEach(a => {
                        const [eventName, listener] = a;
                        document.removeEventListener(eventName, listener);
                    });
                    delete this.eventsToRemove;
                }
            }
        }
    }

    configCanvas(ref) {

        if (ref) {
            this.mount = ref;
            this.mount.appendChild(this.renderer.domElement);
        }

    }

    render() {
        const {ready, loading} = this.state;
        if (ready) {
            if (!this.shouldReloadSample()) {
                this.shouldRecolor();
            }
            this.shouldSwitchMode();


        }


        return (
            <QDashBlock name="3D Explorer">
                {loading ? <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    height: '100%',
                    width: '100%'
                }}><CircularProgress/></div> : undefined}
                <div className="Qviz-canvas" ref={this.configCanvas}/>
            </QDashBlock>);


    }


}