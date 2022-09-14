function displayGrid(ctx) {
    for (var i = 0; i < rows; i++) {
        for (var j = 0; j < columns; j++) {
            var x =  (j * size);
            var y =  (i * size);
            ctx.strokeRect(x, y, size, size);
        }
    }
    ctx.strokeStyle = "black";
    ctx.stroke();
}