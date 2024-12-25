import subprocess

class WiFi:
    def __init__(self):
        self.wifi_details = {}

    def fetch_profiles(self):
        """Fetch all stored Wi-Fi profiles."""
        try:
            command_profiles = "netsh wlan show profiles"
            profiles_result = subprocess.run(command_profiles, shell=True, capture_output=True, text=True)
            profiles = profiles_result.stdout.split("\n")
            profile_names = [line.split(":")[1].strip() for line in profiles if "All User Profile" in line]
            return profile_names
        except Exception as e:
            print(f"Error fetching profiles: {e}")
            return []

    def fetch_password(self, profile_name):
        """Fetch the password for a given Wi-Fi profile."""
        try:
            command_key = f'netsh wlan show profile "{profile_name}" key=clear'
            key_result = subprocess.run(command_key, shell=True, capture_output=True, text=True)
            key_lines = key_result.stdout.split("\n")
            key_content = [line.split(":")[1].strip() for line in key_lines if "Key Content" in line]
            return key_content[0] if key_content else "No Password"
        except Exception as e:
            print(f"Error fetching password for {profile_name}: {e}")
            return "Error"

    def get_wifi_details(self):
        """Retrieve details of all Wi-Fi profiles and their passwords."""
        profiles = self.fetch_profiles()
        for profile in profiles:
            self.wifi_details[profile] = self.fetch_password(profile)
        return self.wifi_details

    def display_wifi_details(self):
        """Display Wi-Fi profiles and passwords."""
        if not self.wifi_details:
            self.get_wifi_details()
        for wifi, password in self.wifi_details.items():
            print(f"Wi-Fi: {wifi}, Password: {password}")


if __name__ == "__main__":
    wifi_manager = WiFi()
    wifi_manager.display_wifi_details()
