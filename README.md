# Zigbee Lock Manager
[![GitHub Release][releases-shield]][releases]
[![hacs][hacsbadge]][hacs]

A Home Assistant integration to provide a dashboard for managing lock codes on Zigbee keypad locks.  Installing dynamically creates the helpers, automations, and dashboard YAML, based on the number of codes (slots) the user wants to manage.  

This integration was inspired by [KeyMaster](https://github.com/FutureTense/keymaster) for Z-Wave locks.  

**Currently this only supports ZHA (Zigbee Home Automation) in Home Assistant.  It does not support Zigbee2MQTT at this time. <br>

** **Test your added codes** - A limitation with Zigbee locks (and a key reason why Keymaster doesn't support them) is that they [don't universally support commands to retrieve codes](https://community.home-assistant.io/t/zha-yale-yrd210-getting-unsup-cluster-command-when-calling-get-pin-code/498428) from the lock. Therefore it's not possible to query the lock to confirm the code was successfully stored in the desired slot.  When setting codes with ZHA locks, as with this integration, you should test the codes to ensure they were successfully stored on the lock. 

## Features
* Generates helpers and dashboard cards for each code slot
* Disable/Enable code slot
* Update code on lock
* Clear code from lock

![Alt Text](ZLM_UI.jpg)

## Prerequisites
1. A Zigbee lock connected with Zigbe Home Automation (ZHA) in Home Assistant
2. Support for Packages directory enabled in your configuration.yaml
```YAML
homeassistant:
  packages: !include_dir_named packages
```

## Installation

The easiest way to install is through HACS by adding this as a custom repository.<br>

1. In Home Assistant, select HACS -> Integrations -> (three dots upper-right) > Add Custom Repositry https://github.com/Fiercefish1/Zigbee-Lock-Manager/
2. Find Zigbee Lock Manager in HACS
3. Download the latest version
4. Restart Home Assistant
5. Set up and configure the integration 


## Manual Installation

Copy the `custom_components/zigbee_lock_manager` directory to your `custom_components` folder. Restart Home Assistant and add the integration from the integrations page.

## Configuration

At this time the integration is only designed to manage the codes for a single lock.  To manage codes for more than a single ZHA locks you can create multiple instances of this integration, but they'll each have their own respsective input helpers. 

*While your lock may support 100 or more lock codes, it is recommended to choose <24 slots for optimal UI appearance and performance. The generated YAML was designed for Masonry layouts, and three cards fit nicely to a row.  For your dashboard OCD, choose a number of slots divisible by three. 

Slots: `# of code slots you want to manage` <br>
Lock: `entity_id of your ZHA keypad lock`

While not required, after install it's a good practice to reload YAML (Developer Tools > YAML > "ALL YAML CONFIGURATION") to ensure all changes are picked up and will be actionable. 

## Dashboard creation
*You will need access to your config directory and a file editor.  e.g. [VSC](https://github.com/hassio-addons/addon-vscode) or something else. <br>
<br>
Copy the YAML from: <br>
```YAML
config/packages/zigbee_lock_manager/zigbee_lock_manager_dashboard
```
Create a new dashboard, edit the raw config (three dots after enabling edit), and paste in the YAML from your clipboard.
Done.


[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/v/release/Fiercefish1/zigbee-lock-manager.svg?style=for-the-badge
[releases]: https://github.com/Fiercefish1/Zigbee-Lock-Manager/releases
