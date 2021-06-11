#az network vnet subnet create --name cloudSubnet1 --vnet-name cloudVNET --resource-group leap_westus --address-prefixes 10.0.1.0/24
#az network nic ip-config update --name ipconfigcloud --nic-name cloudVMNic --resource-group leap_westus --subnet cloudSubnet1 --vnet-name cloudVNET
#az network vnet subnet delete --name cloudSubnet --vnet-name cloudVNET --resource-group leap_westus

#az network vnet subnet create --name site.1Subnet1 --vnet-name site.1VNET --resource-group leap_westus --address-prefixes 10.0.2.0/24
#az network nic ip-config update --name ipconfigsite.1 --nic-name site.1VMNic --resource-group leap_westus --subnet site.1Subnet1 --vnet-name site.1VNET
#az network vnet subnet delete --name site.1Subnet --vnet-name site.1VNET  --resource-group leap_westus

az network vnet subnet create --name site.2Subnet1 --vnet-name site.2VNET --resource-group leap_westus --address-prefixes 10.0.3.0/24
az network nic ip-config update --name ipconfigsite.2 --nic-name site.2VMNic --resource-group leap_westus --subnet site.2Subnet1 --vnet-name site.2VNET
az network vnet subnet delete --name site.2Subnet --vnet-name site.2VNET  --resource-group leap_westus

az network vnet subnet create --name site.3Subnet1 --vnet-name site.3VNET --resource-group leap_westus --address-prefixes 10.0.4.0/24
az network nic ip-config update --name ipconfigsite.3 --nic-name site.3VMNic --resource-group leap_westus --subnet site.3Subnet1 --vnet-name site.3VNET
az network vnet subnet delete --name site.3Subnet --vnet-name site.3VNET  --resource-group leap_westus

az network vnet subnet create --name site.4Subnet1 --vnet-name site.4VNET --resource-group leap_westus --address-prefixes 10.0.5.0/24
az network nic ip-config update --name ipconfigsite.4 --nic-name site.4VMNic --resource-group leap_westus --subnet site.4Subnet1 --vnet-name site.4VNET
az network vnet subnet delete --name site.4Subnet --vnet-name site.4VNET  --resource-group leap_westus

az network vnet subnet create --name site.5Subnet1 --vnet-name site.5VNET --resource-group leap_westus --address-prefixes 10.0.6.0/24
az network nic ip-config update --name ipconfigsite.5 --nic-name site.5VMNic --resource-group leap_westus --subnet site.5Subnet1 --vnet-name site.5VNET
az network vnet subnet delete --name site.5Subnet --vnet-name site.5VNET  --resource-group leap_westus

az network vnet subnet create --name site.6Subnet1 --vnet-name site.6VNET --resource-group leap_westus --address-prefixes 10.0.7.0/24
az network nic ip-config update --name ipconfigsite.6 --nic-name site.6VMNic --resource-group leap_westus --subnet site.6Subnet1 --vnet-name site.6VNET
az network vnet subnet delete --name site.6Subnet --vnet-name site.6VNET  --resource-group leap_westus

az network vnet subnet create --name site.7Subnet1 --vnet-name site.7VNET --resource-group leap_westus --address-prefixes 10.0.8.0/24
az network nic ip-config update --name ipconfigsite.7 --nic-name site.7VMNic --resource-group leap_westus --subnet site.7Subnet1 --vnet-name site.7VNET
az network vnet subnet delete --name site.7Subnet --vnet-name site.7VNET  --resource-group leap_westus

az network vnet subnet create --name site.8Subnet1 --vnet-name site.8VNET --resource-group leap_westus --address-prefixes 10.0.9.0/24
az network nic ip-config update --name ipconfigsite.8 --nic-name site.8VMNic --resource-group leap_westus --subnet site.8Subnet1 --vnet-name site.8VNET
az network vnet subnet delete --name site.8Subnet --vnet-name site.8VNET  --resource-group leap_westus

az network vnet subnet create --name site.9Subnet1 --vnet-name site.9VNET --resource-group leap_westus --address-prefixes 10.0.10.0/24
az network nic ip-config update --name ipconfigsite.9 --nic-name site.9VMNic --resource-group leap_westus --subnet site.9Subnet1 --vnet-name site.9VNET
az network vnet subnet delete --name site.9Subnet --vnet-name site.9VNET  --resource-group leap_westus

az network vnet subnet create --name site.10Subnet1 --vnet-name site.10VNET --resource-group leap_westus --address-prefixes 10.0.11.0/24
az network nic ip-config update --name ipconfigsite.10 --nic-name site.10VMNic --resource-group leap_westus --subnet site.10Subnet1 --vnet-name site.10VNET
az network vnet subnet delete --name site.10Subnet --vnet-name site.10VNET  --resource-group leap_westus

az network vnet subnet create --name site.11Subnet1 --vnet-name site.11VNET --resource-group leap_westus --address-prefixes 10.0.12.0/24
az network nic ip-config update --name ipconfigsite.11 --nic-name site.11VMNic --resource-group leap_westus --subnet site.11Subnet1 --vnet-name site.11VNET
az network vnet subnet delete --name site.11Subnet --vnet-name site.11VNET  --resource-group leap_westus

az network vnet subnet create --name site.12Subnet1 --vnet-name site.12VNET --resource-group leap_westus --address-prefixes 10.0.13.0/24
az network nic ip-config update --name ipconfigsite.12 --nic-name site.12VMNic --resource-group leap_westus --subnet site.12Subnet1 --vnet-name site.12VNET
az network vnet subnet delete --name site.12Subnet --vnet-name site.12VNET  --resource-group leap_westus

az network vnet subnet create --name site.13Subnet1 --vnet-name site.13VNET --resource-group leap_westus --address-prefixes 10.0.14.0/24
az network nic ip-config update --name ipconfigsite.13 --nic-name site.13VMNic --resource-group leap_westus --subnet site.13Subnet1 --vnet-name site.13VNET
az network vnet subnet delete --name site.13Subnet --vnet-name site.13VNET  --resource-group leap_westus

az network vnet subnet create --name site.14Subnet1 --vnet-name site.14VNET --resource-group leap_westus --address-prefixes 10.0.15.0/24
az network nic ip-config update --name ipconfigsite.14 --nic-name site.14VMNic --resource-group leap_westus --subnet site.14Subnet1 --vnet-name site.14VNET
az network vnet subnet delete --name site.14Subnet --vnet-name site.14VNET  --resource-group leap_westus

az network vnet subnet create --name site.15Subnet1 --vnet-name site.15VNET --resource-group leap_westus --address-prefixes 10.0.16.0/24
az network nic ip-config update --name ipconfigsite.15 --nic-name site.15VMNic --resource-group leap_westus --subnet site.15Subnet1 --vnet-name site.15VNET
az network vnet subnet delete --name site.15Subnet --vnet-name site.15VNET  --resource-group leap_westus
