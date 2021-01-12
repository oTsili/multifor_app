
// DOM element class reference
const gElements = {
  pestel_pie: document.querySelector('.pestel-pie'),
  table_indicator_first: document.querySelector('.first-indicator'),
  table_indicator_second: document.querySelector('.second-indicator'),
  table_indicator_third: document.querySelector('.third-indicator'),
  table_cell: document.querySelector('.cssTableCell'),
  line_chart: document.querySelector('.svg-container'),
  google_table: document.querySelector('.svg-table_div'),
  hidden_form_var: document.querySelector('#hidden_submit_btn'),
  update_btn: document.querySelector('#update_btn'),
  switch_btn: document.querySelector('#switch_btn'),
  navCountries: document.querySelector('.countries-list'),
  navIndicators: document.querySelector('.indicators-list'),
  btns: document.querySelector('.btn'),
  iconSmall: $('ion-icon'),
  nav_icon: $('.js--nav-icon'),
  mob_nav: $('.mob-nav'),
  main_nav: $('nav'),
  icon_menu: $('.icon-menu'),

};


for (let i=0; i < countries.length; i++){
    gElements.navCountries.insertAdjacentHTML('afterbegin', `<li><a href=${lineUrl}/${countries[i]}?col=GDP_growth>${countries[i].replace(/_/g, ' ')}</a></li>`);
}

for (let i=0; i < indicators.length; i++){
    gElements.navIndicators.insertAdjacentHTML('afterbegin', `<li><a href=${lineUrl}/${indicators[i]}?col=Belgium>${indicators[i].replace(/_/g, ' ')}</a></li>`);
}

/* Mobile nav */
gElements.nav_icon.click(function() {
  gElements.main_nav.slideToggle(200);

  if (gElements.icon_menu.attr('name') === 'menu'){
    gElements.icon_menu.attr('name', 'close');
  } else if (gElements.icon_menu.attr('name') === 'close'){
    gElements.icon_menu.attr('name', 'menu');
  }
});