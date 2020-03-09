const NATIONS = ['Saudi', 'Iran', 'Venezuela', 'Iraq'];
var scenario = null;
var greed = null;
var recommend = .4;
const drift = .427;

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
      if (! isNonStrategic(x, nation)) {
        cell.classList.add('hoverGray');
        cell.onclick = onClick.bind(null, cell, x, nation);
      }
    });
  });
};

const onSlider = ({ target }) => {
  document.getElementById('valueDisplay').innerHTML = target.value;
  scenario = target.value / 100;
  updateValuation();
};

const onGreeder = ({ target }) => {
  greed = target.value / 100;
  updateGreedDisplay();
  updateValuation();
};

const formatPercent = (value) => (
  `${Math.round(value * 100)}%`
);

const updateGreedDisplay = () => {
  const d = document.getElementById('greedDisplay');
  d.innerHTML = `${formatPercent(greed)} (Recommend ${formatPercent(recommend)})`;
};

window.onload = () => {
  generateTable();
  const slider = document.getElementById("slider");
  slider.oninput = onSlider;
  onSlider({ target: slider });
  const greeder = document.getElementById("greeder");
  greeder.oninput = onGreeder;
  onGreeder({ target: greeder });
};

const DATA = {
  A:   [ 3768, 521, 386, 100 ], 
  B:   [ 3791, 522, 389, 100 ], 
  BBC: [ 3748, 502, 367, null ], 
};

const updateValuation = () => {
  const twoSides = {
    A: ['A', 'B'], 
    B: ['A', 'BBC'], 
    C: ['A', 'BBC'], 
  };
  const mask = [1 - scenario, scenario];
  [...'ABC'].forEach((market) => {
    NATIONS.forEach((nation, j) => {
      const cell = document.getElementById(
        `cell-${market}-${nation}`
      );
      if (cell.classList.contains('sold')) return;
      if (isNonStrategic(market, nation)) {
        cell.innerHTML = 'N/A';
        return;
      }
      let value = twoSides[market].map((scene, i) => (
        DATA[scene][j] * mask[i]
      )).reduce((x, y) => (x + y));
      value = value * (1 - greed) + 100 * greed;
      cell.innerHTML = value.toFixed(0);
    });
  });
};

const onClick = (cell, market, nation) => {
  const saved_greed = greed;
  greed = 0;
  updateValuation();
  const ref_price = parseInt(cell.innerHTML);
  greed = saved_greed;
  updateValuation();
  const op = prompt(`Market ${market} ${nation} sold at:`, ref_price);
  if (op === null) return;
  const price = parseInt(op);
  cell.innerHTML = price;
  cell.classList.remove('hoverGray');
  cell.classList.add('sold');
  const this_greed = 1 - (price - 100) / (ref_price - 100);
  recommend = recommend * (1 - drift) + this_greed * drift;
  recommend = Math.max(0, recommend);
  updateGreedDisplay();
};

const isNonStrategic = (market, nation) => (
  market !== 'A' && nation === 'Iraq'
);
