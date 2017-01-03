#!/bin/bash
set -e

docker rm -f exp models es kafka batch redis lb web1 web2 web3 &> /dev/null || {
    echo "Some container(s) cannot be removed"
    echo "Try docker ps -a"
}

docker rm -f mysql mysql-cmdline &> /dev/null {
    echo "Error removing database container(s)"
    echo "Try docker ps -a"
}

docker start mysql mysql-cmdline &> /dev/null || {
    echo "Error starting docker container(s)!"
    exit 1
}
sleep 1

docker exec -it mysql-cmdline bash -c \
"mysql -uroot -p'\$3cureUS' -h db -Bse \"drop database cs4501;
create database cs4501 character set utf8;
grant all on *.* to 'www'@'%'; \"; " &> /dev/null || {
    echo "Error clearing the database!"
    exit 2
}

docker stop mysql-cmdline &> /dev/null || {
    echo "Error stopping mysql-cmdline!"
    exit 3
}
echo "Successfully cleared the database!"
