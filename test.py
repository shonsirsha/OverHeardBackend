from pytube import YouTube
YouTube('https://www.youtube.com/watch?v=s1UXW4eWB2Q').streams.filter(only_audio=True).first().download()