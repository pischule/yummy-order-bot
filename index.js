const img = new Image();

const container = document.getElementById("container");
const canvas = document.getElementById("canvas");
const resultDiv = document.getElementById("result");
const file = document.getElementById("file");
const input = document.getElementById("input");
const button = document.getElementById("copy");
const ctx = canvas.getContext("2d");

canvas.width = container.clientWidth;

let x = 0;
let y = 0;
let isDrawing = false;
let ratio = 1;

let rectangles = [];

function getMousePos(canvas, evt) {
  const rect = canvas.getBoundingClientRect();
  return {
    x: ((evt.clientX - rect.left) / (rect.right - rect.left)) * canvas.width,
    y: ((evt.clientY - rect.top) / (rect.bottom - rect.top)) * canvas.height,
  };
}

function initImage() {
  canvas.width = container.clientWidth;
  ratio = canvas.width / img.width;
  canvas.height = img.height * ratio;
  draw();
}

function draw() {
  // prettier-ignore
  ctx.drawImage(img,
    0, 0, img.width, img.height,
    0, 0, img.width * ratio, img.height * ratio
  );

  for (r of rectangles) {
    ctx.fillStyle = "rgba(255, 221, 75, 0.5)";
    ctx.fillRect(r.x, r.y, r.w, r.h);
  }
}

function round(x) {
  return Math.round(x * 100000) / 100000;
}

function mapRectangles(rectangles) {
  const w = img.width * ratio;
  const h = img.height * ratio;
  return rectangles.map((r) => {
    const x1 = round(r.x / w);
    const y1 = round(r.y / h);
    const x2 = round((r.x + r.w) / w);
    const y2 = round((r.y + r.h) / h);
    return [
      Math.min(x1, x2),
      Math.min(y1, y2),
      Math.max(x1, x2),
      Math.max(y1, y2),
    ];
  });
}

function updateInput() {
  input.value = JSON.stringify(mapRectangles(rectangles));
}

canvas.addEventListener("mousedown", (e) => {
  if (e.button !== 0) {
    return;
  }
  pos = getMousePos(canvas, e);
  rectangles.push({
    x: pos.x,
    y: pos.y,
    w: 0,
    h: 0,
  });
  isDrawing = true;
});

canvas.addEventListener("mouseup", (e) => {
  if (e.button !== 0) {
    return;
  }
  x = 0;
  y = 0;
  isDrawing = false;
  updateInput();
});

canvas.addEventListener("mousemove", (e) => {
  if (!isDrawing) {
    return;
  }

  last = rectangles[rectangles.length - 1];
  if (last) {
    const { x, y } = getMousePos(canvas, e);
    last.w = x - last.x;
    last.h = y - last.y;
  }
  draw();
});

window.addEventListener("keydown", (e) => {
  if (e.key == "Backspace" || e.key == "Delete") {
    rectangles.pop();
    draw();
    updateInput();
  }
});

function updateClipboard(newClip) {
  navigator.clipboard.writeText(newClip).then(
    () => {},
    () => {
      console.log("Failed to copy");
    }
  );
}

button.addEventListener("click", () => {
  updateClipboard(JSON.stringify(mapRectangles(rectangles)));
});

file.addEventListener(
  "change",
  (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      img.src = e.target.result;
      rectangles = [];
      img.onload = initImage;
      updateInput();
    };
    result.classList.remove("invisible");
    reader.readAsDataURL(file);
  },
  false
);

window.onresize = initImage;
