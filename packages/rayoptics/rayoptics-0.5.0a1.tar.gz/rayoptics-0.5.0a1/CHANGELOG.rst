=========
Changelog
=========

Version 0.4.12
==============

Misc bug fixes and improvements: draw mirror substrates consistently, old .roa files should be resaved. Consolidate InteractiveFigure color and lw control in dicts, and retrofit layout usage to match diagrams. 

Version 0.4.11
==============

Add single field monochromatic PSF calc and display. Add dashboards for jupyter notebook usage for refocusing, etc. Revisions to app manager protocols for wider usage, esp. including matplotlib Figures. Use brute force OPD calc instead of equally inclined chords until eic behavior with decentered systems is fixed.

Version 0.4.10
==============

Add add_from_file() method to OpticalModel to enable importing pieces of optical
models to a master model. Include a Jupyter notebook demonstration.

Version 0.4.9
=============

Add single panel refactoring of ray fan, spot diagram and wavefront map plots
that are designed for use in a scripting environment.

Version 0.4.8
=============

Bug fixes and doc improvements

Version 0.4.7
=============

UI improvements. For Qt app, add light and dark mode, add zoom, and pan
capabilities to InteractiveFigures, rework main menu bar. For Diagram, add
object and stop shifts, lens thickness and bending, replace node with system
option. Reorganize doc structure.

Version 0.4.6
=============

Add SpecSheet capability. V2 of y-ybar diagram with more editing capability

Version 0.4.0
=============

Add initial version of Interactive Layout (Live Layout). Work in Progress...

Version 0.3.5
=============

Update aperture import and layout rendering for y-z plane tilts and decenters

Version 0.3.0
=============

Rework packaging using PyScaffold and Versioneer. Deploy documentation to ReadTheDocs

Version 0.2.0
=============

first version of documentation support for rayoptics. continue refactoring

Version 0.1.5
=============

separate qt gui files from mpl and generic ones. add rayoptics script to start qt version

Version 0.1.0
=============

major update that reads CV files, supports Hoya, Ohara and Schott glass catalogs, computes paraxial and real rays, and has Qt UI for lens data table, 2D lens picture and glass map view.
