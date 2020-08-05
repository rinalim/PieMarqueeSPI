sudo apt-get install libjpeg8 -y
sudo apt-get install imagemagick -y
sudo apt-get install fbi -y
sudo apt-get install mplayer -y

rm -rf /opt/retropie/configs/all/PieMarqueeSPI/
mkdir /opt/retropie/configs/all/PieMarqueeSPI/
cp -f -r ./PieMarqueeSPI /opt/retropie/configs/all/

sudo sed -i '/PieMarqueeSPI.py/d' /opt/retropie/configs/all/autostart.sh
sudo sed -i '1i\\/usr/bin/python /opt/retropie/configs/all/PieMarqueeSPI/PieMarqueeSPI.py &' /opt/retropie/configs/all/autostart.sh

echo
echo "Setup Completed. Reboot after 3 Seconds."
sleep 3
reboot
