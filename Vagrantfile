Vagrant.configure("2") do |config|
    config.vm.box = "hashicorp/bionic64"

    config.vm.provision "shell", :privileged => false, inline: <<-SHELL
        set -e
        sudo apt-get update
        sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl

        if [ ! -d "~/vagrant/.pyenv" ]
        then
            git clone https://github.com/pyenv/pyenv.git ~/vagrant/.pyenv

            echo 'export PYENV_ROOT="~/vagrant/.pyenv"' >> ~/vagrant/.profile
            echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/vagrant/.profile
            echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/vagrant/.profile

            exec "$SHELL"
        fi

        pyenv install 3.8.5
        pyenv global 3.8.5

        curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
        SHELL

    config.trigger.after :up do |trigger|
        trigger.name = "Launching App"
        trigger.info = "Running the TODO app setup script"
        trigger.run_remote = {privileged: false, inline: <<-SHELL
            cd /vagrant
            poetry install
            poetry run flask run --host=0.0.0.0
        SHELL
        }
    end

    config.vm.network "forwarded_port", guest: 5000, host: 5001
end