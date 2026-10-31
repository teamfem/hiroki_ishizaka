/* Exact mathematical model for the introductory linear-algebra lesson.
   No numerical eigenvalue routine is used: results follow from the matrix family. */
(function (root) {
  'use strict';
  function matrix(t) {
    if (!Number.isFinite(t)) throw new TypeError('t must be finite');
    return [[1, t], [0, 1]];
  }
  function apply(t, point) {
    if (!Array.isArray(point) || point.length !== 2 ||
        !Object.prototype.hasOwnProperty.call(point, 0) ||
        !Object.prototype.hasOwnProperty.call(point, 1) ||
        !Number.isFinite(point[0]) || !Number.isFinite(point[1])) {
      throw new TypeError('point must be a finite 2-vector');
    }
    const A = matrix(t);
    return [A[0][0] * point[0] + A[0][1] * point[1],
            A[1][0] * point[0] + A[1][1] * point[1]];
  }
  function determinant(t) {
    const A = matrix(t);
    return A[0][0] * A[1][1] - A[0][1] * A[1][0];
  }
  function eigenspaceDimensionAtOne(t) {
    matrix(t);
    return t === 0 ? 2 : 1;
  }
  // The lesson state separates a student's prediction from the exact result.
  function createLesson(initialT = 1) {
    function validateParameter(value) {
      matrix(value);
      if (value < -2 || value > 2) throw new RangeError('lesson t must be between -2 and 2');
    }
    validateParameter(initialT);
    let t = initialT, prediction = null, result = null, proofStep = 0;
    function getState() {
      return Object.freeze({
        t,
        prediction: prediction && Object.freeze({ ...prediction }),
        result: result && Object.freeze({ ...result }),
        proofStep
      });
    }
    function setParameter(value) {
      validateParameter(value);
      t = value;
      prediction = null;
      result = null;
      proofStep = 0;
      return getState();
    }
    function predict(dimension, diagonalizable) {
      if (dimension !== 1 && dimension !== 2) throw new TypeError('prediction dimension must be 1 or 2');
      if (typeof diagonalizable !== 'boolean') throw new TypeError('prediction diagonalizable must be boolean');
      if (result) throw new Error('change t or reset before making a new prediction');
      const actualDimension = eigenspaceDimensionAtOne(t);
      prediction = { dimension, diagonalizable };
      result = {
        dimension: actualDimension,
        diagonalizable: actualDimension === 2,
        dimensionCorrect: dimension === actualDimension,
        diagonalizableCorrect: diagonalizable === (actualDimension === 2)
      };
      return getState();
    }
    function nextProofStep() {
      if (!result) throw new Error('confirm a prediction before opening the proof');
      proofStep = Math.min(3, proofStep + 1);
      return getState();
    }
    function reset() { return setParameter(0); }
    return Object.freeze({ getState, setParameter, predict, nextProofStep, reset });
  }

  // UI and SVG rendering use the exact model above, without an eigenvalue solver.
  function mountLesson(document) {
    const form = document.getElementById('prediction-form');
    if (!form || form.dataset.shearMounted) return null;
    form.dataset.shearMounted = 'true';
    const byId = id => document.getElementById(id);
    const slider = byId('parameter');
    const lesson = createLesson(Number(slider.value));
    const radios = [...form.querySelectorAll('input[type="radio"]')];
    const diagrams = [byId('diagram-in'), byId('diagram-out')];
    const ns = 'http://www.w3.org/2000/svg';
    // The square's image lies in [-2,3] × [0,1]. Both fixed viewBoxes have
    // bounds ±168 and the same scale, leaving at least 24 SVG units of margin.
    const scale = 48;
    function element(name, attributes, parent, text) {
      const node = document.createElementNS(ns, name);
      for (const key in attributes) node.setAttribute(key, String(attributes[key]));
      if (text !== undefined) node.textContent = text;
      parent.appendChild(node);
      return node;
    }
    function point(t, x, y) {
      const image = apply(t, [x, y]);
      return [scale * image[0], -scale * image[1]];
    }
    function line(parent, t, x1, y1, x2, y2, attributes) {
      const a = point(t, x1, y1), b = point(t, x2, y2);
      return element('line', { x1: a[0], y1: a[1], x2: b[0], y2: b[1], ...attributes }, parent);
    }
    function clearDrawing(svg) {
      const drawing = svg.querySelector('[data-drawing]');
      if (drawing) drawing.remove();
      const description = svg.querySelector('desc');
      if (description) description.textContent = '予想を確定すると、基底ベクトルとその像を表示します。';
    }
    function draw(svg, t, transformed) {
      clearDrawing(svg);
      const drawing = element('g', { 'data-drawing': '' }, svg);
      const defs = element('defs', {}, drawing);
      for (const [name, color] of [['e1', '#a44b17'], ['e2', '#146a9e']]) {
        const marker = element('marker', {
          id: svg.id + '-' + name + '-arrow', viewBox: '0 0 10 10',
          refX: 9, refY: 5, markerWidth: 5, markerHeight: 5,
          orient: 'auto', markerUnits: 'userSpaceOnUse'
        }, defs);
        element('path', { d: 'M 0 0 L 10 5 L 0 10 z', fill: color }, marker);
      }
      if (transformed && t === 0) {
        element('rect', {
          x: -168, y: -168, width: 336, height: 336,
          fill: '#8957b1', 'fill-opacity': .13, 'data-eigenspace': 'plane'
        }, drawing);
      }
      for (let k = -3; k <= 3; k++) {
        line(drawing, 0, k, -3, k, 3, { stroke: '#9aa9b7', 'stroke-width': .7, 'stroke-opacity': .6, 'stroke-dasharray': '3 4' });
        line(drawing, 0, -3, k, 3, k, { stroke: '#9aa9b7', 'stroke-width': .7, 'stroke-opacity': .6, 'stroke-dasharray': '3 4' });
        if (transformed) {
          line(drawing, t, k, -3, k, 3, { stroke: '#2675a8', 'stroke-width': .9, 'stroke-opacity': .45 });
          line(drawing, t, -3, k, 3, k, { stroke: '#2675a8', 'stroke-width': .9, 'stroke-opacity': .45 });
        }
      }
      if (transformed && t !== 0) {
        element('line', {
          x1: -160, y1: 0, x2: 160, y2: 0, stroke: '#75449c',
          'stroke-width': 5, 'stroke-opacity': .65, 'data-eigenspace': 'line'
        }, drawing);
      }
      element('line', { x1: -160, y1: 0, x2: 160, y2: 0, stroke: '#63717f', 'stroke-width': .9 }, drawing);
      element('line', { x1: 0, y1: -160, x2: 0, y2: 160, stroke: '#63717f', 'stroke-width': .9 }, drawing);
      element('text', { x: 151, y: 16, 'font-size': 11, fill: '#42556a' }, drawing, 'x');
      element('text', { x: 8, y: -151, 'font-size': 11, fill: '#42556a' }, drawing, 'y');
      const corners = [[0, 0], [1, 0], [1, 1], [0, 1]];
      element('polygon', {
        points: corners.map(p => point(t, p[0], p[1]).join(',')).join(' '),
        fill: '#88bee2', 'fill-opacity': .5, stroke: '#186a9e', 'stroke-width': 2
      }, drawing);
      for (const [index, color] of [[1, '#a44b17'], [2, '#146a9e']]) {
        const basis = index === 1 ? [1, 0] : [0, 1];
        const tip = point(t, basis[0], basis[1]);
        const key = transformed ? 'Ae' + index : 'e' + index;
        line(drawing, t, 0, 0, basis[0], basis[1], {
          stroke: color, 'stroke-width': 3,
          'stroke-dasharray': transformed ? '6 3' : '',
          'marker-end': 'url(#' + svg.id + '-e' + index + '-arrow)', 'data-vector': key
        });
        let x = tip[0] + 8, y = tip[1] - 8, anchor = 'start';
        if (index === 1) y = 16;
        if (index === 2 && transformed) {
          anchor = tip[0] >= 0 ? 'end' : 'start';
          x = tip[0] >= 0 ? Math.min(154, tip[0] + 24) : Math.max(-154, tip[0] - 24);
          y = tip[1] - 12;
        }
        element('text', {
          x, y, 'text-anchor': anchor, 'font-size': 14, 'font-weight': 700,
          class: 'vector-label',
          fill: color, 'data-vector-label': key
        }, drawing, (transformed ? 'A(t)' : '') + 'e' + (index === 1 ? '₁' : '₂'));
      }
      element('circle', { cx: 0, cy: 0, r: 3, fill: '#24364a' }, drawing);
      const description = svg.querySelector('desc');
      if (description) description.textContent = transformed
        ? 'A(t)e₁=(1,0)、A(t)e₂=(' + t.toFixed(1) + ',1)。' + (t === 0
          ? '紫色は固有空間である全平面のうち、表示窓に入る一部です。'
          : '紫色の第1座標軸は、正負両方向へ続く固有空間の一部です。')
        : '元の単位正方形と、実線の基底ベクトルe₁=(1,0)、e₂=(0,1)。';
    }
    function render() {
      const state = lesson.getState();
      const confirmed = !!state.result;
      if (!confirmed) form.reset();
      slider.value = String(state.t);
      byId('t-value').value = state.t.toFixed(1);
      byId('t-value').textContent = state.t.toFixed(1);
      byId('matrix').textContent = 'A(' + state.t.toFixed(1) + ') = [[1, ' + state.t.toFixed(1) + '], [0, 1]]';
      byId('observation').hidden = !confirmed;
      byId('proof').hidden = !confirmed;
      for (const radio of radios) radio.disabled = confirmed;
      byId('confirm-prediction').disabled = confirmed;
      byId('dimension').textContent = confirmed ? String(state.result.dimension) : '';
      byId('verdict').textContent = confirmed ? (state.result.diagonalizable ? '可能' : '不可能') : '';
      byId('prediction-feedback').textContent = confirmed
        ? 'あなたの予想：次元' + state.prediction.dimension + '、対角化' + (state.prediction.diagonalizable ? '可能' : '不可能') + '。' +
          '次元の予想は' + (state.result.dimensionCorrect ? '一致しました' : '一致しませんでした') + '。' +
          '対角化の予想は' + (state.result.diagonalizableCorrect ? '一致しました' : '一致しませんでした') + '。図と証明を使って理由を説明しましょう。'
        : '';
      byId('eigenspace-description').textContent = confirmed ? (state.t === 0
        ? 't=0：紫色は固有空間である全平面です。図はその一部だけを示します。2本の軸だけが固有空間なのではありません。'
        : 't≠0：紫色は第1座標軸全体です。正負両方向に続き、原点も含みます。') : '';
      byId('diagram-description').textContent = confirmed
        ? '左は実線のe₁・e₂、右は破線のA(t)e₁・A(t)e₂です。A(t)e₁=(1,0)、A(t)e₂=(' + state.t.toFixed(1) + ',1)。ベクトルが重なるときも位置をずらしていません。'
        : '';
      if (confirmed) { draw(diagrams[0], 0, false); draw(diagrams[1], state.t, true); }
      else { for (const svg of diagrams) clearDrawing(svg); }
      for (const step of document.querySelectorAll('.proof-step')) {
        step.hidden = !confirmed || Number(step.dataset.step) > state.proofStep;
      }
      byId('proof-next').disabled = !confirmed || state.proofStep === 3;
      byId('proof-next').textContent = state.proofStep === 3 ? '証明をすべて表示しました' : '証明の次の段階を開く';
      byId('proof-progress').textContent = confirmed ? '証明の表示：' + state.proofStep + ' / 3段階' : '';
    }
    function restart(message) {
      byId('prediction-error').textContent = '';
      render();
      byId('activity-status').textContent = message;
    }
    slider.addEventListener('input', function () {
      lesson.setParameter(Number(slider.value));
      restart('t=' + lesson.getState().t.toFixed(1) + 'に変更しました。予想・結果・証明を初期化しました。もう一度予想してください。');
    });
    byId('reset').addEventListener('click', function () {
      lesson.reset();
      restart('t=0に戻しました。予想・結果・証明を初期化しました。もう一度予想してください。');
    });
    form.addEventListener('invalid', function () {
      byId('prediction-error').textContent = '固有空間の次元と対角化可能性を、それぞれ選んでください。';
    }, true);
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      const dimension = form.querySelector('input[name="dimension"]:checked');
      const diagonalizable = form.querySelector('input[name="diagonalizable"]:checked');
      if (!dimension || !diagonalizable) {
        byId('prediction-error').textContent = '固有空間の次元と対角化可能性を、それぞれ選んでください。';
        form.querySelector('input[name="' + (!dimension ? 'dimension' : 'diagonalizable') + '"]').focus();
        return;
      }
      lesson.predict(Number(dimension.value), diagonalizable.value === 'yes');
      byId('prediction-error').textContent = '';
      render();
      byId('activity-status').textContent = '予想を確定しました。次元は' + lesson.getState().result.dimension + '、対角化は' + (lesson.getState().result.diagonalizable ? '可能' : '不可能') + 'です。次に図を観察し、証明へ進みましょう。';
      const heading = byId('observation-title');
      if (heading) heading.focus();
    });
    byId('proof-next').addEventListener('click', function () { lesson.nextProofStep(); render(); });
    render();
    byId('activity-status').textContent = 't=' + lesson.getState().t.toFixed(1) + 'の予想を、それぞれ選んでください。';
    return lesson;
  }

  const api = Object.freeze({ matrix, apply, determinant, eigenspaceDimensionAtOne, createLesson, mountLesson });
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (root) {
    root.ShearMath = api;
    const ready = () => mountLesson(root.document);
    if (root.document.readyState === 'loading') root.document.addEventListener('DOMContentLoaded', ready);
    else ready();
  }
})(typeof window !== 'undefined' ? window : undefined);
