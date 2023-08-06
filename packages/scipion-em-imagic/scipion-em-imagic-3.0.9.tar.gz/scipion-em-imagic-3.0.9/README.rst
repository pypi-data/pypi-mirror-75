=============
IMAGIC plugin
=============

This plugin includes two protocols to provide wrappers around Multivariate Statistical Analysis (MSA) module of `IMAGIC <https://www.imagescience.de/imagic.html>`_ software suite. IMAGIC is a licensed software, not distributed with Scipion and has to be installed by user.

Installation
------------

You will need to use `3.0 <https://github.com/I2PC/scipion/releases/tag/V3.0.0>`_ version of Scipion to be able to run these protocols. To install the plugin, you have two options:

a) Stable version

.. code-block::

    scipion installp -p scipion-em-imagic

b) Developer's version

    * download repository

    .. code-block::

        git clone https://github.com/scipion-em/scipion-em-imagic.git

    * install

    .. code-block::

        scipion installp -p path_to_scipion-em-imagic --devel

Also, you need a working IMAGIC installation. Default installation path assumed is ``software/em/imagic-190830``, if you want to change it, set *IMAGIC_HOME* in ``scipion.conf`` file to the folder where the IMAGIC is installed (it is the same as *IMAGIC_ROOT* variable in your shell environment). If you want to use MPI-based parallel job execution, make sure you have `openmpi` directory inside IMAGIC installation folder.
To check the installation, simply run the following Scipion test:

``scipion tests tests.em.workflows.test_workflow_imagicMSA.TestImagicWorkflow``

Supported versions
------------------

* 190830

Since with every version of IMAGIC software user interaction with IMAGIC programs is changed, we came up with a way to provide multiple version support. In `imagic/scripts` directory you have a folder for each corresponding version, that contains batch scripts similar to those used by IMAGIC. This way one can create a similar script specific to a certain version. At the moment version 190830 (Aug 2019) is supported. If you experience any problems or need help with adapting scripts for your IMAGIC version, do not hesitate to `create an issue on Github <https://github.com/scipion-em/scipion-em-imagic/issues/new>`_. Besides editing scripts directory you would need to add version number to `_supportedVersions` list in file ``imagic/__init__.py`` and edit IMAGIC_HOME variable in ``scipion.conf``.

Protocols
---------

    * imagic - msa
    * imagic - msa-classify

References
----------

1. M van Heel and W Keegstra (1981). IMAGIC: A fast, flexible and friendly image analysis software system. Ultramicroscopy 7: 113-130.
2. M van Heel, G Harauz, EV Orlova, R Schmidt and M Schatz (1996). A new generation of the IMAGIC image processing system. J. Struct. Biol. 116: 17-24.
3. M van Heel, R Portugal, A Rohou, C Linnemayr, C Bebeacua, R Schmidt, T Grant and M Schatz (2012). Four-Dimensional Cryo Electron Microscopy at Quasi Atomic Resolution: "IMAGIC 4D”. International Tables for Crystallography, vol. F, ch. 19.9: 624-628.
4. M van Heel (1984). Multivariate statistical classification of noisy images (randomly oriented biological macromolecules). Ultramicroscopy 13(1-2): 165-183.
5. Lisa Borland and Marin van Heel (1990). Classification of image data in conjugate representation spaces. Journal of the Optical Society of America A 7(4): 601-610.
