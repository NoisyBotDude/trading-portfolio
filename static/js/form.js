function undropdown() {
    document.getElementById("coins-info").style.display = "none";
}

function filterFunction() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("coin-name");
    document.getElementById("coins-info").style.display = "block";
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdown");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
        txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
        } else {
        a[i].style.display = "none";
        }
    }
}