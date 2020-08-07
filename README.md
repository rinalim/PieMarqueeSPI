# PieMarqueeSPI
Marquee plugin for SPI screen
## Screen Setup
```
cd ~
git clone https://github.com/rinalim/PieMarqueeSPI
cd PieMarqueeSPI/waveshare
cp /boot/config.txt ./config.org
cd LCD-show
sudo chmod 755 LCD*
./LCD35(B)-show
--After rebooting--
cd /home/pi/PieMarqueeSPI/waveshare
sudo sh lcd-restore.sh
```
## Install
```
cd /home/pi/PieMarqueeSPI
sudo sh ./install.sh
```
