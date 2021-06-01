#!/bin/bash -x

if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters (expecting 4):"
    echo "[r-group, vm-name, location]"
    exit
fi

rgroup=$1    # resource group in which to create VM
vm=$2        # the name of the newly created VM
location=$3

# Create the VM
az vm create --resource-group $rgroup --name $vm \
   --admin-username stolet \
   --ssh-key-value ~/.ssh/id_rsa.pub \
   --location $location \
   --size "Standard_D4s_v3"

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

