document.addEventListener("DOMContentLoaded", function () {
    // Configuración inicial del gráfico
    Highcharts.chart("container", {
        chart: {
            type: "pie",
        },
        title: {
            text: "Total de Dispositivos por Tipo",
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
                name: "Dispositivos",
                data: [],
                colorByPoint: true,
            },
        ],
    });

    // Cargar datos con fetch
    fetch("/get_data_tipo_dispositivos")
        .then((response) => response.json())
        .then((data) => {
            const parsedData = data.map((item) => ({
                name: item.tipo,
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
