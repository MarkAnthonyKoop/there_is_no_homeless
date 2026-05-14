# How to make phone pulls work without a tap-to-allow next time

The bottleneck on the first run of this project: Android phones plug in as
*charging-only* by default. To enumerate files (MTP) you have to swipe down
on the phone and select **File transfer**. This needs to be done **every
time** you reattach in MTP mode.

The fix is to use **ADB over Wi-Fi**, which only needs a one-time pairing.
After that, host-side `adb connect <ip>:<port>` works with zero phone-side
interaction as long as Wireless Debugging stays on.

---

## One-time setup (do this once, on the phone)

1. **Settings → About phone → Software information** → tap *Build number* 7
   times → "You are now a developer."
2. **Settings → Developer options** → enable **USB debugging** AND **Wireless
   debugging**.
3. With the phone on the same Wi-Fi as the WSL host, open **Wireless
   debugging** → tap **Pair device with pairing code**. Note the
   `IP:port` and the 6-digit code.
4. On the WSL host:
   ```bash
   ADB="/mnt/c/Program Files (x86)/Android/android-sdk/platform-tools/adb.exe"
   "$ADB" pair <ip>:<pair-port>
   # paste the 6-digit code when prompted
   "$ADB" connect <ip>:<connect-port>   # this is shown separately on the phone
   "$ADB" devices
   ```
5. On the phone, the host's RSA fingerprint dialog will pop **once**. Check
   "Always allow from this computer" and approve.

That's it. From now on:

```bash
"$ADB" connect <phone-ip>:5555
"$ADB" pull /sdcard/Recordings ./pull/recordings
"$ADB" pull /sdcard/DCIM        ./pull/dcim
```

…runs **without any phone-side tap**.

## Notes / gotchas

- The connect-port (5555 is the classic; modern Android picks a random one)
  changes after every phone reboot if you use Wireless Debugging's auto-port.
  For maximum stability, after pairing run `adb tcpip 5555` once over USB,
  then use `5555` permanently — but this resets if the phone reboots.
- Keep the host and phone on the **same Wi-Fi network**. WSL2 shares the
  Windows host's network, so this just works.
- If `adb devices` shows `unauthorized`, the "Always allow" box wasn't
  checked — re-pair and check it.
- `adb pull` is recursive; pull a whole directory at once.
- For full backup: `adb backup -all -apk -obb -shared -f phone-backup.ab`
  works on stock Android but is increasingly deprecated; prefer pulling
  `/sdcard/` directly which gets all user-visible media.

## Where Sound Recorder files live on Samsung One UI

- Built-in **Voice Recorder / Sound Recorder**:
  `/sdcard/Recordings/Voice Recorder/` (older)  or
  `/sdcard/Recordings/Voice/` or
  `/sdcard/Sounds/`
- **DCIM** (camera videos): `/sdcard/DCIM/Camera/`
- **Movies/Screen recorder**: `/sdcard/Movies/`
- **Downloads**: `/sdcard/Download/`

When pulling, grab `/sdcard/Recordings`, `/sdcard/DCIM`, `/sdcard/Movies`,
`/sdcard/Sounds`, `/sdcard/Download` — that covers every place a recording
or video could be.
