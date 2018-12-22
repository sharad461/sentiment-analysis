from threading import Thread

i = 0

def function():
	global i
	i += 1
	if i < 10:
		print("Hi")
		return True
	else:
		return False

if __name__ == "__main__":
	thread = None
	thread = Thread(target=function())
	thread.daemon = True
	thread.start()