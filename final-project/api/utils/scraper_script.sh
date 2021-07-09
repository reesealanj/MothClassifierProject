#!/bin/sh
#SBATCH --time 30:00
#SBATCH -o scraper%j.out
#SBATCH -e scraper%j.err
#SBATCH -p defq -N 2
#SBATCH -n 16
#SBATCH --mail-user=abidahmed@gwu.edu
#SBATCH --mail-type=ALL

module load anaconda
pip install --no-index --upgrade pip
pip install virtualenv
virtualenv --no-download env/
source env/bin/activate
pip install -r requirements.txt 

python scraper.py -u [USERNAME] -p [PASSWORD] --album I_JPA --range 1 10000 --cpus 16