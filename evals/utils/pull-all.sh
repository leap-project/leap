if [ "$#" -ne 5 ]; then
    echo "Illegal number of parameters (expecting 3):"
    echo "[ipfile-sites, ipfile-client, ipfile-cloud, uname, branchname]"
    exit
fi

ipfile_sites=$1
ipfile_client=$2
ipfile_cloud=$3
uname=$4
branchname=$5

leapPath="/home/$uname/gopath/src/leap"

for ip in $(cat $ipfile_sites);do

	ssh -t $uname@$ip "
		cd $leapPath
		git stash
		git fetch origin
		git checkout $branchname
		git pull origin $branchname
	"

done

for ip in $(cat $ipfile_client);do

	ssh -t $uname@$ip "
		cd $leapPath
		git stash
		git fetch origin
		git checkout $branchname
		git pull origin $branchname
	"

done

for ip in $(cat $ipfile_cloud);do

	ssh -t $uname@$ip "
		cd $leapPath
		git stash
		git fetch origin
		git checkout $branchname
		git pull origin $branchname
	"

done

exit