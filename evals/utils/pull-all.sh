if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters (expecting 3):"
    echo "[ipfile, uname, branchname]"
    exit
fi

ipfile=$1
uname=$2
branchname=$3

leapPath="/home/$uname/gopath/src/leap"
hostFile="../azure-conf/$ipfile"

for ip in $(cat $hostFile);do

	ssh -t $uname@$ip "
		cd $leapPath
		git stash
		git fetch origin
		git checkout $branchname
		git pull origin $branchname
	"

done

exit