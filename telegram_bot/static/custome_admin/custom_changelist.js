document.addEventListener('DOMContentLoaded', function() {
    var resultTable = document.getElementById('result_list');
    if (resultTable) {
        var rows = resultTable.getElementsByTagName('tr');
        Array.from(rows).forEach(function(row) {
            var mileageBeforeMaintenanceCell = row.querySelector('.field-mileage_before_maintenance');
            var mileageCell = row.querySelector('.field-mileage');

            if (mileageBeforeMaintenanceCell && mileageCell) {
                var mileageBeforeMaintenance = parseFloat(mileageBeforeMaintenanceCell.textContent.trim());
                var mileage = parseFloat(mileageCell.textContent.trim());

                if (!isNaN(mileageBeforeMaintenance) && !isNaN(mileage)) {
                    var diff = mileageBeforeMaintenance - mileage;
                    if (diff < 0) {
                        row.classList.add('red-row');
                    } else if (diff < 2000) {
                        row.classList.add('yellow-row');
                    }
                }
            }
        });
    }
});