#!/bin/bash -x

if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters (expecting 4):"
    echo "[r-group, vm-name, image-name, location]"
    exit
fi

rgroup=$1    # resource group in which to find the image/create VM
vm=$2        # the name of the newly created VM
imagename=$3 # imagename from which to create the VM
location=$4

# Create the VM
az vm create --resource-group $rgroup --name $vm --image $imagename \
   --admin-username stolet \
   --ssh-key-value ~/.ssh/id_rsa.pub \
   --location $location \
   --plan-name "5-6" \
   --plan-publisher "bitnami" \
   --plan-product  "lampstack"

# Set the public IP address to static
az network public-ip update --name ${vm}PublicIp --resource-group $rgroup --allocation-method Static

# Associate the permissive network security group policy with the nic for this VM
# group name: 'permissive-all-in-all-out'
az network nic update \
--resource-group $rgroup \
--name ${vm}VMNic \
--network-security-group permissive-all-in-all-out

# Show details about the newly created VM
az vm show \
   --resource-group $rgroup \
   --name $vm \
   --show-details \
   -o table

