import os, re, markdown, html
from collections import Counter

OUT = '/home/claude/site'
SRC = '/home/claude/src2/AML-CS.github.io-master'
YEAR = 2026

LAB = ['Nino-Ruiz', 'Niño-Ruiz', 'Nino Ruiz', 'Nino, E', 'Ruiz, E', 'Guzman', 'Guzmán', 'Beltran', 'Beltrán', 'Mancilla', 'Calabria',
       'Morales-Retat', 'Consuegra', 'Acevedo', 'Valbuena', 'Diaz-Rodriguez', 'Cabarcas', 'Fernandez Quiroz', 'Quintero, N']

def bold_lab(a):
    parts = a.split(', ')
    # bold whole "Surname, I." tokens that belong to lab members
    out = re.sub(r'([A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+(?:[ \-][A-ZÁÉÍÓÚÑ][\w\-áéíóúñ]+)?(?:, [A-Z]\.(?: ?[A-Z]\.)?)?)',
                 lambda m: f'<b>{m.group(1)}</b>' if any(l.lower() in m.group(1).lower() for l in LAB) else m.group(1), a)
    return out

# (year, kind, title, authors, venue, url)
PUBS = [
 (2026,'soft','PyTEDA-web: A FastAPI platform for interactive data assimilation benchmarking with real-time streaming and persistent experiment tracking','Nino-Ruiz, E. D.','SoftwareX, 34, 102738 · Elsevier','https://doi.org/10.1016/j.softx.2026.102738'),
 (2026,'journal','Language development and inequality in early childhood: a study in Caribbean Colombian contexts','Nino-Ruiz, E. D. et al.','Vulnerable Children and Youth Studies · Taylor & Francis','https://doi.org/10.1080/17450128.2026.2646858'),
 (2025,'soft','TEDA: A lightweight Python framework for educational data assimilation','Nino-Ruiz, E. D.','SoftwareX, 31, 102297 · Elsevier','https://doi.org/10.1016/j.softx.2025.102297'),
 (2025,'journal','Improved Rosenbrock method with error estimator and Jacobian approximation using complex step','Perez Rivera, J. D., Turizo, D., Nino-Ruiz, E. D., Montoya, O. D.','Results in Applied Mathematics, 27, 100629 · Elsevier','https://doi.org/10.1016/j.rinam.2025.100629'),
 (2025,'soft','Statistical package for computing precision covariance matrices via modified Cholesky decomposition','Nino-Ruiz, E. D., Cabarcas Arrieta, D. S., Fernandez Quiroz, G. R., Quintero, N.','SoftwareX, 30, 102125 · Elsevier','https://doi.org/10.1016/j.softx.2025.102125'),
 (2024,'journal','A 4D-EnKF method via a modified Cholesky decomposition and line search optimization for non-linear data assimilation','Nino-Ruiz, E. D., Diaz-Rodriguez, J.','Atmosphere, 15(12), 1412 · MDPI','https://doi.org/10.3390/atmos15121412'),
 (2023,'journal','A Stochastic Covariance Shrinkage Approach in Ensemble Transform Kalman Filtering','Popov, A. A., Sandu, A., Nino-Ruiz, E. D., Evensen, G.','Tellus A: Dynamic Meteorology and Oceanography, 75(1), 159–171','https://doi.org/10.16993/tellusa.214'),
 (2023,'soft','AMLCS-DA: A data assimilation package in Python for Atmospheric General Circulation Models','Nino-Ruiz, E. D., Consuegra Ortega, R. S.','SoftwareX · Elsevier','https://doi.org/10.1016/j.softx.2023.101374'),
 (2023,'journal','Ensemble based methods for leapfrog integration in the simplified parameterizations, primitive-equation dynamics model','Nino-Ruiz, E. D., Consuegra Ortega, R. S., Lucini, M.','Quarterly Journal of the Royal Meteorological Society · RMetS','https://doi.org/10.1002/qj.4424'),
 (2022,'journal','Ensemble Driven Shrinkage Covariance Matrix Estimation for Sequential Data Assimilation','Nino-Ruiz, E. D., Guzman, L., Jabba, D.','International Journal of Artificial Intelligence, 20(2) · CESER',''),
 (2022,'conf','TEDA: A Computational Toolbox for Teaching Ensemble Based Data Assimilation','Nino-Ruiz, E. D., Valbuena, S. R.','Computational Science – ICCS 2022, Lecture Notes in Computer Science, vol. 13353 · Springer',''),
 (2021,'journal','A line-search optimization method for non-Gaussian data assimilation via random quasi-orthogonal sub-spaces','Nino-Ruiz, E. D.','Journal of Computational Science, 53, 101373 · Elsevier',''),
 (2021,'journal','An efficient ensemble Kalman Filter implementation via shrinkage covariance matrix estimation: exploiting prior knowledge','Lopez-Restrepo, S., Nino-Ruiz, E. D., Guzman-Reyes, L. G., Yarce, A., Pinel, N., Heemink, A. W.','Computational Geosciences, 25(3), 985–1003 · Springer','https://doi.org/10.1007/s10596-021-10035-4'),
 (2021,'journal','A data-driven localization method for ensemble based data assimilation','Nino-Ruiz, E. D.','Journal of Computational Science, 51, 101328 · Elsevier','https://www.sciencedirect.com/science/article/abs/pii/S1877750321000260'),
 (2021,'journal','An ensemble Kalman filter implementation based on the Ledoit and Wolf covariance matrix estimator','Nino-Ruiz, E. D., Guzman, L., Jabba, D.','Journal of Computational and Applied Mathematics, 384, 113163 · Elsevier','https://doi.org/10.1016/j.cam.2020.113163'),
 (2021,'conf','Data-Driven Methods for Weather Forecast','Nino-Ruiz, E. D., Acevedo García, F. J.','International Conference on Computational Science (ICCS), pp. 326–336 · Springer',''),
 (2020,'journal','On the mathematical modelling and data assimilation for air pollution assessment in the Tropical Andes','Montoya, O. L., Niño-Ruiz, E. D., Pinel, N.','Environmental Science and Pollution Research, 27(29), 35993–36012 · Springer','https://doi.org/10.1007/s11356-020-08268-4'),
 (2020,'journal','A numerical method for solving linear systems in the preconditioned Crank–Nicolson algorithm','Nino-Ruiz, E. D.','Applied Mathematics Letters, 104, 106254 · Elsevier','https://doi.org/10.1016/j.aml.2020.106254'),
 (2020,'journal','An adjoint-free four-dimensional variational data assimilation method via a modified Cholesky decomposition and an iterative Woodbury matrix formula','Nino-Ruiz, E. D., Guzman-Reyes, L. G., Beltran-Arrieta, R.','Nonlinear Dynamics, 99(3), 2441–2457 · Springer','https://doi.org/10.1007/s11071-019-05411-w'),
 (2020,'journal','A Maximum Likelihood Ensemble Filter via a Modified Cholesky Decomposition for Non-Gaussian Data Assimilation','Nino-Ruiz, E. D., Mancilla-Herrera, A., Lopez-Restrepo, S., Quintero-Montoya, O.','Sensors, 20(3), 877 · MDPI','https://doi.org/10.3390/s20030877'),
 (2020,'journal','A Four Dimensional Variational Data Assimilation Framework for Wind Energy Potential Estimation','Nino-Ruiz, E. D., Calabria-Sarmiento, J. C., Guzman-Reyes, L. G., Henao, A.','Atmosphere, 11(2), 167 · MDPI','https://doi.org/10.3390/atmos11020167'),
 (2020,'journal','Hybrid Ensemble Kalman Filter and Markov Chain Monte Carlo Implementations for Non-Gaussian Data Assimilation','Nino-Ruiz, E. D.','International Journal of Artificial Intelligence, 18(2) · CESER','http://www.ceser.in/ceserp/index.php/ijai/issue/view/680'),
 (2020,'conf','A Random Line-Search Optimization Method via Modified Cholesky Decomposition for Non-linear Data Assimilation','Nino-Ruiz, E. D.','International Conference on Computational Science (ICCS), pp. 189–202 · Springer','https://link.springer.com/chapter/10.1007/978-3-030-50426-7_15'),
 (2019,'journal','Dynamic Site Response Characterization Via Bayesian Inference: Analysis of the SGC Station Deposit in Bogota, Colombia','Mercado, V., Nino, E. D., Arteta, C. A.','Journal of Earthquake Engineering, 23(10), 1629–1650 · Taylor & Francis',''),
 (2019,'journal','Improved Tabu Search and Simulated Annealing methods for nonlinear data assimilation','Nino-Ruiz, E. D., Yang, X.-S.','Applied Soft Computing, 83, 105624 · Elsevier','https://doi.org/10.1016/j.asoc.2019.105624'),
 (2019,'journal','Non-linear data assimilation via trust region optimization','Nino-Ruiz, E. D.','Computational and Applied Mathematics, 38(3), 1–26 · Springer','https://doi.org/10.1007/s40314-019-0901-x'),
 (2019,'journal','A parallel implementation of the ensemble Kalman filter based on modified Cholesky decomposition','Nino-Ruiz, E. D., Sandu, A., Deng, X.','Journal of Computational Science, 36, 100654 · Elsevier',''),
 (2019,'journal','A Tabu Search implementation for adaptive localization in ensemble-based methods','Nino-Ruiz, E. D., Morales-Retat, L. E.','Soft Computing, 23(14), 5519–5535 · Springer','https://doi.org/10.1007/s00500-018-3210-1'),
 (2019,'journal','A reduced-space line-search method for unconstrained optimization via random descent directions','Nino-Ruiz, E. D., Ardila, C., Estrada, J., Capacho, J.','Applied Mathematics and Computation, 341, 15–30 · Elsevier','https://doi.org/10.1016/j.amc.2018.08.020'),
 (2019,'journal','Efficient parallel implementation of DDDAS inference using an ensemble Kalman filter with shrinkage covariance matrix estimation','Nino-Ruiz, E. D., Sandu, A.','Cluster Computing, 22(1), 2211–2221 · Springer',''),
 (2019,'journal','Water Cycle Algorithm: Implementation and Analysis of Solutions to the Bi-Objective Travelling Salesman Problem','Pimentel, J., Ardila, C. J., Niño, E., Jabba, D., Ruiz-Rangel, J.','International Journal of Artificial Intelligence, 17(2) · CESER','http://www.ceser.in/ceserp/index.php/ijai/article/view/6256'),
 (2019,'conf','Container-based architecture for optimal face-recognition tasks in edge computing','Tellez, N., Jimeno, M., Salazar, A., Nino-Ruiz, E. D.','4th ACM/IEEE Symposium on Edge Computing, pp. 301–303',''),
 (2018,'journal','Local search methods for the solution of implicit inverse problems','Nino-Ruiz, E. D., Ardila, C., Capacho, R.','Soft Computing, 22(14), 4819–4832 · Springer','https://doi.org/10.1007/s00500-017-2670-z'),
 (2018,'journal','Implicit surrogate models for trust region based methods','Nino-Ruiz, E. D.','Journal of Computational Science, 26, 264–274 · Elsevier','https://doi.org/10.1016/j.jocs.2018.02.003'),
 (2018,'journal','An ensemble Kalman filter implementation based on modified Cholesky decomposition for inverse covariance matrix estimation','Nino-Ruiz, E. D., Sandu, A., Deng, X.','SIAM Journal on Scientific Computing, 40(2), A867–A886 · SIAM',''),
 (2018,'journal','A Robust Non-Gaussian Data Assimilation Method for Highly Non-Linear Models','Nino-Ruiz, E. D., Cheng, H., Beltran, R.','Atmosphere, 9(4), 126 · MDPI','http://www.mdpi.com/2073-4433/9/4/126'),
 (2018,'conf','Non-Gaussian data assimilation via modified Cholesky decomposition','Nino-Ruiz, E. D., Mancilla-Herrera, A. M., Beltran-Arrieta, R.','7th International Conference on Computers Communications and Control (ICCCC), pp. 29–36 · IEEE','https://ieeexplore.ieee.org/document/8390433/'),
 (2017,'journal','Robust Data Assimilation Using L1 and Huber Norms','Rao, V., Sandu, A., Ng, M., Nino-Ruiz, E. D.','SIAM Journal on Scientific Computing, 39(3), B548–B570 · SIAM',''),
 (2017,'journal','A Matrix-Free Posterior Ensemble Kalman Filter Implementation Based on a Modified Cholesky Decomposition','Nino-Ruiz, E. D.','Atmosphere, 8, 125 · MDPI','https://doi.org/10.3390/atmos8070125'),
 (2017,'conf','A Surrogate Model Based on Mixtures of Taylor Expansions for Trust Region Based Methods','Nino-Ruiz, E. D., Ardila, C. J., Mancilla, A., Estrada, J.','Procedia Computer Science, 108, 1473–1482 (ICCS) · Best Workshop Paper Award','https://doi.org/10.1016/j.procs.2017.05.200'),
 (2017,'conf','A Posterior Ensemble Kalman Filter Based on a Modified Cholesky Decomposition','Nino-Ruiz, E. D., Mancilla, A., Calabria, J. C.','Procedia Computer Science, 108, 2049–2058 (ICCS)','https://doi.org/10.1016/j.procs.2017.05.062'),
 (2016,'journal','A high-performance computing framework for analyzing the economic impacts of wind correlation','Petra, C. G., Zavala, V. M., Nino-Ruiz, E. D., Anitescu, M.','Electric Power Systems Research, 141, 372–380 · Elsevier',''),
 (2016,'journal','A derivative-free trust region framework for variational data assimilation','Nino-Ruiz, E. D., Sandu, A.','Journal of Computational and Applied Mathematics, 293, 164–179 · Elsevier',''),
 (2016,'conf','A novel framework for the parallel solution of combinatorial problems implementing tabu search and simulated annealing algorithms','Guzman, L. G., Nino-Ruiz, E. D., Ardila, C. J., Jabba, D., Nieto, W.','6th International Conference on Computers Communications and Control (ICCCC), pp. 259–263 · IEEE',''),
 (2015,'journal','Ensemble Kalman filter implementations based on shrinkage covariance matrix estimation','Nino-Ruiz, E. D., Sandu, A.','Ocean Dynamics, 65(11), 1423–1439 · Springer',''),
 (2015,'journal','An efficient implementation of the ensemble Kalman filter based on an iterative Sherman–Morrison formula','Nino-Ruiz, E. D., Sandu, A., Anderson, J.','Statistics and Computing, 25(3), 561–577 · Springer',''),
 (2015,'conf','An efficient parallel implementation of the ensemble Kalman filter based on shrinkage covariance matrix estimation','Nino-Ruiz, E. D., Sandu, A.','IEEE 22nd International Conference on High Performance Computing Workshops (HiPCW)',''),
 (2015,'conf','A parallel ensemble Kalman filter implementation based on modified Cholesky decomposition','Nino-Ruiz, E. D., Sandu, A., Deng, X.','6th Workshop on Latest Advances in Scalable Algorithms for Large-Scale Systems (ScalA), pp. 1–8',''),
 (2014,'conf','Variational Data Assimilation Based on Derivative-Free Optimization','Nino, E. D., Sandu, A.','International Conference on Dynamic Data-Driven Environmental Systems Science, pp. 239–250 · Springer',''),
]

NAV = [('Home','/'),('Research','/#research'),('Projects','/projects/'),('Publications','/publications/'),('Software','/software/'),('People','/people/'),('Talks & events','/talks/'),('Resources','/resources/')]

def shell(title, body, current='', desc='Applied Math and Computer Science Lab at Universidad del Norte, Barranquilla, Colombia.', depth=0, extra_head=''):
    rel = '../' * depth if depth else './'
    def href(h): return h.replace('/', rel, 1) if h.startswith('/') else h
    items = ''.join(f'<li><a href="{href(h)}"{" aria-current=\"page\"" if n==current else ""}>{n}</a></li>' for n, h in NAV)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<link rel="icon" href="{rel}assets/img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/css/site.css">
{extra_head}
</head>
<body>
<header class="site"><div class="wrap nav">
  <a href="{rel}"><img class="logo" src="{rel}assets/img/logo.png" alt="AML-CS: Applied Math and Computer Science Lab"></a>
  <nav aria-label="Main"><ul>{items}<li><a class="cta" href="mailto:enino@uninorte.edu.co">Join the lab</a></li></ul></nav>
  <button class="burger" aria-expanded="false" aria-label="Open menu">Menu</button>
</div></header>
{body}
<footer class="site"><div class="wrap">
  <div>
    <a href="{rel}"><img class="logo-foot" src="{rel}assets/img/logo.png" alt="AML-CS"></a>
    <p class="contact">Universidad del Norte, Km 5 Vía Puerto Colombia<br>Barranquilla, Colombia.<br><a href="mailto:enino@uninorte.edu.co">enino@uninorte.edu.co</a></p>
  </div>
  <div><h5>Lab</h5><ul><li><a href="{rel}#research">Research</a></li><li><a href="{rel}projects/">Projects &amp; funding</a></li><li><a href="{rel}people/">People</a></li></ul></div>
  <div><h5>Output</h5><ul><li><a href="{rel}publications/">Publications</a></li><li><a href="{rel}talks/">Talks &amp; events</a></li><li><a href="https://github.com/AML-CS">GitHub</a></li></ul></div>
  <div><h5>Tools</h5><ul><li><a href="{rel}software/">Software</a></li><li><a href="{rel}resources/">HPC guides</a></li><li><a href="{rel}wrf-baq-0.5km/">WRF-BAQ 0.5 km</a></li></ul></div>
  <div class="copy"><span>© {YEAR} AML-CS · Universidad del Norte</span><span>Director: <a href="https://enino84.github.io/">Elias D. Nino-Ruiz, Ph.D.</a></span></div>
</div></footer>
<script src="{rel}assets/js/site.js"></script>
</body></html>'''

def pagehead(title, sub, crumb, counts=''):
    return f'''<div class="pagehead"><div class="wrap">
  <div><div class="crumb"><a href="../">Home</a> / {crumb}</div><h1>{title}</h1><p>{sub}</p></div>
  {f'<div class="counts">{counts}</div>' if counts else '<div></div>'}
</div></div>'''

def write(path, content):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(content)

# ---------------------------------------------------------------- HOME
recent = [p for p in PUBS if p[0] >= 2024][:6]
recent_html = ''.join(f'<li><span class="year">{y}</span><div><div class="t">{"<a href=\"%s\">%s</a>" % (u, t) if u else t}</div><div class="v">{bold_lab(a)} · {v}</div></div>{f"<a class=\"l\" href=\"{u}\">Article</a>" if u else ""}</li>' for y,k,t,a,v,u in recent)

home = f'''
<section class="hero">
  <canvas id="da" aria-hidden="true"></canvas>
  <div class="wrap">
    <div>
      <h1>We teach models to listen to data.</h1>
      <p>The Applied Math and Computer Science Lab in Barranquilla, Colombia, builds data assimilation, inverse-problem and optimization methods that turn noisy observations into better forecasts for weather, air quality and the city around us.</p>
      <div class="actions"><a class="btn primary" href="#research">Explore our research</a><a class="btn ghost" href="publications/">Read the papers</a></div>
    </div><div></div>
    <div class="legend"><span><i style="background:#F0A92B"></i>ensemble members</span><span><i style="background:#fff"></i>observation</span><span><i style="background:#4BA2DE"></i>analysis</span></div>
  </div>
</section>
<div class="stats"><div class="wrap">
  <div><b>2017</b>Founded at Universidad del Norte</div>
  <div><b>{len(PUBS)}</b>Journal &amp; conference papers</div>
  <div><b>4</b><a href="software/" style="color:#9FC2E0">Open-source software packages</a></div>
  <div><b>WRF · 0.5 km</b>Operational forecasts for Barranquilla</div>
</div></div>
<div class="sponsors"><div class="wrap">
  <span>Research supported by</span>
  <a class="sponsor" href="projects/#minciencias"><img src="assets/img/sponsors/minciencias.png" alt="Minciencias: Ministerio de Ciencia, Tecnología e Innovación"></a>
  <a class="sponsor" href="projects/#banrep"><img src="assets/img/sponsors/banco-republica.png" alt="Banco de la República"><span>Banco de la República<small>FPIT research fund</small></span></a>
  <a class="sponsor" href="https://www.uninorte.edu.co/"><img src="assets/img/sponsors/uninorte-logo.jpg" alt="Universidad del Norte"></a>
</div></div>

<section id="research"><div class="wrap">
  <div class="sec-head"><h2>What we work on</h2><p>A space that brings together people from different fields of science, motivated to solve real problems through scientific computing, mathematics and statistics.</p></div>
  <div class="areas">
    <div class="area"><h3>Data assimilation</h3><p>Ensemble Kalman filters, 4D-Var and hybrid MCMC schemes that fold observations into numerical models, including non-Gaussian and adjoint-free formulations.</p><span>Core line</span></div>
    <div class="area"><h3>Inverse problems &amp; parameter estimation</h3><p>Recovering what we cannot measure directly from what we can, with shrinkage covariance estimators and modified Cholesky decompositions.</p><span>Core line</span></div>
    <div class="area"><h3>Numerical optimization</h3><p>Trust-region, line-search and random-direction methods for large, expensive objective functions.</p><span>Methods</span></div>
    <div class="area"><h3>Combinatorial optimization</h3><p>Tabu search, simulated annealing and nature-inspired algorithms applied to localization and scheduling problems.</p><span>Methods</span></div>
    <div class="area"><h3>Bayesian inference</h3><p>Posterior sampling and uncertainty quantification for physical models.</p><span>Methods</span></div>
    <div class="area"><h3>High performance computing</h3><p>Running WRF, MPI and parallel Python on UN-HPC to make all of the above feasible at real-world scale.</p><span>Infrastructure</span></div>
    <div class="area"><h3>Data science &amp; engineering</h3><p>Urban analytics, climate downscaling and PM2.5 monitoring for Barranquilla and the Colombian Caribbean.</p><span>Applications</span></div>
  </div>
</div></section>

<section class="tint" id="projects"><div class="wrap">
  <div class="sec-head"><h2>Funded projects</h2><p>Externally funded research where the lab leads or co-leads the work. Full details on the <a href="projects/">projects page</a>.</p></div>
  <div class="projects">
    <div class="proj amber">
      <div class="funder">Banco de la República · FPIT · Project 5.056</div>
      <h3>High-resolution atmospheric data repository for the Atlántico department via data assimilation and machine learning</h3>
      <p>A 1980–2100 dataset of wind, temperature and humidity for the Atlántico region, produced by downscaling NCEP-DOE Reanalysis 2 with data assimilation and machine learning. Released as the open-source TEDA framework.</p>
      <div class="row"><span><b>Role</b> Principal investigator</span><span><b>2024–2025</b></span><span class="status done">Completed</span></div>
    </div>
    <div class="proj">
      <div class="funder">Minciencias · SIGP 68747 / 68790 · with EAFIT and Universidad de Antioquia</div>
      <h3>ExPoR2: Ensemble of models to estimate human exposure to air pollutants in urban areas</h3>
      <p>Part of the ExPoR2 programme on human exposure to atmospheric pollution as a decision-making tool. The lab contributes ensemble-based data assimilation for air-quality models in the Tropical Andes.</p>
      <div class="row"><span><b>Role</b> Co-investigator</span><span><b>Started 2020</b></span><span class="status done">Completed</span></div>
    </div>
  </div>
</div></section>

<section id="publications"><div class="wrap">
  <div class="feat">
    <figure><img src="assets/img/figures/error-bounds.jpg" alt="Error bounds for solving linear systems in the preconditioned Crank–Nicolson scheme"><figcaption>Error bounds in the preconditioned Crank–Nicolson scheme. The black line separates convergence from divergence in proposal steps.</figcaption></figure>
    <div>
      <h3>A numerical method for solving linear systems in the preconditioned Crank–Nicolson algorithm</h3>
      <div class="meta">Nino-Ruiz, E. D. · Applied Mathematics Letters, Elsevier · 2020</div>
      <p>When can the linear solves inside pCN proposals be trusted? The paper gives explicit bounds on the error they introduce and a practical rule for choosing the step.</p>
      <a class="btn primary" href="https://doi.org/10.1016/j.aml.2020.106254">Read at the publisher</a>
    </div>
  </div>
  <div class="sec-head" style="margin-top:88px"><h2>Recent publications</h2><p>Journal, conference and software papers from the group and its collaborators.</p></div>
  <ul class="pubs">{recent_html}</ul>
  <div class="more"><a href="publications/">All {len(PUBS)} publications</a></div>
</div></section>

<section class="tint" id="gallery"><div class="wrap">
  <div class="sec-head"><h2>From the lab</h2><p>Figures from recent projects. Click one to enlarge it.</p></div>
  <div class="carousel"><button class="car-btn prev" aria-label="Scroll left">‹</button>
  <div class="strip">
    <figure><picture><source srcset="assets/img/figures/qg-model.webp" type="image/webp"><img class="fit" src="assets/img/figures/qg-model.jpg" alt="1.5-layer quasi-geostrophic model: potential vorticity and streamfunction on a 193 by 193 grid"></picture><figcaption>1.5-layer quasi-geostrophic model on a 193 × 193 grid: potential vorticity (left) and streamfunction (right). One of the test models in our data assimilation software.</figcaption></figure>
    <figure><img src="assets/img/figures/iota-simulation.gif" alt="WRF simulations of hurricane Iota"><figcaption>WRF simulations of hurricane Iota.</figcaption></figure>
    <figure><picture><source srcset="assets/img/figures/global-wind-da.webp" type="image/webp"><img class="fit" src="assets/img/figures/global-wind-da.jpg" alt="Global wind field at 925 mb: reference, background and analyses from several ensemble filters"></picture><figcaption>Global wind at 925 mb: reference, background and analyses from several ensemble-based filters.</figcaption></figure>
    <figure><img src="assets/img/figures/urban-analytics.jpg" alt="Car accidents in Barranquilla"><figcaption>Urban analytics: car accidents in Barranquilla.</figcaption></figure>
    <figure><img src="assets/img/figures/estimation-of-PM2.jpg" alt="PM2.5 estimation"><figcaption>Estimation of PM2.5 levels via Markovian models.</figcaption></figure>
    <figure><img src="assets/img/figures/levels-of-PM2.5.jpg" alt="PM2.5 levels per interval"><figcaption>Levels of PM2.5 per interval in Barranquilla.</figcaption></figure>
    <figure><img src="assets/img/figures/open-crime-estimation.jpg" alt="Open crime estimation"><figcaption>Open Crime Estimation: probability surface for different regions given a user profile.</figcaption></figure>
  </div>
  <button class="car-btn next" aria-label="Scroll right">›</button></div>
</div></section>


<section id="memories"><div class="wrap">
  <div class="sec-head"><h2>Good memories</h2><p>Workshops, visits and everyday life in the lab over the years. Click a photo to enlarge it.</p></div>
  <div class="carousel">
    <button class="car-btn prev" aria-label="Scroll left">‹</button>
    <div class="strip photos">
      <figure><img src="assets/img/memories/lab-team.jpg" alt="AML-CS members in the lab at Universidad del Norte"><figcaption>The lab at Universidad del Norte, whiteboard included.</figcaption></figure>
      <figure><img src="assets/img/memories/workshop-2019-sandu.jpg" alt="At the 1st International Workshop on Data Assimilation for Decision Making, Barranquilla 2019"><figcaption>1st International Workshop on Data Assimilation for Decision Making, Barranquilla, 2019.</figcaption></figure>
      <figure><img src="assets/img/memories/workshop-2019-speakers.jpg" alt="Speakers of the 1st International Workshop on Data Assimilation for Decision Making"><figcaption>Speakers and organisers of the 2019 workshop.</figcaption></figure>
      <figure><img class="fit" src="assets/img/memories/workshop-2020-poster.jpg" alt="Poster of the 2nd International Workshop on Data Assimilation for Decision Making, October 2020"><figcaption>2nd International Workshop on Data Assimilation for Decision Making, online, October 2020, with Jeffrey Anderson, Adrian Sandu, Geir Evensen and Arnold Heemink.</figcaption></figure>
      <figure><img src="assets/img/memories/modemat-ecuador.jpg" alt="Visit to MODEMAT, Ecuador"><figcaption>Visit to the Centro de Modelización Matemática (MODEMAT), Ecuador.</figcaption></figure>
      <figure><img src="assets/img/memories/lab-lunch.jpg" alt="Lab lunch"><figcaption>Lab lunch.</figcaption></figure>
      <figure><img class="fit" src="assets/img/memories/wmo-symposium.jpg" alt="At the WMO International Symposium on Data Assimilation"><figcaption>An early one: the WMO International Symposium on Data Assimilation, College Park, USA.</figcaption></figure>
    </div>
    <button class="car-btn next" aria-label="Scroll right">›</button>
  </div>
</div></section>

<section class="dark" id="people"><div class="wrap">
  <div class="sec-head"><h2>People</h2><p>Students face problems in data assimilation, inverse problems, applied statistics and numerical optimization from their first semester in the group.</p></div>
  <div class="director">
    <img src="assets/img/people/elias-nino.jpg" alt="Elias D. Nino-Ruiz">
    <div>
      <h3>Elias D. Nino-Ruiz, Ph.D.</h3>
      <div class="role">Director · Founded the lab in April 2017</div>
      <p>Data-driven models are of primary interest for us; it is fascinating to see what data can tell us about the underlying physical process. Feel free to contact me if you want to be part of the group.</p>
      <p style="margin-top:14px"><a href="https://enino84.github.io/">Personal site</a> &nbsp;·&nbsp; <a href="people/">Meet the whole team</a></p>
    </div>
  </div>
</div></section>

<section id="resources"><div class="wrap two" style="align-items:center">
  <div><h2 style="font-size:32px">Resources for the group</h2><p style="color:var(--muted);margin:10px 0 0">Practical guides we wrote so that nobody has to fight the cluster twice.</p></div>
  <ul class="pubs" style="border-top:0">
    <li style="grid-template-columns:1fr auto"><div class="t"><a href="resources/wrf-wrfda-unhpc/">Run WRF and WRFDA on UN-HPC</a></div><a class="l" href="resources/wrf-wrfda-unhpc/">Guide</a></li>
    <li style="grid-template-columns:1fr auto"><div class="t"><a href="resources/mpi4py-unhpc/">Set up mpi4py on UN-HPC</a></div><a class="l" href="resources/mpi4py-unhpc/">Guide</a></li>
    <li style="grid-template-columns:1fr auto"><div class="t"><a href="resources/python-conda-unhpc/">Run Python scripts with conda on UN-HPC</a></div><a class="l" href="resources/python-conda-unhpc/">Guide</a></li>
    <li style="grid-template-columns:1fr auto"><div class="t"><a href="wrf-baq-0.5km/">WRF Barranquilla 0.5 km forecast viewer</a></div><a class="l" href="wrf-baq-0.5km/">Open</a></li>
  </ul>
</div></section>
'''
write('index.html', shell('AML-CS: Applied Math and Computer Science Lab · Universidad del Norte', home, 'Home'))

# ---------------------------------------------------------------- PUBLICATIONS
cnt = Counter(p[1] for p in PUBS); years = sorted({p[0] for p in PUBS}, reverse=True)
label = {'journal':'Journal','conf':'Conference','soft':'Software'}
groups = []
for y in years:
    ps = [p for p in PUBS if p[0] == y]
    items = ''.join(f'<article class="pub" data-k="{k}"><div><div class="t">{"<a href=\"%s\">%s</a>" % (u,t) if u else t}</div><div class="au">{bold_lab(a)}</div><div class="v">{v}</div></div><div class="side"><span class="kind {k}">{label[k]}</span>{f"<a href=\"{u}\">Read</a>" if u else ""}</div></article>' for _,k,t,a,v,u in ps)
    groups.append(f'<section class="yeargroup" data-y="{y}"><h2>{y}<small>{len(ps)} papers</small></h2><div>{items}</div></section>')
ychips = ''.join(f'<button class="chip" aria-pressed="false" data-y="{y}">{y}</button>' for y in years)
pubs_page = pagehead('Publications', 'Journal articles, conference papers and software publications on data assimilation, inverse problems and optimization, 2014 to date. Lab members in bold.', 'Publications',
  f'<div><b>{len(PUBS)}</b>Papers</div><div><b>{cnt["journal"]}</b>Journal</div><div><b>{cnt["conf"]}</b>Conference</div><div><b>{cnt["soft"]}</b>Software</div>') + f'''
<div class="toolbar"><div class="wrap">
  <div class="chips" id="kind"><button class="chip" aria-pressed="true" data-k="all">All</button><button class="chip" aria-pressed="false" data-k="journal">Journal</button><button class="chip" aria-pressed="false" data-k="conf">Conference</button><button class="chip" aria-pressed="false" data-k="soft">Software</button></div>
  <div class="sep"></div>
  <div class="chips" id="year"><button class="chip" aria-pressed="true" data-y="all">All years</button>{ychips}</div>
  <input class="search" id="q" type="search" placeholder="Search title, author or venue">
</div></div>
<main class="wrap" style="padding:40px 0 96px">
{''.join(groups)}
<div class="empty" id="empty">No publications match. Clear the filters to see everything.</div>
<p style="margin-top:48px;font-family:var(--display);font-size:14px;color:var(--muted)">Complete record: <a href="https://orcid.org/0000-0001-7784-8163">ORCID</a> · <a href="https://scholar.google.com/citations?user=IE8dAAgAAAAJ&hl=en">Google Scholar</a> · <a href="https://www.scopus.com/authid/detail.uri?authorId=36603283600">Scopus</a></p>
</main>'''
write('publications/index.html', shell('Publications: AML-CS', pubs_page, 'Publications', depth=1))

# ---------------------------------------------------------------- PROJECTS
def facts(rows): return '<div class="facts"><dl>' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k,v in rows) + '</dl></div>'
projects = pagehead('Projects &amp; funding', 'Externally funded research programmes the lab leads or co-leads, and the institutions that make them possible.', 'Projects',
  '<div><b>2</b>Funded projects</div><div><b>3</b>Partner institutions</div><div><b>2</b>Funders</div>') + f'''
<section style="padding:64px 0 0"><div class="wrap">
  <div class="sponsors box">
    <span>Funders and partners</span>
    <a class="sponsor" href="#banrep"><img src="../assets/img/sponsors/banco-republica.png" alt="Banco de la República"><span>Banco de la República<small>Fondo para la Promoción de la Investigación y la Tecnología</small></span></a>
    <a class="sponsor" href="#minciencias"><img src="../assets/img/sponsors/minciencias.png" alt="Minciencias: Ministerio de Ciencia, Tecnología e Innovación"></a>
    <a class="sponsor" href="https://www.eafit.edu.co/"><img src="../assets/img/sponsors/eafit-logo.jpg" alt="Universidad EAFIT"></a>
    <a class="sponsor" href="https://www.uninorte.edu.co/"><img src="../assets/img/sponsors/uninorte-logo.jpg" alt="Universidad del Norte"></a>
  </div>
</div></section>

<section style="padding-top:24px"><div class="wrap">

<div class="pdetail" id="banrep">
  <div>
    <span class="status done">Completed · July 2025</span>
    <h2 style="margin-top:14px">High-resolution atmospheric data repository for climate-change studies in the Atlántico department</h2>
    <div class="lead">
      <p>Funded by the Banco de la República through its Fondo para la Promoción de la Investigación y la Tecnología (FPIT), the project built an open atmospheric dataset for the Atlántico department at high spatial resolution, covering 1980 to 2100.</p>
      <p>Zonal and meridional wind, temperature and humidity fields were obtained by downscaling the NCEP-DOE Reanalysis 2 with a combination of data assimilation and machine learning. Uncertainty was quantified against the OGIMET observational network, using precision matrices estimated via a modified Cholesky decomposition.</p>
      <p>The methods were released as open-source software: the TEDA framework (SoftwareX, 2025) and the DownscalingMethods repository.</p>
    </div>
    <ul class="outputs">
      <li><span>Software paper</span><a href="https://doi.org/10.1016/j.softx.2025.102297">TEDA: A lightweight Python framework for educational data assimilation, SoftwareX 31, 102297 (2025)</a></li>
      <li><span>Code</span><a href="https://github.com/enino84/TEDA">github.com/enino84/TEDA</a> · DownscalingMethods repository</li>
    </ul>
  </div>
  {facts([('Funder','Banco de la República, FPIT'),('Project','No. 5.056 · FPIT filing 184'),('Approved','Board of Directors, 5 August 2024'),('Funding','COP 18,000,000 of a COP 32,760,000 total budget'),('Duration','12 months · closed successfully July 2025'),('Principal investigator','Elias D. Nino-Ruiz'),('Co-investigator','H. R. Peñaranda Bello'),('Institution','Universidad del Norte')])}
</div>

<div class="pdetail" id="minciencias">
  <div>
    <span class="status done">Completed</span>
    <h2 style="margin-top:14px">ExPoR2: Ensemble of models to estimate human exposure to air pollutants</h2>
    <div class="lead">
      <p>The lab was a co-investigator in the programme <em>Human exposure models to atmospheric pollution in urban areas as a decision-making tool</em> (Exposure to Pollutants Regional Research, ExPoR2), funded by Minciencias and led by Universidad EAFIT with Universidad de Antioquia and Universidad del Norte as co-executing institutions.</p>
      <p>Within the programme, the project <em>Ensemble of models to estimate human exposure to atmospheric pollutants</em> developed ensemble-based data assimilation for air-quality models in the Tropical Andes, in collaboration with the Mathematical Modelling group led by Prof. Olga Lucía Quintero Montoya at EAFIT.</p>
    </div>
    <ul class="outputs">
      <li><span>Journal paper</span><a href="https://doi.org/10.1007/s10596-021-10035-4">An efficient ensemble Kalman Filter implementation via shrinkage covariance matrix estimation: exploiting prior knowledge, Computational Geosciences (2021)</a></li>
      <li><span>Journal paper</span><a href="https://doi.org/10.3390/s20030877">A Maximum Likelihood Ensemble Filter via a Modified Cholesky Decomposition for Non-Gaussian Data Assimilation, Sensors (2020)</a></li>
      <li><span>Event</span><a href="../talks/#workshop">3rd International Workshop on Data Assimilation</a>, organised as part of the programme</li>
    </ul>
  </div>
  {facts([('Funder','Ministerio de Ciencia, Tecnología e Innovación (Minciencias)'),('Programme','ExPoR2 · SIGP 68747 · COP 1,635,189,082'),('Project','SIGP 68790 · COP 389,949,080'),('Contract','No. 936-2019, 30 December 2019'),('Type','Research and development · external funding'),('Period','Started January 2020 · completed'),('Lead institution','Universidad EAFIT (Medellín)'),('Co-executing','Universidad de Antioquia · Universidad del Norte'),('Lab role','Co-investigator')])}
</div>


</div></section>'''
write('projects/index.html', shell('Projects & funding: AML-CS', projects, 'Projects', depth=1))


# ---------------------------------------------------------------- SOFTWARE
teda_methods = [
 ('AnalysisEnKF','EnKF with the full covariance matrix','Evensen (2009)'),
 ('AnalysisEnKFNaive','EnKF via an iterative Sherman-Morrison formula','Nino-Ruiz, Sandu, Anderson (2015)'),
 ('AnalysisEnKFCholesky','EnKF via Cholesky decomposition','Mandel (2006)'),
 ('AnalysisEnKFModifiedCholesky','EnKF via modified Cholesky decomposition','Nino-Ruiz, Sandu, Deng (2018)'),
 ('AnalysisEnKFShrinkagePrecision','EnKF with shrinkage precision matrix','Nino-Ruiz, Sandu (2015)'),
 ('AnalysisEnKFBLoc','EnKF with B-localization','Greybush et al. (2011)'),
 ('AnalysisEnSRF','Ensemble square root filter','Tippett et al. (2003)'),
 ('AnalysisETKF','Ensemble transform Kalman filter','Bishop, Etherton, Majumdar (2001)'),
 ('AnalysisLETKF','Local ensemble transform Kalman filter','Hunt, Kostelich, Szunyogh (2007)'),
 ('AnalysisLEnKF','Local ensemble Kalman filter','Ott et al. (2004)'),
]
mrows = ''.join(f'<tr><td><code>{c}</code></td><td>{d}</td><td>{r}</td></tr>' for c,d,r in teda_methods)
sw = pagehead('Software', 'Open-source code from the lab. Every package is documented in a SoftwareX paper and lives on GitHub.', 'Software',
  '<div><b>4</b>Packages</div><div><b>4</b>SoftwareX papers</div><div><b>10</b>Ensemble methods in TEDA</div>') + f"""
<section style="padding:64px 0"><div class="wrap">
  <div class="feat" id="pyteda">
    <figure><picture><source srcset="../assets/img/figures/qg-model.webp" type="image/webp"><img src="../assets/img/figures/qg-model.jpg" alt="1.5-layer quasi-geostrophic model: potential vorticity and streamfunction"></picture><figcaption>1.5-layer quasi-geostrophic model on a 193 × 193 grid, one of the benchmark models: potential vorticity (left) and streamfunction (right).</figcaption></figure>
    <div>
      <span class="status">Benchmarking platform · FastAPI · 2026</span>
      <h3 style="margin-top:14px">PyTEDA-web</h3>
      <div class="meta">Nino-Ruiz, E. D. · SoftwareX 34, 102738 · 2026</div>
      <p>A web platform for interactive data assimilation benchmarking. Experiments run on the server and stream their output to the browser in real time, and every run is stored so it can be compared later. It builds on the TEDA code base and adds larger test models such as the quasi-geostrophic model shown here.</p>
      <p style="margin:0"><a class="btn primary" href="pyteda/">About PyTEDA-web</a> &nbsp; <a class="btn dark" href="https://github.com/enino84/pyTEDA">GitHub</a> &nbsp; <a class="btn ghost" style="border-color:var(--rule);color:var(--navy)" href="https://doi.org/10.1016/j.softx.2026.102738">Paper</a></p>
    </div>
  </div>
</div></section>

<section class="tint" id="teda"><div class="wrap">
  <div class="sec-head"><h2>TEDA</h2><p>A lightweight, object-oriented Python toolbox for teaching ensemble-based data assimilation. Students pick a method, a toy model and an observation setup, run the simulation and look at how background and analysis errors evolve.</p></div>
  <div class="two" style="align-items:start">
    <div class="prose">
      <h3 style="margin-top:0">How easy is it to use?</h3>
      <pre><code>from analysis.analysis_enkf_modified_cholesky \\
    import AnalysisEnKFModifiedCholesky

model = Lorenz96()
background = Background(model, ensemble_size=20)
analysis = AnalysisEnKFModifiedCholesky(model, r=2)
observation = Observation(m=32, std_obs=0.01)

params = {{'obs_freq': 0.1,
          'obs_times': 10,
          'inf_fact': 1.04}}
simulation = Simulation(model, background,
                        analysis, observation,
                        params=params)
simulation.run()

# background and analysis errors per step
errb, erra = simulation.get_errors()</code></pre>
      <p>Toy models included: the Duffing equation (2 variables), Lorenz-63 (3 variables) and Lorenz-96 (40 variables), all chaotic under the right parameters. New models and methods plug in through the same abstract classes.</p>
      <p style="margin:0"><a class="btn dark" href="https://github.com/enino84/TEDA">GitHub</a> &nbsp; <a class="btn primary" href="https://doi.org/10.1016/j.softx.2025.102297">Paper, SoftwareX 2025</a> &nbsp; <a class="btn ghost" style="border-color:var(--rule);color:var(--navy)" href="https://doi.org/10.1007/978-3-031-08760-8_60">ICCS 2022</a></p>
    </div>
    <div class="prose" style="max-width:none">
      <h3 style="margin-top:0">Supported methods</h3>
      <table><thead><tr><th>Class</th><th>Method</th><th>Reference</th></tr></thead><tbody>{mrows}</tbody></table>
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><h2>Research packages</h2><p>Code we use in our own experiments, packaged for reuse.</p></div>
  <div class="projects">
    <div class="proj" id="amlcs-da">
      <div class="funder">Research package · Python · SoftwareX 2023</div>
      <h3>AMLCS-DA</h3>
      <p>Data assimilation for atmospheric general circulation models. This is the package the lab uses for experiments with the SPEEDY model at near-operational resolutions, including ensemble-based methods for its leapfrog integration scheme.</p>
      <div class="row"><a href="https://github.com/enino84/AMLCS"><b>GitHub</b></a><a href="https://doi.org/10.1016/j.softx.2023.101374"><b>Paper</b></a><a href="https://doi.org/10.1002/qj.4424"><b>QJRMS 2023</b></a></div>
    </div>
    <div class="proj amber" id="mcholesky">
      <div class="funder">Statistical package · SoftwareX 2025</div>
      <h3>Precision matrices via modified Cholesky decomposition</h3>
      <p>The <code>aml_pred_assim</code> package estimates precision (inverse covariance) matrices from small samples in high dimensions via a modified Cholesky decomposition. It downloads climate fields from the Copernicus Climate Data Store, builds the predecessor structure of each grid point and fits the sparse factors with ridge regression, saving everything to NetCDF.</p>
      <div class="row"><a href="https://github.com/Dysaca22/aml_pred_assim"><b>GitHub</b></a><a href="https://github.com/Dysaca22/aml_pred_assim/blob/main/Modules_Guide.md"><b>Modules guide</b></a><a href="https://doi.org/10.1016/j.softx.2025.102125"><b>Paper</b></a></div>
    </div>
  </div>
</div></section>"""
write('software/index.html', shell('Software · AML-CS', sw, 'Software', depth=1))

# PyTEDA dedicated page
pyteda = f"""
<div class="pagehead" style="padding-bottom:0"><div class="wrap" style="display:block">
  <div class="crumb"><a href="../../">Home</a> / <a href="../">Software</a> / PyTEDA-web</div>
  <h1>PyTEDA-web</h1>
  <p style="max-width:60ch">Interactive data assimilation benchmarking in the browser: experiments run on the server, stream their results live and stay stored so you can come back and compare them.</p>
  <div class="hero-media"><picture><source srcset="../../assets/img/figures/qg-model.webp" type="image/webp"><img src="../../assets/img/figures/qg-model.jpg" alt="1.5-layer quasi-geostrophic model: potential vorticity and streamfunction on a 193 by 193 grid"></picture></div>
</div></div>
<section style="padding-top:40px"><div class="wrap two" style="align-items:start">
  <div class="prose">
    <p style="font-family:var(--display);font-size:13px;color:var(--muted);text-align:left">Above: 1.5-layer quasi-geostrophic model on a 193 × 193 grid, potential vorticity (left) and streamfunction (right), one of the benchmark models in PyTEDA-web.</p>
    <h2 style="margin-top:8px">What it does</h2>
    <p>PyTEDA-web is a FastAPI platform built on the TEDA code base. Instead of running scripts locally, you configure a data assimilation experiment in the browser, launch it, and watch the output arrive in real time while it runs on the server.</p>
    <p>Every experiment is tracked and persisted, so results from different methods, ensemble sizes, observation networks or models can be compared side by side days later, without rerunning anything.</p>
    <h2>Benchmark models</h2>
    <p>Besides the Duffing, Lorenz-63 and Lorenz-96 models inherited from TEDA, PyTEDA-web adds larger test cases such as the 1.5-layer quasi-geostrophic model shown above, which brings realistic multi-scale dynamics to the benchmarks at a size that still runs interactively.</p>
    <h2>Methods</h2>
    <p>All ensemble-based methods available in TEDA can be benchmarked: the stochastic EnKF and its Cholesky and modified Cholesky variants, shrinkage precision estimators, B-localization, EnSRF, ETKF, LETKF and LEnKF.</p>
    <p style="margin-top:28px"><a class="btn dark" href="https://github.com/enino84/pyTEDA">GitHub</a> &nbsp; <a class="btn primary" href="https://doi.org/10.1016/j.softx.2026.102738">Paper, SoftwareX 2026</a></p>
  </div>
  {facts([('Package','PyTEDA-web'),('Type','Web platform · FastAPI · Python'),('Paper','SoftwareX 34, 102738 (2026)'),('Author','Elias D. Nino-Ruiz'),('Builds on','TEDA (SoftwareX 2025)'),('Code','github.com/enino84/pyTEDA'),('License','Open source')])}
</div></section>
"""
write('software/pyteda/index.html', shell('PyTEDA-web · AML-CS', pyteda, 'Software', depth=2))


# ---------------------------------------------------------------- PEOPLE
def person(img, name, role, link=''):
    im = f'<img src="../assets/img/people/{img}" alt="{name}">' if img else '<i></i>'
    l = f' · <a href="{link}">Website</a>' if link else ''
    return f'<div class="person">{im}<h3>{name}</h3><p>{role}{l}</p></div>'
people = pagehead('People', 'The director, current students and everyone who has been part of the lab since 2017.', 'People') + f'''
<section class="dark" style="padding:64px 0"><div class="wrap">
  <div class="director" style="border:0;margin:0;padding:0">
    <img src="../assets/img/people/elias-nino.jpg" alt="Elias D. Nino-Ruiz">
    <div>
      <h3>Elias D. Nino-Ruiz, Ph.D.</h3>
      <div class="role">Director · Professor, Department of Computer Science and Engineering, Universidad del Norte</div>
      <p>Founded the lab in April 2017. Works on ensemble-based data assimilation, covariance matrix estimation and numerical optimization for atmospheric models.</p>
      <div class="profiles"><a href="https://enino84.github.io/">Personal site</a><a href="https://orcid.org/0000-0001-7784-8163">ORCID</a><a href="https://scholar.google.com/citations?user=IE8dAAgAAAAJ&hl=en">Google Scholar</a><a href="mailto:enino@uninorte.edu.co">Email</a></div>
    </div>
  </div>
</div></section>
<section><div class="wrap">
  <div class="sec-head"><h2>Current students</h2><p>Students working with the group.</p></div>
  <div class="grid-people">
    {person('hernaldo-penaranda.jpg','Hernaldo R. Peñaranda Bello','Ph.D. student · Atmospheric data downscaling via data assimilation and machine learning · Co-investigator, Banco de la República FPIT project')}
  </div>
</div></section>
<section class="tint"><div class="wrap">
  <div class="sec-head"><h2>Alumni</h2><p>Former students of the lab and the work they did with us.</p></div>
  <div class="grid-people">
    {person('andres-movilla.jpg','Andres Felipe Movilla Obregon','M.Sc. in Computer Science','https://andremov.github.io')}
    {person('giuliano.jpg','Giuliano','M.Sc. in Computer Science')}
    {person('alejandro-manotas.jpg','Alejandro Manotas','M.Sc. in Computer Science')}
    {person('omar-mejia.jpg','Omar Angel Mejia Suarez','M.Sc. in Computer Science · Data assimilation for air-quality estimation','https://sites.google.com/view/omarmejiasuarez/inicio')}
    {person('sebastian-ariza.jpg','Sebastian Ariza','M.Sc. in Computer Science')}
    {person('juan-calabria.jpg','Juan C. Calabria Sarmiento','M.Sc. in Computer Science · 4D-Var for wind energy estimation')}
    {person('luis-guzman.jpg','Luis G. Guzman Reyes','M.Sc. in Computer Science · Shrinkage covariance estimation in EnKF')}
    {person('rolando-beltran.jpg','Rolando Beltran Arrieta','M.Sc. in Computer Science · Adjoint-free 4D-Var')}
    {person('alfonso-mancilla.jpg','Alfonso Mancilla Herrera','M.Sc. in Computer Science · Non-Gaussian data assimilation')}
    {person('randy-consuegra.jpg','Randy Consuegra Ortega','M.Sc. in Computer Science · AMLCS-DA package')}
    {person('felipe-acevedo.jpg','Felipe Acevedo García','M.Sc. in Computer Science · Data-driven weather forecast')}
    {person('luis-morales.jpg','Luis E. Morales Retat','M.Sc. in Computer Science · Adaptive localization via Tabu Search')}
    {person('juan-rodriguez.jpg','Juan Rodriguez','M.Sc. in Computer Science')}
  </div>
</div></section>'''
write('people/index.html', shell('People: AML-CS', people, 'People', depth=1))

# ---------------------------------------------------------------- TALKS & EVENTS
series = [
 ('31-07-2020','31 Jul 2020','Spanish','Algunos aspectos teóricos y prácticos de la asimilación de datos en la predicción meteorológica','Juan Carlos De Los Reyes, Ph.D. · MODEMAT, Ecuador','https://youtu.be/05F8pX-IIIA'),
 ('14-08-2020','14 Aug 2020','English','Scientific Machine Learning and its potentials','Haiyan Cheng, Ph.D. · Willamette University, USA',''),
 ('28-08-2020','28 Aug 2020','English','Nature-inspired algorithms: challenges and open problems','Xin-She Yang, Ph.D. · National Physical Laboratory / Middlesex University, UK','https://drive.google.com/file/d/1QXyE74a6RNGI6DvfOby0ORhRuLgzB7tl/view?usp=sharing'),
 ('11-09-2020','11 Sep 2020','English','Calibration and Kalman filtering for tide and storm-surge models','Martin Verlaan, Ph.D. · Deltares, The Netherlands','https://youtu.be/K3Yt4zkXyUk'),
 ('12-11-2020','12 Nov 2020','Spanish','Towards scalable algorithms for distributed optimization and learning','César A. Uribe, Ph.D. · Massachusetts Institute of Technology, USA','https://youtu.be/zw-S7B2h3cM'),
 ('24-11-2020','24 Nov 2020','English','Data assimilation: from dynamically based to data-driven approaches','Alberto Carrassi, Ph.D. · University of Reading, UK / Utrecht University','https://youtu.be/6rDwD6CqPBM'),
 ('18-03-2021','18 Mar 2021','Spanish','Model error covariance estimation in particle filters using batch and online smoother-free adaptations of the EM algorithm','María Magdalena Lucini, Ph.D. · FaCENA, UNNE / CONICET, Argentina','https://drive.google.com/file/d/140gKi8jwk1bONUfC7kczxscHJRap59xT/view?usp=sharing'),
]
vids = ''.join(f'<div class="video">{f"<a href=\"{u}\">" if u else ""}<img src="../assets/img/talks/{img}.jpg" alt="{t}">{"</a>" if u else ""}<h3>{f"<a href=\"{u}\">{t}</a>" if u else t}</h3><p>{d} · {lang}{" · Recording" if u else ""}<br>{v}</p></div>' for img,d,lang,t,v,u in series)
keynotes = [
 ('9 Jun 2021','Ensemble based Data Assimilation via a Modified Cholesky Decomposition','EnKF Workshop 2021 · NORCE, Norway · English','http://www.youtube.com/watch?v=7_laGIOn__I&t=238m39s','Keynote'),
 ('22 Jan 2019','Ensemble Kalman Filter Based on a Modified Cholesky Decomposition','ISDA 2019, RIKEN R-CCS, Kobe, Japan · English','https://www.youtube.com/watch?v=1eqTuMCGnKY','Keynote'),
 ('24 Jun 2021','Implementaciones eficientes de métodos de asimilación de datos secuenciales para el pronóstico meteorológico','AUGM webinar · Spanish','https://www.youtube.com/watch?v=F-fp1Ze5a7g','Invited'),
 ('27 May 2020','Uso de la analítica de datos para enfrentar los nuevos y rápidos retos de nuestra sociedad','Universidad del Norte webinar · Spanish','https://www.youtube.com/watch?v=COo-wWCS46o','Invited'),
 ('15 May 2020','Métodos de machine learning e inteligencia artificial: oportunidades para estimar el impacto del SARS-CoV-2 en Colombia','Universidad del Norte webinar · Spanish','https://www.youtube.com/watch?v=mW3P-UxZDZA','Invited'),
 ('19 Sep 2019','Efficient Implementation of Ensemble Based Methods','1st International Workshop on Data Assimilation for Decision Making, Barranquilla · English','https://youtu.be/cf80zobQzGM','Invited'),
 ('27 Nov 2018','Covariance Matrix Estimation','Ph.D. in Mathematical Engineering seminar, Universidad EAFIT · English','https://youtu.be/LELXfvfQTXE','Invited'),
]
kh = ''.join(f'<div class="talk"><time>{d}</time><div><a href="{u}">{t}</a><small>{v} · {k}</small></div></div>' for d,t,v,u,k in keynotes)
program = [('08:00','Welcome and programme presentation',''),('08:10','Data Assimilation Context','Elias D. Niño Ruiz, Universidad del Norte'),('08:30','Localized Stochastic Shrinkage Rejuvenation in the Ensemble Transport Particle Filter','Andrey Popov, Virginia Tech, USA'),('09:10','Data-Driven Methods for Weather Forecast','Felipe Acevedo, Universidad del Norte'),('09:30','On the robustness of Ensemble Based Data Assimilation','Santiago Lopez, Universidad EAFIT'),('10:00','Assimilating infrasound measurements to constrain stratospheric variables','Javier Amezcua, University of Reading, UK'),('10:40','Data Assimilation using the EnKF with a Modified Cholesky decomposition','Randy Consuegra, Universidad del Norte'),('11:00','Ensemble Kalman Smoother via Modified Cholesky Decomposition','Andres Yarce Botero, TU Delft'),('11:20','Variance localization schemes via precision matrix in numerical weather forecast','Valentina Movil Sandoval, Universidad EAFIT'),('11:40','Airborne atmospheric measurement and data assimilation platform','Simple-Space EAFIT')]
ph = ''.join(f'<div class="talk"><time>{t} COT</time><div>{x}<small>{s}</small></div></div>' for t,x,s in program)
talks = pagehead('Talks &amp; events', 'Recorded talks by the lab and its guests, workshops we organise, and calls for papers.', 'Talks &amp; events') + f'''
<section><div class="wrap">
  <div class="sec-head"><h2>Talk series in Computer Science and Applications</h2><p>An online series of invited talks hosted by the lab in 2020–2021. Recordings where available.</p></div>
  <div class="videos">{vids}</div>
</div></section>
<section class="tint"><div class="wrap two">
  <div><div class="sec-head" style="grid-template-columns:1fr;gap:10px"><h2>Keynote and invited talks</h2><p>By Elias D. Nino-Ruiz.</p></div>{kh}</div>
  <div>
    <div class="sec-head" style="grid-template-columns:1fr;gap:10px"><h2>Calls &amp; awards</h2><p></p></div>
    <div class="event"><span class="tag">Call for papers</span><h3>IJAI special issue on machine learning methods to solve inverse problems</h3><p>International Journal of Artificial Intelligence. Topics: data assimilation, inverse problems, uncertainty quantification, data-driven models. Guest editor: Elias D. Nino-Ruiz. <a href="http://www.ceser.in/ceserp/index.php/ijai/about/editorialPolicies#custom-1">Special issue website</a>.</p></div>
    <div class="event"><span class="tag">Award</span><h3>Best Workshop Paper Award, ICCS 2017</h3><p>A Surrogate Model Based on Mixtures of Taylor Expansions for Trust Region Based Methods. Zurich, June 2017.</p></div>
  </div>
</div></section>
<section id="workshop"><div class="wrap">
  <div class="sec-head"><h2>3rd International Workshop on Data Assimilation</h2><p>Organised by Universidad del Norte, AML-CS and Universidad EAFIT as part of the Minciencias-funded ExPoR2 programme (SIGP 68747).</p></div>
  <div class="two">
    <div class="prose">
      <p>Data assimilation adjusts an imperfect numerical forecast according to real, noisy observations. The workshop addressed open issues in the community: efficient implementations of background error covariance estimators, matrix-free ensemble Kalman filters for highly non-linear models, adjoint-free 4D-Var methods, and sampling methods for non-Gaussian data assimilation.</p>
      <p style="margin-top:20px"><img src="../assets/img/sponsors/uninorte-logo.jpg" alt="Universidad del Norte" style="height:56px;margin-right:24px;vertical-align:middle"><img src="../assets/img/sponsors/eafit-logo.jpg" alt="Universidad EAFIT" style="height:56px;vertical-align:middle"></p>
    </div>
    <div>{ph}</div>
  </div>
</div></section>'''
write('talks/index.html', shell('Talks & events: AML-CS', talks, 'Talks & events', depth=1))

# ---------------------------------------------------------------- RESOURCES (guides from markdown)
GUIDES = [
 ('wrf-wrfda-unhpc','posts/wrf-wrfda-syseng-unhpc/index.md','Run WRF and WRFDA on UN-HPC','Install, configure and run the Weather Research and Forecasting model and WRFDA on CentOS 7 / OpenHPC.','June 2021'),
 ('mpi4py-unhpc','posts/run-mpi4py-unhpc/index.md','Set up mpi4py on UN-HPC','mpi4py with miniconda, with examples for interactive sessions and SBATCH jobs.','April 2021'),
 ('python-conda-unhpc','posts/run-python-scripts-unhpc/index.md','Run Python scripts with conda on UN-HPC','Virtual environments on the cluster, plus JupyterLab through an SSH tunnel.','June 2021'),
 ('netcdf-c-fortran','posts/install-c-and-fortran-netcdf/index.md','Install C and Fortran NetCDF libraries','Step-by-step PDF for Ubuntu.','February 2017'),
]
def md_body(path):
    txt = open(os.path.join(SRC, path)).read()
    txt = re.sub(r'^---.*?---\s*', '', txt, flags=re.S).replace('<!--more-->', '')
    return markdown.markdown(txt, extensions=['fenced_code', 'tables'])
cards = ''.join(f'<a class="guide" href="{slug}/"><h3>{t}</h3><p>{d}</p><span>{when}</span></a>' for slug,_,t,d,when in GUIDES)
res = pagehead('Resources', 'Guides for the Universidad del Norte HPC cluster, the Barranquilla forecast viewer and the software the lab maintains.', 'Resources') + f'''
<section><div class="wrap">
  <div class="sec-head"><h2>HPC guides</h2><p>Written for UN-HPC (CentOS 7 / OpenHPC), but most steps apply to any Slurm cluster.</p></div>
  <div class="guides">{cards}</div>
</div></section>
<section class="tint"><div class="wrap">
  <div class="sec-head"><h2>Tools &amp; software</h2><p>Open-source code and operational systems maintained by the group.</p></div>
  <div class="guides">
    <a class="guide" href="../wrf-baq-0.5km/"><h3>WRF-BAQ 0.5 km forecast viewer</h3><p>Barranquilla forecasts at 0.5 km grid spacing, updated every 3 hours on the Granado HPC cluster.</p><span>Operational</span></a>
    <a class="guide" href="../software/"><h3>Software packages</h3><p>TEDA, PyTEDA-web, AMLCS-DA and the modified Cholesky precision package, all open source and documented in SoftwareX.</p><span>Software page</span></a>
  </div>
</div></section>'''
write('resources/index.html', shell('Resources: AML-CS', res, 'Resources', depth=1))
for slug, path, t, d, when in GUIDES:
    body = pagehead(t, d, f'<a href="../">Resources</a> / Guide') + f'<section><div class="wrap"><article class="prose">{md_body(path)}</article></div></section>'
    body = body.replace('<div class="crumb"><a href="../">Home</a>', '<div class="crumb"><a href="../../">Home</a>')
    write(f'resources/{slug}/index.html', shell(f'{t}: AML-CS', body, 'Resources', depth=2))

# ---------------------------------------------------------------- WRF-BAQ
wrf = open(os.path.join(SRC, 'wrf-baq-0.5km/index.md')).read()
wrf = re.sub(r'^---.*?---\s*', '', wrf, flags=re.S)
wrf_html = markdown.markdown(wrf, extensions=['fenced_code', 'tables'])
wrf_body = pagehead('WRF-BAQ 0.5 km forecast', 'Barranquilla forecasts at 0.5 km grid spacing, updated every 3 hours on the Granado HPC cluster at Universidad del Norte.', 'WRF-BAQ 0.5 km') + f'<section><div class="wrap"><article class="prose" style="max-width:none">{wrf_html}</article></div></section>'
write('wrf-baq-0.5km/index.html', shell('WRF-BAQ 0.5 km forecast: AML-CS', wrf_body, 'Resources', depth=1,
  extra_head='<link rel="stylesheet" href="../assets/css/wrf-baq.css"><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css"><script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js"></script><script src="../assets/js/wrf-baq.js"></script><script>document.addEventListener("DOMContentLoaded",()=>{if(window.initWRFBaqApp)window.initWRFBaqApp()});</script>'))

open(os.path.join(OUT, '.nojekyll'), 'w').write('')
open(os.path.join(OUT, 'README.md'), 'w').write('''# AML-CS website

Sitio estático del Applied Math and Computer Science Lab (Universidad del Norte).
No necesita Hugo ni Jekyll: es HTML, CSS y JS puros, listo para GitHub Pages.

## Cómo publicar

1. Borra el contenido anterior del repo `AML-CS.github.io` (o crea una rama nueva).
2. Copia **todo** lo que hay en esta carpeta en la raíz del repo.
3. `git add -A && git commit -m "Nuevo diseño" && git push`
4. En Settings → Pages asegúrate de que la fuente sea la rama `master`/`main`, carpeta `/ (root)`.

## Estructura

- `index.html`: portada
- `projects/`: proyectos y financiadores (Banco de la República, Minciencias)
- `publications/`: lista completa con filtros
- `people/`, `talks/`, `resources/`, `wrf-baq-0.5km/`
- `assets/css/site.css`: todo el diseño
- `assets/js/site.js`: menú móvil, animación del hero, filtros de publicaciones
- `assets/img/`: logo, fotos y figuras

## Cómo editar

- **Publicaciones y contenido**: el sitio se genera con `build.py` (incluido). Edita la lista `PUBS`
  o los textos en ese archivo y ejecuta `python3 build.py` para regenerar todas las páginas.
  También puedes editar los `.html` directamente si es un cambio pequeño.
- **Logos de patrocinadores**: en `assets/img/sponsors/`.
- **Fotos de estudiantes**: `assets/img/people/`, cuadradas (480×480).
''')
print('built')
