class VisionAssertion:
    pass


vision = VisionAssertion()


class TestGoogleSearch:

    def test_cats(self, engine) -> None:
        engine.get_web("https://www.google.com")
        engine.get_element("search").fill("cats")
        engine.get_element("button").click()

        screenshot = engine.get_screenshot()
        result = vision.run(image_path=screenshot, prompt="what do you see in this image?")

        assert result.decision == "Passed", result.justification
