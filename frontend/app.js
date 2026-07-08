// ---- 1. Basic Three.js setup ----
const container = document.getElementById('canvas-container');

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
  75,
  container.clientWidth / container.clientHeight,
  0.1,
  1000
);
camera.position.z = 3;

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

// ---- 2. Create the avatar shape (an icosahedron = spiky-able sphere) ----
const geometry = new THREE.IcosahedronGeometry(1, 1); // radius 1, detail 1
const material = new THREE.MeshStandardMaterial({
  color: 0x7f5af0,
  flatShading: true,
  metalness: 0.3,
  roughness: 0.4
});
const avatar = new THREE.Mesh(geometry, material);
scene.add(avatar);

// ---- 3. Lighting (without light, MeshStandardMaterial looks black) ----
const light1 = new THREE.DirectionalLight(0xffffff, 1);
light1.position.set(5, 5, 5);
scene.add(light1);

const light2 = new THREE.AmbientLight(0x404040, 1.5);
scene.add(light2);

// ---- 4. Animation loop ----
function animate() {
  requestAnimationFrame(animate);

  avatar.rotation.x += 0.003;
  avatar.rotation.y += 0.005;

  renderer.render(scene, camera);
}
animate();

// ---- 5. Handle window resize ----
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});