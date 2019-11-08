import pafy
url = "https://www.youtube.com/watch?v=vEvXWUUTzqU"
video = pafy.new(url)

bestaudio = video.getbestaudio()
print(bestaudio.url)

