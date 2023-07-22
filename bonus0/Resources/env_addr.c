#include <stdio.h>

int main(int argc, char *argv[])
{
  int j;
  printf("Argument vector:\n");
  for (j = 0; ; j++) {
    if (argv[j] == NULL) break;
    printf("%2d: %p %s\n", j, argv[j], argv[j]);
  }
  printf("Environment vector:\n");
  for (j++; ; j++) {
    if (argv[j] == NULL) break;
    printf("%2d: %p %s\n", j, argv[j], argv[j]);
  }
  return 0;
}
