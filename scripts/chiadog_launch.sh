echo 'Configuring Chiadog...'
mkdir -p /root/.chia/chiadog/logs
cp -n /machinaris/config/${blockchains}dog.sample.yaml /root/.chia/chiadog/config.yaml
cp -f /machinaris/scripts/chiadog_notifier.sh /root/.chia/chiadog/notifier.sh && chmod 755 /root/.chia/chiadog/notifier.sh

# Temporary fixes for bad key in fork config.yaml during v0.6.0 development stream
sed -i 's/flax_logs/chia_logs/g' /root/.chia/chiadog/config.yaml
sed -i "s/flax@/${blockchains}@/g" /root/.chia/chiadog/config.yaml

echo 'Starting Chiadog...'
cd /chiadog
chiadog_pids=$(pidof python3)
if [[ ! -z $chiadog_pids ]]; then
    kill $chiadog_pids
fi
/chia-blockchain/venv/bin/python3 -u main.py --config /root/.chia/chiadog/config.yaml > /root/.chia/chiadog/logs/chiadog.log 2>&1 &
