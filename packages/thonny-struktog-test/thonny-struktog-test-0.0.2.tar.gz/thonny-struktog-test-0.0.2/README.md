# Webdriver Plugin for the thonny IDE

## Usage with struktog

All the following elements can be found in the "tools" menu of thonny. "Open website" opens the struktog website in the browser and shows the Python source code. "Start observing element by id" will observe the changes in the python code and send it directly to your thonny code view. "Stop observing element by id" will stop looking for changes and updating the code view. "Transform code view to JSON" will transform the python code view source code to a JSON representation which can be loaded by struktog. An example can be found [here](./struktog.json).

## Warning

The browser Chromium is not supported. Advanced security features can only be set on Firefox.

## Installation

- Install a browser and webdriver which is supported by Selenium. You can get a list of supported software [here](https://www.selenium.dev/documentation/en/getting_started_with_webdriver/browsers/).

- Install the python dependencies

```bash
pip install -r requirements.txt --user
```

## Start the plugin with thonny

```bash
cd /path/to/thonny/
PYTHONPATH=/path/to/thonny-webdriver/ python -m thonny
```

## Usage in thonny

Click on the "Tools" section in the menu at the top of the program. And then select "Open Website". You will be asked to input a website. A new browser window will open with the desired website. After that, you can click on the "Tools" section in the menu again and select "Start observing element by id". You will be asked to input a HTML element id which will be observed in the background. To stop observing an elment you can select the "Stop observing element by id" option and provide the HTML element id.

## Licenses

This project is using third party projects and libraries.

| Name     | Website                                 | License    |
| -------- | --------------------------------------- | ---------- |
| thonny   | https://thonny.org                      | MIT        |
| selenium | https://github.com/SeleniumHQ/selenium/ | Apache 2.0 |
