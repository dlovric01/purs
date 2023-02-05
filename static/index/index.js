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

function chart2Function() {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/get_current_temperature2", true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      if (this.responseText == "Sensor not connected") {
        document.getElementById("loader2").style.display = "none";
        document.getElementById("errorSensorNotConnected2").style.display =
          "flex";
        document.getElementById("temp2").style.display = "none";
        document.getElementById(
          "lastActiveDate2"
        ).innerHTML = `Last time active: ${dates2[dates2.length - 1]}`;
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

function chart1Function() {
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

        document.getElementById(
          "lastActiveDate1"
        ).innerHTML = `Last time active: ${dates1[dates1.length - 1]}`;
      } else {
        temperatures1.push(parseFloat(this.responseText));
        dates1.push(new Date().toLocaleTimeString());
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

function chart2Draw() {
  var myChart2 = new Chart(
    document.getElementById("myChart2").getContext("2d"),
    {
      type: "line",
      data: {
        labels: dates2,
        datasets: [
          {
            label: "Basement (°C)",

            backgroundColor: ["rgba(255, 255, 255, 0)"],
            borderColor: ["rgba(0,0,132,1)"],
            data: temperatures2,
          },
        ],
      },
      options: {
        scales: {
          yAxes: [
            {
              ticks: {
                min: 0,
                max: parseFloat(maxValue) + 10,
              },
            },
          ],
        },
        elements: {
          point: {
            radius: 2,
          },
        },
      },
    }
  );
}

function chart1Draw() {
  var myChart1 = new Chart(
    document.getElementById("myChart1").getContext("2d"),
    {
      type: "line",
      data: {
        labels: dates1,
        datasets: [
          {
            label: "Living room (°C)",

            backgroundColor: ["rgba(255, 99, 132, 0)"],
            borderColor: ["rgba(255,99,132,1)"],
            data: temperatures1,
          },
        ],
      },
      options: {
        scales: {
          yAxes: [
            {
              ticks: {
                min: 0,
                max: parseFloat(maxValue) + 10,
              },
            },
          ],
        },
        elements: {
          point: {
            radius: 2,
          },
        },
      },
    }
  );
}
