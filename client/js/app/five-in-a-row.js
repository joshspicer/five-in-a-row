var ctx, canvas;

var rows = 19;
var columns = 19;
var size = 50;

function mapClickToGrid(x, y) {
  xx = Math.floor(x / size);
  yy = Math.floor(y / size);
  console.log(xx, yy);
  return {xIdx: xx,  yIdx: yy }
}

function fillRect(tile, color) {
  ctx.fillStyle = "black";
  ctx.fillRect(tile['xIdx'] * size, tile['yIdx'] * size, size, size);
}

function loadGame() {
  canvas = document.getElementById("gameCanvas");
  ctx = canvas.getContext("2d");
  displayGrid(ctx);
  
  canvas.onmousedown = function(event){
    console.log("x: " + event.offsetX + " y: " + event.offsetY);
    const tile = mapClickToGrid(event.offsetX - 10, event.offsetY - 10);
    fillRect(tile, "red");
  };
}

