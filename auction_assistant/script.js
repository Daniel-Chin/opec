const NATIONS = ['Saudi', 'Iran', 'Venezuela', 'Iraq'];

const generateTable = () => {
  const table = document.getElementById('table');
  const newRow = () => (document.createElement('tr'))
  const newCell = () => (document.createElement('th'))
  const first_row = newRow();
  table.appendChild(first_row);
  first_row.appendChild(newCell());
  NATIONS.forEach((x) => {
    const cell = newCell();
    cell.innerHTML = x;
    first_row.appendChild(cell);
  });
  [...'ABC'].forEach((x) => {
    const row = newRow();
    table.appendChild(row);
    const nameCell = newCell();
    row.appendChild(nameCell);
    nameCell.innerHTML = 'Market ' + x;
    NATIONS.forEach((nation) => {
      const cell = newCell();
      row.appendChild(cell);
      cell.id = `cell-${x}-${nation}`;
    });
  });
};

const onSlider = ({ target }) => {
  document.getElementById('valueDisplay').innerHTML = target.value;
  updateValuation(target.value / 100);
};

window.onload = () => {
  generateTable();
  const slider = document.getElementById("slider");
  slider.oninput = onSlider;
  onSlider({ target: slider });
};

const DATA = {
  A:   [ 3768, 521, 386, 100 ], 
  B:   [ 3791, 522, 389, 100 ], 
  BBC: [ 3748, 502, 367, null ], 
};

const updateValuation = (ratio) => {
  const twoSides = {
    A: ['A', 'B'], 
    B: ['A', 'BBC'], 
    C: ['A', 'BBC'], 
  };
  const mask = [1 - ratio, ratio];
  [...'ABC'].forEach((market) => {
    NATIONS.forEach((nation, j) => {
      const cell = document.getElementById(
        `cell-${market}-${nation}`
      );
      if (market !== 'A' && nation === 'Iraq') {
        cell.innerHTML = 'N/A';
        return;
      }
      const value = twoSides[market].map((scene, i) => (
        DATA[scene][j] * mask[i]
      )).reduce((x, y) => (x + y));
      cell.innerHTML = value.toFixed(0);
    });
  });
};
