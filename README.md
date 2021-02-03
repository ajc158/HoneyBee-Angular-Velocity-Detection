# HoneyBee-Angular-Velocity-Detection

## RUNNING THE MODEL:

Below are instructions for obtaining and running the Corridor Centring Model. There are three experiments included, and there is some set up work to configure each. The model can be run on Linux or OSX.

First, download the zip file from here, and unzip it.

Second install Qt 5 and download the simulated environment (beeworld) from the GitHub repository. You’ll also need scipy.

Third, run QtCreator, load the .pro file and use the default build options, then build the beeworld. Copy the beeworld2 binary (if on Mac you need the one ”inside” the .app package (right click and select ‘show package contents’ to get it). Then replace the beeworld2 file from the zip you downloaded (it is compiled for Mac, but almost certainly won’t work on your computer).

Fourth, install SpineML_2_BRAHMS and BRAHMS as described [here](http://spineml.github.io/). Note the installation locations (on Mac the installation locations are ”inside” the .app package,right click and select ‘show package contents’)

Fifth. The zip contains three directories beginning ‘Paper’ – these are the experiments. The `cc_XXXX_model` directories are the SpineML models. You now need to configure each experiment for your system – replace the `SML_2_B_dir`, `SML_dir` and `Model_dir` variables in `run_FigX.py` and `analyse_FigX.py` with the SpineML_2_BRAHMS, SystemML and model directories on your system, respectively.

Sixth, run

```bash
python run_FigX.py && python analyse_FigX.py
```

You will get a labelled graph of the model output when the batch run is complete.
