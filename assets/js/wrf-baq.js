window.initWRFBaqApp = async function init() {
  const API_ENDPOINT = 'https://api.github.com/repos/AML-CS/wrf-baq-0.5km';
  const RAW_API_ENDPOINT = 'https://raw.githubusercontent.com/AML-CS/wrf-baq-0.5km';

  const SHA = new URLSearchParams(document.location.search).get('report_sha') || 'master';

  const allReportsPagination = {
    itemsPerPage: 15,
    currentPage: 1,
    loading: false,
  };

  const ncVariablesToName = {
    'pwater': 'Precipitable Water',
    'wind': 'Wind speed',
    'temp': 'Temperature',
    'uwind': 'U wind speed',
    'vwind': 'V wind speed',
    'press': 'Pressure',
  };

  function apiFetch(url) {
    return fetch(url)
      .then(async (res) => ({
        hasMore: (res.headers.get('link') || '').includes('next'),
        data: (await res.json())
      }))
      .catch(err => {
        console.error(err);
        hideApp();
      });
  }

  async function fetchReport(sha) {
    const { data: { files } } = await apiFetch(`${API_ENDPOINT}/commits/${sha}`);
    const { data: report } = await apiFetch(`${RAW_API_ENDPOINT}/${sha}/output/report.json`);

    const images = {};
    const folium = {};
    const filenameRegex = new RegExp(/output\/(.*)\..*/);

    await Promise.all(files.map(async ({ filename, 'contents_url': contentsUrl }) => {
      const key = filenameRegex.exec(filename)[1];
      if (filename.includes('.gif')) {
        images[key] = `${RAW_API_ENDPOINT}/${sha}/${filename}`;
      }
      if (filename.includes('.html')) {
        const { data: { content } } = await apiFetch(contentsUrl);
        folium[key] = `data:text/html;base64,${content}`;
      }
    }));

    return { report, images, folium };
  }

  async function fetchAllReportsWithPagination(pagination) {
    const { currentPage, itemsPerPage } = pagination;

    pagination.loading = true;
    const { data: commits, hasMore } = await apiFetch(`${API_ENDPOINT}/commits?page=${currentPage}&per_page=${itemsPerPage}`);

    const reports = commits.map(({ sha, commit }) => {
      if (commit.message.includes('BAQ 0.5km WRF output')) {
        return {
          message: commit.message,
          sha,
        }
      }
    }).filter(Boolean);

    pagination.loading = false;

    return { reports, hasMore };
  }

  function displayReportData(data) {
    const reportTitle = document.getElementById('report-title');
    const reportDataTable = document.getElementById('report-data');

    reportTitle.innerHTML = `Report: ${data.createdAt}`;
    reportDataTable.innerHTML = '';

    const formatter = {
      createdAt: (value) => ['Updated', `${value} UTC`],
      startDate: (value) => ['WRF Start Date', `${value}:00 UTC`],
      endDate: (value) => ['WRF End Date', `${value}:00 UTC`],
      gfsUrls: (value) => [`<a href="https://registry.opendata.aws/noaa-gfs-bdp-pds/" target="_blank" rel="noopener noreferrer nofollow">NOAA - GFS data</a>`, value.map((url) => `<a href="https://noaa-gfs-bdp-pds.s3.amazonaws.com/index.html#${url}" target="_blank" rel="noopener noreferrer nofollow">${url}</a>`).join('<br>')],
      ogimetUrl: (value) => [`<a href="https://www.ogimet.com/home.phtml.en" target="_blank" rel="noopener noreferrer nofollow">OGIMET</a> query`, `<a href="${value}" target="_blank" rel="noopener noreferrer nofollow">${value}</a>`],
      ogimetStationCoordinates: (value) => ['SKBQ station', `<a href="https://www.google.com/maps/place/${value.join(',')}" target="_blank" rel="noopener noreferrer nofollow" >${value.join(',')}</a>`],
      interpolatedVariables: (value) => ['Interpolated variables', value.join('<br>').replace(/:fcst(.*?):from [0-9]+/g, '')],
    }

    Object.entries(data).forEach(([key, value]) => {
      const tr = document.createElement('tr');
      const keyTd = document.createElement('td');
      const valueTd = document.createElement('td');

      if (key in formatter) {
        const [title, valueParsed] = formatter[key](value);

        keyTd.innerHTML = title;
        valueTd.innerHTML = valueParsed;

        tr.appendChild(keyTd);
        tr.appendChild(valueTd);

        reportDataTable.appendChild(tr);
      }
    });
  }

  function displayAllReportsTable(data) {
    const allReportsTable = document.getElementById('all-reports');
    allReportsTable.innerHTML = '';

    data.forEach(({ message, sha }) => {
      const tr = document.createElement('tr');
      const messageTd = document.createElement('td');
      const urlTd = document.createElement('td');

      messageTd.innerHTML = message;
      urlTd.innerHTML = `<a href="${window.location.href}?report_sha=${sha}" target="_blank" rel="noopener noreferrer nofollow">See report</a>`;

      tr.appendChild(messageTd);
      tr.appendChild(urlTd);

      allReportsTable.appendChild(tr);
    });
  }

  function createElementIntoContainer(containerId, tag, variables) {
    const parent = document.getElementById(containerId);
    const child = document.createElement(tag);

    Object.entries(variables).forEach(([key, value]) => {
      child[key] = value;
    });

    if (parent.querySelector(tag)) {
      parent.removeChild(parent.querySelector(tag));
    }
    parent.appendChild(child);
  }

  function loadFolium(variable, url) {
    createElementIntoContainer('maps-folium', 'iframe', {
      src: url,
      title: ncVariablesToName[variable],
    });
  }

  function loadGif(variable, url) {
    createElementIntoContainer('maps-gif', 'img', {
      src: url,
      alt: ncVariablesToName[variable],
    });
  }

  function initVariablesSelect(report, images, folium) {
    const variablesSelect = document.getElementById('variables-select');

    report.ncVariables.forEach((variable, index) => {
      const option = document.createElement('option');
      option.value = variable;
      option.textContent = ncVariablesToName[variable];

      if (index === 0) {
        option.selected = true;
        loadGif(variable, images[variable]);
        loadFolium(variable, folium[variable]);
      }

      variablesSelect.appendChild(option);
    });

    variablesSelect.addEventListener('change', (e) => {
      const variable = e.target.value;

      loadGif(variable, images[variable]);
      loadFolium(variable, folium[variable]);
    });
  }

  function initAllReportsPagination() {
    const newerButton = document.getElementById('newer');
    const olderButton = document.getElementById('older');

    newerButton.addEventListener('click', (e) => {
      const { currentPage, loading } = allReportsPagination;

      if (loading) {
        return;
      }

      if (currentPage > 1) {
        allReportsPagination.currentPage -= 1;
      }

      if (allReportsPagination.currentPage === 1) {
        newerButton.disabled = true;
      }

      showAllReportsWithPagination();

      olderButton.disabled = false;
    });

    olderButton.addEventListener('click', async (e) => {
      const { loading } = allReportsPagination;

      if (loading) {
        return;
      }

      allReportsPagination.currentPage += 1;
      const { success, hasMore } = await showAllReportsWithPagination();

      if (!success) {
        allReportsPagination.currentPage -= 1;
      }

      if (!hasMore || !success) {
        olderButton.disabled = true;
      }

      newerButton.disabled = false;
    });
  }

  function showApp() {
    const app = document.getElementById('wrf-baq-app');
    app.classList.remove('hide');
  }

  function hideApp() {
    const app = document.getElementById('wrf-baq-app');
    app.classList.add('hide');
  }

  async function showReport() {
    const { report, images, folium } = await fetchReport(SHA);

    if (Object.keys(report).length >= 7) {
      initVariablesSelect(report, images, folium);
      displayReportData(report);

      return true;
    }
  }

  async function showAllReportsWithPagination() {
    const { reports, hasMore } = await fetchAllReportsWithPagination(allReportsPagination);

    const success = reports.length > 0;

    if (success) {
      displayAllReportsTable(reports);
    }

    return { success, hasMore }
  }

  if ((await showReport()) && (await showAllReportsWithPagination()).success ) {
    initAllReportsPagination();
    showApp();
  }
}
