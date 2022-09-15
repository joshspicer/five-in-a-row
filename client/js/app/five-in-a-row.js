var ctx, canvas;
var socket;

var rows = 19;
var columns = 19;
var size = 50;


const EMPTY = 0;
const BLACK = 1;
const BLUE = 2;

var state;

function mapClickToGrid(x, y) {
  xx = Math.floor(x / size);
  yy = Math.floor(y / size);
  console.log(xx, yy);
  return { xIdx: xx, yIdx: yy }
}

// Sends move to server
function tryCommitMove(tile) {
}

function displayMove(tile, color) {
  ctx.fillStyle = color;
  ctx.fillRect(tile['xIdx'] * size, tile['yIdx'] * size, size, size);
}

function updateBoard() {
  for (var i = 0; i < rows; i++) {
    for (var j = 0; j < columns; j++) {
      if (state.board[i][j] === BLACK) {
        displayMove({ xIdx: j, yIdx: i }, "black");
      } else if (state.board[i][j] === BLUE) {
        displayMove({ xIdx: j, yIdx: i }, "blue");
      }
    }
  }
}


function loadGame() {
  canvas = document.getElementById("gameCanvas");
  ctx = canvas.getContext("2d");
  displayGrid(ctx);

  // Set up WebSocket connection 
  var socket = io("ws://localhost:5000");

  // Event handler for new connections.
  // The callback function is invoked when a connection with the
  // server is established.
  socket.emit("join_game");

  socket.on("state", function (msg) {
    console.log("state: ", msg);
    state = msg
    updateBoard();
  });

  socket.on("accept_player", function (msg) {
    alert("You are player " + msg + "!");
  });

  socket.on("reject_player", function (msg) {
    alert("Rejected!");
  });


  canvas.onmousedown = function (event) {
    console.log("x: " + event.offsetX + " y: " + event.offsetY);
    const tile = mapClickToGrid(event.offsetX - 10, event.offsetY - 10);

    tryCommitMove(tile);
  };
}

