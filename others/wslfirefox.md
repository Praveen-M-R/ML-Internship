# Installing and Solving Issues with Geckodriver and Firefox

## Step 1: Fixing Permissions for Geckodriver and Firefox

If you encounter permission issues with `geckodriver` and `firefox`, try running the following commands:

```sh
sudo chown 1000 -R /usr/bin/geckodriver
sudo chmod 775 -R /usr/bin/geckodriver
sudo chown 1000 -R /usr/bin/firefox
sudo chmod 775 -R /usr/bin/firefox
```

If you see an error like:
```sh
RUN: command not found
```
Make sure you are running the commands in a shell (bash or zsh) and not inside a script that misinterprets them.

---

## Step 2: Removing Snap Version of Firefox

To resolve compatibility issues, uninstall the snap version of Firefox:

```sh
sudo snap remove firefox
```

---

## Step 3: Adding Mozilla PPA Repository

Since Firefox may be installed as a snap package by default, you can install it from the Mozilla PPA instead:

```sh
sudo add-apt-repository ppa:mozillateam/ppa
```

After adding the repository, update your package lists:

```sh
sudo apt update
```

---

## Step 4: Setting Firefox to Install from PPA

To ensure Firefox updates come from the Mozilla PPA, set the repository priority:

```sh
echo 'Package: *
Pin: release o=LP-PPA-mozillateam
Pin-Priority: 1001' | sudo tee /etc/apt/preferences.d/mozilla-firefox
```

Additionally, configure unattended upgrades for Firefox:

```sh
echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' | sudo tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox
```

---

## Step 5: Installing Firefox from PPA

Once the setup is complete, install Firefox:

```sh
sudo apt install firefox
```

If prompted with package downgrades, accept by pressing `Y`.

---

## Step 6: Installing Geckodriver

Download and install `geckodriver` (replace `VERSION` with the latest version):

```sh
GECKO_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d '"' -f 4)
wget https://github.com/mozilla/geckodriver/releases/download/$GECKO_VERSION/geckodriver-$GECKO_VERSION-linux64.tar.gz
tar -xvzf geckodriver-$GECKO_VERSION-linux64.tar.gz
sudo mv geckodriver /usr/bin/
sudo chmod +x /usr/bin/geckodriver
```

Verify the installation:

```sh
geckodriver --version
```

---

## Step 7: Verify Installation

Run the following command to check if Firefox is installed correctly:

```sh
firefox --version
```

Check if `geckodriver` is recognized:

```sh
geckodriver --version
```

If both commands return valid version numbers, the installation is successful!
