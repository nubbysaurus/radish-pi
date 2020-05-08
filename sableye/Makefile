# Compiler features:
# 	* -g			adds debugging info to the executable
# 	* -Wall		turns on some compiler warnings
CC = g++
#CPP_FLAGS = -g -Wall
CPP_FLAGS = -g

#CMD := scrape
#COMPILE_LIST := scraper.sh
CMD := test
COMPILE_LIST := ./devices/bag/camera_utils/*.cpp
# Build all.
default: $(COMPILE_LIST)
	$(CC) $(CPP_FLAGS) -o $(CMD) $(COMPILE_LIST)

clean:
	$(RM) $(CMD)
