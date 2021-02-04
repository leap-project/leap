echo "IPs for sites:"
for i in {1..15}
do
    echo "site.${i}:"
    ./get-vm-ip.sh leap site.${i}
done

