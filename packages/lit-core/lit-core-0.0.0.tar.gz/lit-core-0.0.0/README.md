# L.I.T.
***Lit Illumination Technology***
## Synopisis
This is an improved version of the <a href="http://github.com/nickpesce/neopixels">Neopixels</a> project</br>
The lit daemon makes it very easy to control ws281x addressable leds using a raspberry pi. Once the daemon is started, 'effects' can be started and state can be queried using a python api. Addition effects can be added very easily, and LEDs over IP (LOIPs) can be connected using [lit_arduino](https://github.com/nickpesce/lit_arduino)
## Installation
<ol>
<li>Install the python module rpi_ws281x<br/>
<code>sudo pip install rpi_ws281x</code></li>
<li>Clone this repository to your Raspberry Pi<br/>
<code>$ git clone https://github.com/nickpesce/lit.git</code></li>
<li>Install the package<br/>
  <code>$ cd lit</code><br/>
  <code>$ sudo  ./setup.py build</code> <br/>
  <code>$ sudo  ./setup.py install</code></li>
</ol>

### Startup Script
*If you are are using a config path that is not "/home/pi/.lit/litd", you must first edit the command in litd.service*
<ol>
<li>
  <code>sudo cp litd.service /etc/systemd/system</code>
</li>
<li>
  <code>sudo systemctl daemon-reload</code>
</li>
<li>
  <code>sudo systemctl start litd && sudo systemctl enable litd</code>
</li>
</ol>

## Customization
litd should be started with a --config PATH flag. The following files should all be in the PATH/config/ directory. Overriding the default configurations is optional, but making changes to config.ini and ranges.json is almost definitely necessary. To copy the default configuration files, use <code>litd -g PATH</code>. For example, <code>litd -g /home/pi/.lit/litd</code>, then run it with <code>sudo litd -c /home/pi/.lit/litd</code>
<ul>
<li>config.ini:
  <ul>
  <li>
  General
    <ul>
    <li>leds: The number of leds connected to your pi</li>
    <li>pin: The pwm/pcm/spi pin that your data line is connected to</li>
    </ul>
   </li>   
   </ul>
</li>

<li>ranges.json: Contains information about light groupings.
  <ul>
  <li>sections: Contiguous sections of leds defined by a name mapped to a start and end index.</li>
  <li>zones: Groups of sections that can all be controlled at once. Defined by a name mapped to a list of sections.</li>
  <li><a href="#virtual-sections">virtual_sections</a>: Light sections that are connected through a udp interface.</li>
  <li>default: The section or zone that should be used if none are explictly chosen.
  </ul>
</li>

<li>presets.json: Named groups of effects that can be run together. Maps preset names to preset objects.
Preset objects contain:
  <ul>
  <li>start_string: Message that is returned when the preset starts</li>
  <li>commands: List of commands to run. Commands are objects with an "effect" string and "args" object</li>
  </ul>
</li>

<li>colors.json: A list of all preset color values defined by an object containing a name and color. The color field is defined as an array contining a red, green, and blue value.
</li>

<li>speeds.json: Preset speed values. An object containing a mapping between names and speeds. 0 is the slowest possible, and 50 is the default.
</li>
</ul>

## Virtual Sections
If your leds can't all be connected by one wire, a udp connection can be made. This can work with any device, but the only officially supported device is the Arduino 8266 with [this library](https://github.com/nickpesce/lit_arduino). To set a virtual section, add an entry in the "virtual_sections" section of ranges.json. The format is as follows:

<code>
"virtual_sections": {"section_name": {"num_pixels": 60, "ip": "192.168.1.2", "port": 9000}}
</code>



_**Note: The virtual section must be named exactly the same as an already defined section. The start and end of the section specifies where the lights will be relative to the other "local" sections. The virtual_section will specify how that section is controlled.**_

## Adding New Effects
Easily add new and personalized effects. Basic python knowlege is required. To start, create a directory called 'effects' in your base directory (same level as the config directory). Create an empty file named '\_\_init\_\_.py' in the new directory. Finally, restart the daemon. Now any python files that are in this directory, or subdirectories of this directory, will try to be imported as effects when the daemon is started. Refer to effects/\_template.py for more information. 
