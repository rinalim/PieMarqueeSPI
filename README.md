# PieMarqueeSPI
Marquee plugin for SPI screen
## Install
cd ~
git clone https://github.com/rinalim/PieMarqueeSPI
cd PieMarqueeSPI/waveshare
cp /boot/config.txt ./config.org
cd LCD-show
sudo chmod 755 LCD*
./LCD35-show
--After rebooting--
cd /home/pi/PieMarqueeSPI/waveshare
sudo sh lcd-restore.sh
--After rebooting--
cd /home/pi/PieMarqueeSPI
sudo sh ./install.sh