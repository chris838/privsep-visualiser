#include <stdio.h>
#include <stdlib.h>

static void static_fun(int i) {
 printf("foo %d\n", i);
}

void fun(int i) {
 printf("bar %d\n", i);
}

int main(int argc, char **argv) {
 static_fun(1);
 fun(2);
 return 0;
}
