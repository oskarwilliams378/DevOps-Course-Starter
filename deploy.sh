echo "$HEROKU_API_KEY" | docker login --username=_ --password-stdin registry.heroku.com
docker tag oskwil/todo-app registry.heroku.com/oskwil-todo-app/web
docker push registry.heroku.com/oskwil-todo-app/web
heroku container:release web -a oskwil-todo-app