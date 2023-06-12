Установка debian:
1) устаноить vim

2) Настройка sid:
    sudo mv /etc/apt/sources.list /etc/apt/sources.list.old
    sudo mv /etc/apt/sources.list.d /etc/apt/sources.list.d.old
    sudo mkdir /etc/apt/sources.list.d
    vim /etc/apt/sources.list
        deb http://deb.debian.org/debian sid main contrib non-free
        deb-src http://deb.debian.org/debian sid main contrib non-free
    apt update
    apt dist-upgrade

3) установить sudo, mdadm, screen, git, telnet, lnav, smartmontools, rsync, wget

4) настроить sudo
    adduser <username> sudo
    /etc/sudoers
        %sudo   ALL=NOPASSWD: ALL #ALL=(ALL:ALL) ALL

5) настроить vim
    ~/.vimrc и в /root/.vimrc
        set mouse-=a
        syntax on

6) настроить ssh-server
    /etc/ssh/sshd_config:
        PermitRootLogin yes
        PubkeyAuthentication yes
        TCPKeepAlive yes
        ClientAliveInterval 10
        ClientAliveCountMax 2
        X11DisplayOffset 10
        GatewayPorts yes
        PubkeyAcceptedAlgorithms +ssh-rsa

    на клиенте:
        /etc/ssh/ssh_config:
            ServerAliveInterval 10

7) Настроить bash подсветку в root и aliases:
    sudo cp /home/stelhs/.profile /root/
    sudo cp /home/stelhs/.bashrc /root/

    vim ~/.bashrc
        # aliases for git
        alias gst='git status'
        alias gl='git log'
        alias ga='git add'
        alias gc='git commit -m'
        alias gp='git pull --rebase && git push'
        alias gull='git pull --rebase'
        alias gush='git push'
        alias gb='git branch'
        alias gco='git checkout'
        alias gd='git diff'


8) настроить /storage
    mkdir /storage
    /etc/fstab
        UID=db51fb17-f806-453b-aea0-b45db07b4cda /storage       ext4     errors=remount-ro,nofail 0       1

8) настроить /backup
    mkdir /backup
    /etc/fstab
        UUID=fde5b054-0665-4e68-945e-f180c3b95449 /backup       ext4     errors=remount-ro,nofail 0       1

9) Настроить мониторинг raid1, mount точек, свободное место
    cd /root
    git clone https://github.com/stelhs/host_monitor.git
    cd host_monitor
    git clone https://github.com/stelhs/sr90lib.git
    cp -r def_configs configs
    vim configs/telegram.conf
        set correct token and chat id

    cp root/etc/systemd/system/host_monitor.service /etc/systemd/system
    systemctl daemon-reload
    systemctl enable host_monitor.service

10) установка и настройка virtualbox (7.0.6_Debianr155176)
    apt install virtualbox, virtualbox-guest-additions-iso, virtualbox-guest-utils, virtualbox-ext-pack, apache2, php-soap, php-xml
    a2dismod --force autoindex
    systemctl restart apache2
    cd /var/www/html/
    git clone https://git.code.sf.net/p/phpvirtualbox-7/code phpvirtualbox-7-code
    mv phpvirtualbox-7-code/phpvirtualbox7.0 ./phpvirtualbox
    cd phpvirtualbox/
    mv config.php-example config.php

    useradd -d /home/vbox -m -g vboxusers -s /bin/bash vbox
    passwd vbox
        12345678

    vim /var/www/html/phpvirtualbox/config.php
        var $username = 'vbox';
        var $password = '12345678';

    cp root/etc/systemd/system/vboxweb.service /etc/systemd/system
    systemctl enable vboxweb.service

    service apache2 restart

    systemctl start vboxweb.service

    vboxmanage createvm --name server_debian12 --ostype Debian_64 --register --basefolder /storage/virtualbox_vms/

    xtightvncviewer 192.168.0.15:3389

    vim /var/www/html/phpvirtualbox/endpoints/jqueryFileTree.php +261
        comment string:
            //if(count($allowed) && !$allowed['.'.$ext]) continue;

11) Проброс папок в VW (лучше использовать NFS)
    внутри VM:
        apt-get update
        apt-get install build-essential linux-headers-`uname -r`
        mount /dev/sr0 /mnt
        /mnt/VBoxLinuxAdditions.run
        reboot
        mkdir /storage
        mount -t vboxsf shared /storage


12) Настройка mysql в guest OS:
    apt insatll mysql-server, phpmyadmin
    mysql
        ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'password';

        для каждой базы данных нужно создать пользователя
        CREATE USER 'sammy'@'localhost' IDENTIFIED BY 'password';
        GRANT ALL PRIVILEGES ON wchat.* TO 'wchat'@'localhost' WITH GRANT OPTION;
        flush privileges;

    vim /root/.my.cnf
    vim /home/stelhs/.my.cnf
        [mysqldump]
        user=user
        password=password

        [mysql]
        user = myuser
        password = secret

    для бакапа:
        mysqldump -uroot --all-databases > mysql_databases.sql


13) настройка overlayroot для host машины
    apt install overlayroot
    cp /etc/overlayroot.conf /etc/overlayroot.conf_rw
    cp /etc/overlayroot.conf /etc/overlayroot.conf_ro
        /etc/overlayroot.conf_ro
            #overlayroot=""
            overlayroot="tmpfs:swap=1,recurse=0"

    cp root/root/overctl_ro.sh /root/
    cp root/root/overctl_rw.sh /root/
    Переключение c RW на RO:
        cd /root
        ./overctl_ro.sh
        reboot

    Переключение c RO на RW:
        overlayroot-chroot
        cd /root
        ./overctl_rw.sh
        exit
        reboot


14) настройка автозапуса virtualbox
    cp root/etc/systemd/system/vbox_server_debian.service /etc/systemd/system/
    systemctl enable vbox_server_debian.service


15) Настроить сеть:
    /etc/network/interfaces
        allow-hotplug enp3s0
        iface enp3s0 inet static
            address 192.168.0.2
            netmask 255.255.255.0
            gateway 192.168.0.1
            dns-nameservers 192.168.0.1 8.8.8.8


16) Проброс /storage через NFS:
    на host машине:
        aptitude install nfs-kernel-server
        systemctl enable nfs-server
        vim /etc/exports
            /storage 192.168.0.3(rw,sync,no_subtree_check,no_root_squash,no_all_squash)
    на VM:
        apt install nfs-common
        mount 192.168.0.2:/storage /mnt/
        /etc/fstab
            192.168.0.2:/storage    /storage   nfs   defaults   0  0

    Необходимо полностью синхронизировать id пользователей и групп между host и guest


17) настройка сайтов
    sudo aptitude install imagemagick
    vim /etc/php/8.2/apache2/php.ini
        error_reporting = E_ALL & ~E_DEPRECATED
        display_errors = On
        display_startup_errors = On
    systemctl restart apache2

    cd /usr/local/lib/
    git clone https://github.com/stelhs/php_common.git
    mv php_common php
    chmod 775 php
    chown stelhs:sr90 /usr/local/lib/php
    chown -R stelhs:sr90 /usr/local/lib/php
    cd php
    git config --global --add safe.directory /usr/local/lib/php

    sudo a2enmod ssl
    sudo mkdir /etc/apache2/certs
    cd /etc/apache2/certs
    openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out apache.crt -keyout apache.key
    sudo vim /etc/apache2/sites-enabled/000-default.conf
	<VirtualHost *:443>
	    ServerAdmin webmaster@localhost

	    DocumentRoot /storage/www/

	    ErrorLog ${APACHE_LOG_DIR}/error.log

	    CustomLog ${APACHE_LOG_DIR}/access.log combined

	    SSLEngine on

	    SSLCertificateFile /etc/apache2/certs/apache.crt

	    SSLCertificateKeyFile /etc/apache2/certs/apache.key

	    <Directory /storage/www/>
		Options FollowSymLinks
		Options -Indexes
		AllowOverride All
	        Require all granted
	    </Directory>
	</VirtualHost>


18) Настройка бакапов:
    cp root/etc/systemd/system/bootable_backup.service /etc/systemd/system
    cp root/etc/systemd/system/storage_backup.service /etc/systemd/system
    cp root/etc/systemd/system/storage_backup.timer /etc/systemd/system
    systemctl daemon-reload
    systemctl enable bootable_backup.service
    systemctl enable storage_backup.timer

19) Настроить принтер на host:
        aptitude install cups printer-driver-foo2zjs hplip

        vim /etc/cups/cupsd.conf
            Listen 192.168.0.3:631
            Browsing Yes
            DefaultAuthType Basic

            <Location />
              Order allow,deny
              Allow from 192.168.0.*
            #  Allow from all
            </Location>

            <Location /admin>
              Order allow,deny
              Allow from 192.168.0.*
            </Location>

            <Location /admin/conf>
              AuthType Default
              Require user @SYSTEM
              Order allow,deny
              Allow from 192.168.0.*
            </Location>


        systemctl restart cups
        hp-setup -i
        открыть: https://192.168.0.3:631/admin
