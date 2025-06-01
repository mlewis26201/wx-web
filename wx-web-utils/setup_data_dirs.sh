# Copy your static and templates directories into /data for bind mounting
mkdir -p data/static
mkdir -p data/templates
cp -r static/* data/static/
cp -r templates/* data/templates/
# Move your history.csv if it exists
if [ -f static/history.csv ]; then mv static/history.csv data/history.csv; fi
