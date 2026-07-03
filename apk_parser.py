import subprocess
import re

# Change this path if your Build Tools version is different
AAPT_PATH = r"C:\Users\Admin\AppData\Local\Android\Sdk\build-tools\37.0.0\aapt.exe"


def extract_apk_metadata(apk_path):
    """
    Extract metadata from APK using Android Asset Packaging Tool (AAPT)
    """

    metadata = {
        "app_name": "Unknown",
        "package_name": "Unknown",
        "version_name": "Unknown",
        "version_code": "Unknown",
        "min_sdk": "Unknown",
        "target_sdk": "Unknown",
        "permissions": [],
        "activities": [],
        "services": [],
        "receivers": [],
        "urls": []
    }

    try:
        output = subprocess.check_output(
            [AAPT_PATH, "dump", "badging", apk_path],
            encoding="utf-8",
            errors="ignore"
        )

        # App Name
        match = re.search(r"application-label:'([^']+)'", output)
        if match:
            metadata["app_name"] = match.group(1)

        # Package Name
        match = re.search(r"package: name='([^']+)'", output)
        if match:
            metadata["package_name"] = match.group(1)

        # Version Name
        match = re.search(r"versionName='([^']+)'", output)
        if match:
            metadata["version_name"] = match.group(1)

        # Version Code
        match = re.search(r"versionCode='([^']+)'", output)
        if match:
            metadata["version_code"] = match.group(1)

        # Minimum SDK
        match = re.search(r"sdkVersion:'([^']+)'", output)
        if match:
            metadata["min_sdk"] = match.group(1)

        # Target SDK
        match = re.search(r"targetSdkVersion:'([^']+)'", output)
        if match:
            metadata["target_sdk"] = match.group(1)

        # Permissions
        metadata["permissions"] = re.findall(
            r"uses-permission: name='([^']+)'",
            output
        )

        # Launchable Activity
        activity = re.search(
            r"launchable-activity: name='([^']+)'",
            output
        )

        if activity:
            metadata["activities"].append(activity.group(1))

        return metadata

    except Exception as e:

        metadata["error"] = str(e)

        return metadata