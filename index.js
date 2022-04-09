const img = new Image();

const container = document.getElementById("container");
const canvas = document.getElementById("canvas");
const resultDiv = document.getElementById("result");
const file = document.getElementById("file");
const input = document.getElementById("input");
const button = document.getElementById("copy");
const ctx = canvas.getContext("2d");

let x = 0;
let y = 0;
let isDrawing = false;
let movingIndex = -1;
let ratio = 1;
let rectangles = [];
let lastPos = null;

function rect2canvas(r) {
  return {
    x: r.x * canvas.width,
    y: r.y * canvas.height,
    w: r.w * canvas.width,
    h: r.h * canvas.height,
  };
}

function initImage() {
  const cs = getComputedStyle(container);
  const paddingX = parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight);
  const borderX = parseFloat(cs.borderLeftWidth) + parseFloat(cs.borderRightWidth);
  canvas.width = container.clientWidth - paddingX - borderX;
  ratio = canvas.width / img.width;
  canvas.height = img.height * ratio;
  draw();
}

function draw() {
  // prettier-ignore
  ctx.drawImage(img,
    0, 0, img.width, img.height,
    0, 0, canvas.width, canvas.height
  );

  for (r of rectangles) {
    ctx.fillStyle = "rgba(255, 221, 75, 0.5)";
    const cr = rect2canvas(r);
    ctx.fillRect(cr.x, cr.y, cr.w, cr.h);
  }
}

function round(x) {
  return Math.round(x * 100000) / 100000;
}

function mapRectangles(rectangles) {
  return rectangles.map(normalizeRectangle).map((r) => {
    return [r.x, r.y, r.x + r.w, r.y + r.h].map(round);
  });
}

function updateInput() {
  input.value = JSON.stringify(mapRectangles(rectangles));
}

function mousePos(e) {
  const rect = canvas.getBoundingClientRect();
  return {
    x: (e.clientX - rect.left) / (rect.right - rect.left),
    y: (e.clientY - rect.top) / (rect.bottom - rect.top),
  };
}

canvas.addEventListener("mousedown", (e) => {
  if (e.button !== 0) {
    return;
  }
  lastPos = mousePos(e);
  const index = rectIndex(lastPos.x, lastPos.y);
  if (index >= 0) {
    isMoving = true;
    // move to top
    r = rectangles[index];
    rectangles.splice(index, 1);
    rectangles.push(r);
  } else {
    isDrawing = true;
    rectangles.push({
      x: lastPos.x,
      y: lastPos.y,
      w: 0,
      h: 0,
    });
  }
});

canvas.addEventListener("mouseup", (e) => {
  if (e.button !== 0) {
    return;
  }
  x = 0;
  y = 0;
  isDrawing = false;
  isMoving = false;
  lastPos = null;
  updateInput();
});

canvas.addEventListener("mousemove", (e) => {
  last = rectangles[rectangles.length - 1];
  if (!last) {
    return;
  }
  const { x, y } = mousePos(e);
  if (isDrawing) {
    last.w = x - last.x;
    last.h = y - last.y;
  } else if (isMoving) {
    last.x += x - lastPos.x;
    last.y += y - lastPos.y;
  }
  lastPos = { x, y };
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

function normalizeRectangle(r) {
  return {
    x: Math.min(r.x, r.x + r.w),
    y: Math.min(r.y, r.y + r.h),
    w: Math.abs(r.w),
    h: Math.abs(r.h),
  };
}

function rectIndex(x, y) {
  for (let i = rectangles.length - 1; i >= 0; i--) {
    const r = rectangles[i];
    const nr = normalizeRectangle(r);
    if (x >= nr.x && x <= nr.x + nr.w && y >= nr.y && y <= nr.y + nr.h) {
      return i;
    }
  }
  return -1;
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

input.addEventListener("keyup", (e) => {
  if (e.key == "Enter") {
    try {
      rectangles = JSON.parse(input.value);
      rectangles = rectangles.map((r) => {
        return {
          x: r[0],
          y: r[1],
          w: r[2] - r[0],
          h: r[3] - r[1],
        };
      });
      draw();
    } catch (e) {
      console.log(e);
    }
  }
});

window.onresize = initImage;
