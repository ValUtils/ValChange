import yaml
from os import getenv
from pathlib import Path

LocalAppData = getenv("LocalAppData")
PrivateYaml = Path(LocalAppData) / "Riot Games" / "Riot Client" / "Data" / "RiotGamesPrivateSettings.yaml"

def read_yaml(file):
	f = open(file)
	data = yaml.load(f, yaml.Loader)
	f.close()
	return data

def write_yaml(file, data):
	f = open(file, 'w')
	yaml.safe_dump(data, f, indent=4)
	f.close()

def get_cookies():
	cookieData = read_yaml(PrivateYaml)
	cookies = cookieData["riot-login"]["persist"]["session"]["cookies"]
	cookieDict = {c["name"]: c["value"] for c in cookies}
	return cookieDict

def save_cookies(cookies):
	cookieData = read_yaml(PrivateYaml)
	oldCookies = cookieData["riot-login"]["persist"]["session"]["cookies"]
	for cookie in oldCookies:
		if cookie["name"] in cookies:
			cookie["value"] = cookies[cookie["name"]]
	write_yaml(PrivateYaml, cookieData)