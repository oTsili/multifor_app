
const pElements = {
    pestel_pie: document.querySelector('.pestel-pie'),
    table_cell: document.querySelector('.cssTableCell'),
    political: document.querySelector('#political'),
    economical: document.querySelector('#economical'),
    social: document.querySelector('#social'),
    technological: document.querySelector('#technological'),
    ecological: document.querySelector('#ecological'),
    legislative: document.querySelector('#legislative'),
};

let isInit = false;


//////////////////// PIE CHART  /////////////////////////

Highcharts.chart('container', {
    chart: {
        type: 'variablepie',
           renderTo: 'container',
            margin: [0, 0, 0, 0],
            spacingTop: 0,
            spacingBottom: 0,
            spacingLeft: 0,
            spacingRight: 0
    },
     plotOptions: {
            pie: {
                size:'100%',
                dataLabels: {
                    enabled: false
                }
            }
    },
    title: {
        text: ''
    },
    tooltip: {
        headerFormat: '',
        pointFormat: '<span style="color:{point.color}">\u25CF</span> <b> {point.name}</b><br/>' +
            '{point.message}' +  '<br/>'
    },
    series: [{
        minPointSize: 10,
        innerSize: '30%',
        zMin: 0,
        name: 'countries',
        data: [{
            name: 'POLITICAL',
            y: 16.666666666666668,
            z: 16.666666666666668,
            message: 'Refer to the degree of intervention each government<br/>' +
                'applies in the country\'s economy'
        }, {
            name: 'ECONOMICAL',
            y: 16.666666666666668,
            z: 16.666666666666668,
            message: 'Refer to the performance of each country\'s economy'
        }, {
            name: 'SOCIAL',
            y: 16.666666666666668,
            z: 16.666666666666668,
            message: 'Are determinants of social trends in each country\'s population'
        }, {
            name: 'TECHNOLOGICAL',
            y: 16.666666666666668,
            z: 16.666666666666668,
            message: 'Indicate the degree of technology perception, from the angle <br/>' +
                ' of innovation and advancement'
        }, {
            name: 'ECOLOGICAL',
            y: 16.666666666666668,
            z: 16.666666666666668,
            message: 'Show the degree of the environmental footprints, of<br/>' +
                'each country, and have emerged due to the scarcity of <br/>' +
                'resources, that mankind confronts'
        }, {
            name: 'LEGISLATIVE',
            y: 16.666666666666668,
            z: 16.666666666666668,
            message: 'Although in some cases may be overlapped by<br/>' +
                'political factors, refer to the degree of <br/>' +
                'respect in law, each country has'
        }]
    }]
});


//////////////////// GOOGLE TABLES /////////////////////////

const drawChart = (data, options, elemID) => {
    var table = new google.visualization.Table(document.getElementById(elemID));
    table.draw(data, options);
};

const drawTable = (google_data, elemID) => {
    var data = new google.visualization.DataTable(google_data);

    var cssClassNames = {
                'headerRow': 'cssHeaderRow',
                'tableRow': 'cssTableRow',
                'oddTableRow': 'cssOddTableRow',
                'selectedTableRow': 'cssSelectedTableRow',
                'hoverTableRow': 'cssHoverTableRow',
                'headerCell': 'cssHeaderCell',
                'tableCell': 'cssTableCell',
                'rowNumberCell': 'cssRowNumberCell'
            };

    var options =
        {
            allowHtml: true,
            showRowNumber: false,
            width: '100%',
            height: '100%',
            cssClassNames: cssClassNames
        };
    drawChart(data, options, elemID);
};


const initialize = (to_google, elemID) => {
    google.charts.load('current', {'packages':['table']});

    // google.charts.setOnLoadCallback(drawTable(to_google));
    if (isInit) {
        drawTable(to_google, elemID);
  } else {
        google.charts.load('current', {
        callback: function () {
        isInit = true;
        drawTable(to_google, elemID);
      },
      packages:['table']
    });
  }
};

//////////////////// TABLE POPUP AJAX FUNCTION /////////////////////////

// $(document).ready( () => { $('table tr th:contains("date")').removeClass('unsorted').addClass("sort-ascending") });
const getIndicators = (url) => {

    $.ajax({
        type: "POST",
        // CORS header fix
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        // the rest parameters
        url: `${url}`,
        dataType: "json",
        success: function(data){
            for (let i=0; i < 6; i++) {
                let google_data = JSON.parse(data['pestel'][i]);
                let header = JSON.parse(data['pestel'][i])['cols'][0]['id'].toLowerCase();
                initialize(google_data, header);
            }
        },
        error: function (xhr, status) {
            window.location.replace(error500Html);
            console.log(xhr);
            console.log(status);
        }
    })
};


$(document).ready(()=>{

    let winWidth = $(window).innerWidth();
    let winHeight = $(window).innerHeight();
    if(winWidth > 590 && winHeight > 480) {
        getIndicators(pestelUrl);

        for (let counter = 0; counter < 6; counter++) {
            document.querySelector(`.highcharts-point.highcharts-color-${counter}`).addEventListener('mouseenter', (e) => {
                pElements.political.classList.remove('visible');
                pElements.economical.classList.remove('visible');
                pElements.social.classList.remove('visible');
                pElements.technological.classList.remove('visible');
                pElements.ecological.classList.remove('visible');
                pElements.legislative.classList.remove('visible');
                if (counter === 0) {
                    pElements.political.classList.add("visible");
                } else if (counter === 1) {
                    pElements.economical.classList.add("visible");
                } else if (counter === 2) {
                    pElements.social.classList.add("visible");
                } else if (counter === 3) {
                    pElements.technological.classList.add("visible");
                } else if (counter === 4) {
                    pElements.ecological.classList.add("visible");
                } else if (counter === 5) {
                    pElements.legislative.classList.add("visible");
                }
            });
        }

        $(document).on("click", ".cssTableCell", function () {
            const clickedBtnID = $(this).text();
            const attr = clickedBtnID.replace(/ /g, "_");
            Lobibox.confirm({
                msg: `Are you sure you want to be transferred to chart page of ${attr}?`,
                callback: function ($this, type, ev) {
                    if (type === 'yes') {
                        window.location.replace(`${lineUrl}/${attr}?col=Belgium`);
                    }
                }
            });
        });
    }
});




