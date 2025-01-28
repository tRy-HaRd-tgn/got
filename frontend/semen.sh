npm run build

rm -rf ../../dist
mv dist ../../dist
sudo systemctl restart nginx
