npm run build

rm -rf ../../../var/www/dist
mv dist ../../../var/www
sudo systemctl restart nginx
