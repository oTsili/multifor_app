const renderLoader = parent => {
    const loader = `
        <div class="${elementStrings.loader}">
        <p class="spinner-msg"><span class="blinking"><b>Working!! Please be patient!!!</b></span></p>
            <svg>
                <use href="${spinnerIcon}#icon-cw"></use>
            </svg>
        </div>
    `;
    parent.insertAdjacentHTML('afterbegin', loader);
};

const clearLoader = () => {
    const loader = document.querySelector(`.${elementStrings.loader}`);
    if (loader) loader.parentElement.removeChild(loader);
};