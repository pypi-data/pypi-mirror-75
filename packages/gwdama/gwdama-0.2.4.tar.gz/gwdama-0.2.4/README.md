# gwdama

GW Data Manager

## 0. Clone this repo
In your working directory, clone this repository:
```bash
$ git clone https://gitlab.com/gwprojects/gwdama.git
```
This will create a `gwdma` repository. Change directory to this one and check the available branches:
```bash
$ cd gwdama
$ git branch -a
```
By default, only the master directory is synchronised. If you want to try different branches, like `fradev`:
```bash
$ git checkout fradev
```
Now you are good to go!

## 1. Getting started
### Environment setup

The following installation procedure works correctly on Virgo farm machines. Remember to put the resulting `env` directory
 into a `.gitignore` file in order to avoid pushing it!

1. Create a Python3 environment called `env`, or whatever (in this case, remember to substitute it to `env` in the following commands). This should be done `without-pip`, which is installed in the next step.
    ```bash
    $ python3 -m venv --without-pip env
    ```
2. Activate the environment, which is going to be empty (really!):
    ```bash
    $ source env/bin/activate
    ```
3. Get pip, setuptools and wheel from the web:
    ```bash
    $ curl https://bootstrap.pypa.io/get-pip.py | python
    ```
4. Deactivate and reactivate the environment and check if the previous packages are installed and up-to dated. Check also the versions atc.:
    ```bash
    $ deactivate
    $ source env/bin/activate
    $ python --version
    $ pip list
    ```
5. Install the required modules. The procedure varies depending on whether a `requirements.txt` file is available 
(provided somebody has created one with `pip freeze > requirements.txt`) or not:
    1. install the packages from the requirements:
        ```bash 
        $ pip install -r requirements.txt
        ```
         
   5. install everything manually:
        ```bash
        $ pip install numpy, scipy, matplotlib, pandas, jupyter, scikit-learn, gwpy   
        ```
        Also, it will be necessary to install ` python-ldas-tools-framecpp` to use the method
        `read` of GWpy TimeSeries:
        ```bash
        $ pip install lalsuite
        ```
6. Check that the previous steps have been completed successfully: entering the following command shouldn't return any arror, warning etc.
    ```bash
    $ python -c "import numpy, matplotlib, pandas, sklearn, scipy"
    ```
**Notice:** for code developing and benchmark tests, it could also be useful to install the `line_profiler` and
`memory_profiler` packages. These are not included in the `requirements.txt` file but you can install them easily,
within the environment, typing:
```bash
$ pip install line_profiler memory_profiler
```
Then, you can exploit the IPython megic commands:
- `%prun`: Run code with the profiler
- `%lprun`: Run code with the line-by-line profiler
- `%memit`: Measure the memory use of a single statement
- `%mprun`: Run code with the line-by-line memory profiler
   
### Install the package (locally)
We can install the package locally (for use on our system), and import it anywhere else.
Passing the parameter `-e`, we can install the package with a symlink, so that changes
to the source files will be immediately available to other users of the package on our system.
From the main directory containing the package:
```bash
$ pip install -e .
```
Done! You are all set up now, and go testing with some jupyter notebook.

## 2. Play with data
There are some test and development notebooks:
- [Example_1](notebooks/Example1_VirgoFarm.ipynb): with basic example about how to fetch data from inside a Virgo farm machine;
- [Example2](notebooks/Example2_PCuniverse2.ipynb): how to use it from PC Universe 2, with cernCV data;
- Under development...