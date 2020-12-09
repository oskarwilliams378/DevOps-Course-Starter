(
  echo "$HEROKU_EMAIL"
  echo "$HEROKU_PASSWORD"
) | heroku login
docker pull oskwil/todo-app
docker tag oskwil/todo-app registry.heroku.com/oskwil-todo-app/web
docker push registry.heroku.com/oskwil-todo-app/web
heroku oskwil-todo-app:release web