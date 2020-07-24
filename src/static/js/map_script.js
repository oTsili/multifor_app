/* Create map instance */

const elements = {
    loliboxYes : document.querySelector('.lobibox-btn lobibox-btn-yes'),
};


const drawMap = (countries) => {

    const chart = am4core.create("chartdiv", am4maps.MapChart);

    /* Set map definition */
    chart.geodata = am4geodata_worldLow;

    /* Set projection */
    chart.projection = new am4maps.projections.Miller();


    function createSeries(name, include, color, hoverColor) {
      const series = chart.series.push(new am4maps.MapPolygonSeries());
      const polygonTemplate = series.mapPolygons.template;
      polygonTemplate.cursorOverStyle = am4core.MouseCursorStyle.pointer;
      polygonTemplate.tooltipText = "{name}";
      polygonTemplate.fill = am4core.color(color);

      polygonTemplate.events.on("hit", function(event){
        chart.zoomToMapObject(event.target);
        const countryName = event.target.dataItem.dataContext.name;
        const countryCode = event.target.dataItem.dataContext.id;

        Lobibox.confirm({
            msg: `Are you sure you want to be transferred to chart page of ${countryName}?`,
            callback: function ($this, type, ev) {
                if (type === 'yes'){
                    const country = countries[countryCode].replace(/\s/g, '_');
                    window.location.replace(`${lineUrl}/${country}?col=GDP_growth`);
                }
            }
        });
      });

      series.name = name;
      series.useGeodata = true;
      series.include = include;
      series.fill = am4core.color(color);
      series.events.on("over", over);
      series.events.on("out", out);

      let hs = polygonTemplate.states.create("hover");
      hs.properties.fill = am4core.color(hoverColor);

      return series;
    }

    createSeries("Northern Europe",  ["FI", "DK", "SE", "NO", "IS"], "#96BDC6", "#669DA6");
    createSeries("Southern Europe", ['PT', 'ES', 'IT', "GR", 'CY', 'MT'], "#81968F", "#51665F");
    createSeries("Eastern Europe", ["EE","LV",'LT', 'PL', 'CZ', 'SK', 'HU', 'RO', "BG", 'HR', 'SI'],"#CFB9A5", "#AF9975");
    createSeries("Western Europe", ['DE', 'NL', "BE", "AT", 'CH', "FR", "IE", "GB", "LU", "LI"], "#99C78F", "#69975F");


    function over(ev) {
      ev.target.mapPolygons.each(function(polygon) {
        polygon.setState("highlight");
      });
    }

    function out(ev) {
      ev.target.mapPolygons.each(function(polygon) {
        polygon.setState("default");
      });
    }


    let winWidth = $(window).innerWidth();
    if(winWidth > 834 ) {
        chart.legend = new am4maps.Legend();
        chart.legend.position = "right";
        chart.legend.align = "right";
    } else if (winWidth > 450 && winWidth <= 834) {
        chart.legend = new am4maps.Legend();
        chart.legend.position = "left";
        chart.legend.align = "left";
    }

};


//////////////////// GET COUNTRY CODES AJAX FUNCTION /////////////////////////

// $(document).ready( () => { $('table tr th:contains("date")').removeClass('unsorted').addClass("sort-ascending") });
const getCountryCodes = (url) => {

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
            const countries = data['data'];
            drawMap(countries);
        },
        error: function (xhr, status) {
            window.location.replace(error500Html);
            console.log(xhr);
            console.log(status);
        }
    })
};


$(document).ready( getCountryCodes(getMapUrl));


