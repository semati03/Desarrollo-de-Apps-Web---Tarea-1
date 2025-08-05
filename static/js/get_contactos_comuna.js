document.addEventListener("DOMContentLoaded", function() {

    Highcharts.chart("container", {
    chart: {
        type: "pie",
    },
    title: {
        text: "Total de Contactos por Comuna",
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
    series: [
        {
            name: "Contactos",
            data: [],
            colorByPoint: true,
        },
    ],
});

    fetch("/get_data_contactos_comuna")
        .then((response) => response.json())
        .then((data) => {
            const parsedData = data.map((item) => ({
                name: item.comuna,
                y: item.total,
            }));

            const chart = Highcharts.charts.find(
                (chart) => chart && chart.renderTo.id === "container"
            );

            chart.update({
                series: [
                    {
                        data: parsedData,
                    },
                ],
            });
        })
        .catch((error) => console.error("Error:", error));
});
