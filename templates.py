# Generates AndroidManifest.xml with overlay for targeted package 
def generate_manifest(package, targetPackage, label):
    return f'''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="{package}">
    <overlay android:isStatic="true" android:priority="0" android:targetPackage="{targetPackage}"/>
    <application android:label="{label}" />
</manifest>
'''


# Generates basic build.gradle for overlay
def generate_gradle(package):
    return f'''apply plugin: \'com.android.application\'

android {{
    compileSdkVersion 28
    defaultConfig {{
        applicationId "{package}"
        minSdkVersion 28
        targetSdkVersion 28
        versionCode 1
        versionName "1"
    }}
    
    buildTypes {{
        debug {{
            minifyEnabled false
        }}
    }}
}}

dependencies {{
    implementation fileTree(dir: \'libs\', include: [\'*.jar\'])
}}
'''
