# IsochroneEquationGalaxyGenerator
This is a basic code demo for the Princeton 2026 ISEC Conference for the paper "Computational Realization of Galactic Morphology: An Interactive 3D Implementation of the Ringermacher-Mead Isochrone Formula". This is a basic demonstration of the galaxy model that was originally made in Desmos and based off of the Isochrone equation
Original Desmos Link is https://www.desmos.com/calculator/kj8c1iqydd
The link to the paper will be added once it is published


These scripts translate the original parametric visual proofs into native, computationally reproducible environments, allowing for the interactive modeling of spiral galaxies (such as the Milky Way and NGC 1365).

The Three Morphological Models
To ensure comprehensive reproducibility and to isolate specific geometric behaviors, the computational translation is divided into three distinct evolutionary scripts.

1. The 2D Projection Matrix (Desmos Replica)
File: 2d_curvature_script.py

Rendering Engine: 2D Cartesian

Core Distinction: This script is a direct, 1-to-1 mathematical replication of the original visual proof. Because standard web graphing calculators lack a true Z-axis, this model utilizes a custom projection algorithm to force a flat 2D screen to render a 3D optical illusion. It is used to verify the trigonometric matrix mathematics independent of native 3D Python libraries.

2. The Pivot to Native Space
File: 3d_curvature_script.py

Rendering Engine: Native 3D

Core Distinction: This model abandons the optical illusion entirely. It maps the Ringermacher-Mead parametric equations directly into a native 3D Cartesian space. By rendering the galactic scaffold as clean, continuous solid lines, researchers can observe how manipulating parameters like winding and bulge fundamentally alters the underlying isochrone geometry in true 3D space, without the interference of stochastic noise.

3. Volumetric Stochastic Density
File: 3d_curvature_with_stars.py

Rendering Engine: Native 3D Scatter

Core Distinction: The most advanced model. It replaces the solid-line structural scaffold with thousands of individual plotted points to simulate stellar density. It implements a dampened noise equation (multiplying a normal distribution by a uniform distribution) to cluster stars tightly along the isochrone arms, simulating realistic galactic morphology.

The Z-Axis Thickness Complication
The transition from a 2D optical projection (Script 1) to a true 3D spatial environment (Script 3) introduces significant physical complexities, primarily regarding the simulation of galactic thickness.

In the initial graphing environment, depth was an illusion mapped strictly onto a flat plane. In a true volumetric engine, applying standard unconstrained random distribution to the Z-axis yields unbounded spherical clouds rather than a structured, flattened galactic disk. 

Current Mitigation
Currently, 3d_curvature_with_stars.py mitigates this unbounded scattering by applying aggressive mathematical clipping and exponential tapering to the vertical noise array. This synthetically forces a high-density, bulbous galactic core that flattens radially into a thin outer disk. However, it was not within the scope of this project to determine whether or not the bounds set onto the models were realistic to real galaxies, but there is a variable for adjusting this for further use.

Future Work
This true-3D thickness complication remains a primary vector for future research. Subsequent iterations of this computational framework will seek to improve vertical density modeling by integrating formal astrophysical vertical density profiles (such as isothermal sech-squared disk models) to govern the Z-axis scatter analytically, rather than relying on synthetic mathematical dampening.

Interactive Parameter Control
All three models feature a split-screen graphical user interface. Researchers can manipulate the following variables in real-time to observe dynamic morphological shifts:

Zoom (Scale): Scales the 3D coordinate boundaries.

Winding (N): Controls the tightness of the spiral arms.

Bulge (B): Adjusts the radius of the central galactic bulge.

Rotation (T): Applies Keplerian differential rotation and twist.

Length (C): Determines the outward extension of the spiral arms.

End Width (Ct): Controls the structural tapering at the arm tips.

Strand Width (d): Modifies the radial spread of the stochastic star noise.

Thickness (Z): Adjusts the vertical bounds of the galactic disk.

Recreating Specific Galaxies (CSV Data)

Included in this repository is a CSV file containing the specific parameter values used to model known galaxies (Milky Way, Whirlpool M51a, Pinwheel M101, and NGC 1300). 

Desmos Implementation:
These parameters were natively calibrated for the 2D visual proof. You can import or manually input these values directly into the provided Desmos link to accurately recreate the exact morphological structures of these galaxies.

Python Implementation Compatibility Note:
Please note that these exact CSV parameters will not translate perfectly 1-to-1 into the Python native 3D models (`3d_curvature_script.py` and `3d_curvature_with_stars.py`). Because the Python scripts abandon the projection matrix in favor of true $\mathbb{R}^3$ spatial mapping and introduce mathematically constrained Z-axis thickness, the underlying algorithms have shifted. You will need to manually adjust the sliders in the Python UI to recalibrate and achieve the same visual results as the Desmos environment.

Installation and Usage
Dependencies:

Python 3.x

NumPy

Matplotlib

Execution:
Clone the repository, install the required dependencies, and run any of the three models directly from your terminal:

python 3d_curvature_with_stars.py

Note: Due to the high volume of coordinate recalculations required for the stochastic density model, please drag the UI sliders with deliberate, steady movements to prevent event-loop overlapping in the rendering engine.
