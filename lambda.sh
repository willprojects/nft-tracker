NAME=nft-data-tracker

mkdir temp/
rsync -av . temp --exclude scratch/ --exclude .git/ --exclude .idea/ --exclude cache/ --exclude venv/ --exclude temp/
cd temp/

pip3 install -r requirements.txt -t ./
chmod -R 755 .
zip -r lambda.zip .
aws lambda update-function-code --function-name $NAME --zip-file fileb://lambda.zip
cd ../
rm -rf temp/