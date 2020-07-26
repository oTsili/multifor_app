// DOM element class reference
const elements = {
    table: $('#table_div'),
    lHeader: $('h1'),
    sHeader: $('.small-header'),
    body: document.querySelector('body'),
    chartContainer: $('.chart-container'),
    tableContainer: document.querySelector('.table-container'),
    table_cell: document.querySelector('.cssTableCell'),
    line_chart: document.querySelector('.svg-container'),
    google_table: document.querySelector('.svg-table_div'),
    hidden_form_var: document.querySelector('#hidden_submit_btn'),
    update_btn: document.querySelector('#update_btn'),
    switch_btn: document.querySelector('#switch_btn'),
    tbl_name_js : document.getElementById('tbl_name'),
    clm_name_js : document.getElementById('cl_name'),
    page_title: document.querySelector('h1'),
    tbl_name : $("#tbl_name"),
    clm_name : $( "#cl_name" ),
    btnAddColumn: document.querySelector('#btn_add_col'),
    btnRemoveColumn: document.querySelector('#btn_remove_col'),
    hiddenAddColVal: document.querySelector('#hidden_column_values'),
    hiddenRemoveColVal: document.querySelector('#hidden_col_values'),
    tableHeader: document.querySelector('.cssHeaderRow'),
    tableClass: document.querySelector('.google-visualization-table-table'),
    alertBox: document.querySelector('#no_result'),
    alertBoxMsg: document.querySelector('#msg'),
    btnAddYear: document.querySelector('#btn_add_year'),
    // btnAddYear: ('#btb_add_year'),
    btnRemoveYear: document.querySelector('#btn_remove_year'),
    ths: document.getElementsByTagName("th"),
    trs: document.getElementsByTagName("tr"),
    hiddenRemoveYearColVal: document.querySelector('#hidden_col_value'),
    hiddenAddYearColVal: document.querySelector('#hidden_column_value'),
    hiddenRemoveYearVal: document.querySelector('#hidden_y_value'),
    hiddenAddYearVal: document.querySelector('#hidden_year_value'),
    google_tab: document.getElementById('table_div'),
    linePlot: document.getElementById('myDiv'),
    add_rem_sel:$('#add_rem_select'),
    add_rem_container:$(".num-of-cols-form")
};

const elementStrings = {
    loader: 'loader',
    last_year: 2018
};


let flag = false;



///////////////////////// CHART CONTAINER SIZE FUNCTION //////////////

const resizeChartContainer = () => {
    //window size//
    let winWidth = $(window).innerWidth();
    let winHeight = $(window).innerHeight();
    // resize the chart and the table with regard the window size
    let layout;
    if (winWidth > 1024) {
        layout = {
            autosize: true,
            width: 750,
            height: 350,
            margin: {
                l: 50,
                r: 50,
                b: 100,
                t: 100,
                pad: 4
            }
        };
        elements.table.attr('max-width', '37%');
    } else if (winWidth > 870 && winWidth <= 1024) {
        layout = {
            autosize: true,
            width: 520,
            height: 350,
            margin: {
                l: 50,
                r: 50,
                b: 100,
                t: 100,
                pad: 4
            }
        };
    } else if (winWidth > 800 && winWidth <= 890) {
        layout = {
            autosize: true,
            width: 550,
            height: 350,
            margin: {
                l: 50,
                r: 50,
                b: 100,
                t: 100,
                pad: 4
            },
            font: {
            family: 'Courier New, monospace',
            size: 14,
            color: '#7f7f7f'
            }

        };
    }else if (winWidth > 415 && winWidth <= 800) {
        layout = {
            autosize: true,
            width: 450,
            height: 350,
            margin: {
                l: 50,
                r: 50,
                b: 100,
                t: 100,
                pad: 4
            }
        };
    } else {
        layout = {
            autosize: true,
            width: 380,
            height: 350,
            margin: {
                l: 50,
                r: 50,
                b: 100,
                t: 100,
                pad: 4
            }
        };
    }
    return layout;
};

/////////////////////// GOOGLE TABLE FUNCTIONS //////////////////////
let isInit = false;

const drawChart = (data, options) => {
        let table = new google.visualization.Table(document.getElementById('table_div'));
        table.draw(data, options);
};

const drawTable = (google_data) => {
    let data = new google.visualization.DataTable(google_data);

    let cssClassNames = {
                'headerRow': 'cssHeaderRow',
                'tableRow': 'cssTableRow',
                'oddTableRow': 'cssOddTableRow',
                'selectedTableRow': 'cssSelectedTableRow',
                'hoverTableRow': 'cssHoverTableRow',
                'headerCell': 'cssHeaderCell',
                'tableCell': 'cssTableCell',
                'rowNumberCell': 'cssRowNumberCell'
            };

    let options =
        {
            allowHtml: true,
            showRowNumber: false,
            width: '100%',
            height: '90%',
            cssClassNames: cssClassNames
        };

    drawChart(data, options);
};


const initialize = (to_google) => {
    google.charts.load('current', {'packages':['table']});
    if (isInit) {
        drawTable(to_google);
  } else {
        google.charts.load('current', {
        callback: function () {
        isInit = true;
        drawTable(to_google);
      },
      packages:['table']
    });
  }
};

///////////////////// SELECT ELEMENTS ON CHANGE HANDLERS //////////////////////////

// function to change the columns dropList when table dropList is changed, with Ajax call to Flask
const columnChangeHandler = (selectedTable, url, column=columns) => {
    renderLoader(elements.body);
    $.ajax({
        type: "POST",
        // CORS header fix
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        // the rest parameters
        url: `${url}`,
        data: { table : selectedTable },
         dataType: "json",
        success: function(data){
            column = column.replace(/_/g, ' ');
            for(let col of data){
                col = col.replace(/_/g, ' ');
                if (col === column){
                    elements.tbl_name.append(`<option selected value="${col}">"${col}"</option>`);

                } else {
                    elements.tbl_name.append(`<option value="${col}">"${col}"</option>`);
                }
            }
        },
        error: function (xhr, status) {
            console.log(xhr, status);
            window.location.replace(error500Html);
        }
    }).done( () => {
        clearLoader();
    })
};


// function to change the columns dropList when table dropList is changed, with Ajax call to Flask
const tableChangeHandler = (selectedTable, url, column=columns) => {
    renderLoader(elements.body);
    // selectedTable = selectedTable.replace(/ /g, "_");

    $.ajax({
        type: "POST",
        // CORS header fix
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        // the rest parameters
        url: `${url}`,
        data: { table : selectedTable },
         dataType: "json",
        success: function(data){
            column = column.replace(/_/g, ' ');
            for(let col of data){
                col = col.replace(/_/g, ' ');
                if (col === column){
                    elements.clm_name.append(`<option selected value="${col}">"${col}"</option>`);
                    elements.add_rem_sel.append(`<option selected value="${col}">"${col}"</option>`);
                } else {
                    elements.clm_name.append(`<option value="${col}">"${col}"</option>`);
                    elements.add_rem_sel.append(`<option selected value="${col}">"${col}"</option>`);
                }
            }
        },
        error: function (xhr, status) {
            console.log(xhr, status);
            window.location.replace(error500Html);
        }
    }).done( () => {
        clearLoader();
    });
};


const fillDropLists = (df_header, url, column) => {
    elements.tbl_name.html('');
    elements.clm_name.html('');
    elements.add_rem_sel.html('');

    // if the columns select is changed
    columnChangeHandler( column, url, df_header);
    tableChangeHandler(df_header, url, column);
};

const fillNextColumn = (remaining_cols) => {
    elements.add_rem_sel.html('');

    for (let col of remaining_cols){
        elements.add_rem_sel.append(`<option selected value="${col}">"${col}"</option>`);
    }
};


////////////////////////////////////////////////////////////////////////
// function to draw the line chart and the table
const drawThePage = (data, columns, dates) => {
    // draw the table
    const google_data = JSON.parse(data['to_google']);
    drawTable(google_data);
    for (let i=0; i <= columns.length-1; i++){
        columns[i] = columns[i].replace(/ /g, "_");
    }
    // draw the scatter
    const data_list = [];
    for (let i=0; i <= columns.length-1; i++){
        const dt = data['data'][`${columns[i]}`];
        data_list.push(
            {
                mode: 'lines',
                name: columns[i],
                x: dates,
                y: dt,
                type: 'scatter'
            }
        );
    }
    let layout = resizeChartContainer();
    Plotly.newPlot('myDiv', data_list, layout);

};


///////////////// PREDICTION AJAX FUNCTION ///////////////////////

const getPredicted = (selectedTable, url, lastYear, cols, dates, col_sel) => {
     renderLoader(elements.body);

    $.ajax({
        type: "POST",
        // CORS header fix
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        // the rest parameters
        url: `${url}`,
        data: { selTbl : selectedTable, lastYear: lastYear, cols: JSON.stringify(cols), flag:'True', col_sel:col_sel},
         dataType: "json",
        success: function(data){
            let columns = data['columns'];
            columns = JSON.parse(columns);
            drawThePage(data, columns, dates);
        },
        error: function (xhr, status) {
            window.location.replace(error500Html);
            console.log(xhr, status);
        }
    }).done( () => {
        clearLoader();
    });
};

//////////////////// UPDATE CHART AJAX FUNCTION /////////////////////////
const changeRowsColumns = (url, type, add) => {
    //spinner
    renderLoader(elements.body);
    //get the add/rem col select value
    const col_sel = elements.add_rem_sel.val();
    // get the header object
    const ths = elements.ths;
    const arr = Array.from(ths);
    // get the column names from the header
    let cols = [];
    for (let col=1; col < arr.length; col++){
        cols.push(arr[col].innerText);
    }
    // get the table's last  row element
    const firstTr = elements.trs[1];
    // get the last date (the first element of the row)
    const lastYear =firstTr.querySelector('td:first-child').innerText;

    let selectedTable = elements.tbl_name.val();
    // if called by switch button, then get the df/table of the right select element(of columns)
    if (type === 'switch') {
        selectedTable = elements.clm_name.val();
        cols = elements.tbl_name.val().replace(/ /g, "_");
    // if called by update button, then get the df/table of the left select element(of columns)
    } else if (type === 'update') {
        cols =  elements.clm_name.val();
    }
    for (let i=0; i <= cols.length-1; i++){
        cols[i] = cols[i].replace(/ /g, "_");
    }

    $.ajax({
        type: "POST",
        // CORS header fix
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        // the rest parameters
        url: `${url}`,
        data: { selTbl:selectedTable, col_sel:`${col_sel}`, lastYear: lastYear, cols: JSON.stringify(cols), flag:'False'},
        dataType: "json",
        success: function(data){
            const lastDate = data['last_year'];
            // get the dates
            let dates = data['dates'];

            let indicators = data['indicators'];
            dates = JSON.parse(dates);
            let columns = data['columns'];
            columns = JSON.parse(columns);

            const remaining_cols = data['remaining_cols'];
            // conditions to check if there are any columns or rows left to add
            if (add === 'col'){
                if (col_sel != null) {
                    drawThePage(data, columns, dates);
                    fillNextColumn(remaining_cols);
                } else {
                    Lobibox.alert('warning', {
                        msg: `No more <b>columns</b> to add!`
                    });
                }
            } else if (add === 'year') {
                if (lastDate < 2018) {
                    drawThePage(data, columns, dates);
                    flag = false;
                } else {
                    // drawThePage(data, columns, dates);
                    Lobibox.confirm({
                        msg: `No more rows to add! Proceed to <b>FORECASTING</b>?`,
                        callback: function ($this, type, ev) {
                            if (type === 'yes') {
                                dates.push(`${Number(dates[0]) + 1}`);
                                dates.splice(0, 0, dates.pop());
                                getPredicted(selectedTable, url, lastYear, cols, dates, col_sel);
                            }
                        }
                    });
                }
            }// if removed a column
            else if (add === 'rem'){
                fillNextColumn(remaining_cols);
                drawThePage(data, columns, dates);
            // if called by switch and update btns
            } else {
                drawThePage(data, columns, dates);
                if (indicators.includes(columns[0])){
                    elements.add_rem_container.attr("width", " 69%");
                }else{
                    // elements.add_rem_container.style.cssText = "width: 47%; ";
                    elements.add_rem_container.attr("width", "47%");
                }
            }
        },
        error: function (xhr, status) {
            window.location.replace(error500Html);
            console.log(xhr);
            console.log(status);
        }
    }).done( () => {
        clearLoader();
    });
};


///////////// INITIAL TABLE AND SCATTER DRAWING ////////////////
const initialize_page = (url, table, selectUrl,  column) => {

    elements.page_title.innerText = table;
    renderLoader(elements.body);
    // table = table.replace(/ /g, "_");
    $.when(
        $.ajax({
        type: "GET",
        // CORS header fix
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        // the rest parameters
        url: `${url}`,
        data: { tbl : table},
        dataType: "json",
        success: function(data){
            let dates = data['years'];
            dates = JSON.parse(dates);
            let indicators = data['indicators'];
            if (indicators.includes(column)){
                elements.add_rem_container.attr("width",  "69%");
            }else{
                elements.add_rem_container.attr("width", "47%");
            }
            // function to draw the line chart and the table
            const drawThePage = (data) => {
                // draw the table
                const google_data = JSON.parse(data['to_google']);
                initialize(google_data);
                // draw the scatter
                const dt = data['data'][0].replace("'"," " ).replace("["," " ).replace("]"," " ).split(',');
                for (let x of dt){
                    x.replace(/ /g, "_");
                }
                const data_list = [{
                            mode: 'lines',
                            name: dt,
                            x: dates,
                            y: dt,
                            type: 'scatter'
                }];

                let layout = resizeChartContainer();

                Plotly.newPlot('myDiv', data_list, layout);
            };
            drawThePage(data, column);
            return data;
            },
            error: function (xhr, status) {
                window.location.replace(error500Html);
                console.log(xhr);
                console.log(status);
            }
        })
    ).then( (data) => {
        // remove 'date' from list
        const idx = data['df_columns'].indexOf('date');
        if ( idx > -1 ){
            data['df_columns'].splice(idx,1);
        }
        let df_columns = data['df_columns'];

        columnChangeHandler(column, selectUrl, table);
        column = column.replace(/_/g, ' ');
        for(let col of df_columns){
            col = col.replace(/_/g, ' ');
            if (col === column){
                elements.clm_name.append(`<option selected value="${col}">"${col}"</option>`);
            } else {
                elements.clm_name.append(`<option value="${col}">"${col}"</option>`);
            }
            if (col !== column){
                elements.add_rem_sel.append(`<option value="${col}">"${col}"</option>`);
            }
        }

    }).done( () => {
        clearLoader();
    });
};

const checkTitleLength = () => {
    const header = elements.page_title;
    if (header.innerText.length <= 15){
        header.classList.remove('large-header');
        header.classList.add('small-header');
    } else {
        header.classList.remove('small-header');
        header.classList.add('large-header');
    }
};


//////////////////// ON LOAD /////////////////////////
$(document).ready(() => {

    initialize_page(initialUrl, table, selectUrl, columns);

    checkTitleLength();

    //////////////////// SELECT OPTIONS LISTENER  /////////////////////////
    elements.tbl_name.change( () => {
        tableChangeHandler( elements.tbl_name.val(), selectUrl, elements.clm_name.val());
    });

    elements.clm_name.change( () => {
        columnChangeHandler(elements.clm_name.val(), selectUrl, elements.tbl_name.val());
    });

    //////////////////// SWITCH-UPDATE BUTTONS /////////////////////////
    // listener to the switch tables button
    elements.switch_btn.addEventListener('click', () => {
        elements.tbl_name.ready( ()  => {
            const prvTable = elements.tbl_name.val();
            const prvCols = elements.clm_name.val();
            changeRowsColumns(switchBtnUrl, type="switch", add='');
            fillDropLists(prvCols, url=selectUrl, column=prvTable);
            elements.page_title.innerText = prvCols;
            checkTitleLength();
        });
    });

    // listener to the update tables button
    elements.update_btn.addEventListener('click', ()=> {
        changeRowsColumns(updBtnUrl, type="update", add='');
        elements.page_title.innerText = elements.tbl_name.val();
        checkTitleLength(elements.tbl_name.val());
    });

    //////////////////// ADD-REMOVE BUTTONS /////////////////////////

    elements.btnAddColumn.addEventListener('click', ()=> {
         changeRowsColumns(addColUrl, type='',  add='col');
    });

    elements.btnRemoveColumn.addEventListener('click', ()=> {
        if (elements.ths.length >=3 ){
            changeRowsColumns(remColUrl, type='', add='rem');

        }else{
            Lobibox.alert('warning', {
                        msg: `No more <b>columns</b> to remove!`
            });
        }
    });

    elements.btnRemoveYear.addEventListener('click', ()=> {
        if (elements.trs.length >=5 ){
            changeRowsColumns(remYearUrl);
        }else{
            Lobibox.alert('warning', {
                        msg: `No more <b>rows</b> to remove!`
            });
        }
    });

    elements.btnAddYear.addEventListener('click', ()=> {
        changeRowsColumns(addYearUrl, type='',add='year');
    });
});


