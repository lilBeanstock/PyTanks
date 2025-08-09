lib.so: libraries.c
	gcc -fPIC -shared libraries.c -o lib.so
