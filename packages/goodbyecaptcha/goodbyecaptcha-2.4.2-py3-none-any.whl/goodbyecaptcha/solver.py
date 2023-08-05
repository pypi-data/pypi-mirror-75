#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Solver module. """

import sys
import time
import traceback

from pyppeteer.errors import NetworkError, PageError, PyppeteerError
from pyppeteer.util import merge_dict

from goodbyecaptcha import util
from goodbyecaptcha.audio import SolveAudio
from goodbyecaptcha.base import Base
from goodbyecaptcha.exceptions import SafePassage, ButtonError, IframeError, TryAgain, ResolveMoreLater
from goodbyecaptcha.image import SolveImage
from goodbyecaptcha.util import get_random_proxy


class Solver(Base):
    def __init__(self, pageurl, loop=None, proxy=None, proxy_auth=None, options=None, lang='en-US', chromePath=None,
                 **kwargs):
        self.url = pageurl
        self.loop = loop or util.get_event_loop()
        self.proxy = proxy
        self.proxy_auth = proxy_auth
        self.options = merge_dict({} if options is None else options, kwargs)
        self.chromePath = chromePath

        super(Solver, self).__init__(loop=loop, proxy=proxy, proxy_auth=proxy_auth, language=lang, options=options,
                                     chromePath=chromePath)

    async def start(self):
        """Begin solving"""
        start = time.time()
        result = None
        try:
            self.browser = await self.get_new_browser()
            self.context = await self.browser.createIncognitoBrowserContext()
            await self.open_page(self.url, new_page=False)  # Use first page
            result = await self.solve()
        except NetworkError as ex:
            traceback.print_exc(file=sys.stdout)
            print(f"Network error: {ex}")
        except ResolveMoreLater as ex:
            traceback.print_exc(file=sys.stdout)
            print(f"Resolve More Captcha error: {ex}")
        except TryAgain as ex:
            traceback.print_exc(file=sys.stdout)
            print(f"Try Again error: {ex}")
        except TimeoutError as ex:
            traceback.print_exc(file=sys.stdout)
            print(f"Error timeout: {ex}")
        except PageError as ex:
            traceback.print_exc(file=sys.stdout)
            print(f"Page Error: {ex}")
        except IframeError as ex:
            print(f"IFrame error: {ex}")
        except PyppeteerError as ex:
            traceback.print_exc(file=sys.stdout)
            print(f"Pyppeteer error: {ex}")
        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            print(f"Error unexpected: {ex}")
        finally:
            # Close all Context and Browser
            if self.context:
                await self.context.close()
                self.context = None
            if self.browser:
                await self.browser.close()
                self.browser = None
            await self.cleanup()
            # Return result
            if isinstance(result, dict):
                status = result['status'].capitalize()
                print(f"Result: {status}")
            elapsed = time.time() - start
            print(f"Time elapsed: {elapsed}")
            return result

    async def solve(self):
        """Click checkbox, otherwise attempt to decipher image/audio"""
        self.log('Solvering ...')
        try:
            await self.get_frames()
        except Exception:
            return await self.get_code({'status': 'success'})
        self.log('Wait for CheckBox ...')
        await self.loop.create_task(self.wait_for_checkbox())
        self.log('Click CheckBox ...')
        await self.click_checkbox()
        try:
            result = await self.loop.create_task(
                self.check_detection(self.animation_timeout))  # Detect Detection or captcha finish
        except SafePassage:
            return await self._solve()  # Start to solver
        else:
            return self.get_code(result)

    async def _solve(self):
        """Select method solver"""
        proxy = get_random_proxy() if self.proxy == 'auto' else self.proxy
        if self.method == 'images':
            self.log('Using Image Solver')
            self.image = SolveImage(page=self.page, image_frame=self.image_frame, loop=self.loop, proxy=proxy,
                                    proxy_auth=self.proxy_auth, options=self.options, chromePath=self.chromePath)
            solve = self.image.solve_by_image
        else:
            self.log('Using Audio Solver')
            self.audio = SolveAudio(page=self.page, image_frame=self.image_frame, loop=self.loop, proxy=proxy,
                                    proxy_auth=self.proxy_auth, options=self.options, chromePath=self.chromePath)
            solve = self.audio.solve_by_audio

        try:
            result = await self.loop.create_task(solve())
            return await self.get_code(result)
        except PyppeteerError as ex:
            raise TryAgain(ex)

    async def get_code(self, result_status):
        if result_status["status"] == "success":
            code = await self.g_recaptcha_response()
            if code:
                result_status["code"] = code
                return result_status
        else:
            return result_status

    async def wait_for_checkbox(self):
        """Wait for checkbox to appear."""
        try:
            await self.checkbox_frame.waitForFunction(
                "jQuery('#recaptcha-anchor').length",
                timeout=self.animation_timeout)
        except ButtonError:
            raise ButtonError("Checkbox missing, aborting")
        except Exception as ex:
            self.log(ex)
            await self.click_checkbox()  # Try Click

    async def click_checkbox(self):
        """Click checkbox on page load."""
        try:
            checkbox = await self.checkbox_frame.J("#recaptcha-anchor")
            await self.click_button(checkbox)
        except Exception as ex:
            self.log(ex)
            raise ex

    async def g_recaptcha_response(self):
        """Result of captcha"""
        code = await self.page.evaluate(
            "jQuery('#g-recaptcha-response').val()")
        return code
