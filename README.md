# Sony VPL-XW6000 Home Assistant Integration

This integration allows you to control and monitor your Sony VPL-XW6000 projector using Sony's ADCP (Advanced Display Control Protocol) over a network. It supports features such as power control, input switching, and status monitoring.

---

## **Features**
- Turn the projector on/off.
- Switch input sources (e.g., HDMI1, HDMI2).
- Monitor projector status (e.g., power state, input source).
- Automatically discover the projector on the network using the advertisement service.
- Optional authentication for secure communication.

---

## **Prerequisites**

1. **Sony VPL-XW6000 Projector**:
   - Ensure the projector is connected to the same network as your Home Assistant instance.
   - Enable **ADCP** and the **advertisement service** on the projector (see instructions below).

2. **Home Assistant**:
   - A running instance of Home Assistant (2023.3 or later is recommended).

---

## **Configuring the Projector for ADCP and Advertisement**

To enable ADCP and the advertisement service on your Sony VPL-XW6000 projector, follow these steps:

### **1. Enable ADCP**
1. **Access the Projector's Settings**:
   - Turn on the projector.
   - Press the **Menu** button on the remote control.

2. **Navigate to Network Settings**:
   - Go to **Network Settings** > **Control Protocol**.

3. **Enable ADCP**:
   - Set the **Control Protocol** to **ADCP**.

4. **Optional: Enable Authentication**:
   - If you want to secure communication, enable **Authentication**.
   - Set a **Username** and **Password** for ADCP access.

5. **Save Settings**:
   - Confirm and save the settings.

---

### **2. Enable the Advertisement Service**
1. **Access Advertisement Settings**:
   - In the projector's **Network Settings**, locate the **Advertisement Service** option.

2. **Enable Advertisement**:
   - Set the **Advertisement Service** to **On**.

3. **Configure Advertisement Details**:
   - Ensure the projector broadcasts its attributes (e.g., model name, software version) on the network.
   - Verify that the advertisement service is configured to use the same network as Home Assistant.

4. **Save Settings**:
   - Confirm and save the settings.

---

### **3. Verify Network Configuration**
1. **Check IP Address**:
   - Go to **Network Settings** > **IP Address Settings**.
   - Ensure the projector has a valid IP address, subnet mask, and gateway configured.

2. **Test Network Connectivity**:
   - Ping the projector's IP address from a computer on the same network to ensure it is reachable.

3. **Verify Advertisement**:
   - Use a network discovery tool (e.g., `nmap` or `Bonjour Browser`) to confirm that the projector is broadcasting its attributes.

---

## **Installing the Integration**

1. **Copy the Integration Files**:
   - Copy the `sony_vpl_xw6000` folder into your Home Assistant `custom_components` directory.

2. **Restart Home Assistant**:
   - Restart Home Assistant to load the custom integration.

3. **Add the Integration**:
   - Go to **Settings > Devices & Services > Add Integration**.
   - Search for **Sony VPL-XW6000** and select it.

4. **Configure the Integration**:
   - Enter the projector's IP address.
   - If authentication is enabled on the projector, toggle **Authentication** to **On** and provide the username and password.
   - The integration will validate the network connection and authentication credentials during setup. If validation fails, an error message will be displayed.

---

## **Usage**

Once the integration is set up:
- The projector will appear as a device in Home Assistant.
- You can control the projector (e.g., turn it on/off) and monitor its status from the Home Assistant UI.
- If the advertisement service is enabled, the integration will automatically discover the projector and populate its attributes.

---

## **Troubleshooting**

1. **Cannot Connect to the Projector**:
   - Ensure the projector is powered on and connected to the same network as Home Assistant.
   - Verify that ADCP and the advertisement service are enabled on the projector.
   - Check the projector's IP address and ensure it matches the one entered in the integration.

2. **Advertisement Service Not Working**:
   - Ensure the advertisement service is enabled in the projector's settings.
   - Verify that the projector is broadcasting its attributes using a network discovery tool.

3. **Authentication Fails**:
   - Ensure the correct username and password are entered.
   - If authentication is not required, ensure the **Authentication** toggle is set to **Off** during setup.

4. **Logs**:
   - Check the Home Assistant logs for error messages related to the integration.

---

## **Error Codes**

- `ERR=01`: Invalid Command. Ensure the command format is correct.
- `ERR=02`: Authentication Failed. Verify the username and password.
- `ERR=03`: Command Not Supported. Ensure the projector supports the requested command.

---

## **Support**

For issues or feature requests, please open an issue on the [GitHub repository](https://github.com/your-repo/sony-vpl-xw6000).

---

## **License**

This integration is licensed under the MIT License.
