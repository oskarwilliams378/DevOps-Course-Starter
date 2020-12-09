docker login --username=_ --password="$(heroku auth:token)" registry.heroku.com
docker pull oskwil/todo-app
docker tag oskwil/todo-app registry.heroku.com/oskwil-todo-app/web
docker push registry.heroku.com/oskwil-todo-app/web
heroku oskwil-todo-app:release web