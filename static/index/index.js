/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function (event) {
  if (!event.target.matches(".logout-btn")) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains("show")) {
        openDropdown.classList.remove("show");
      }
    }
  }
};

function chart1Function(myChart1) {
  console.log(temperatures1.length);

  // get first temperature
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/get_current_temperature1", true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      if (this.responseText == "Sensor not connected") {
        document.getElementById("loader1").style.display = "none";
        document.getElementById("errorSensorNotConnected1").style.display =
          "flex";
        document.getElementById("temp1").style.display = "none";
        if (dates1.length == 1) {
          document.getElementById(
            "lastActiveDate1"
          ).innerHTML = `Last time active: Never`;
        } else {
          document.getElementById(
            "lastActiveDate1"
          ).innerHTML = `Last time active: ${dates1[dates1.length - 1]}`;
        }
      } else {
        temperatures1.push(parseFloat(this.responseText));
        document.getElementById("temperature1").innerHTML = this.responseText;
        document.getElementById("loader1").style.display = "none";
        document.getElementById("errorSensorNotConnected1").style.display =
          "none";
        document.getElementById("temp1").style.display = "flex";
        dates1.push(new Date().toLocaleTimeString());
        if (dates1.length >= 30) {
          temperatures1.shift();
          dates1.shift();
        }
        myChart1.update();
      }
    }
  };
  xhr.send();
}

function chart2Function(myChart2) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/get_current_temperature2", true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      if (this.responseText == "Sensor not connected") {
        document.getElementById("loader2").style.display = "none";
        document.getElementById("errorSensorNotConnected2").style.display =
          "flex";
        document.getElementById("temp2").style.display = "none";
        if (dates2.length == 1) {
          document.getElementById(
            "lastActiveDate2"
          ).innerHTML = `Last time active: Never`;
        } else {
          document.getElementById(
            "lastActiveDate2"
          ).innerHTML = `Last time active: ${dates2[dates2.length - 1]}`;
        }
      } else {
        temperatures2.push(parseFloat(this.responseText));

        document.getElementById("temperature2").innerHTML = this.responseText;
        document.getElementById("loader2").style.display = "none";
        document.getElementById("errorSensorNotConnected2").style.display =
          "none";
        document.getElementById("temp2").style.display = "flex";
        dates2.push(new Date().toLocaleTimeString());
        if (dates2.length >= 30) {
          dates2.shift();
          temperatures2.shift();
        }
        myChart2.update();
      }
    }
  };
  xhr.send();
}

function setTemperature() {
  var xhr = new XMLHttpRequest();
  var temp = document.getElementById("set_targeted_temperature").value;

  if (!isNaN(temp) && temp > 10 && temp < 40) {
    xhr.open("POST", "/targeted_temperature", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
      if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        console.log("Value sent successfully");
      }
    };
    xhr.send(
      "value=" +
        encodeURIComponent(
          document.getElementById("set_targeted_temperature").value
        )
    );
  } else {
    alert("Input is not valid. Value must be numeric and between 10 and 40");
    return false;
  }
}
