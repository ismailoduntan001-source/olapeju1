# Olápèjú Yoruba Class (Android app project)

A teacher cat who helps children build Yoruba sentences. The app is the web page in `www/`, wrapped as a real Android app with Capacitor. The Yoruba voice recordings are saved inside the app, so it works with no internet.

## Get the APK (no Android Studio needed)

1. Make a free account at github.com and create a new empty repository named `olapeju`.
2. In the repository, choose **Add file > Upload files** and drag in everything from this folder. Include the hidden `.github` folder. If the **Actions** tab later shows no workflow, choose **Add file > Create new file**, type `.github/workflows/android.yml` as the name, and paste in the contents of that file from this folder.
3. Open the **Actions** tab, choose **Build Android app**, then **Run workflow**. It takes about 8 minutes.
4. When it finishes, open the run and download **olapeju-apk** at the bottom. Unzip it to get `app-debug.apk`.
5. Send the APK to an Android phone (WhatsApp, Google Drive or a cable). Open it and allow "install from this source" when asked.

The build records the Yoruba voice with Google Text-to-Speech. If Google refuses the request from GitHub's servers, the build still works but those words use the phone's own voice. To fix that, run `pip install gTTS` and `python tools/make_audio.py` on your own computer, then upload the new `www/audio` folder and run the build again.

## Build on your own computer instead

You need Node.js 22, Java 21 and Android Studio.

```
pip install gTTS
python tools/make_audio.py
npm install
npx cap add android
npx capacitor-assets generate --android
npx cap sync android
npx cap open android
```

In Android Studio press the green Run button with a phone or emulator connected.

## Change the lessons

Lessons live in the `lessons` block inside `www/index.html`. Add a sentence as `[["word", "word"], "English meaning."]`, then run `python tools/make_audio.py` so the new words get a voice.

## Publishing on Google Play

The debug APK is for testing and sharing directly. Google Play needs a signed release bundle and a Play developer account. Ask me and I will add a signed-release step to the workflow.

## iPhone

An iPhone build needs a Mac with Xcode and an Apple developer account. The same `www/` folder works there with `npx cap add ios`.
