def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST",
            '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior':
        'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)
# EOF
