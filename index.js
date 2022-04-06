img = new Image();
img.src = null;

rectangles = [];

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;

draw = () => {
  canvas.setAttribute("width", 800);
  canvas.setAttribute("height", 1000);

  if (img) {
    var hRatio = canvas.width / img.width;
    var vRatio = canvas.height / img.height;
    var ratio = Math.min(hRatio, vRatio);
    ctx.drawImage(
      img,
      0,
      0,
      img.width,
      img.height,
      0,
      0,
      img.width * ratio,
      img.height * ratio
    );
  }

  for (r of rectangles) {
    ctx.fillStyle = "rgba(0, 255, 0, 0.3)";
    ctx.strokeStyle = "rgba(0, 255, 0, 1)";
    ctx.fillRect(r.x, r.y, r.w, r.h);
    ctx.strokeRect(r.x, r.y, r.w, r.h);
  }
};

input = document.getElementById("input");

const round = (x) => {
  return Math.round(x * 10000) / 10000;
};

const mapRectangles = (rectangles) => {
  const w = img.width;
  const h = img.height;
  return rectangles.map((r) => {
    x1 = round(r.x / w);
    y1 = round(r.y / h);
    x2 = round((r.x + r.w) / w);
    y2 = round((r.y + r.h) / h);
    return {
      x1: Math.min(x1, x2),
      y1: Math.min(y1, y2),
      x2: Math.max(x1, x2),
      y2: Math.max(y1, y2),
    };
  });
};

const updateInput = () => {
  input.value = JSON.stringify(mapRectangles(rectangles));
};

let x = 0;
let y = 0;
let isDrawing = false;

canvas.addEventListener("mousedown", (e) => {
  x = e.offsetX;
  rectangles.push({
    x: e.offsetX,
    y: e.offsetY,
    w: 0,
    h: 0,
  });
  isDrawing = true;
});

canvas.addEventListener("mouseup", (e) => {
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
    last.w = e.offsetX - last.x;
    last.h = e.offsetY - last.y;
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

updateClipboard = (newClip) => {
  navigator.clipboard.writeText(newClip).then(
    () => {},
    () => {
      console.log("Failed to copy");
    }
  );
};

button = document.getElementById("copy");
button.addEventListener("click", () => {
  updateClipboard(JSON.stringify(mapRectangles(rectangles)));
});

resultDiv = document.getElementById("result");

file = document.getElementById("file");
file.addEventListener(
  "change",
  (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      img.src = e.target.result;
      rectangles = [];
      img.onload = draw;
      updateInput();
      resultDiv.style.display = "block";
    };
    reader.readAsDataURL(file);
  },
  false
);
