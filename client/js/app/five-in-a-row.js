var ctx, canvas;

var rows = 19;
var columns = 19;
var size = 50;

const EMPTY = 0;
const BLACK = 1;
const WHITE = 2;

const initial_state = {
  board: new Array(rows).fill(new Array(columns).fill(EMPTY)),
  turn: BLACK,
}

var state;

function mapClickToGrid(x, y) {
  xx = Math.floor(x / size);
  yy = Math.floor(y / size);
  console.log(xx, yy);
  return {xIdx: xx,  yIdx: yy }
}

// POSTs move to server
function tryCommitMove(tile) {

  // POST to server
  const url = "http://localhost:5000/checkMove";
  const data = {tile: tile, turn: state.turn};
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  };
  fetch(url, options)
    .then(res => {
      res.json().then(data => {
        console.log(data);
      });

      // Update the global state.
      // console.log(state);
      return true;
    })
}

function displayMove(tile) {
  ctx.fillStyle = state.turn === BLACK ? "black" : "white";
  ctx.fillRect(tile['xIdx'] * size, tile['yIdx'] * size, size, size);
}

function loadGame() {
  canvas = document.getElementById("gameCanvas");
  ctx = canvas.getContext("2d");
  displayGrid(ctx);
  state = initial_state;
  console.log(state);
  
  canvas.onmousedown = function(event) {
    console.log("x: " + event.offsetX + " y: " + event.offsetY);
    const tile = mapClickToGrid(event.offsetX - 10, event.offsetY - 10);
    
    tryCommitMove(tile);
  };
}

