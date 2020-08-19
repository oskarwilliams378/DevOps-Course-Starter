Vagrant.configure("2") do |config|
    config.vm.box = "hashicorp/bionic64"

    config.vm.provision "shell", inline: <<-SHELL
        set -e
        sudo apt-get update
        sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl

        if [ ! -d "/home/vagrant/.pyenv" ]
        then
            git clone https://github.com/pyenv/pyenv.git /home/vagrant/.pyenv

            echo 'export PYENV_ROOT="/home/vagrant/.pyenv"' >> /home/vagrant/.profile
            echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /home/vagrant/.profile
            echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> /home/vagrant/.profile

            exec "$SHELL"
        fi
        SHELL

    config.vm.provision "shell", :privileged => false, inline: <<-SHELL
        pyenv install 3.8.5
        pyenv global 3.8.5

        curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
        source $HOME/.poetry/env
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