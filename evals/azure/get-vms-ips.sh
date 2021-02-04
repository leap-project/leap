echo "IPs for testing machines:"
for i in {1..15}
do
    echo "site.${i}:"
    ./get-vm-ip.sh leap site.${i}
done

echo "client"
./get-vm-ip.sh leap client

echo "cloud"
./get-vm-ip.sh leap cloud
