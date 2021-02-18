#!/bin/bash -x

if [ "$#" -ne 5 ]; then
    echo "Illegal number of parameters (expecting 5):"
    echo "[gallery_group_name, gallery_name, r-group, image-name]"
    exit
fi

gallery_group=$1 # Name of the resource group holding gallery
gallery_name=$2  # Name of gallery
rgroup=$3        # resource group in which to find the image/create VM
vm_name=$4       # the name of the vm to make an image of
imagename=$5     # the name of the image

# Create gallery for images
az group create --name $gallery_group --location westus
az sig create --resource-group $gallery_group --gallery-name $gallery_name

vm_id=$(az vm get-instance-view -g Leap -n leap-image --query id)

# Generalize vm to make image
echo "Generalizing VM"
az vm deallocate --resource-group $rgroup --name $vm_name
az vm generalize --resource-group $rgroup --name $vm_name

# Create image definition
echo "Creating image definition"
az sig image-definition create \
   --resource-group $gallery_group \
   --gallery-name $gallery_name \
   --gallery-image-definition leapImageDefinition \
   --publisher myPublisher \
   --offer myOffer \
   --sku mySKU \
   --os-type Linux \
   --os-state generalized \
   --plan-name "5-6" \
   --plan-publisher "bitnami" \
   --plan-product  "lampstack"

echo $vm_id

# Create image version
echo "Creating image version"
az sig image-version create \
   --resource-group $gallery_group \
   --gallery-name $gallery_name \
   --gallery-image-definition leapImageDefinition \
   --gallery-image-version 1.0.0 \
   --target-regions "westus" "eastus" "centralindia" "japaneast" "australiaeast" "westeurope" \
   --replica-count 1 \
   --managed-image "/subscriptions/cd833591-8043-4ff5-b7b9-5566b3a24d0e/resourceGroups/Leap/providers/Microsoft.Compute/virtualMachines/leap-image"
#   --managed-image $vm_id \
