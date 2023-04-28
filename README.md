# Auto-GPT-AlpacaTrader


Credit where credit is due to [isaiahbjork](https://github.com/isaiahbjork/Auto-GPT-MetaTrader-Plugin/) this is meant to be pretty similar to his just using the
Alpaca Trading platform

### Plugin Installation Steps

for Linux, depending on distro
```
sudo apt-get install zip
apk add zip
sudo pacman -S zip
sudo yum install zip
```
Mac / Linux / WSL
```
cd plugins && git clone https://github.com/danikhan632/Auto-GPT-AlpacaTrader-Plugin.git && zip -r ./Auto-GPT-AlpacaTrader-Plugin.zip ./Auto-GPT-AlpacaTrader-Plugin && rm -rf ./Auto-GPT-AlpacaTrader-Plugin && cd .. && ./run.sh --install-plugin-deps

```
Windows, Powershell
```
cd plugins; git clone https://github.com/danikhan632/Auto-GPT-AlpacaTrader-Plugin.git; Compress-Archive -Path .\Auto-GPT-AlpacaTrader-Plugin -DestinationPath .\Auto-GPT-AlpacaTrader-Plugin.zip; Remove-Item -Recurse -Force .\Auto-GPT-AlpacaTrader-Plugin; cd ..
```



5. **Allowlist the plugin (optional):**
   Add the plugin's class name to the `ALLOWLISTED_PLUGINS` in the `.env` file to avoid being prompted with a warning when loading the plugin:

   ``` shell
   ALLOWLISTED_PLUGINS=AutoGPTAlpacaTraderPlugin
   APCA_API_KEY_ID=your_api_key
   APCA_API_SECRET_KEY=your_api_secret_key
   APCA_API_BASE_URL=your_api_base_url
   ```

   If the plugin is not allowlisted, you will be warned before it's loaded.
