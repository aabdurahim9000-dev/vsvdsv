"""Права, иконка для Android-проекта, который создаёт `npx cap add android`."""
import glob, os, shutil

man = "android/app/src/main/AndroidManifest.xml"
s = open(man, encoding="utf-8").read()
perms = ["INTERNET", "RECORD_AUDIO", "MODIFY_AUDIO_SETTINGS", "VIBRATE", "POST_NOTIFICATIONS",
         "SCHEDULE_EXACT_ALARM", "USE_EXACT_ALARM", "RECEIVE_BOOT_COMPLETED", "WAKE_LOCK"]
add = "".join(f'    <uses-permission android:name="android.permission.{p}" />\n'
              for p in perms if f'android.permission.{p}"' not in s)
s = s.replace("<application", add + "    <application", 1)
if "<queries>" not in s:
    q = ('    <queries>\n'
         '        <intent><action android:name="android.intent.action.VIEW" /><data android:scheme="https" /></intent>\n'
         '        <intent><action android:name="android.intent.action.VIEW" /><data android:scheme="tg" /></intent>\n'
         '        <intent><action android:name="android.speech.RecognitionService" /></intent>\n'
         '    </queries>\n')
    s = s.replace("</manifest>", q + "</manifest>")
open(man, "w", encoding="utf-8").write(s)
print("manifest patched")

try:
    from PIL import Image
    src = Image.open("www/icon-512.png").convert("RGBA")
    shutil.rmtree("android/app/src/main/res/mipmap-anydpi-v26", ignore_errors=True)
    for d in glob.glob("android/app/src/main/res/mipmap-*"):
        for name in ("ic_launcher.png", "ic_launcher_round.png", "ic_launcher_foreground.png"):
            f = os.path.join(d, name)
            if os.path.exists(f):
                w = Image.open(f).size[0]
                src.resize((w, w), Image.LANCZOS).save(f)
    print("icons replaced")
except Exception as e:                      # иконка не критична
    print("icons skipped:", e)
