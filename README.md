# 3DCPath-datasets
Compilation of publicly available datasets in 3D Computational Pathology

## Volumetric morphological/imaging data

<div style="overflow-x: auto;">
<table>
  <thead>
    <tr>
      <th>Venue / Date</th>
      <th>Dataset</th>
      <th>Title</th>
      <th>Modality</th>
      <th>Resolution</th>
      <th>Organ</th>
      <th>Volumes</th>
      <th>Size</th>
    </tr>
  </thead>
  <tbody>
    </tr>
      <tr>
      <td><em>arXiv<em>(2025)</td>
      <td>
        <a href="https://huggingface.co/datasets/cristinaperez9/VISTACT"><strong>VISTACT</strong></a><br>
      </td>
      <td>VIrtual histological STAining of micro-Computed Tomography (VISTACT)</td>
      <td>Synchtron-based phase-contrast microCT and serial H&E and EvG-stained histological sections</td>
      <td> Human lung microCT scans: 1.63 μm/voxel ; Mouse lung microCT scan: 0.88 μm/voxel</td>
      <td>Human lung tissue from patients with pulmonary hypertension and mice heart-lung tissue</td>
      <td>10 from human tissue (4 patients), and 1 from mice tissue</td>
      <td>869GB</td>
    </tr>
    <tr>
      <td><em>Cancer Research<em>(March 2023)</td>
      <td>
        <a href="https://www.cancerimagingarchive.net/collection/pca_bx_3dpathology/"><strong>PCa_Bx_3Dpathology</strong></a><br>
        <a href="https://aacrjournals.org/cancerres/article/82/2/334/675486/Prostate-Cancer-Risk-Stratification-via?guestAccessKey="><strong>[Paper]</strong></a>
      </td>
      <td>3D pathology of prostate biopsies with biochemical recurrence outcomes: raw H&E-analog datasets and image translation-assisted segmentation in 3D (ITAS3D) datasets</td>
      <td>OTLS</td>
      <td>0.88 μm/pixel</td>
      <td>Human prostate</td>
      <td>118 (50 patients)</td>
      <td>3.8TB</td>
    </tr>
      <tr>
      <td><em>MICCAI challenge<em>(2023)</td>
      <td>
        <a href="https://acrobat.grand-challenge.org/"><strong>ACROBAT</strong></a><br>
      </td>
      <td>AutomatiC Registration Of Breast cAncer Tissue (ACROBAT)</td>
      <td>H&E and IHC (ER, PGR, HER2, KI67)</td>
      <td> Multiple. Validation conducted at 1.25x</td>
      <td>Human breast cancer</td>
      <td>750 (1 H&E and 1-4 matched routine IHC)</td>
      <td>n/a</td>
    </tr>
    <tr>
      <td><em>PNAS<em>(2022)</td>
      <td>
        <a href="https://zenodo.org/records/5658994#.YZKJWXso_mF"><strong>3D virtual histology of the human hippocampus</strong></a><br>
        <a href="https://www.pnas.org/doi/10.1073/pnas.2113835118"><strong>[Paper]</strong></a>
      </td>
      <td>Three-dimensional virtual histology of the human hippocampus based on phase-contrast computed tomography</td>
      <td>Phase-contrast microCT (Histomography scanner)</td>
      <td>n/a</td>
      <td>Human hippocampus</td>
      <td>n/a</td>
      <td>64.8GB</td>
</tr>
    </tr>
      <td><em>eLife<em>(2021)</td>
      <td>
        <a href="https://zenodo.org/records/5658380"><strong>3D virtual Histopathology</strong></a><br>
        <a href="https://elifesciences.org/articles/71359"><strong>[Paper]</strong></a>
      </td>
      <td>3D virtual histopathology of cardiac tissue from Covid-19 patients based on phase-contrast X-ray tomography</td>
      <td>Phase-contrast microCT (Histomography scanner)</td>
      <td>1.3µm</td>
      <td>Cardiac Tissue from Covid-19 Patients</td>
      <td>6</td>
      <td>175.4 GB</td>
    <tr>
      <td><em>eLife<em>(2020)</td>
      <td>
        <a href="https://zenodo.org/records/3892637"><strong>3D virtual pathohistology</strong></a><br>
        <a href="https://elifesciences.org/articles/60408"><strong>[Paper]</strong></a>
      </td>
      <td>3D virtual pathohistology of lung tissue from Covid-19 patients</td>
      <td>Phase-contrast microCT (Histomography scanner)</td>
      <td>1.3µm, 650nm, and 167nm</td>
      <td>Human lung tissue</td>
      <td>6 Covid-19 patients and one control tissue (healthy lung)</td>
      <td>568.4GB</td>
    </tr>
  </tbody>
</table>
</div>



## Volumetric genomic data
StarMAP and RiBOMAP should have some data, but theses are purely molecular

## Volumetric morphological & genomic data 

<div style="overflow-x: auto;">
<table>
  <thead>
    <tr>
      <th>Journal / Date</th>
      <th>Dataset</th>
      <th>Title</th>
      <th>Modality</th>
      <th>Resolution</th>
      <th>Organ</th>
      <th>Volumes</th>
      <th>Serial sections</th>
      <th>Num. spots/cells</th>
      <th>Size</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><em>Cell<em> (July 2024)</td>
      <td>
        <a href="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE251926"><strong>OpenST</strong></a><br>
        <a href="https://www.cell.com/cell/fulltext/S0092-8674(24)00636-6"><strong>[Paper]</strong></a>
      </td>
      <td>Open-ST: High-resolution spatial transcriptomics in 3D</td>
      <td>Serial H&E sections and OpenST transcriptomics</td>
      <td>0.345 μm/pixel, single-cell ST data</td>
      <td>Head-and-neck metastatic lymph node</td>
      <td>1 (1 patient)</td>
      <td>19</td>
      <td>1,097,769 cells</td>
      <td>2.2GB</td>
    </tr>
    <tr>
      <td><em>Nature Communications<em> (February 2022)</td>
      <td>
        <a href="https://singlecell.broadinstitute.org/single_cell/study/SCP1414/3dst-ra#study-summary"><strong>3DST_RA</strong></a><br>
        <a href="https://www.nature.com/articles/s42003-022-03050-3"><strong>[Paper]</strong></a>
      </td>
      <td>Three-dimensional spatial transcriptomics uncovers cell type localizations in the human rheumatoid arthritis synovium</td>
      <td>Serial H&E sections and Spatial Transcriptomics</td>
      <td>20x, Spatial Transcriptomics technology (~100μm-diameter spots)</td>
      <td>Synovial joints (Rheumatoid arthritis)</td>
      <td>6 (6 patients)</td>
      <td>27 (RA1: 4, RA2: 7, RA3: 4, RA4: 3, RA5: 5, RA6: 4). RA1 spacing between sections -> 21μm ; RA2~RA6: consecutive sections  </td>
      <td>17,117 spots</td>
      <td>2.2GB (.gz format)</td>
    </tr>
  </tbody>
</table>
</div>




 
