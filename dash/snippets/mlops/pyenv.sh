# update local packages
sudo apt-get update -y
# install dependencies
sudo apt-get install -y python3-pip python3-dev python3-venv
# create the python enviroment
python3 -m venv pyenv
# activate a virtual environment¶
source ./pyenv/bin/activate
#install packages
pip install -r ./src/score_interactive_endpoint/requirements.txt
#run application
chmod +x ./run.py
python ./run.py
