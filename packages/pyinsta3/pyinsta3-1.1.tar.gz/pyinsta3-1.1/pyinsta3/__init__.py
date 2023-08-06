from urllib.request import urlopen
import aiohttp
import json
import re

class UserNotFoundError(Exception):
	"""No users found with the given username"""

class Profile:
	def __init__(self, user):
		self.user = user
		self.url = f"https://www.instagram.com/{self.user}"
		self.data = None
	def get_data(self):
		if not self.data:
			self.data = str(urlopen(self.url).read())
		data = {}
		try:
			data["username"] = re.search('"username":"(.*?)"', self.data).group(1)
			data["full_name"] = re.search('"full_name":"(.*?)"', self.data).group(1)
			data["biography"] = re.search('{"biography":"(.*?)"', self.data).group(1)
			data["followers"] = re.search('<meta content="(.*?) Followers', self.data).group(1)
			data["following"] = re.search('Followers, (.*?) Following,', self.data).group(1)
			data["posts"] = re.search('Following, (.*?) Posts', self.data).group(1)
			prv = re.search('"is_private":(.*?)', self.data)
			if prv == "true":
				prv = True
			else:
				prv = False
			verf = re.search('"is_verified":(.*?)', self.data)
			if verf == "true":
				verf = True
			else:
				verf = False
			data["is_privage"] = prv
			data["is_verified"] = verf
			data["profile_pic_url"] = re.search('<meta property="og:image" content="(.*?)"', self.data).group(1)
			return data
		except:
			Error = UserNotFoundError("No users found with the given username")
			raise Error
			
class AsyncProfile:
	def __init__(self, user):
		self.user = user
		self.url = f"https://www.instagram.com/{self.user}"
		self.data = None
	async def get_data(self):
		if not self.data:
			async with aiohttp.ClientSession() as session:
				async with session.get(self.url) as resp:
					self.data = str(await resp.read())
		data = {}
		try:
			data["username"] = re.search('"username":"(.*?)"', self.data).group(1)
			data["full_name"] = re.search('"full_name":"(.*?)"', self.data).group(1)
			data["biography"] = re.search('{"biography":"(.*?)"', self.data)
			data["followers"] = re.search('<meta content="(.*?) Followers', self.data).group(1)
			data["following"] = re.search('Followers, (.*?) Following,', self.data).group(1)
			data["posts"] = re.search('Following, (.*?) Posts', self.data).group(1)
			prv = re.search('"is_private":(.*?)', self.data)
			if prv == "true":
				prv = True
			else:
				prv = False
			verf = re.search('"is_verified":(.*?)', self.data)
			if verf == "true":
				verf = True
			else:
				verf = False
			data["private_profile"] = prv
			data["verified_profile"] = verf
			data["profile_pic_url"] = re.search('"profile_pic_url":"(.*?)"', self.data)
			return data
		except:
			Error = UserNotFoundError("No users found with the given username")
			raise Error