Introduction
------------

.. image:: /../../design/logo.png
    :width: 250px

The goal of *starfish* is to **prototype** a reference pipeline for the analysis of image-based
transcriptomics data that works for each image-based transcriptomic assay. This is a **work in
progress** and will be developed in the open.

We are currently in **pre-alpha**, finishing proof of concept pipelines for each of the spaceTx
contributors that leverage starfish's shared object model. At this time starfish is mature enough to
support computational developers interested in adapting other assays to starfish's object model.
The below table lists the current state of support for each image-based transcriptomics assay.

=============  ==========  ===================  ==================
 assay         loads data  single-fov pipeline  multi-fov pipeline
-------------  ----------  -------------------  ------------------
 MERFISH       [x]         [x]                  in process
 ISS           [x]         [x]                  in process
 osmFISH       [x]         in process           [ ]
 allen_smFISH  [x]         in review            [ ]
 DARTFISH      [x]         [x]                  [ ]
 BaristaSeq    [ ]         [ ]                  [ ]
 StarMAP       [ ]         [ ]                  [ ]
 dypFISH       [x]         no pipeline          [ ]
 ex-FISH       [x]         no pipeline          [ ]
 FISSEQ        no data     no pipeline          [ ]
 seq-FISH      no data     no pipeline          [ ]
=============  ==========  ===================  ==================

Concept
-------

See this document_ for details. The diagram below describes the core pipeline components and
associated file manifests that this package plans to standardize and implement.

.. _document: https://docs.google.com/document/d/1IHIngoMKr-Tnft2xOI3Q-5rL3GSX2E3PnJrpsOX5ZWs/edit?usp=sharing

.. image:: /../../design/pipeline-diagram.png
    :alt: pipeline diagram
