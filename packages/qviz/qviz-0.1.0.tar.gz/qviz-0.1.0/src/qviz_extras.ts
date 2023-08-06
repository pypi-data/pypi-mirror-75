import * as THREE from "three"
import {OrbitControls} from "three/examples/jsm/controls/OrbitControls"
import {PointSource, QvizModel, SourceModel} from "./widget"
import {SelectionBox} from "three/examples/jsm/interactive/SelectionBox"
import * as dat from 'dat.gui'
import {TrackballControls} from "three/examples/jsm/controls/TrackballControls"
import ResizeObserver from 'resize-observer-polyfill'
// @ts-ignore
import chroma from "chroma-js"
//import Stats from "three/examples/jsm/libs/stats.module"
import {Mesh} from "three";

// @ts-ignore
const UNSELECTED_OPACITY = 0.2
const SELECTED_OPACITY = 1.0

interface PointMeta {
    source: SourceModel
    position: number
}

export class Qviz {
    private scene: THREE.Scene
    private renderer: THREE.WebGLRenderer
    private camera: THREE.PerspectiveCamera
    // @ts-ignore
    private raycaster: THREE.Raycaster
    private particles: THREE.Mesh[] = []
    // @ts-ignore
    private mouse: THREE.Vector2

    private controls: OrbitControls | TrackballControls
    private helper: SelectionArea
    public selectionMode = false
    private selectionBox: SelectionBox
    private eventsToRemove: RegisteredListener<any>[]
    public colorScale = chroma.scale(['green', 'red', 'navy']).mode('hsl')
    private model: QvizModel
    private highlighted_points: Mesh[] = []
    private tmp_selection: Mesh[] = []
    private particles_scale = 1


    constructor(destination: HTMLElement, model: QvizModel) {
        this.model = model


        this.scene = new THREE.Scene()
        // @ts-ignore
        window.debug_handler = this

        this.camera = new THREE.PerspectiveCamera(45, destination.clientWidth / destination.clientHeight, 1, 10000)
        const axesHelper = new THREE.AxesHelper(100)
        this.scene.add(axesHelper)
        this.camera.position.z = 250

        //


        this.renderer = new THREE.WebGLRenderer({alpha: true, antialias: true})
        this.renderer.setPixelRatio(window.devicePixelRatio)


        this.raycaster = new THREE.Raycaster()
        this.mouse = new THREE.Vector2()
        //

        //stats =
        //destination.appendChild(Stats().dom)

        //
        const gui = new dat.GUI({autoPlace: false})
        gui.add(this, "selectionMode").onFinishChange((newValue) => {
            console.log("SelectionMode=", newValue)
            this.switchMode()
        })
        gui.add(this, "dropSelection")
        gui.add(this, "resetCamera")
        gui.add(this, "particles_scale", 0.1, 2).onChange(value => {
            this.particles.forEach(point => {
                const geom = point.geometry as THREE.SphereGeometry
                const scale = geom.parameters.radius * this.particles_scale
                point.scale.set(scale, scale, scale)
            })
            this.render()

        })
        destination.appendChild(gui.domElement)


        console.log("Qviz initialized")
        destination.appendChild(this.renderer.domElement)
        this.selectionBox = new SelectionBox(this.camera, this.scene)
        this.helper = new SelectionArea(this.renderer, "selectBox")
        this.switchMode()
        this.animate()

        window.addEventListener('resize', this.resizeRendererToDisplaySize.bind(this), false)

        const ro = new ResizeObserver(this.resizeRendererToDisplaySize.bind(this))
        ro.observe(destination)
        this.resizeRendererToDisplaySize()

    }

    resetCamera() {
        this.controls.reset()
    }

    dropSelection() {
        this.model.set("_selected", {})
        this.model.save_changes()
        this.highlighted_points.forEach(item =>
            // @ts-ignore
            item.material.opacity = UNSELECTED_OPACITY
        )
        this.highlighted_points = []
        this.render()

    }

    switchMode() {
        const {selectionMode} = this
        const {controls, selectionBox, helper, renderer} = this

        if (selectionMode) {
            if (controls) {
                controls.dispose()
                delete this.controls
            }
            helper.enable()
            this.eventsToRemove = [
                {
                    name: 'mousedown',
                    callback: (event) => {
                        // @ts-ignore
                        const lx = event.layerX
                        // @ts-ignore
                        const ly = event.layerY
                        selectionBox.startPoint.set(
                            (lx / renderer.domElement.clientWidth) * 2 - 1,
                            -(ly / renderer.domElement.clientHeight) * 2 + 1,
                            0.5)
                    }
                },
                {
                    name: 'mousemove',
                    callback: (event) => {
                        if (helper.isDown) {
                            // @ts-ignore
                            const lx = event.layerX
                            // @ts-ignore
                            const ly = event.layerY
                            selectionBox.endPoint.set(
                                (lx / renderer.domElement.clientWidth) * 2 - 1,
                                -(ly / renderer.domElement.clientHeight) * 2 + 1,
                                0.5)

                            this.tmp_selection.forEach(item =>
                                // @ts-ignore
                                item.material.opacity = UNSELECTED_OPACITY
                            )
                            this.tmp_selection = selectionBox.select()
                            this.tmp_selection.forEach(item =>
                                // @ts-ignore
                                item.material.opacity = SELECTED_OPACITY
                            )

                            this.render()

                        }
                    }
                },
                {
                    name: 'mouseup',
                    callback: (event: MouseEvent) => {
                        // @ts-ignore
                        const lx = event.layerX
                        // @ts-ignore
                        const ly = event.layerY
                        selectionBox.endPoint.set(
                            (lx / renderer.domElement.clientWidth) * 2 - 1,
                            -(ly / renderer.domElement.clientHeight) * 2 + 1,
                            0.5)
                        this.highlighted_points = this.highlighted_points.concat(selectionBox.select())
                        this.tmp_selection.forEach(item =>
                            // @ts-ignore
                            item.material.opacity = UNSELECTED_OPACITY
                        )
                        this.tmp_selection = []
                        this.highlighted_points.forEach(item =>
                            // @ts-ignore
                            item.material.opacity = SELECTED_OPACITY
                        )


                        const source_positions = this.highlighted_points
                            .map(a => a.userData as PointMeta)
                            .map(a => (a.source.get("URI"), a))
                            .reduce<{ [key: string]: [SourceModel, any[]] }>(
                                (a, b) => {
                                    const uri = b.source.get("URI")
                                    const entry = a[uri] || [b.source, []]
                                    entry[1].push(b.position)
                                    a[uri] = entry
                                    return a
                                }, {}
                            )
                        console.log(source_positions)
                        const selected = Object.assign({}, this.model.get("_selected"))
                        Object.values(source_positions).forEach(
                            ([source, positions]) => {
                                const current_selection = selected[source.get("URI")] || []
                                current_selection.push(...positions)
                                selected[source.get("URI")] = [...new Set(current_selection)]
                            }
                        )
                        console.log(selected)
                        this.model.set("_selected", selected)
                        this.model.save_changes()
                        this.render()
                    }
                }
            ]

            this.eventsToRemove.forEach(a => {
                const {name, callback} = a
                this.renderer.domElement.addEventListener(name, callback)
            })


        } else {
            helper.disable()
            /* const controls = new TrackballControls(this.camera, renderer.domElement)
             controls.rotateSpeed = 1.2
             controls.zoomSpeed = 1.2
             controls.panSpeed = 1.2
             controls.noZoom = false
             controls.noPan = false
             controls.staticMoving = true
             controls.dynamicDampingFactor = 0.3
             controls.keys = [65, 83, 68]
             */
            const controls = new OrbitControls(this.camera, this.renderer.domElement)
            controls.enableDamping = false // an animation loop is required when either damping or auto-rotation are enabled
            //controls.dampingFactor = 0.05
            controls.screenSpacePanning = true

            //controls.minDistance = 100
            //controls.maxDistance = 500

            controls.maxPolarAngle = Math.PI / 2
            controls.addEventListener("change", this.render.bind(this))


            this.controls = controls
            if (this.eventsToRemove) {
                this.eventsToRemove.forEach(a => {
                    const {name, callback} = a
                    this.renderer.domElement.removeEventListener(name, callback)
                })
                delete this.eventsToRemove
            }
        }
    }


    resizeRendererToDisplaySize() {
        console.log("Called resizeRendererToDisplaySize ")
        const canvas = this.renderer.domElement
        const pixelRatio = window.devicePixelRatio
        const width = canvas.clientWidth * pixelRatio | 0
        const height = canvas.clientHeight * pixelRatio | 0
        const needResize = canvas.width !== width || canvas.height !== height
        if (needResize) {
            this.renderer.setSize(width, height, false)
            this.camera.aspect = canvas.clientWidth / canvas.clientHeight
            this.camera.updateProjectionMatrix()
        }
        if (this.controls) {
            this.controls.update()
        }
        this.render()

    }


    addData(points: PointSource, reset: Boolean = true): void {

        const geometry = new THREE.SphereGeometry(.3)
        if (reset) {
            this.scene.remove(...this.particles)
        }
        for (let i = 0, l = points.positions.length; i < l; i++) {

            const [x, y, z] = points.positions[i]
            const material = new THREE.MeshBasicMaterial({
                opacity: UNSELECTED_OPACITY,
                transparent: true,
                color: new THREE.Color(this.colorScale(points.colors[i]).toString())
            })

            // const [r, g, b] = points.colors[i]


            const cube = new THREE.Mesh(geometry, material)
            cube.userData = {
                source: points.source,
                position: points.index[i]
            }
            cube.position.set(x, y, z)
            this.scene.add(cube)
            this.particles.push(cube)


        }
        /*    const [targetX, targetY, targetZ] = points.positions.reduce(
                                 (totals, elem) => totals.map((v, i) => elem[i] + v)
                             ).map(a => Math.abs(a / points.positions.length));

                             //sthis.center.position.set(targetX, targetY, targetZ);
                             console.log(targetX, targetY, targetZ);
 */
        this.render()
    }

    /*    onDocumentMouseMove(event) {
            console.log("onDocumentMouseMove")

            event.preventDefault()

            this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1
            this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1

        }

   */


    animate() {
        //TODO check if we can remove this to avoid useless rendering
        // this.render()

    }

    render() {
        this.renderer.render(this.scene, this.camera)
    }


}

class SelectionArea {
    private readonly element: HTMLDivElement
    private readonly renderer: THREE.WebGLRenderer
    private startPoint: THREE.Vector2
    private pointTopLeft: THREE.Vector2
    private pointBottomRight: THREE.Vector2
    public isDown: boolean
    private readonly mdown: (event: MouseEvent) => void
    private readonly mmove: (event: MouseEvent) => void
    private readonly mup: (event: MouseEvent) => void


    constructor(renderer: THREE.WebGLRenderer, cssClassName: string) {

        this.element = document.createElement('div')
        this.element.classList.add(cssClassName)
        this.element.style.pointerEvents = 'none'

        this.renderer = renderer

        this.startPoint = new THREE.Vector2()
        this.pointTopLeft = new THREE.Vector2()
        this.pointBottomRight = new THREE.Vector2()

        this.isDown = false
        this.mdown = (event) => {
            this.isDown = true
            this.onSelectStart(event)
        }
        this.mmove = (event) => {
            if (this.isDown) {
                this.onSelectMove(event)
            }
        }
        this.mup = (event) => {
            this.isDown = false
            this.onSelectOver()
        }

    }

    enable() {
        this.renderer.domElement.addEventListener('mousedown', this.mdown, false)

        this.renderer.domElement.addEventListener('mousemove', this.mmove, false)

        this.renderer.domElement.addEventListener('mouseup', this.mup, false)
    }

    disable() {
        this.renderer.domElement.removeEventListener('mousedown', this.mdown)

        this.renderer.domElement.removeEventListener('mousemove', this.mmove)

        this.renderer.domElement.removeEventListener('mouseup', this.mup)
    }

    onSelectStart(event: MouseEvent) {

        const parent = this.renderer.domElement.parentElement
        if (parent) {
            parent.appendChild(this.element)
        } else {
            console.error("Elements ", this.renderer.domElement, " has not parent, I cannot add the canvas")
        }
        //const {top, left} = parent.getBoundingClientRect()
        this.element.style.left = (event.offsetX) + 'px'
        this.element.style.top = (event.offsetY) + 'px'
        this.element.style.width = '10px'
        this.element.style.height = '10px'

        this.startPoint.x = event.offsetX
        this.startPoint.y = event.offsetY

    }

    onSelectMove(event: MouseEvent) {

        this.pointBottomRight.x = Math.max(this.startPoint.x, event.offsetX)
        this.pointBottomRight.y = Math.max(this.startPoint.y, event.offsetY)
        this.pointTopLeft.x = Math.min(this.startPoint.x, event.offsetX)
        this.pointTopLeft.y = Math.min(this.startPoint.y, event.offsetY)

        this.element.style.left = this.pointTopLeft.x + 'px'
        this.element.style.top = this.pointTopLeft.y + 'px'
        this.element.style.width = (this.pointBottomRight.x - this.pointTopLeft.x) + 'px'
        this.element.style.height = (this.pointBottomRight.y - this.pointTopLeft.y) + 'px'

    }

    onSelectOver() {
        if (this.element.parentElement)
            this.element.parentElement.removeChild(this.element)
    }


}

interface RegisteredListener<K extends keyof DocumentEventMap> {
    name: K
    callback: EventListenerOrEventListenerObject


}
