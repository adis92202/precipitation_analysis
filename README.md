# Precipitation analysis using SPI (Standardized Precipitation Index)

## Contents
This repository has following structure:
- data/ - empty folder in which analysed data will appear when running analysis
- documentation/ - additional comments on code
- notebooks/ - folder with development notebooks; to be hidden after final deployment
- results/ - folder containing all of the results of the analysis
- src/ - source code for project, further divided into thematical groups
- .gitignore - paths to be ignored by github
- README.md - this file
- run.py - main script to run analysis (see **Usage** section)
- spi_env.yml - file with environment snapshot (see **Environment** section) - in future to be replaced by conda-lock file


## GitHub
To clone this repo follow these steps:
1. Go into your preferred location
2. Open the command prompt and type `git clone https://github.com/adis92202/precipitation_analysis.git`, then hit enter
3. Close command prompt window if needed

## Jira
SCRUM Board: https://student-team-xbkle2tpwdsd.atlassian.net/jira/software/projects/SPI/boards/1

## Environment
1. Clone this repository to your preferred location as mentioned in the **GitHub** section
2. Go into this location and copy the absolute path
3. Open the Anaconda Prompt and use `cd <copied_absolute_path>` command
4. Use `conda env create -f spi_env.yml` command in the Anaconda Prompt
5. Still in the Anaconda Prompt, activate this environment via `conda activate spi_env`
6. Verify that the new environment was installed correctly using `conda env list` - you should see `spi_env` on the list
7. Now, you can close Anaconda Prompt window

## Usage
To run this project do the steps below:
1. Open terminal in the location of your repository
2. Activate environment by `conda activate spi_env`
3. Type `python run.py` to start all of the fun! If you don't provide an --voivodeship argument, the program will analyze the precipitation data for the Lubusz voivodeship by default. If you want to analyze precipitation data for another voivodeship, provide its name as an argument. Here is an example:

    `python run.py --voivodeship Masovian`

    Here is the list of available voivodeships you can choose from:
    - Silesian
    - LesserPoland
    - Subcarpathian
    - LowerSilesian
    - Opole
    - Podlachian
    - WarmianMasurian
    - Lubusz
    - WestPomeranian
    - Lublin
    - Pomeranian
    - Masovian
    - Łódź
    - KuyavianPomeranian
    - GreaterPoland
    - Świętokrzyskie
4. The data will appear in 'data' folder and other results in 'results' folder

### Authors:
- [Anna Kaniowska](https://github.com/ania15)
- [Adam Piwowarski](https://github.com/adis92202)
- [Ewa Szewczyk](https://github.com/drateffka)