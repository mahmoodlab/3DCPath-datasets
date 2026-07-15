# 3DCPath-datasets: A compilation of publicly available datasets in 3D pathology

*3DCPath-datasets* is a compilation of publicly available datasets in 3D Computational Pathology (3D CPath), spanning morphological data (3D tissue images) and molecular 3D data. It is organized into three main categories: [volumetric morphological/imaging data](#volumetric-morphologicalimaging-data), [volumetric genomic data](#volumetric-genomic-data), and [combined volumetric morphological and genomic data](#volumetric-morphological-and-genomic-data). The goal of this repository is to accelerate research in 3D CPath and provide the community with a centralized place to access 3D pathology datasets for future studies.

> [!NOTE]
> Contributions are welcome! Please check the [contributions](#contributions) section below!

## Updates

- **07/22/26**: *3DCPath-datasets* is now live and will be continuously updated as new datasets become available.

## Volumetric morphological/imaging data

<div>
<table width="1600">
  <thead>
    <tr>
      <th width="115">Added</th>
      <th width="150">Venue / Date</th>
      <th width="160">Dataset</th>
      <th width="360">Title</th>
      <th width="200">Modality</th>
      <th width="180">Resolution</th>
      <th width="180">Organ</th>
      <th width="280">Volumes</th>
      <th width="90">Size</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>07/15/26</td>
      <td><em>Royal Society Interface </em>(2026)</td>
      <td>
        <a href="https://huggingface.co/datasets/cristinaperez9/VISTACT"><strong>VISTACT</strong></a><br>
        <a href="https://royalsocietypublishing.org/rsif/article/23/239/20251186/482117/Histology-guided-3D-virtual-staining-of-microCT"><strong>[Paper]</strong></a>
      </td>
      <td>VIrtual histological STAining of micro-Computed Tomography (VISTACT)</td>
      <td>Synchtron-based phase-contrast microCT and serial H&E and EvG-stained histological sections</td>
      <td> Human lung microCT scans: 1.63 μm/voxel ; Mouse lung microCT scan: 0.88 μm/voxel</td>
      <td>Human lung tissue from patients with pulmonary hypertension and mice heart-lung tissue</td>
      <td>10 from human tissue (4 patients), and 1 from mice tissue</td>
      <td>869GB</td>
    </tr>
    <tr>
      <td>07/15/26</td>
      <td><em>Nature Communications </em>(2025)</td>
      <td>
        <a href="https://www.scidb.cn/en/detail?dataSetId=a41dec8943814999a6149b7c2c7c82fc"><strong>Holotomography</strong></a><br>
        <a href="https://www.nature.com/articles/s41467-025-59820-0"><strong>[Paper]</strong></a>
      </td>
      <td>Revealing 3D microanatomical structures of unlabeled thick cancer tissues using holotomography and virtual H&E staining</td>
      <td>Holotomography and H&E-virtually-stained images</td>
      <td>Lateral resolution: 156 nm; Axial resolution: 1.07 μm</td>
      <td>Human colon cancer samples</td>
      <td>N/A</td>
      <td>24.74GB</td>
    </tr>
    <tr>
      <td>07/15/26</td>
      <td><em>Cancer Research</em>(March 2023)</td>
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
      <td>07/15/26</td>
      <td><em>MICCAI challenge</em>(2023)</td>
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
      <td>07/15/26</td>
      <td><em>Optica</em>(December 2022)</td>
      <td>
        <a href="https://drive.google.com/file/d/1mjYYLMLYX5H5GK6XmmXt_3lPo_dmFuJE/view?pli=1"><strong>Data</strong></a><br>
        <a href="https://opg.optica.org/optica/fulltext.cfm?uri=optica-10-12-1605"><strong>[Paper]</strong></a>
      </td>
      <td>Label- and slide-free tissue histology using 3D epi-mode quantitative phase imaging and virtual hematoxylin and eosin staining</td>
      <td>3D epi-mode quantitative phase imaging</td>
      <td>Lateral resolution of 0.6µm and cross-sectional/axial resolution of 3.5 µm</td>
      <td>Mouse liver, rat gliosarcoma, and human gliomas</td>
      <td>Mouse liver: 8,  rat gliosarcoma: 14, human gliomas: 5</td> 
      <td>26 GB</td>
    </tr>
    <tr>
      <td>07/15/26</td>
      <td><em>Cell</em>(2022)</td>
      <td>
        <a href="https://github.com/labsyspharm/CRC_atlas_2022"><strong>3DCRC</strong></a><br>
        <a href="https://www.cell.com/cell/fulltext/S0092-8674(22)01571-9"><strong>[Paper]</strong></a>
      </td>
      <td>Multiplexed 3D atlas of state transitions and immune interaction in colorectal cancer</td>
      <td>H&E and t‑CyCIF serial histological sections</td>
      <td>Tissue sections with 5μm thickness and variable spacing. Images scanned at 20x</td> 
      <td>Colorectal cancer sample</td>
      <td>1 (47 serial histological sections)</td>
      <td>2.1 TB</td>
    </tr>
    <tr>
      <td>07/15/26</td>
      <td><em>PNAS</em>(2022)</td>
      <td>
        <a href="https://zenodo.org/records/5658994#.YZKJWXso_mF"><strong>3d virtual histology of the human hippocampus</strong></a><br>
        <a href="https://www.pnas.org/doi/epdf/10.1073/pnas.2113835118"><strong>[Paper]</strong></a>
      </td>
      <td>Three-dimensional virtual histology of the human hippocampus based on phase-contrast computed-tomography</td>
      <td>Phase-contrast microCT</td>
      <td>160 nm/px and 50 nm/px</td>
      <td>Human hippocampus tissue</td>
      <td>N/A</td>
      <td>64.8 GB</td>
    </tr>
    <tr>
      <td>07/15/26</td>
      <td><em>eLife</em>(2021)</td>
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
    </tr>
    <tr>
      <td>07/15/26</td>
      <td><em>eLife</em>(2020)</td>
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

<div>
<table width="1800">
  <thead>
    <tr>
      <th width="115">Added</th>
      <th width="160">Journal / Date</th>
      <th width="170">Dataset</th>
      <th width="400">Title</th>
      <th width="180">Modality</th>
      <th width="160">Resolution</th>
      <th width="220">Organ</th>
      <th width="100">Volumes</th>
      <th width="220">Z-levels</th>
      <th width="130">Num. spots/cells</th>
      <th width="60">Size</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>07/15/26</td>
      <td><em>Nature Methods</em> (November 2025)</td>
      <td>
        <a href="https://zenodo.org/records/16783355"><strong>Deep-STARmap</strong></a><br>
        <a href="https://www.nature.com/articles/s41592-025-02867-0"><strong>[Paper]</strong></a>
      </td>
      <td>Scalable spatial single-cell transcriptomics and translatomics in 3D thick tissue blocks</td>
      <td>3D Spatial Transcriptomics (Deep-STARmap) and proteomics (Deep-RIBOmap)</td>
      <td>Single-cell 3D ST/SP data</td> 
      <td>Mouse brain and human cutaneous squamous cell carcinoma (cSCC) tissue</td>
      <td>2</td>
      <td>cSCC: 60µm depth, mouse brain: 150µm depth </td>
      <td>cSCC: N/A cells,254 genes; Mouse brain: 198,675 cells, 1,017 genes</td>
      <td>2.1GB</td>
    </tr>
    <tr>
      <td>07/15/26</td>
      <td><em>Nature Methods</em> (September 2025)</td>
      <td>
        <a href="https://zenodo.org/records/15230302"><strong>3Dniches</strong></a><br>
        <a href="https://www.nature.com/articles/s41592-025-02824-x"><strong>[Paper]</strong></a>
      </td>
      <td>Highly multiplexed 3D profiling of cell states and immune niches in human tumors</td>
      <td>3D CyCIF</td>
      <td>140 nm × 140 nm × 280 nm voxels (200–500 voxels per cell) - 20–54-plex</td> 
      <td>Melanoma specimens: (1) preinvasive cutaneous melanoma, (2) invasive VGP primary melanoma, (3) Metastatic melanoma to the skin</td>
      <td>3</td>
      <td>5–50-µm-thick sections</td> 
      <td>N/A</td>
      <td>3.17TB</td>
    </tr>
    <tr>
      <td>07/15/26</td>
      <td><em>Nature Methods</em> (December 2025)</td>
      <td>
        <a href="https://figshare.com/articles/dataset/SpatialZ_Bridging_the_Dimensional_Gap_from_Planar_Spatial_Transcriptomics_to_3D_Cell_Atlases-processed_datasets/30418285"><strong>SpatialZ</strong></a><br>
        <a href="https://www.nature.com/articles/s41592-025-02969-9"><strong>[Paper]</strong></a>
      </td>
      <td>Bridging the dimensional gap from planar spatial transcriptomics to 3D cell atlases</td>
      <td>3D Spatial Transcriptomics with StarMAP</td>
      <td>Single-cell 3D ST data</td> 
      <td>Mouse visual cortex</td>
      <td>1</td>
      <td>89</td>
      <td>32,845 cells</td>
      <td>30.5MB</td>
    </tr>
    <tr>
      <td>07/15/26</td>
      <td><em>Nature Metabolism</em> (March 2025)</td>
      <td>
        <a href="https://zenodo.org/records/14212427"><strong>MetaVision3D</strong></a><br>
        <a href="https://www.nature.com/articles/s42255-025-01242-9"><strong>[Paper]</strong></a>
      </td>
      <td>AI-driven framework to map the brain metabolome in three dimensions</td>
      <td>3D metabolomics (MALDI)</td>
      <td>50 µm</td> 
      <td>Brain mice samples: two wild-type, 5xFAD, and GAA </td>
      <td>4</td>
      <td>79 serial brain sections (10-µm-thick sections). Sections are 50 µm apart (z axis), corresponding to the MALDI imaging spatial resolution of 50 µm (x and y axes).  </td>
      <td>N/A</td>
      <td>3.3GB</td>
    </tr>
    <tr>
      <td>07/15/26</td>
      <td><em>Nature Cancer</em> (January 2022)</td>
      <td>
        <a href="https://zenodo.org/records/4752030"><strong>3D IMC</strong></a><br>
        <a href="https://www.nature.com/articles/s43018-021-00301-w"><strong>[Paper]</strong></a>
      </td>
      <td>Three-dimensional imaging mass cytometry for highly multiplexed molecular and cellular mapping of tissues and the tumor microenvironment</td>
      <td>3D proteomics (IMC)</td>
      <td>Single-cell resolution (40 markers)</td> 
      <td>HER2+ ductal breast carcinoma sample</td>
      <td>4 (Size of the main sample: 652×488×304µm3)</td>
      <td>152 consecutive slices (2-µm-thick sections)</td>
      <td>N/A</td>
      <td>6.6GB</td>
    </tr>
  </tbody>
</table>
</div>





## Volumetric morphological and genomic data

<div>
<table width="1800">
  <thead>
    <tr>
      <th width="115">Added</th>
      <th width="160">Journal / Date</th>
      <th width="170">Dataset</th>
      <th width="400">Title</th>
      <th width="180">Modality</th>
      <th width="150">Resolution</th>
      <th width="140">Organ</th>
      <th width="90">Volumes</th>
      <th width="350">Serial sections</th>
      <th width="100">Num. spots/cells</th>
      <th width="60">Size</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>07/15/26</td>
      <td><em>Nature</em> (October 2024)</td>
      <td>
        <a href="https://humantumoratlas.org/explore?selectedFilters=%5B%7B%22group%22%3A%22AtlasName%22%2C%22value%22%3A%22HTAN+WUSTL%22%7D%5D&tab=file"><strong>2D3DTumorEvolution</strong></a><br>
        <a href="https://www.nature.com/articles/s41586-024-08087-4"><strong>[Paper]</strong></a>
      </td>
      <td>Tumour evolution and microenvironment interactions in 2D and 3D space</td>
      <td>Serial H&E sections and Visium ST</td>
      <td>20x,55μm-diameter ST spots</td>
      <td>BRCA,CHOL,CRC,PDAC,RCC,UCEC</td>
      <td>78 patients (combined 2D and 3D) - <a href="metadata/2D3D_tumor_evolution_Nature2024.md">Detailed description</a></td> 
      <td>131</td>
      <td>433,000 spots</td> 
      <td>N/A</td>
    </tr>
    <tr>
      <td>07/15/26</td>
      <td><em>Cell</em> (July 2024)</td>
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
      <td>07/15/26</td>
      <td><em>Nature Communications</em> (February 2022)</td>
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
    <tr>
      <td>07/15/26</td>
      <td><em>Nature Neuroscience</em> (March 2021)</td>
      <td>
        <a href="http://spatial.libd.org/spatialLIBD/"><strong>Human prefrontal cortex</strong></a><br>
        <a href="https://www.nature.com/articles/s41593-020-00787-0"><strong>[Paper]</strong></a>
      </td>
      <td>Transcriptome-scale spatial gene expression in the human dorsolateral prefrontal cortex</td>
      <td>Serial H&E sections and Visium ST</td>
      <td>Visium ST technology (55μm-diameter spots)</td>
      <td>Human dorsolateral prefrontal cortex</td>
      <td>3 patient</td>
      <td>12 (4 sections for each patient; The distance between sections is 10μm - 300μm - 10μm)</td>
      <td>47,681 spots</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td>07/15/26</td>
      <td><em>Nature Communications</em> (February 2021)</td>
      <td>
        <a href="https://zenodo.org/records/4751624"><strong>HER2+</strong></a><br>
        <a href="https://www.nature.com/articles/s41467-021-26271-2"><strong>[Paper]</strong></a>
      </td>
      <td>Spatial deconvolution of HER2-positive breast cancer delineates tumor-associated cell type interactions</td>
      <td>Serial H&E sections and Spatial Transcriptomics</td>
      <td>20x, Spatial Transcriptomics technology (~100μm-diameter spots)</td>
      <td>HER2+ breast cancer</td>
      <td>8 (8 patients)</td>
      <td>36 (A~D:6, E~H:3). Spacing between sections: 36μm. Section thickness: 16μm</td>
      <td>13,299 spots</td>
      <td>629.6 MB</td>
    </tr>
    <tr>
      <td>07/15/26</td>
      <td><em>Cell</em> (December 2019)</td>
      <td>
        <a href="https://data.mendeley.com/datasets/dgnysc3zn5/1"><strong>Human Heart</strong></a><br>
        <a href="https://www.cell.com/cell/fulltext/S0092-8674(19)31282-6?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS0092867419312826%3Fshowall%3Dtrue"><strong>[Paper]</strong></a>
      </td>
      <td>A Spatiotemporal Organ-Wide Gene Expression and Cell Atlas of the Developing Human Heart</td>
      <td>Serial H&E sections and Spatial Transcriptomics</td>
      <td>20x, Spatial Transcriptomics technology (~100μm-diameter spots)</td>
      <td>Developing Human Heart</td>
      <td>Four developmental heart tissues</td>
      <td>19 (4,9,6 sections for 4.5–5, 6.5, and 9 PCW heart tissues). Spacing between sections: 36μm. Section thickness: 5μm</td>
      <td> 3,115 spots</td>
      <td>211 MB</td>
    </tr>
  </tbody>
</table>
</div>

## Contributions

If you would like to add a 3D dataset to the current compilation, please create a pull request with details for each field in the tables above, or contact calmagro@mit.edu .

##

<img src=docs/images/joint_logo.png>






 
