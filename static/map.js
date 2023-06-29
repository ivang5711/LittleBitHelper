// sorting functions based on the examples from the https://www.w3schools.com
// sorts numbers ascending
function sortTableAsc (val) {
  var table;
  var rows;
  var switching;
  var i;
  var shouldSwitch;
  table = document.getElementById('myTable');
  switching = true;
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      let x = rows[i].getElementsByTagName('TD')[val];
      let y = rows[i + 1].getElementsByTagName('TD')[val];
      let ti = x.innerHTML.toLowerCase();
      let di = y.innerHTML.toLowerCase();
      const regex = /\D/g;
      var n = parseInt(ti.replace(regex, ''));
      var m = parseInt(di.replace(regex, ''));
      console.log('Take a look right here: ti, di:');
      if (parseInt(n) > parseInt(m)) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

// sorts numbers descending
function sortTableDesc (val) {
  var table;
  var rows;
  var switching;
  var i;
  var shouldSwitch;
  table = document.getElementById('myTable');
  switching = true;
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      let x = rows[i].getElementsByTagName('TD')[val];
      let y = rows[i + 1].getElementsByTagName('TD')[val];
      let ti = x.innerHTML.toLowerCase();
      let di = y.innerHTML.toLowerCase();
      const regex = /\D/g;
      var n = parseInt(ti.replace(regex, ''));
      var m = parseInt(di.replace(regex, ''));
      if (parseInt(n) < parseInt(m)) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

// sorts numbers ascending
function sortTableTypeAsc (val) {
  var table;
  var rows;
  var switching;
  var i;
  var x;
  var y;
  var shouldSwitch;
  table = document.getElementById('myTable');
  switching = true;
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName('TD')[val];
      y = rows[i + 1].getElementsByTagName('TD')[val];
      if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

// sorts numbers descending
function sortTableTypeDesc (val) {
  var table;
  var rows;
  var switching;
  var i;
  var x;
  var y;
  var shouldSwitch;
  table = document.getElementById('myTable');
  switching = true;
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName('TD')[val];
      y = rows[i + 1].getElementsByTagName('TD')[val];
      if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

// the following filter script originates from https://www.w3schools.com/howto/howto_js_filter_table.asp
// filters a table by the specified column (5th in this case which is "date" column)
function myFunction () {
  // Declare variables
  var input;
  var filter;
  var table;
  var tr;
  var td;
  var i;
  var txtValue;
  input = document.getElementById('myInput');
  filter = input.value.toUpperCase();
  table = document.getElementById('myTable');
  tr = table.getElementsByTagName('tr');
  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName('td')[4];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = '';
      } else {
        tr[i].style.display = 'none';
      }
    }
  }
}
