# Goldhand Clinic Blog Codex plugin

Windows recipients can install this plugin from one file. They do not need Git, a ZIP extractor, or a PowerShell command.

## Windows one-file install

**[Download INSTALL-WINDOWS.cmd](https://github.com/seojun03/goldhand-clinic-blog-plugin/releases/latest/download/INSTALL-WINDOWS.cmd)**

1. Download the file from the link above.
2. Close ChatGPT completely.
3. Double-click `INSTALL-WINDOWS.cmd`.
4. Wait for `INSTALLATION COMPLETE`, close the window, and reopen ChatGPT.

The installer does not install, update, remove, or modify the ChatGPT app. It verifies Python and a Codex CLI that supports plugins, downloads the complete package to a short path, copies it to `%USERPROFILE%\GoldhandClinicPlugin`, and connects it as a local marketplace plugin.

If the recipient edits the local skill, run `goldhand-clinic-blog-apply-my-edits.cmd` from the Desktop to refresh the installed cache.

Direct selector: `goldhand-clinic-blog@goldhand-clinic`

## Source archive fallback

[Download the complete source ZIP](https://github.com/seojun03/goldhand-clinic-blog-plugin/archive/refs/heads/main.zip), extract it, and double-click `INSTALL-WINDOWS.cmd`. If the CMD is accidentally separated from the other files, it downloads a complete copy and continues.

## Verification

The GitHub Actions workflow runs on Windows PowerShell 5.1 and verifies complete-archive installation, isolated-CMD recovery, invalid Codex candidate rejection, missing `CODEX_HOME` creation, nonfatal locked cleanup, and enabled local plugin registration.
