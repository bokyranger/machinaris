#!/bin/env bash
#
# Initialize Maize service, depending on mode of system requested
#

cd /maize-blockchain

. ./activate

# Only the /root/.chia folder is volume-mounted so store maize within
mkdir -p /root/.chia/maize
rm -f /root/.maize
ln -s /root/.chia/maize /root/.maize 

if [[ "${blockchain_db_download}" == 'true' ]] \
  && [[ "${mode}" == 'fullnode' ]] \
  && [[ ! -f /root/.maize/mainnet/db/blockchain_v1_mainnet.sqlite ]] \
  && [[ ! -f /root/.maize/mainnet/db/blockchain_v2_mainnet.sqlite ]]; then
  mkdir -p /root/.maize/mainnet/db/ && cd /root/.maize/mainnet/db/
  echo "Sorry, Maize does not offer a recent blockchain DB for download via script.  Standard sync will happen over a few days."
  echo "It is recommended to add some peer node connections on the Connections page of Machinaris."
fi

mkdir -p /root/.maize/mainnet/log
maize init >> /root/.maize/mainnet/log/init.log 2>&1 

echo 'Configuring Maize...'
if [ -f /root/.maize/mainnet/config/config.yaml ]; then
  sed -i 's/log_stdout: true/log_stdout: false/g' /root/.maize/mainnet/config/config.yaml
  sed -i 's/log_level: WARNING/log_level: INFO/g' /root/.maize/mainnet/config/config.yaml
  sed -i 's/localhost/127.0.0.1/g' /root/.maize/mainnet/config/config.yaml
fi

# Loop over provided list of key paths
label_num=0
for k in ${keys//:/ }; do
  if [[ "${k}" == "persistent" ]]; then
    echo "Not touching key directories."
  elif [ -s ${k} ]; then
    echo "Adding key #${label_num} at path: ${k}"
    maize keys add -l "key_${label_num}" -f ${k} > /dev/null
    ((label_num=label_num+1))
  fi
done

# Loop over provided list of completed plot directories
IFS=':' read -r -a array <<< "$plots_dir"
joined=$(printf ", %s" "${array[@]}")
echo "Adding plot directories at: ${joined:1}"
for p in ${plots_dir//:/ }; do
    maize plots add -d ${p}
done

# Start services based on mode selected. Default is 'fullnode'
if [[ ${mode} =~ ^fullnode.* ]]; then
  for k in ${keys//:/ }; do
    while [[ "${k}" != "persistent" ]] && [[ ! -s ${k} ]]; do
      echo 'Waiting for key to be created/imported into mnemonic.txt. See: http://localhost:8926'
      sleep 10  # Wait 10 seconds before checking for mnemonic.txt presence
      if [ -s ${k} ]; then
        maize keys add -f ${k}
        sleep 10
      fi
    done
  done
  if [ -f /root/.chia/machinaris/config/wallet_settings.json ]; then
    maize start farmer-no-wallet
  else
    maize start farmer
  fi
  if [[ ${mode} =~ .*timelord$ ]]; then
    if [ ! -f vdf_bench ]; then
        echo "Building timelord binaries..."
        apt-get update > /tmp/timelord_build.sh 2>&1 
        apt-get install -y libgmp-dev libboost-python-dev libboost-system-dev >> /tmp/timelord_build.sh 2>&1 
        BUILD_VDF_CLIENT=Y BUILD_VDF_BENCH=Y /usr/bin/sh ./install-timelord.sh >> /tmp/timelord_build.sh 2>&1 
    fi
    maize start timelord-only
  fi
elif [[ ${mode} =~ ^farmer.* ]]; then
  if [ ! -f ~/.maize/mainnet/config/ssl/wallet/public_wallet.key ]; then
    echo "No wallet key found, so not starting farming services.  Please add your Chia mnemonic.txt to the ~/.machinaris/ folder and restart."
  else
    maize start farmer-only
  fi
elif [[ ${mode} =~ ^harvester.* ]]; then
  if [[ -z ${farmer_address} || -z ${farmer_port} ]]; then
    echo "A farmer peer address and port are required."
    exit
  else
    if [ ! -f /root/.maize/farmer_ca/private_ca.crt ]; then
      mkdir -p /root/.maize/farmer_ca
      response=$(curl --write-out '%{http_code}' --silent http://${farmer_address}:8933/certificates/?type=maize --output /tmp/certs.zip)
      if [ $response == '200' ]; then
        unzip /tmp/certs.zip -d /root/.maize/farmer_ca
      else
        echo "Certificates response of ${response} from http://${farmer_address}:8933/certificates/?type=maize.  Is the fork's fullnode container running?"
      fi
      rm -f /tmp/certs.zip 
    fi
    if [[ -f /root/.maize/farmer_ca/private_ca.crt ]] && [[ ! ${keys} == "persistent" ]]; then
      maize init -c /root/.maize/farmer_ca 2>&1 > /root/.maize/mainnet/log/init.log
      #chmod 755 -R /root/.maize/mainnet/config/ssl/ &> /dev/null
      #maize init --fix-ssl-permissions > /dev/null 
    else
      echo "Did not find your farmer's certificates within /root/.maize/farmer_ca."
      echo "See: https://github.com/guydavis/machinaris/wiki/Workers#harvester"
    fi
    echo "Configuring farmer peer at ${farmer_address}:${farmer_port}" 
    maize configure --set-farmer-peer ${farmer_address}:${farmer_port}  2>&1 >> /root/.maize/mainnet/log/init.log
    maize configure --enable-upnp false  2>&1 >> /root/.maize/mainnet/log/init.log
    maize start harvester -r
  fi
elif [[ ${mode} == 'plotter' ]]; then
    echo "Starting in Plotter-only mode.  Run Plotman from either CLI or WebUI."
fi
