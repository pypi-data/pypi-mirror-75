# igeAutoTest

C++ extension Firebase Auto Test Lab for 3D and 2D games.

### Before running this tutorial, you have to install igeAutoTest
	[pip install igeAutoTest]

### Functions - [**DEV**]
- First, you need to impor the module
	```
	import igeAutoTest
	```
- Helper function
	- Check if the game is running with Auto Test or not
		```
		auto_test = igeAutoTest.isLoopTest()
		```
	- Capture the screenshot, the image will be saved under **.jpg** format with the name based on the system time
		```
		igeAutoTest.screenshots()
		```
	- Write message information to a results file, in string format
		```
		igeAutoTest.writeResultsTest(message)
		```
	- Finish the auto test loop, all the result information and screenshot will be upload to **Test Lab** firebase console
		```
		igeAutoTest.finishLoopTest()
		```
	- The default test loop result should be (**result.json**)
		```json
		{
            "Adjust": {
                "adid": "4f05a489cecc11a55b9b3a8f4210c1f1",
                "debug": true,
                "event": [],
                "secret": "(1, 1588245832, 1151454453, 1814556983, 1969935874)",
                "token": "7m5evag9v7k0"
            },
            "Applovin": {
                "banner": "7f7bd2e768a442b5",
                "interstitial": "e1eb7ecd4a858332",
                "rewarded": "042ce899efe8b87e"
            },
            "Facebook": {
                "id": "321633655547110"
            },
            "GameAnalytics": {
                "debug": true,
                "event": {
                "complete": [
                    "world01"
                ],
                "fail": [],
                "start": [
                    "world01",
                    "world02",
                    "world03",
                    "world04"
                ]
                },
                "game_key": "02e1f6be051f6035a1f2c1479c40a086",
                "secret_key": "e3dbce0764a99a0ba5de331d1c02b363c938e614"
            },
            "Result": "Success"
        }
	    ```
### The checklist [**PLANNER / QA / DEV**]
- Mandatory
    - Result = Success
    - has the screenshot capturing throughout the auto test run
    - the video

- Adjust
    - debug = false
    - has the correct token / secret key

- Applovin
    - we should have correct the banner / interstitial / rewarded key
    - show ads when the game has them supported

- Facebook
    - has the correct Facebook id

- GameAnalytics
    - debug = false
    - has start / complete event before send the build to Ketchapp

- Depending on the feature supported, we should have some modules disabled

### Reference
- https://firebase.google.com/docs/test-lab

