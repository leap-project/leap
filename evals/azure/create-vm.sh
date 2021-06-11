#!/bin/bash -x

if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters (expecting 4):"
    echo "[r-group, vm-name, location, image-name]"
    exit
fi

rgroup=$1    # resource group in which to create VM
vm=$2        # the name of the newly created VM
location=$3
image=$4

# Create the VM
az vm create --resource-group $rgroup --name $vm --image $image\
   --admin-username stolet \
   --vnet-name ${location}VNET \
   --subnet Subnet1 \
   --ssh-key-value ~/.ssh/id_rsa.pub \
   --location $location \
   --size "Standard_D4s_v3"

# Set the public IP address to static
az network public-ip update --name ${vm}PublicIp --resource-group $rgroup --allocation-method Static

# Associate the permissive network security group policy with the nic for this VM
# group name: 'permissive-all-in-all-out'
nsg_name="permissive-all-in-all-out-${location}"
az network nic update \
--resource-group $rgroup \
--name ${vm}VMNic \
--network-security-group $nsg_name

# Show details about the newly created VM
az vm show \
   --resource-group $rgroup \
   --name $vm \
   --show-details \
   -o table

