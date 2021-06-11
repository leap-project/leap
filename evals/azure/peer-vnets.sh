rgroup=leap_westus

#vnets=('clientVNET' 'cloudVNET' 'site.1VNET' 'site.2VNET' 'site.3VNET' 'site.4VNET' 'site.5VNET' 'site.6VNET' 'site.7VNET' \
#       'site.8VNET' 'site.9VNET' 'site.10VNET' 'site.11VNET' 'site.12VNET' 'site.13VNET' 'site.14VNET' 'site.15VNET')

vnets=('clientVNET' 'cloudVNET')

let numlocations=2

# For every vnet created, establish peering with other vnets
for (( i = 0; i < numlocations; i++ )); do

  vnetName1=${vnets[i]}

  echo ${vnetName1}
  echo ${rgroup}
  # Get the id of first VNET.
  vNet1Id=$(az network vnet show \
    --resource-group ${rgroup} \
    --name ${vnetName1} \
    --query id --out tsv)

  echo $vNet1Id

  for (( j = 0; j < numlocations; j++ )); do

      if [[ "i" -eq "j" ]]; then
        continue
      fi

      vnetName2=${vnets[j]}

      # Get the id of second VNET.
      vNet2Id=$(az network vnet show \
        --resource-group $rgroup \
        --name ${vnetName2} \
        --query id --out tsv)

      az network vnet peering create \
        --name ${vmlocation1}VNET-${vmlocation2}VNET \
        --resource-group $rgroup \
        --vnet-name  ${vnetName1} \
        --remote-vnet-id $vNet2Id \
        --allow-vnet-access

   done



done