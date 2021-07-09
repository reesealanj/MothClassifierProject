#!/bin/sh
#SBATCH --time 03:30:00
#SBATCH -o training%j.out
#SBATCH -e training%j.err
#SBATCH -p defq -N 2
#SBATCH -n 32
#SBATCH --mail-user=bengia99@gwu.edu
#SBATCH --mail-type=ALL

module load anaconda
pip install --no-index --upgrade pip
pip install virtualenv
virtualenv --no-download env/
source env/bin/activate
pip install -r requirements.txt 

python train_model.py