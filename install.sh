#!/usr/bin/env bash

CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)

wget -N http://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip
unzip -o chromedriver_linux64.zip
rm chromedriver_linux64.zip
sudo mv -f chromedriver /usr/local/bin/chromedriver
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod 0755 /usr/local/bin/chromedriver

python setup.py install

if [[ $? == 0 ]]; then
    echo
    echo "$(tput setaf 2)Script successfully installed. Now you can use it from command-line as $(tput setaf 5)remove_actions_vm$(tput setaf 2)"
fi

python setup.py clean --all
