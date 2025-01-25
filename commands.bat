# Generate Heroku auth token
heroku auth:token

# Set Git remote with auth token
git remote remove heroku
git remote add heroku https://git.heroku.com/fastapi-elias.git

# Store Heroku credentials
git config credential.helper store
heroku git:credentials

# Create required Heroku files
echo web: uvicorn app.main:app --host=0.0.0.0 --port=$PORT > Procfile
echo python-3.9.18 > runtime.txt

# Commit and push
git add .
git commit -m "chore: add Heroku configuration files"
git push heroku main