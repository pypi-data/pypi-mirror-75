MNE Widgets for Orange 3 is a python package, that provides methods from MNE for Python for Orange 3 in a form of widgets, 
to allow for electrophysiological data processing.

### Installation
1. The installation process is quite straightforward, first we need to install the Orange 3 tool:
    > *Note: If you have Orange 3 already installed, you can skip this step and continue to step 2.*
    ```bash
    virtualenv orange          # Create a virtual environment
    ./orange/Scripts/activate  # Activate the environment (source ./orange/Scripts/activate for linux)
    pip install Orange3 PyQt5  # Install Orange 3 and PyQt library
    ```
2. Then run Orange: `python -m Orange.canvas`
3. In Orange navigate to Options -> Add-ons
4. Click on `Add more...` and enter the package name: `Orange3-MNE`
5. Confirm the settings and Orange will install the library
6. Restart Orange and the electrophysiological data processing library will be available