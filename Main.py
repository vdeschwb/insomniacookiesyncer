import json
from ChromiumCookieGrabber import ChromiumCookieGrabber
from InsomniaCookieInjector import InsomniaCookieInjector


if __name__ == "__main__":
    grabber = ChromiumCookieGrabber()
    injector = InsomniaCookieInjector()

    all_cookies = grabber.get_cookies()

    # print(injector.get_cookies())
    # injector.load([(h, k, v) for (h, k, v) in all_cookies if h == "test.platform.service.acodis.io"])
    synced_cookies = injector.load(all_cookies)

    print("Synced the following cookies:\n\n" + "\n".join([f"[{c['domain']}] {c['key']}={c['value'][:50] + '...' if len(c['value']) > 50 else c['value']}" for c in synced_cookies]))
