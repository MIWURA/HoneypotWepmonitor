$(document).ready(function () {

    var socket = io.connect();

    ///setInterval(function() {
    ///    if (socket.connected) {
     ///       console.log("Connected to server");
    ///    } else {
    ///        console.log("Not connected to server");
    ///    }
    ///}, 3000);

    socket.on("updateResponse_data", function (msg) {
        //console.log("Response_data :: " + msg);
        var data = msg;
    
        // ดึง tbody ของตาราง
        var tbody = document.getElementById("data-table-body");
    
        // ลบข้อมูลเก่าทั้งหมดใน tbody   
        tbody.innerHTML = "";
    
        // เพิ่มข้อมูลใหม่ลงใน tbody
        data.data.forEach(function(rowData) {
            var row = document.createElement("tr");
    
            Object.values(rowData).forEach(function(cellData) {
                var cell = document.createElement("td");

                // ตรวจสอบเงื่อนไขและเพิ่มคลาส CSS ตามเงื่อนไข
                if (cellData === "RED!") {
                    cell.classList.add("red-cell");
                } else if (cellData === "YELLOW!") {
                    cell.classList.add("yellow-cell");
                } else if (cellData === "ORANGE!") {
                    cell.classList.add("orange-cell");
                }

                cell.textContent = cellData;
                row.appendChild(cell);
            });
    
            tbody.appendChild(row);
        });
    });

    document.getElementById('SORTBY').addEventListener('change', function() {
        var sortby = this.value;
        var intable_value_dropdown = document.getElementById('intable_value');
    
        // Clear existing options
        intable_value_dropdown.innerHTML = '';
    
        // Add default option
        var defaultOption = document.createElement('option');
        defaultOption.text = '- Select -';
        defaultOption.value = '';
        intable_value_dropdown.add(defaultOption);
    
        // Populate options based on selected SORTBY value
        if (sortby === 'Type') {
            var options = ['Cowrie', 'Dionaea']; // Example options
            options.forEach(function(option) {
                var newOption = document.createElement('option');
                newOption.value = option;
                newOption.textContent = option;
                intable_value_dropdown.appendChild(newOption);
            });
        } else if (sortby === 'Alert') {
            var options = ['RED!', 'YELLOW!']; // Example options
            options.forEach(function(option) {
                var newOption = document.createElement('option');
                newOption.value = option;
                newOption.textContent = option;
                intable_value_dropdown.appendChild(newOption);
            });
        }
        // Add more conditions for other SORTBY values if needed
    });



});

