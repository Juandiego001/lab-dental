function netcalc(a, b, c, d, e, f, g, h, i, j) {
  var c1 = a * b;
  var d1 = c / (d * e);
  var e1 = a * d1;
  var r1 = f / g;
  var t1 = r1 * h;
  var f1 = t1 / 720;
  var g1 = a * f1;
  var h1 = e1 + g1;
  var i1 = c1 - h1;
  var k1 = i1 - (i / 30)
  var l1 = k1 * d;
  var u1 = l1 * 12;
  return u1
}
function yearcalc(k, m) {
  return Math.round((k / m) * 12);
}
function nFormatter(num, digits) {
  var si = [
    { value: 1, ivalue: 1, symbol: "" },
    { value: 1E3, ivalue: 99.999E3, symbol: "k" },
    { value: 1E6, ivalue: 1E6, symbol: "M" },
    { value: 1E9, ivalue: 1E9, symbol: "G" },
    { value: 1E12, ivalue: 1E12, symbol: "T" },
    { value: 1E15, ivalue: 1E15, symbol: "P" },
    { value: 1E18, ivalue: 1E18, symbol: "E" }
  ];
  var rx = /\B(?=(\d{3})+(?!\d))/g;
  var i;
  for (i = si.length - 1; i > 0; i--) {
    if (Math.abs(num) >= si[i].ivalue) {
      break;
    }
  }
  if (digits == 0 && num > 99999) {
    digits = 2;
  }
  return (num / si[i].value).toFixed(digits).replace(rx, ',') + si[i].symbol;
}

function show_value(x, y) {
  document.getElementById("form-label" + y.substr(y.length - 1)).innerHTML = nFormatter(x, 0);

  var net = netcalc(
    document.getElementById("customRange1").value,
    document.getElementById("customRange2").value,
    document.getElementById("customRange3").value,
    document.getElementById("customRange4").value,
    document.getElementById("customRange5").value,
    document.getElementById("customRange6").value,
    document.getElementById("customRange7").value,
    document.getElementById("customRange8").value,
    document.getElementById("customRange9").value,
    document.getElementById("customRange0").value
  );
  var tot = yearcalc(document.getElementById("customRange0").value, net);

  document.getElementById("net-value").innerHTML = nFormatter(net, 2);
  document.getElementById("year-value").innerHTML = tot;
  if (tot < 0) {
    document.getElementById("year-value").innerHTML = "Inversión no rentable, por favor revise";
    document.getElementById("year-value").classList.add('btn');
    document.getElementById("year-value").classList.add('btn-primary');
  }
  else {
    document.getElementById("year-value").classList.remove('btn');
  }
}

function exchange_rate(x) {
  if (!(x == 1 || x == 0 || x == null)) {
    document.getElementById("customRange0").max = 50000 * x;
    document.getElementById("customRange9").max = 1000 * x;
    document.getElementById("customRange6").max = 50000 * x;
    document.getElementById("customRange3").max = 1500 * x;
    document.getElementById("customRange2").max = 50 * x;

    document.getElementById("customRange0").value = 10000 * x;
    document.getElementById("customRange9").value = 50 * x;
    document.getElementById("customRange6").value = 1000 * x;
    document.getElementById("customRange3").value = 1000 * x;
    document.getElementById("customRange2").value = 20 * x;

    document.getElementById("form-label0").innerHTML = nFormatter(document.getElementById("customRange0").value, 0);
    document.getElementById("form-label9").innerHTML = nFormatter(document.getElementById("customRange9").value, 0);
    document.getElementById("form-label6").innerHTML = nFormatter(document.getElementById("customRange6").value, 0);
    document.getElementById("form-label3").innerHTML = nFormatter(document.getElementById("customRange3").value, 0);
    document.getElementById("form-label2").innerHTML = nFormatter(document.getElementById("customRange2").value, 0);
    show_value(document.getElementById("customRange0").value, "customRange0")
  }
  else {
    document.getElementById("customRange0").max = 50000;
    document.getElementById("customRange9").max = 1000;
    document.getElementById("customRange6").max = 50000;
    document.getElementById("customRange3").max = 1500;
    document.getElementById("customRange2").max = 50;

    document.getElementById("customRange0").value = 10000;
    document.getElementById("customRange9").value = 50;
    document.getElementById("customRange6").value = 1000;
    document.getElementById("customRange3").value = 1000;
    document.getElementById("customRange2").value = 20;

    document.getElementById("form-label0").innerHTML = nFormatter(document.getElementById("customRange0").value, 0);
    document.getElementById("form-label9").innerHTML = nFormatter(document.getElementById("customRange9").value, 0);
    document.getElementById("form-label6").innerHTML = nFormatter(document.getElementById("customRange6").value, 0);
    document.getElementById("form-label3").innerHTML = nFormatter(document.getElementById("customRange3").value, 0);
    document.getElementById("form-label2").innerHTML = nFormatter(document.getElementById("customRange2").value, 0);

    show_value(document.getElementById("customRange0").value, "customRange0")
  }
}
