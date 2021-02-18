echo "IPs for testing machines:"
for i in {1..15}
do
    echo "site.${i}:"
    bash get-vm-ip.sh Leap site.${i}
done

echo "client"
bash get-vm-ip.sh Leap client

echo "cloud"
bash get-vm-ip.sh Leap cloud
