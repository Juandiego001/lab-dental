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
  return k / m;
}


function show_value(x, y) {
  document.getElementById("form-label" + y.substr(y.length - 1)).innerHTML = x;

  var net = netcalc(
    parseInt(document.getElementById("form-label1").innerHTML),
    parseInt(document.getElementById("form-label2").innerHTML),
    parseInt(document.getElementById("form-label3").innerHTML),
    parseInt(document.getElementById("form-label4").innerHTML),
    parseInt(document.getElementById("form-label5").innerHTML),
    parseInt(document.getElementById("form-label6").innerHTML),
    parseInt(document.getElementById("form-label7").innerHTML),
    parseInt(document.getElementById("form-label8").innerHTML),
    parseInt(document.getElementById("form-label9").innerHTML),
    parseInt(document.getElementById("form-label0").innerHTML)
  );
  var tot = yearcalc(parseInt(document.getElementById("customRange0").value), net);

  document.getElementById("net-value").innerHTML = net.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  document.getElementById("year-value").innerHTML = tot.toFixed(2).toString();
  if (tot < 0) {
    document.getElementById("year-value").innerHTML = "Investment not profitable, please review";
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

    document.getElementById("form-label0").innerHTML = document.getElementById("customRange0").value;
    document.getElementById("form-label9").innerHTML = document.getElementById("customRange9").value;
    document.getElementById("form-label6").innerHTML = document.getElementById("customRange6").value;
    document.getElementById("form-label3").innerHTML = document.getElementById("customRange3").value;
    document.getElementById("form-label2").innerHTML = document.getElementById("customRange2").value;
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

    document.getElementById("form-label0").innerHTML = document.getElementById("customRange0").value;
    document.getElementById("form-label9").innerHTML = document.getElementById("customRange9").value;
    document.getElementById("form-label6").innerHTML = document.getElementById("customRange6").value;
    document.getElementById("form-label3").innerHTML = document.getElementById("customRange3").value;
    document.getElementById("form-label2").innerHTML = document.getElementById("customRange2").value;

    show_value(document.getElementById("customRange0").value, "customRange0")
  }
}
